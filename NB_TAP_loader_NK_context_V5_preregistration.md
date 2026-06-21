# A Mapping-Certified, NK-Enriched Cytotoxic-Context Modifier of the TAP-Loader State in Neuroblastoma

### A Preregistered Bulk-Transcriptomic Interaction Protocol with a Mandatory Feature-to-Gene Mapping-Integrity Gate

**Version:** V5 (mapping-certified) · **Hypothesis ID:** `GTIM_2026_NB_LOADER_NK_CONTEXT_V5`
**Claim class:** `NEUROBLASTOMA_LOADER_NK_ENRICHED_CONTEXT_MODIFIER_CANDIDATE`
**Status:** Preregistered hypothesis and analysis plan. No results are reported.

---

## Abstract

**Background.** Neuroblastoma is an immunologically cold pediatric solid tumour in which the MHC class I antigen-processing machinery — including the peptide-loading complex formed by TAP1, TAP2 and the chaperone tapasin (TAPBP) — is frequently downregulated. Whether a low TAP-loader state is clinically adverse may not be fixed, but conditional on whether cytotoxic lymphocytes capable of recognising MHC-I-deficient cells are present. This interaction has not been formally tested. Separately, reanalyses of the most widely used neuroblastoma expression cohort risk a silent feature-to-gene mapping error that can assign expression rows to the wrong genes.

**Hypothesis.** The adverse-outcome association of a low TAP-loader state (APM3_loader = mean z-score of TAP1, TAP2, TAPBP) is attenuated in tumours with a higher NK-enriched cytotoxic context (mean z-score of NKG7, GZMB, KLRD1). The prespecified interaction coefficient is positive.

**Design.** A preregistered, two-sided interaction test (α = 0.01) adjusted for B2M and MYCN, executed only after a mandatory Data-Mapping-Integrity Gate certifies that every expression row resolves to its intended gene by full-platform annotation join, multi-identifier concordance and probe-sequence re-alignment, with a biological positive-control gate. All prior results derived from numeric-identifier coincidence are quarantined and replayed after certified remapping.

**Boundaries.** This is an association hypothesis only. It does not prove NK-cell identity or function, does not predict response to any therapy, is not a treatment-selection classifier, and is not clinically actionable.

---

## 1. Background and Rationale

### 1.1 The TAP-loader state in neuroblastoma

Neuroblastoma carries a low mutational burden and sparse T-cell infiltration, and repeatedly shows reduced surface MHC class I with downregulation of antigen-processing-machinery (APM) components, associated with MYCN amplification and adverse features (Raffaghello et al., 2005; Corrias et al., 2001). The peptide-loading complex — the TAP1/TAP2 transporter and the tapasin (TAPBP) editor — is rate-limiting for assembled, peptide-optimised surface MHC-I (Blees et al., 2017).

### 1.2 Why an interaction, not a main effect

The clinical meaning of a low TAP-loader state is plausibly **conditional**. Where cytotoxic lymphocytes capable of MHC-unrestricted killing (NK and γδ T cells) are present, reduced MHC-I may be exploited through missing-self recognition; where they are absent, low MHC-I may simply mark an immune-cold state or facilitate T-cell evasion. This reasoning predicts that the association between the loader state and outcome is **modified by** cytotoxic context — an interaction hypothesis with a predeclared direction, not a main-effect claim.

### 1.3 Why NK-enriched, not pan-cytotoxic

A general cytotoxic signature such as NKG7 + GZMB conflates effectors that move in opposite directions on a loader-low tumour: MHC-restricted CD8⁺ T cells, which **cannot** recognise MHC-I-deficient cells, and NK/γδ cells, which **can**. A pan-cytotoxic modifier therefore risks self-cancellation or a signal driven by the non-informative arm. Adding KLRD1 (CD94), which is enriched in NK and NK-like lymphocytes, biases the modifier toward the MHC-unrestricted arm whose direction the missing-self logic predicts. KLRD1 is mandatory and may not be dropped or substituted.

### 1.4 Why mapping integrity is a precondition

