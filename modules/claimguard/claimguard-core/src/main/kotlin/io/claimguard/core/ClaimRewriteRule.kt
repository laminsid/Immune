package io.claimguard.core

/**
 * Generic, configurable claim-rewrite rule, replacing the hardcoded
 * Cd276StatusCorrectionV30391 coupling.
 *
 * The original engine hardwired one disease-specific rewrite (CD276 "computational
 * null" → "selected-matrix null-like; official kill blocked"). That belongs in a
 * domain adapter, not in the portable core. Here, a rule is just: a regex to find,
 * a replacement to apply, and the tier at/below which the rewrite is enforced.
 *
 * Tier-2 runs are exempt (computational evidence language may stand once earned).
 */
data class ClaimRewriteRule(
    val id: String,
    val pattern: Regex,
    val replacement: String,
    /** Rewrite applies when the run tier is NOT in this allow-set. */
    val allowedAtTiers: Set<String> = setOf(EvidenceVerificationTier.TIER2),
) {
    fun applyIfNeeded(text: String, tier: String): String =
        if (tier in allowedAtTiers) text else pattern.replace(text, replacement)

    companion object {
        /**
         * Default tier-gated rewrites that are domain-agnostic: below Tier-2, any
         * unsupported "official" kill/survive token is downgraded to the blocked verdict.
         */
        fun defaultTierGatedRules(): List<ClaimRewriteRule> = listOf(
            ClaimRewriteRule(
                id = "computational_kill_to_blocked",
                pattern = Regex("COMPUTATIONAL_KILL", RegexOption.IGNORE_CASE),
                replacement = VerificationTierVerdictPolicy.BLOCKED),
            ClaimRewriteRule(
                id = "computational_survive_to_blocked",
                pattern = Regex("COMPUTATIONAL_SURVIVE", RegexOption.IGNORE_CASE),
                replacement = VerificationTierVerdictPolicy.BLOCKED),
            ClaimRewriteRule(
                id = "surviving_computational_to_blocked",
                pattern = Regex("SURVIVING_COMPUTATIONAL", RegexOption.IGNORE_CASE),
                replacement = VerificationTierVerdictPolicy.BLOCKED))
    }
}
