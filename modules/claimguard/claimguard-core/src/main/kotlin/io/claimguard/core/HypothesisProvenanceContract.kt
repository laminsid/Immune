package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject

/**
 * Hypothesis provenance so the slice cannot be quietly cherry-picked after the result.
 *
 * Ported from HypothesisProvenanceContractV30392. The neuroblastoma axis constants
 * were removed: the declared gene set / covariates / outcome are taken from the
 * caller's hypothesis contract (or generic defaults), never from a hardcoded disease.
 *
 * The anti-cherry-picking guarantee is unchanged: hypothesis text, gene set, outcome
 * and covariates are hashed BEFORE the verdict is interpreted.
 */
object HypothesisProvenanceContract {
    const val REQUIRED_TOKEN: String = "HYPOTHESIS_PROVENANCE_CONTRACT"
    const val PREDECLARED: String = "HYPOTHESIS_PREDECLARED"
    const val POST_HOC_REVIEW_ONLY: String = "HYPOTHESIS_POST_HOC_REVIEW_ONLY"
    const val IMPORTED_FROM_LITERATURE: String = "HYPOTHESIS_IMPORTED_FROM_LITERATURE"
    const val USER_SUPPLIED_UNREGISTERED: String = "HYPOTHESIS_USER_SUPPLIED_UNREGISTERED"
    const val AI_GENERATED_UNREGISTERED: String = "HYPOTHESIS_AI_GENERATED_UNREGISTERED"
    const val ENGINE_LOCKED_BEFORE_MODEL_INTERPRETATION: String = "ENGINE_LOCKED_BEFORE_THIS_RUN_MODEL_INTERPRETATION"

    /**
     * Build the provenance contract from a generic "hypothesis_contract" object:
     *   {
     *     "hypothesisId": "...", "hypothesisText": "...", "dataset": "...",
     *     "declaredGenes": [...], "covariates": [...], "outcome": "...",
     *     "locked": true|false,
     *     "source": { "system": "Google Co-Scientist", "model_version": "...",
     *                 "prompt": "...", "raw_output": "...", "captured_at": "..." }
     *   }
     */
    fun evaluate(run: JSONObject): JSONObject {
        val contract = run.optJSONObject("hypothesis_contract") ?: JSONObject()
        val declaredGenes = Hashing.unique(contract.optJSONArray("declaredGenes") ?: JSONArray())
        val covariates = contract.optJSONArray("covariates") ?: JSONArray()
        val topic = contract.optString("hypothesisText", run.optString("topic", ""))
        val source = contract.optJSONObject("source") ?: JSONObject()

        val registrationState = when {
            contract.optString("registrationState", "").isNotBlank() -> contract.optString("registrationState")
            contract.optBoolean("literatureImported", false) -> IMPORTED_FROM_LITERATURE
            contract.optBoolean("externallyPredeclared", false) -> PREDECLARED
            source.optString("system", "").isNotBlank() -> AI_GENERATED_UNREGISTERED
            topic.isBlank() -> POST_HOC_REVIEW_ONLY
            else -> USER_SUPPLIED_UNREGISTERED
        }
        return JSONObject()
            .put("schema", "hypothesis_provenance_contract")
            .put("requiredToken", REQUIRED_TOKEN)
            .put("hypothesis_id", contract.optString("hypothesisId", "UNREGISTERED_HYPOTHESIS"))
            .put("hypothesis_registration_state", registrationState)
            .put("run_lock_state", if (contract.optBoolean("locked", false)) ENGINE_LOCKED_BEFORE_MODEL_INTERPRETATION else POST_HOC_REVIEW_ONLY)
            .put("declared_before_result", contract.optBoolean("locked", false))
            .put("external_preregistration", registrationState == PREDECLARED)
            // Provenance of an AI-proposed hypothesis: which system/model/prompt produced it.
            .put("hypothesis_source", source)
            .put("hypothesis_text", topic.take(1200))
            .put("hypothesis_text_sha256", Hashing.sha256(topic))
            .put("declared_genes", declaredGenes)
            .put("declared_gene_set_sha256", Hashing.sha256(Hashing.canonicalArray(declaredGenes)))
            .put("declared_outcome", contract.optString("outcome", "OUTCOME_UNSPECIFIED"))
            .put("declared_covariates", covariates)
            .put("declared_covariates_sha256", Hashing.sha256(Hashing.canonicalArray(covariates)))
            .put("dataset", contract.optString("dataset", "DATASET_UNSPECIFIED"))
            .put("anti_cherry_picking_rule", "Hypothesis text, gene set, outcome, covariates, sample inclusion rule, model formula, and transform code are hashed as a contract before interpreting the verdict.")
    }
}