The principal discovery cohort, GSE49710 (n = 498), is hosted on platform **GPL16876, Agilent-020382 Human Custom Microarray 44k (Feature Number version)**. The matrix `ID_REF` values are Agilent feature numbers, **not** Entrez Gene IDs. Assigning rows by numeric coincidence — for example mapping rows "6890/6891/6892" to TAP1/TAP2/TAPBP because those are the Entrez IDs of those genes — silently attaches expression to the wrong features. Because such an analysis can be statistically valid while measuring the wrong genes, feature-to-gene mapping certification is a precondition for any model or verdict, not a downstream check. The validation cohort GSE85047 is on a different platform (GPL5175, Affymetrix Human Exon 1.0 ST) and requires its own independent mapping certification.

---

## 2. Hypothesis

**Primary hypothesis (H1).** In neuroblastoma, the association between APM3_loader and adverse outcome is modified by NK_enriched_context such that higher NK_enriched_context attenuates the adverse association of low APM3_loader. With higher expression encoded as a higher score, the prespecified `APM3_loader × NK_enriched_context` interaction coefficient is positive.

**Null hypothesis (H0).** The interaction coefficient is zero after adjustment for B2M and MYCN.

---

## 3. Methods

### 3.1 Frozen score definitions

| Score | Genes | Formula | Status |
|---|---|---|---|
| **APM3_loader** | TAP1, TAP2, TAPBP | mean z-score(TAP1, TAP2, TAPBP) | FROZEN |
| **NK_enriched_context** | NKG7, GZMB, KLRD1 | mean z-score(NKG7, GZMB, KLRD1) | FROZEN |
| **B2M** | B2M | z-score(B2M) | Separate integrity/adjustment variable; never scored with the loader |

B2M is excluded from APM3_loader because B2M and the loader genes are co-regulated, which would create partial circularity when B2M also informs the MHC-I surface phenotype. Definitions are frozen and may not be modified after any outcome field is examined.

### 3.2 Data-Mapping-Integrity Gate (required before all analysis)

Execution is blocked unless `identifier_namespace_verified = PASS`. The lock `NUMERIC_ID_COINCIDENCE_IS_NOT_GENE_MAPPING` applies. The gate proceeds, strictly blind to all outcome fields, as:

1. **Platform identity.** Confirm the exact GPL accession and matrix ID namespace before any join.
2. **Full annotation join.** Resolve every matrix feature through the complete official platform annotation: `matrix_ID_REF → platform_feature_ID → gene`.
3. **Multi-identifier concordance.** For each of the eight frozen genes require concordant GeneSymbol and EntrezGeneID, plus Ensembl, RefSeq or UniProt where available. Reject control, ambiguous, multi-gene or conflicting features.
4. **Sequence-level confirmation (mandatory for the eight frozen genes).** Re-align each candidate feature's probe sequence to the current genome assembly and confirm it maps uniquely to the intended gene locus. Annotation-identifier concordance alone is insufficient, because all identifiers can inherit a common upstream annotation error. A gene whose feature fails sequence confirmation is `PRIMARY_GENE_NOT_SOURCE_CERTIFIED`.
5. **Probe-collapse rule with a predeclared concordance threshold.** When a gene maps to multiple validated features, compute pairwise across-sample Spearman correlations among those features (outcome-blind). If the minimum pairwise ρ ≥ 0.50, collapse by the per-sample median of standardised features. If the minimum pairwise ρ < 0.50, return `MULTI_PROBE_DISCORDANCE_DATA_TILE_REQUIRED`. Probe selection by outcome association, p-value, effect size or survival performance is prohibited.
6. **Biological positive-control gate (blocking, not advisory).** After mapping, the join must pass predeclared biological checks or execution halts: (a) **MYCN concordance** — MYCN expression must be bimodal and concordant with the known MYCN-amplification labels in the cohort (strong positive control available in GSE49710); (b) **sex concordance** — XIST and Y-linked genes consistent with recorded sex where available; (c) a housekeeping-gene sanity check. Failure returns `BIOLOGICAL_QA_FAILED_MAPPING_SUSPECT`.
7. **Outcome-blind mapping freeze and receipt.** Freeze the verified feature set and issue a mapping receipt recording, per gene, the selected platform feature IDs, the annotation source/version/date, the sequence-confirmation result, the concordance metric and collapse decision, the biological-QA status, and a SHA-256 of the frozen mapping.

### 3.3 Prior-result quarantine

