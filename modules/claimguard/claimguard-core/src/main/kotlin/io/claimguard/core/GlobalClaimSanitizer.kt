package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * End-to-end final claim sanitizer: the claim firewall.
 *
 * Ported from GlobalClaimSanitizerV30393. It scans every output surface of a run
 * and, when the run is below Tier-2, downgrades unsupported kill/survive language
 * to the blocked verdict so nothing leaks into a final exported surface.
 *
 * The CD276-specific rewrite was removed from the core and replaced by an injected
 * list of [ClaimRewriteRule]. Domain adapters (e.g. a neuroblastoma adapter) supply
 * their own canonical rewrites; the core stays disease-agnostic.
 */
class GlobalClaimSanitizer(
    private val rewriteRules: List<ClaimRewriteRule> = ClaimRewriteRule.defaultTierGatedRules(),
    /** JSON keys whose string values should be scanned for unsupported claims. */
    private val scannedSurfaceKeys: List<String> = DEFAULT_SCANNED_SURFACE_KEYS,
) {
    companion object {
        const val REQUIRED_TOKEN: String = "GLOBAL_CLAIM_SANITIZER_END_TO_END"
        const val PASS: String = "FINAL_OUTPUT_CLAIM_GUARD_PASS"
        const val BLOCKED: String = "FINAL_OUTPUT_CLAIM_GUARD_BLOCKED_SURFACE_DOWNGRADE_REQUIRED"

        val DEFAULT_SCANNED_SURFACE_KEYS: List<String> = listOf(
            "report_surface", "verdict_surface", "executive_summary",
            "final_surface", "prior_receipt", "evidence_pack")
    }

    fun evaluate(run: JSONObject, receipt: JSONObject = VerificationReceiptBridge.evaluate(run)): JSONObject {
        val verification = receipt.optJSONObject("verification") ?: JSONObject()
        val tier = verification.optString("verification_tier", EvidenceVerificationTier.TIER0)
        val claimLevel = receipt.optJSONObject("evidence_strength")?.optString("claim_level", EvidenceClaimLevel.REVIEW_ONLY)
            ?: EvidenceClaimLevel.REVIEW_ONLY
        val hits = JSONArray()
        for (key in scannedSurfaceKeys) {
            val node = run.opt(key) ?: continue
            scanAny(node, key, tier, hits)
        }
        val blocked = hits.length() > 0 && tier != EvidenceVerificationTier.TIER2
        return JSONObject()
            .put("schema", "global_claim_sanitizer")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("state", if (blocked) BLOCKED else PASS)
            .put("verificationTier", tier)
            .put("claimLevel", claimLevel)
            .put("unsafeLegacyClaimCount", hits.length())
            .put("unsafeLegacyClaims", hits)
            .put("safeFinalVerdict", safeVerdict(receipt, blocked))
            .put("safeClaimLanguage", safeClaimLanguage(tier, claimLevel))
            .put("openGate", if (blocked) "surface_contains_unsupported_kill_survive_language" else JSONObject.NULL)
            .put("rule", "Final exported surfaces must use the enforced verdict and safe claim language, not legacy route labels, unless Tier-2 is reached.")
    }

    /** Apply every configured rewrite to [text] for the given [tier]. */
    fun sanitizeTextForTier(text: String, tier: String): String {
        var out = text
        for (rule in rewriteRules) out = rule.applyIfNeeded(out, tier)
        return out
    }

    private fun scanAny(value: Any?, path: String, tier: String, hits: JSONArray) {
        when (value) {
            is JSONObject -> {
                val keys = value.keys()
                while (keys.hasNext()) {
                    val key = keys.next()
                    scanAny(value.opt(key), "$path.$key", tier, hits)
                }
            }
            is JSONArray -> for (i in 0 until value.length()) scanAny(value.opt(i), "$path[$i]", tier, hits)
            is String -> if (isUnsafeClaim(value, tier)) {
                hits.put(JSONObject()
                    .put("path", path)
                    .put("value", value.take(220))
                    .put("replacement", sanitizeTextForTier(value, tier)))
            }
        }
    }

    private fun isUnsafeClaim(value: String, tier: String): Boolean {
        if (tier == EvidenceVerificationTier.TIER2) return false
        val v = value.uppercase()
        if (isBoundaryLanguage(v)) return false
        if (v.contains("COMPUTATIONAL_KILL") || v.contains("COMPUTATIONAL_SURVIVE") || v.contains("SURVIVING_COMPUTATIONAL")) return true
        if (v.startsWith("KILLED_") || v.contains("=KILLED_") || v.contains(":KILLED_")) return true
        if (v.startsWith("SURVIVED_") || v.contains("=SURVIVED_") || v.contains(":SURVIVED_")) return true
        return false
    }

    private fun isBoundaryLanguage(v: String): Boolean =
        v.contains("REVIEW_ONLY") || v.contains("REQUIRES_TIER2") || v.contains("BLOCKED") ||
            v.contains("NO_COMPUTATIONAL_KILL") || v.contains("NOT COMPUTATIONAL_KILL") ||
            v.contains("NOT PUBLICATION") || v.contains("ALLOWED ONLY AFTER")

    private fun safeVerdict(receipt: JSONObject, blocked: Boolean): String {
        val enforced = receipt.optString("enforced_verdict", VerificationTierVerdictPolicy.BLOCKED)
        return if (blocked) VerificationTierVerdictPolicy.BLOCKED else enforced
    }

    private fun safeClaimLanguage(tier: String, claimLevel: String): String = when {
        tier == EvidenceVerificationTier.TIER2 && claimLevel == EvidenceClaimLevel.COMPUTATIONAL_EVIDENCE ->
            "COMPUTATIONAL_EVIDENCE_LANGUAGE_ALLOWED_SUBJECT_TO_BOUNDARIES"
        tier == EvidenceVerificationTier.TIER1 -> "SOURCE_CERTIFIED_REVIEW_GRADE_ONLY_NO_KILL_SURVIVE"
        else -> "REPLAY_ONLY_REVIEW_ONLY_NO_KILL_SURVIVE"
    }
}
