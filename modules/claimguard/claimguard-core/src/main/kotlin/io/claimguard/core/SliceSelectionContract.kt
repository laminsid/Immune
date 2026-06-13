package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * Records why this exact evidence slice exists, and under what redistribution terms.
 *
 * Ported from SliceSelectionContractV30392. The GSE85047/GPL5175 specifics became
 * caller-supplied: the source anchor and sample rule come from the run's
 * "slice_config" (or neutral defaults). Default fixture policy stays HASH_ONLY so a
 * library user never accidentally redistributes a licensed derived slice.
 */
object SliceSelectionContract {
    const val REQUIRED_TOKEN: String = "SLICE_SELECTION_CONTRACT"
    const val REDISTRIBUTION_HASH_ONLY: String = "HASH_ONLY_REGENERATE_LOCALLY"
    const val REDISTRIBUTION_ALLOWED: String = "ALLOWED_PUBLIC_DERIVED_SLICE"

    fun evaluate(run: JSONObject, provenance: JSONObject): JSONObject {
        val cfg = run.optJSONObject("slice_config") ?: JSONObject()
        val declaredGenes = provenance.optJSONArray("declared_genes") ?: JSONArray()
        val dataset = provenance.optString("dataset", "DATASET_UNSPECIFIED")
        val sampleRule = cfg.optString(
            "sample_inclusion_rule",
            "Include samples with the declared outcome, the declared covariates, and the declared expression features available; exclude samples missing any required outcome/covariate/feature field.")
        val modelFormula = cfg.optString("model_formula", defaultModelFormula(provenance))
        val redistribution = cfg.optString("redistribution_status", REDISTRIBUTION_HASH_ONLY)
        return JSONObject()
            .put("schema", "slice_selection_contract")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("redistribution_status", redistribution)
            .put("fixture_directory", cfg.optString("fixture_directory", "data/fixtures/$dataset" + "_tier0"))
            .put("evidence_slice_csv_in_repo", redistribution == REDISTRIBUTION_ALLOWED)
            .put("evidence_slice_sha256", cfg.optString("evidence_slice_sha256", "PENDING_TIER0_SLICE_HASH"))
            .put("dataset", dataset)
            .put("source_anchor", sourceAnchor(cfg, dataset))
            .put("gene_selection_rule", "Features are derived from the declared hypothesis text/feature set before verdict interpretation, not chosen after seeing HR/p/FDR.")
            .put("declared_genes", declaredGenes)
            .put("sample_selection_rule", sampleRule)
            .put("exclusion_rule", "Missing outcome, missing declared covariate, or missing declared feature blocks inclusion for this slice.")
            .put("model_formula", modelFormula)
            .put("sample_inclusion_rule_sha256", Hashing.sha256(sampleRule))
            .put("model_formula_sha256", Hashing.sha256(modelFormula))
            .put("license_gate", "Do not publish derived slices unless redistribution status is explicitly cleared; otherwise store hash + manifest only and regenerate locally from official source files.")
    }

    private fun defaultModelFormula(provenance: JSONObject): String {
        val outcome = provenance.optString("declared_outcome", "OUTCOME")
        val covs = provenance.optJSONArray("declared_covariates") ?: JSONArray()
        val covList = (0 until covs.length()).joinToString(", ") { covs.optString(it) }.ifBlank { "covariates" }
        return "$outcome ~ declared_feature_composite + $covList"
    }

    private fun sourceAnchor(cfg: JSONObject, dataset: String): JSONObject {
        cfg.optJSONObject("source_anchor")?.let { return it }
        return JSONObject()
            .put("repository", cfg.optString("repository", "REPOSITORY_UNSPECIFIED"))
            .put("series_accession", dataset)
            .put("platform_accession", cfg.optString("platform_accession", "PLATFORM_UNSPECIFIED"))
            .put("doi", JSONObject.NULL)
            .put("zenodo_optional", "Allowed only if a separately licensed reproducibility archive is later published.")
            .put("source_files", JSONArray(listOf(
                JSONObject()
                    .put("accession_or_path", "$dataset official source/processed files")
                    .put("sha256", "PENDING_TIER1_SOURCE_CERTIFICATION")
                    .put("role", "full source matrix"),
                JSONObject()
                    .put("accession_or_path", "platform annotation / feature mapping")
                    .put("sha256", "PENDING_FULL_MAPPING_AUDIT")
                    .put("role", "feature-to-entity mapping"))))
    }
}

/**
 * Hashes the full anti-cherry-picking transform contract — not code alone.
 * Ported from TransformContractHashV30392, behavior preserved.
 *
 * Changing genes, sample rules, covariates, formula, topic text, or transform code
 * changes this hash. That is the mechanical defense against post-hoc selection.
 */
object TransformContractHash {
    const val REQUIRED_TOKEN: String = "TRANSFORM_CONTRACT_HASH"
    const val DEFAULT_TRANSFORM_CODE_ID: String = "build_slice_hash_only_manifest"

    fun evaluate(provenance: JSONObject, slice: JSONObject, transformCodeId: String = DEFAULT_TRANSFORM_CODE_ID): JSONObject {
        val parts = linkedMapOf(
            "hypothesis_text_hash" to provenance.optString("hypothesis_text_sha256", ""),
            "declared_gene_set_hash" to provenance.optString("declared_gene_set_sha256", ""),
            "sample_inclusion_rule_hash" to slice.optString("sample_inclusion_rule_sha256", ""),
            "covariate_rule_hash" to provenance.optString("declared_covariates_sha256", ""),
            "model_formula_hash" to slice.optString("model_formula_sha256", ""),
            "transform_code_hash" to Hashing.sha256(transformCodeId))
        val canonical = parts.entries.joinToString("\n") { "${it.key}=${it.value}" }
        val partsJson = JSONObject()
        for ((key, value) in parts) partsJson.put(key, value)
        return JSONObject()
            .put("schema", "transform_contract_hash")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("transform_code_id", transformCodeId)
            .put("contract_parts", partsJson)
            .put("canonical_contract", canonical)
            .put("transform_contract_sha256", Hashing.sha256(canonical))
            .put("anti_cherry_picking_hash", true)
            .put("rule", "Changing genes, sample rules, covariates, formula, topic text, or transform code changes this hash.")
    }
}