All previous GSE49710 results derived from direct numeric `ID_REF`-to-Entrez interpretation are quarantined: treated as neither supported, null, nor falsified, and labelled `PREVIOUS_RESULT_MAPPING_DEPENDENT_NOT_INTERPRETABLE`. This explicitly includes the founding discovery anchor (the APM-low/adverse-event association) and every dependent model; the entire lineage is provisionally un-anchored until the discovery anchor is replayed on the certified mapping.

### 3.4 Primary model

After mapping certification and outcome-blind score construction:

- **Event endpoint (e.g., GSE49710):**
  `adverse_event ~ APM3_loader + NK_enriched_context + APM3_loader:NK_enriched_context + B2M + MYCN`
- **Time-to-event endpoint (e.g., GSE85047, TARGET-NBL):**
  `Surv(time, event) ~ APM3_loader + NK_enriched_context + APM3_loader:NK_enriched_context + B2M + MYCN`

**Primary test:** the `APM3_loader:NK_enriched_context` interaction coefficient. **Significance threshold:** α = 0.01, two-sided, with a predeclared positive direction. Scores are continuous z-scores; no median split enters the primary model (a predeclared median-split view may be used for visualisation only).

### 3.5 Power, estimand and replication strategy

Interaction tests require substantially larger samples than main effects, and α = 0.01 is conservative; an uninformative result is a realistic outcome and is reported honestly as `INTERACTION_NOT_ESTIMABLE_UNDERPOWERED`.

- **Predeclared power screen.** For each cohort, report the minimum detectable interaction effect at α = 0.01 and 80% power given its n and event count, computed before interpreting the estimate.
- **Primary promotion path: directional independent replication.** The confirmatory criterion is replication of the identical, KLRD1-anchored, sign-consistent interaction in an independently mapping-certified cohort with a harmonised endpoint. This path requires only directional concordance and therefore avoids cross-platform measurement-scale pooling.
- **Sensitivity only: harmonised meta-analysis.** A prespecified random-effects interaction meta-analysis across cohorts may be reported as sensitivity, with an explicit caveat that GPL16876 (Agilent), GPL5175 (Affymetrix Exon) and RNA-seq differ in dynamic range and require per-platform standardisation to a common gene-symbol space; it does not replace directional replication.

### 3.6 Sensitivity models

- Add continuous ADRN and MES lineage scores.
- Add an NK-orthogonal tumour-purity estimate (e.g., copy-number-based) when available.
- Do **not** adjust for an immune-infiltration score containing NKG7, GZMB, KLRD1 or overlapping cytotoxic genes; adjusting for infiltration that overlaps the modifier risks overadjustment and removal of the very signal under test.

### 3.7 Cohorts and platform-specific certification

| Cohort | Platform | n | Endpoint | Role | Mapping requirement |
|---|---|---|---|---|---|
| GSE49710 | GPL16876 (Agilent 44k, Feature Number) | 498 | Event label | Discovery | Full GPL16876 feature-number → gene join + sequence confirmation + certified replay |
| GSE85047 | GPL5175 (Affymetrix Exon 1.0 ST) | ~272 | PFS | Replication | Independent GPL5175 transcript-cluster mapping |
| TARGET-NBL | RNA-seq | ~150+ | EFS/OS | Replication | Certified gene-level identifiers + endpoint alignment |

A cohort is primary-eligible only if all eight frozen genes — including KLRD1 — are mapping-certified and source-present. No primary gene may be dropped, imputed or substituted; KLRD1 absence on a certified platform yields `PRIMARY_GENE_NOT_SOURCE_CERTIFIED` for that cohort.

### 3.8 Required reporting

Per analysis: selected platform feature IDs for every gene; annotation source, version, date and SHA-256; multi-identifier concordance; sequence-confirmation result; probe-collapse decision and concordance ρ; biological-QA status; interaction β; OR or HR; 95% CI; two-sided p; declared-direction match; model convergence; maximum VIF; condition number; and the minimum-detectable-effect / precision screen.

---

## 4. Predeclared Outcomes

