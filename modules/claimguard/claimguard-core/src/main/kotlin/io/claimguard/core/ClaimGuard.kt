package io.claimguard.core

import org.json.JSONObject

/**
 * One-call entry point for the common path:
 *   "Here is an AI-proposed hypothesis and a claimed result. At what tier is it
 *    supported, what verdict is actually allowed, and is any surface overclaiming?"
 *
 * Independent of the generator: feed it Co-Scientist / any LLM output plus your
 * dataset signals, and it returns a receipt whose enforced verdict cannot exceed
 * the verification tier — plus a firewall report on the run's surfaces.
 */
object ClaimGuard {

    data class Result(
        val receipt: JSONObject,
        val firewall: JSONObject,
    ) {
        val verificationTier: String
            get() = receipt.optJSONObject("verification")?.optString("verification_tier") ?: EvidenceVerificationTier.TIER0
        val enforcedVerdict: String
            get() = firewall.optString("safeFinalVerdict", receipt.optString("enforced_verdict"))
        val promotionAllowed: Boolean
            get() = receipt.optJSONObject("evidence_strength")?.optBoolean("promotion_allowed", false) ?: false
        val overclaiming: Boolean
            get() = firewall.optString("state") == GlobalClaimSanitizer.BLOCKED
    }

    fun assess(
        run: JSONObject,
        identity: EngineIdentity = EngineIdentity.DEFAULT,
        sanitizer: GlobalClaimSanitizer = GlobalClaimSanitizer(),
    ): Result {
        val receipt = VerificationReceiptBridge.evaluate(run, identity)
        val firewall = sanitizer.evaluate(run, receipt)
        return Result(receipt, firewall)
    }
}
