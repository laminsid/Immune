package io.claimguard.core

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Behavior ported 1:1 from the original Tier0Gse85047ReplayV30392Test, restated
 * against the decoupled core. If these pass, the fence still holds after extraction.
 */
class ClaimGuardCoreTest {

    @Test
    fun tier0BlocksComputationalKillAndSurviveLanguage() {
        val kill = VerificationTierVerdictPolicy.enforce(EvidenceVerificationTier.TIER0, "COMPUTATIONAL_KILL")
        assertFalse(kill.getBoolean("allowed"))
        assertEquals(VerificationTierVerdictPolicy.BLOCKED, kill.getString("enforcedVerdict"))

        val survive = VerificationTierVerdictPolicy.enforce(EvidenceVerificationTier.TIER0, "SURVIVING_COMPUTATIONAL_EVIDENCE")
        assertFalse(survive.getBoolean("allowed"))
        assertEquals(VerificationTierVerdictPolicy.BLOCKED, survive.getString("enforcedVerdict"))
    }

    @Test
    fun tier1AllowsLabUpgradeButNotKill() {
        val lab = VerificationTierVerdictPolicy.enforce(EvidenceVerificationTier.TIER1, "LAB_UPGRADE_CANDIDATE")
        assertTrue(lab.getBoolean("allowed"))
        val kill = VerificationTierVerdictPolicy.enforce(EvidenceVerificationTier.TIER1, "COMPUTATIONAL_KILL")
        assertFalse(kill.getBoolean("allowed"))
    }

    @Test
    fun tier2AllowsKill() {
        val kill = VerificationTierVerdictPolicy.enforce(EvidenceVerificationTier.TIER2, "COMPUTATIONAL_KILL")
        assertTrue(kill.getBoolean("allowed"))
        assertEquals("COMPUTATIONAL_KILL", kill.getString("enforcedVerdict"))
    }

    @Test
    fun selectedMatrixStaysTier0ReviewOnly() {
        val run = JSONObject()
            .put("hypothesis_contract", JSONObject()
                .put("hypothesisId", "NK_EFFECTOR_PFS_MYCN_GSE85047")
                .put("hypothesisText", "NK effector CD276 neuroblastoma PFS")
                .put("declaredGenes", JSONArray(listOf("NKG7", "GZMB", "MYCN", "CD276")))
                .put("covariates", JSONArray(listOf("MYCN")))
                .put("outcome", "PFS").put("dataset", "GSE85047").put("locked", true))
            .put("prior_receipt", JSONObject().put("verdict", "COMPUTATIONAL_KILL"))
        val receipt = VerificationReceiptBridge.evaluate(run)
        assertEquals(EvidenceVerificationTier.TIER0, receipt.getJSONObject("verification").getString("verification_tier"))
        assertEquals(VerificationTierVerdictPolicy.BLOCKED, receipt.getString("enforced_verdict"))
        assertFalse(receipt.getJSONObject("evidence_strength").getBoolean("promotion_allowed"))
    }

    @Test
    fun transformContractHashChangesWhenDeclaredGenesChange() {
        fun hashFor(genes: List<String>): String {
            val run = JSONObject().put("hypothesis_contract", JSONObject()
                .put("hypothesisText", "topic")
                .put("declaredGenes", JSONArray(genes))
                .put("covariates", JSONArray(listOf("MYCN"))))
            val prov = HypothesisProvenanceContract.evaluate(run)
            val slice = SliceSelectionContract.evaluate(run, prov)
            return TransformContractHash.evaluate(prov, slice).getString("transform_contract_sha256")
        }
        assertNotEquals(hashFor(listOf("CD276", "GZMB", "MYCN", "NKG7")),
            hashFor(listOf("CD276", "GZMB", "MYCN", "NKG7", "ODC1")))
        // stable under reordering (canonical set)
        assertEquals(hashFor(listOf("CD276", "GZMB", "MYCN", "NKG7")),
            hashFor(listOf("NKG7", "MYCN", "GZMB", "CD276")))
    }

    @Test
    fun fullTier2ChainPromotes() {
        val run = JSONObject()
            .put("hypothesis_contract", JSONObject().put("hypothesisText", "t").put("locked", true))
            .put("prior_receipt", JSONObject().put("verdict", "COMPUTATIONAL_KILL"))
            .put("source_certification", JSONObject().put("sourceCertified", true))
            .put("full_mapping_audit", JSONObject().put("state", "FULL_MAPPING_PASS"))
            .put("replication_gate", JSONObject().put("independent_replication", "PASS"))
        val receipt = VerificationReceiptBridge.evaluate(run)
        assertEquals(EvidenceVerificationTier.TIER2, receipt.getJSONObject("verification").getString("verification_tier"))
        assertEquals("COMPUTATIONAL_KILL", receipt.getString("enforced_verdict"))
        assertTrue(receipt.getJSONObject("evidence_strength").getBoolean("promotion_allowed"))
    }

    @Test
    fun sanitizerDowngradesUnsupportedKillBelowTier2() {
        val run = JSONObject()
            .put("hypothesis_contract", JSONObject().put("hypothesisText", "t"))
            .put("report_surface", JSONObject().put("verdict", "COMPUTATIONAL_KILL"))
        val result = ClaimGuard.assess(run)
        assertTrue(result.overclaiming)
        assertEquals(VerificationTierVerdictPolicy.BLOCKED, result.enforcedVerdict)
    }

    @Test
    fun aiProposedHypothesisCarriesProvenance() {
        val run = JSONObject().put("hypothesis_contract", JSONObject()
            .put("hypothesisText", "MICA-high + low NK predicts worse PFS independent of MYCN")
            .put("declaredGenes", JSONArray(listOf("MICA", "NKG7", "GZMB", "MYCN")))
            .put("source", JSONObject()
                .put("system", "Google Co-Scientist").put("model_version", "gemini-x")
                .put("prompt", "propose neuroblastoma immune-evasion hypotheses")
                .put("captured_at", "2026-06-10T16:40:00Z")))
        val prov = HypothesisProvenanceContract.evaluate(run)
        assertEquals(HypothesisProvenanceContract.AI_GENERATED_UNREGISTERED,
            prov.getString("hypothesis_registration_state"))
        assertEquals("Google Co-Scientist", prov.getJSONObject("hypothesis_source").getString("system"))
    }
}