| Outcome | Meaning |
|---|---|
| `INTERACTION_SUPPORTED_DECLARED_DIRECTION` | Significant positive interaction; loader–outcome association attenuated by NK-enriched context |
| `INTERACTION_SUPPORTED_OPPOSITE_DIRECTION` | Significant interaction in the non-declared direction; distinct, non-promoting |
| `INTERACTION_NOT_SUPPORTED` | Interaction not significant after adjustment |
| `INTERACTION_NOT_ESTIMABLE_UNDERPOWERED` | Sample size, events or collinearity preclude estimation |
| `PLATFORM_MAPPING_REQUIRED_BEFORE_ANALYSIS` | Mapping not yet source-certified |
| `MULTI_PROBE_DISCORDANCE_DATA_TILE_REQUIRED` | Validated probes for a gene are discordant below threshold |
| `BIOLOGICAL_QA_FAILED_MAPPING_SUSPECT` | Mapping passed annotation but failed positive-control checks |
| `PRIMARY_GENE_NOT_SOURCE_CERTIFIED` | A frozen primary gene (incl. KLRD1) cannot be certified on the platform |

---

## 5. Falsification Conditions

1. A correctly mapped, adequately powered, non-significant interaction → `INTERACTION_NOT_SUPPORTED`: the NK-enriched modifier hypothesis is not supported.
2. A significant interaction in the opposite direction → the declared modifier is not promoted.
3. An interaction that disappears after ADRN/MES or B2M adjustment → attributable to lineage or B2M co-regulation, not the loader–context interaction.
4. Mapping or biological-QA failure → execution is blocked; no biological inference is drawn.

The hypothesis is not promoted on any uninterpretable, underpowered or mapping-deficient result.

---

## 6. Claim Boundaries

**Permitted:** testing and reporting whether the loader–outcome association is modified by NK-enriched cytotoxic context, including the interaction term, its direction and its confidence interval; clearly labelled exploratory analyses of secondary modifiers (HLA-E/KLRC1, NECTIN2/TIGIT/CD226, MICA/MICB, ODC1, γδ markers), excluded from the primary model.

**Not permitted:** claiming that low MHC-I causes NK-cell killing; proving NK-cell identity or function; predicting response to NK, γδ, T-cell or vaccine therapy; functioning as a treatment-selection classifier; excluding patients from any therapy; claiming immune-escape proof, clinical actionability or wet-lab readiness.

The only claim class is `NEUROBLASTOMA_LOADER_NK_ENRICHED_CONTEXT_MODIFIER_CANDIDATE`.

---

## 7. Relationship to Prior Work

This protocol is the bulk-cohort-testable, mapping-certified companion to a more specific mechanistic model (the TAP-loader immune-recognition-switch hypothesis, which proposes that a low loader state collapses the HLA-E/NKG2A inhibitory checkpoint and licenses NK/γδ killing conditional on activating-ligand and polyamine context, and which requires matched tumour-cell surface measurement and causal perturbation). It is the successor to earlier APM4 matched-state versions: it removes B2M from the score (breaking partial circularity), upgrades the modifier from pan-cytotoxic to NK-enriched, and elevates feature-to-gene mapping integrity from an implicit assumption to an explicit, certified precondition.

---

## 8. Data, Code and Registration

All datasets are publicly available (GSE49710, GSE85047, TARGET-NBL). The hypothesis, frozen score definitions, mapping-integrity gate, primary model and outcome vocabulary are preregistered in this document prior to certified mapping and outcome examination. Mapping receipts and execution receipts are versioned and hashed.

---

## References (to be verified against primary sources before deposit)

1. Raffaghello L, et al. Multiple defects of the antigen-processing machinery in human neuroblastoma. *J Natl Cancer Inst*, 2005.
2. Corrias MV, et al. Lack of HLA class I antigens in human neuroblastoma cells. *Int J Cancer*, 2001.
3. Blees A, et al. Structure of the human MHC-I peptide-loading complex. *Nature*, 2017.
4. van Groningen T, et al. Neuroblastoma is composed of two super-enhancer-associated differentiation states. *Nat Genet*, 2017.
5. Zhang W, et al. Comparison of RNA-seq and microarray-based models for the SEQC neuroblastoma cohort (GSE49710). *Genome Biol*, 2015.
6. Ng SS, et al. The NK cell granule protein NKG7 regulates cytotoxic granule exocytosis and inflammation. *Nat Immunol*, 2020.
7. Jongsma MLM, et al. The regulatory network behind MHC class I expression. *Mol Immunol*, 2019.

*Citation list is provisional; verify every reference and add DOIs before submission or deposit.*
