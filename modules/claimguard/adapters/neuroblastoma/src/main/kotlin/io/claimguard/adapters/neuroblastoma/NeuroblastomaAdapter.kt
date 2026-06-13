package io.claimguard.adapters.neuroblastoma

import io.claimguard.core.ClaimRewriteRule
import io.claimguard.core.EvidenceVerificationTier
import io.claimguard.core.GlobalClaimSanitizer

/**
 * Neuroblastoma / GSE85047 domain adapter.
 *
 * This is where everything disease-specific lives — proving the core is genuinely
 * decoupled. The CD276 canonical rewrite that the original engine hardwired into
 * Cd276StatusCorrectionV30391 is now just one preset rule supplied to the core
 * sanitizer. The core never mentions CD276, GSE85047, GPL5175, NKG7, or MYCN.
 */
object NeuroblastomaAdapter {

    const val CD276_CANONICAL: String =
        "CD276 selected-matrix null-like signal; official computational kill blocked pending full GPL5175 mapping."

    /** The CD276 rewrite, expressed as a portable core rule. */
    fun cd276Rule(): ClaimRewriteRule = ClaimRewriteRule(
        id = "cd276_computational_null_to_selected_matrix_null_like",
        pattern = Regex("CD276\\s+computational\\s+(null|kill)", RegexOption.IGNORE_CASE),
        replacement = CD276_CANONICAL,
        allowedAtTiers = setOf(EvidenceVerificationTier.TIER2))

    /** A sanitizer pre-loaded with the neuroblastoma presets plus the core defaults. */
    fun sanitizer(): GlobalClaimSanitizer =
        GlobalClaimSanitizer(rewriteRules = listOf(cd276Rule()) + ClaimRewriteRule.defaultTierGatedRules())
}
