package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * The code-level fence binding verification tiers to allowed verdicts.
 * Tier-0/Tier-1 cannot emit official kill/survive/computational-evidence language.
 *
 * Ported from VerificationTierVerdictPolicyV30392; behavior preserved exactly.
 */
object VerificationTierVerdictPolicy {
    const val REQUIRED_TOKEN: String = "VERIFICATION_TIER_VERDICT_POLICY"
    const val BLOCKED: String = "BLOCKED_COMPUTATIONAL_CLAIM_REQUIRES_TIER2"

    fun enforce(verificationTier: String, requestedVerdict: String): JSONObject {
        val computationalClaim = isComputationalEvidenceClaim(requestedVerdict)
        val labUpgrade = requestedVerdict.contains("LAB_UPGRADE", ignoreCase = true) ||
            requestedVerdict.contains("LAB-UPGRADE", ignoreCase = true)
        val allowed = when (verificationTier) {
            EvidenceVerificationTier.TIER2 -> true
            EvidenceVerificationTier.TIER1 -> !computationalClaim
            else -> !computationalClaim && !labUpgrade
        }
        val enforcedVerdict = if (allowed) requestedVerdict.ifBlank { "INCONCLUSIVE" } else BLOCKED
        val claimLevel = EvidenceClaimLevel.levelFor(verificationTier, requestedVerdict)
        return JSONObject()
            .put("schema", "verification_tier_verdict_policy")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("verificationTier", verificationTier)
            .put("requestedVerdict", requestedVerdict)
            .put("requestedComputationalClaim", computationalClaim)
            .put("allowed", allowed)
            .put("enforcedVerdict", enforcedVerdict)
            .put("claimLevel", claimLevel)
            .put("matrix", policyMatrix())
            .put("reason", reason(verificationTier, requestedVerdict, allowed))
    }

    fun isComputationalEvidenceClaim(verdict: String): Boolean {
        val v = verdict.uppercase()
        return v.contains("COMPUTATIONAL_KILL") ||
            v.contains("COMPUTATIONAL_SURVIVE") ||
            v.contains("SURVIVING_COMPUTATIONAL") ||
            v == "COMPUTATIONAL_SUPPORT_CANDIDATE" ||
            v.startsWith("KILLED_") ||
            v == "KILLED" ||
            v.startsWith("SURVIVED_") ||
            v == "SURVIVED"
    }

    fun policyMatrix(): JSONObject = JSONObject()
        .put(EvidenceVerificationTier.TIER0, JSONObject()
            .put("inconclusive", true).put("lab_upgrade", false).put("killed_or_survived", false))
        .put(EvidenceVerificationTier.TIER1, JSONObject()
            .put("inconclusive", true).put("lab_upgrade_exploratory", true).put("killed_or_survived", false))
        .put(EvidenceVerificationTier.TIER2, JSONObject()
            .put("inconclusive", true).put("lab_upgrade", true).put("killed_or_survived", true))
        .put("canonicalBoundary", JSONArray(listOf(
            EvidenceVerificationTier.SENTENCE_TIER0,
            EvidenceVerificationTier.SENTENCE_TIER1,
            EvidenceVerificationTier.SENTENCE_TIER2)))

    private fun reason(tier: String, verdict: String, allowed: Boolean): String = when {
        allowed -> "Verdict is allowed at $tier under the tier/verdict policy."
        isComputationalEvidenceClaim(verdict) -> "Official kill/survive/computational-evidence language is blocked until Tier-2: source-certified + full mapping audit + independent replication."
        else -> "Tier-0 allows inconclusive/replay-only review, not lab-upgrade or publication-grade language."
    }
}

/** Claim levels are separate from reproducibility tiers. Ported from EvidenceClaimLevelV30392. */
object EvidenceClaimLevel {
    const val REVIEW_ONLY: String = "REVIEW_ONLY"
    const val LAB_UPGRADE_EXPLORATORY: String = "LAB_UPGRADE_EXPLORATORY"
    const val COMPUTATIONAL_EVIDENCE: String = "COMPUTATIONAL_EVIDENCE"
    const val BLOCKED_COMPUTATIONAL_CLAIM_REQUIRES_TIER2: String = "BLOCKED_COMPUTATIONAL_CLAIM_REQUIRES_TIER2"

    fun levelFor(tier: String, requestedVerdict: String): String = when {
        VerificationTierVerdictPolicy.isComputationalEvidenceClaim(requestedVerdict) &&
            tier != EvidenceVerificationTier.TIER2 -> BLOCKED_COMPUTATIONAL_CLAIM_REQUIRES_TIER2
        tier == EvidenceVerificationTier.TIER2 &&
            VerificationTierVerdictPolicy.isComputationalEvidenceClaim(requestedVerdict) -> COMPUTATIONAL_EVIDENCE
        tier == EvidenceVerificationTier.TIER1 &&
            requestedVerdict.contains("LAB", ignoreCase = true) -> LAB_UPGRADE_EXPLORATORY
        else -> REVIEW_ONLY
    }
}
