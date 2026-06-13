package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * Three-tier verifiable evidence contract.
 *
 *  Tier-0 proves deterministic replay of a declared slice/fixture only.
 *  Tier-1 proves the slice was regenerated from source files using the registered transform.
 *  Tier-2 is required before any computational evidence claim language is allowed.
 *
 * Ported verbatim in behavior from EvidenceVerificationTierV30392. The only change
 * is that nothing here is neuroblastoma-specific: it reads generic signals from the
 * input JSON. Field names are kept stable so existing receipts remain compatible.
 */
object EvidenceVerificationTier {
    const val REQUIRED_TOKEN: String = "THREE_TIER_VERIFIABLE_EVIDENCE_CONTRACT"
    const val TIER0: String = "TIER0_SLICE_REPRODUCIBLE_REVIEW_ONLY"
    const val TIER1: String = "TIER1_SOURCE_CERTIFIED_REVIEW_GRADE"
    const val TIER2: String = "TIER2_REPLICATION_CERTIFIED_COMPUTATIONAL_EVIDENCE"

    const val SENTENCE_TIER0: String = "Tier-0 proves replayability, not source truth."
    const val SENTENCE_TIER1: String = "Tier-1 proves source extraction, not biological truth."
    const val SENTENCE_TIER2: String = "Tier-2 is required before any computational evidence claim."
    const val STRATEGIC_RULE: String = "Ship the verifiable evidence contract, not the cargo."

    /**
     * Classify a run into a tier from generic signals:
     *  - replay:        verification.replay.verified  (bool)  → tile/slice hash replays
     *  - sourceCert:    source_certification.state contains SOURCE_CERTIFIED, or .sourceCertified
     *  - mappingPass:   full_mapping_audit contains PASS  (the "full GPL5175 audit" generalization)
     *  - replication:   replication_gate.independent_replication contains PASS
     */
    fun classify(run: JSONObject): JSONObject {
        val verification = run.optJSONObject("verification_signals") ?: JSONObject()
        val sourceCertification = run.optJSONObject("source_certification") ?: JSONObject()
        val mappingAudit = run.optJSONObject("full_mapping_audit") ?: JSONObject()
        val replicationGate = run.optJSONObject("replication_gate") ?: JSONObject()

        val replayPassed = (verification.optJSONObject("replay")?.optBoolean("verified", false) ?: false) ||
            verification.optBoolean("replay_passed", false)
        val sourceCertified = sourceCertification.optBoolean("sourceCertified", false) ||
            sourceCertification.optString("state", "").contains("SOURCE_CERTIFIED", ignoreCase = true)
        val mappingPass = mappingAudit.optString("state", mappingAudit.optString("decision", ""))
            .contains("PASS", ignoreCase = true)
        val replicationCertified = replicationGate.optString("independent_replication", "")
            .contains("PASS", ignoreCase = true) ||
            sourceCertification.optBoolean("independentReplicationCertified", false)

        val tier = when {
            sourceCertified && mappingPass && replicationCertified -> TIER2
            sourceCertified -> TIER1
            else -> TIER0
        }
        return JSONObject()
            .put("schema", "evidence_verification_tier")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("verification_tier", tier)
            .put("replay_passed", replayPassed)
            .put("source_certified", sourceCertified)
            .put("full_mapping_pass", mappingPass)
            .put("independent_replication_pass", replicationCertified)
            .put("promotion_allowed", tier == TIER2)
            .put("tier_sentences", JSONArray(listOf(SENTENCE_TIER0, SENTENCE_TIER1, SENTENCE_TIER2)))
            .put("strategic_rule", STRATEGIC_RULE)
            .put("rationale", rationale(tier, replayPassed, sourceCertified, mappingPass, replicationCertified))
    }

    private fun rationale(tier: String, replay: Boolean, source: Boolean, mapping: Boolean, replication: Boolean): String = when (tier) {
        TIER2 -> "Source-certified, full mapping audit passed, and independent replication passed; computational evidence language may be considered subject to boundary checks."
        TIER1 -> "Source extraction is certified, but full mapping/replication gates are not both satisfied; review-grade only, no kill/survive language."
        else -> "Slice replay/hash can be checked locally (replayPassed=$replay), but source truth is not certified (sourceCertified=$source, fullMapping=$mapping, replication=$replication); review-only."
    }
}
