package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * Assembles the full three-tier verifiable evidence receipt from a run.
 *
 * Ported from VerificationReceiptBridgeV30392. Two couplings were severed:
 *   1. The Android ResearchEngineV3ReleaseIdentity is now an injected [EngineIdentity].
 *   2. The CleanEvidenceReceiptV30391 fallback is gone: the prior verdict is read
 *      from the run's "prior_receipt" object, defaulting to INCONCLUSIVE.
 *
 * This is the one call most integrations need: give it a run, get back a receipt
 * whose enforced verdict cannot exceed what the verification tier allows.
 */
object VerificationReceiptBridge {
    const val REQUIRED_TOKEN: String = "VERIFICATION_RECEIPT_BRIDGE"
    const val RECEIPT_VERSION: String = "claimguard-receipt-0.1.0"

    fun evaluate(run: JSONObject, identity: EngineIdentity = EngineIdentity.DEFAULT): JSONObject {
        val priorReceipt = run.optJSONObject("prior_receipt") ?: JSONObject()
        val provenance = HypothesisProvenanceContract.evaluate(run)
        val slice = SliceSelectionContract.evaluate(run, provenance)
        val transform = TransformContractHash.evaluate(provenance, slice)
        val tier = EvidenceVerificationTier.classify(run)
        val tierName = tier.optString("verification_tier", EvidenceVerificationTier.TIER0)

        val requestedVerdict = priorReceipt.optString("verdict", run.optString("requested_verdict", "INCONCLUSIVE"))
        val policy = VerificationTierVerdictPolicy.enforce(tierName, requestedVerdict)
        val promotionAllowed = policy.optBoolean("allowed", false) && tierName == EvidenceVerificationTier.TIER2

        return JSONObject()
            .put("receipt_version", RECEIPT_VERSION)
            .put("schema", "three_tier_verifiable_evidence_receipt")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("prior_receipt_version", priorReceipt.optString("receipt_version", "none"))
            .put("hypothesis_id", priorReceipt.optString("hypothesis_id", provenance.optString("hypothesis_id")))
            .put("requested_verdict", requestedVerdict)
            .put("enforced_verdict", policy.optString("enforcedVerdict"))
            .put("verification", tier)
            .put("tier_verdict_policy", policy)
            .put("hypothesis_provenance", provenance)
            .put("slice_selection", slice)
            .put("transform_contract", transform)
            .put("reproducibility", JSONObject()
                .put("verification_tier", tierName)
                .put("replay_passed", tier.optBoolean("replay_passed", false))
                .put("slice_sha256", slice.optString("evidence_slice_sha256"))
                .put("transform_contract_sha256", transform.optString("transform_contract_sha256")))
            .put("evidence_strength", JSONObject()
                .put("claim_level", policy.optString("claimLevel", EvidenceClaimLevel.REVIEW_ONLY))
                .put("promotion_allowed", promotionAllowed)
                .put("promotion_blockers", promotionBlockers(tier)))
            .put("runtime_environment", identity.runtimeEnvironmentJson())
            .put("boundary", JSONObject()
                .put("tier0", EvidenceVerificationTier.SENTENCE_TIER0)
                .put("tier1", EvidenceVerificationTier.SENTENCE_TIER1)
                .put("tier2", EvidenceVerificationTier.SENTENCE_TIER2)
                .put("strategic_rule", EvidenceVerificationTier.STRATEGIC_RULE)
                .put("clinical_claim", false)
                .put("causal_claim", false)
                .put("publication_grade", promotionAllowed))
    }

    fun renderOnePageLines(receipt: JSONObject): List<String> {
        val verification = receipt.optJSONObject("verification") ?: JSONObject()
        val policy = receipt.optJSONObject("tier_verdict_policy") ?: JSONObject()
        val reproducibility = receipt.optJSONObject("reproducibility") ?: JSONObject()
        val evidenceStrength = receipt.optJSONObject("evidence_strength") ?: JSONObject()
        return listOf(
            "Three-Tier Verifiable Evidence Receipt ${receipt.optString("receipt_version", RECEIPT_VERSION)}",
            "Hypothesis: ${receipt.optString("hypothesis_id", "UNKNOWN")}",
            "Requested verdict: ${receipt.optString("requested_verdict", "UNKNOWN")}",
            "Enforced verdict: ${receipt.optString("enforced_verdict", VerificationTierVerdictPolicy.BLOCKED)}",
            "Verification tier: ${verification.optString("verification_tier", EvidenceVerificationTier.TIER0)} | replay=${verification.optBoolean("replay_passed", false)} | sourceCertified=${verification.optBoolean("source_certified", false)} | fullMapping=${verification.optBoolean("full_mapping_pass", false)} | replication=${verification.optBoolean("independent_replication_pass", false)}",
            "Claim level: ${evidenceStrength.optString("claim_level", EvidenceClaimLevel.REVIEW_ONLY)} | promotionAllowed=${evidenceStrength.optBoolean("promotion_allowed", false)} | policyAllowed=${policy.optBoolean("allowed", false)}",
            "Slice hash: ${reproducibility.optString("slice_sha256", "missing")} | transform contract: ${reproducibility.optString("transform_contract_sha256", "missing")}",
            EvidenceVerificationTier.SENTENCE_TIER0,
            EvidenceVerificationTier.SENTENCE_TIER1,
            EvidenceVerificationTier.SENTENCE_TIER2,
            EvidenceVerificationTier.STRATEGIC_RULE)
    }

    private fun promotionBlockers(tier: JSONObject): JSONArray {
        val blockers = mutableListOf<String>()
        if (!tier.optBoolean("source_certified", false)) blockers += "source extraction not certified"
        if (!tier.optBoolean("full_mapping_pass", false)) blockers += "full mapping/audit missing"
        if (!tier.optBoolean("independent_replication_pass", false)) blockers += "independent replication missing"
        if (blockers.isEmpty()) blockers += "none"
        return JSONArray(blockers)
    }
}
