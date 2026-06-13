# ImmuneErrorRadar / GTIM

**Vraimony-powered hypothesis stress-test, evidence-readiness gate, and falsification protocol for immunology and oncology research.**

ImmuneErrorRadar / GTIM is a research-oriented Android/Kotlin engine for testing biomedical hypotheses before expensive experimental follow-up. It parses a supplied claim, maps it to available evidence, applies falsification gates, blocks over-claiming, and produces reviewer-readable reports with explicit boundaries.

This project is **not** a medical device, not a diagnostic tool, not a treatment recommendation system, not a clinical decision-support product, and not a wet-lab validation system. It is a research software prototype for hypothesis triage, falsification, evidence-readiness review, calibration, and preprint-preparation workflows.

Repository: https://github.com/laminsid/Immune

---

## Current Release

**Version:** `v3.0.6.9.8-history-titles-privacy-final`

This release is the current professional preprint-ready baseline. It consolidates the earlier publication-data fuel, UI cleanup, report history, calibration ledger, Vraimony documentation layer, ERF-inspired receipts, multi-cohort expansion guard, and privacy-safe report naming.

Key additions in the current baseline:

- **Powered by Vraimony** report identity.
- **ImmuneErrorRadar falsification protocol** as the named methodology standard.
- **ERF-inspired evidence receipt discipline**: hash-first, portable, replayable, claim-bounded report records.
- Local falsification receipts with `receipt_id`, `contentSha256`, protocol name, report boundary, and `signedByVraimony=false` unless a future server-signing workflow is used.
- Professional report history panel with date-grouped reports, hypothesis-derived titles, selected report reading view, copy, download, and print actions.
- Calibration set / translation memory: every tested hypothesis is stored as a pattern outcome such as killed, watchlist, data-only, not measurable, null-like, or review-only survivor.
- APM/B2M-TAP-HLA remains the only current `INVEST_IN_DATA_ONLY` route.
- CK2, HDAC/DNMT, NECTIN2/TIGIT, gamma-delta/NKG2D, ODC1/polyamine, CD276/B7-H3, hypoxia/stroma, and mesenchymal/stromal routes remain killed, watchlist, not measurable, or counter-signal only unless stronger independent evidence is supplied.
- Pediatric cross-tumor scope guard: neuroblastoma-only evidence is explicitly blocked from pan-pediatric-tumor promotion.
- APM multi-cohort fuel: validation targets are injected as **data-fuel only**, not as executed replication and not as synthetic evidence.
- Upload button remains directly visible; obsolete More controls path was removed.
- Search/progress feedback remains visible while maintaining CI compatibility.
- Hypothesis input clears after successful report generation.
- Large uploaded files are processed through streaming/chunked reading instead of loading the full file into memory.
- Report titles are derived from the tested hypothesis, making history search and retrieval usable.
- Personal-name attribution was removed from generated reports; public reports use Vraimony methodology wording.

---

## Core Research Purpose

The engine is designed around one operational question:

> Does this supplied biomedical hypothesis survive first-pass falsification well enough to justify further data work?

It is **not** a hypothesis generator and should not be marketed as an AI discovery engine. Its value is in killing weak claims early, preserving bounded data-only leads, and producing audit-friendly evidence receipts.

The engine classifies each supplied hypothesis into practical states:

- `DO_NOT_INVEST_CLAIM_KILLED`
- `WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB`
- `WATCHLIST_METHOD_COUNTERSIGNAL_NO_INVEST`
- `NOT_MEASURABLE_PROBE_AND_CONTEXT_BLOCKED`
- `NULL_LIKE_OR_INCONCLUSIVE`
- `SURVIVED_LOCAL_DIRECTION_REVIEW_ONLY`
- `INVEST_IN_DATA_ONLY`

Only `INVEST_IN_DATA_ONLY` allows more computational/data acquisition work. It does **not** allow wet-lab promotion or biology-proof language.

---

## Vraimony-Powered Documentation Layer

Every generated report is branded and bounded as:

```text
Powered by Vraimony
Protocol: ImmuneErrorRadar falsification protocol
Documentation standard: ERF-inspired evidence receipt discipline
```

The report receipt is local and claim-bounded. It records the report payload hash and replay identity, but it does not claim clinical validation, wet-lab evidence, or biological proof.

Current receipt boundary:

```text
signedByVraimony=false
```

This is intentional. The current Android-local build creates a falsification receipt, not a Vraimony server-signed certificate.

---

## ERF-Inspired Evidence Receipt Discipline

ImmuneErrorRadar borrows the evidence discipline from Vraimony-style ERF thinking:

1. **Hash-first**: every report can carry a content hash or replay receipt.
2. **Portable**: report text, decision state, and evidence boundaries are readable outside the app.
3. **Replayable**: a report should describe enough of the route, missing gates, and claim guard to be reviewed later.
4. **Claim-bounded**: a receipt proves report integrity and workflow state, not scientific truth.
5. **Reviewer-readable**: the receiver must understand what was tested, what was not tested, and what is blocked.

This makes the report useful for researchers, reviewers, and preprint readers without overstating the evidence.

---

## Current Biomedical Focus

The active publication-readiness track focuses on pediatric neuroblastoma immune-evasion hypotheses.

Primary axis retained for data-only follow-up:

- Antigen-presentation machinery (APM)
- B2M / TAP / HLA signal review
- NK and immune-effector context
- MYCN-aware interpretation
- Independent replication requirement before promotion

Current rule:

```text
APM / B2M-TAP-HLA = INVEST_IN_DATA_ONLY
```

This means mapping, vector extraction, independent cohort replication, direction-stability checks, and bulk-attribution/deconvolution checks may continue. It does **not** mean wet-lab candidacy.

---

## Three-Cohort / Cross-Tumor Expansion Guard

A single neuroblastoma cohort is not enough for a broad pediatric oncology claim. The current release therefore uses a three-layer validation guard:

1. **Primary neuroblastoma cohort**
   - GSE85047 is treated as the current primary neuroblastoma stress-test dataset.

2. **Neuroblastoma replication candidates**
   - GSE49710 and TARGET-NBL are treated as required replication/data-acquisition targets before Tier-2 computational evidence language.

3. **External pediatric tumor-family expansion targets**
   - Medulloblastoma
   - Wilms tumor / nephroblastoma
   - Ewing sarcoma

The app must not promote pan-pediatric-tumor claims until independent human datasets from the required external tumor families are reviewed with separate receipts.

Current cross-tumor guard:

```text
NEUROBLASTOMA_ONLY_SINGLE_COHORT_SCOPE
crossTumorPromotionAllowed=false
wetLabPromotionAllowed=false
```

---

## Calibration Set / Translation Memory

Every hypothesis tested through the platform contributes to a calibration set.

Stored pattern examples:

- This pattern was killed after MYCN adjustment.
- This mechanism collapsed into APM but was not attributable.
- This bulk checkpoint claim was not measurable.
- This signal survived only as data-only follow-up.
- This subgroup route remained watchlist only.

The calibration set is not biological proof. It is a historical translation layer that helps future reports recognize recurring failure and survival patterns.

---

## Report History and Retrieval

The report history panel is intended for real research use.

Current behavior:

- Reports are grouped by date.
- Reports are sorted chronologically.
- Each report title is derived from the tested hypothesis.
- Selecting a date filters the report list.
- Selecting a report opens a readable report panel.
- Report actions include copy, download, and print.

Examples of generated report titles:

```text
CK2/CSNK2A1 -> APM mechanism claim - killed as written
HDAC/DNMT -> APM mechanism claim - killed as written
NECTIN2/TIGIT bulk checkpoint claim - killed as written
Gamma-delta/NKG2D surrogate claim - killed as written
APM/B2M-TAP-HLA data axis - data-only follow-up
```

---

## Uploaded File Handling

Large uploaded files are treated as routing context, not automatic proof.

The current reader avoids loading full large files into memory. It uses streaming/chunked reading and extracts only relevant text slices:

- file head sample
- file tail sample
- route-relevant lines
- dataset/accession markers
- gene/pathway/platform terms
- partition summaries

Boundary:

> A user-uploaded file can support routing and review context, but it does not certify provenance, biological truth, or statistical validity by itself.

---

## Scientific Boundaries

The project follows strict claim boundaries:

- No diagnosis.
- No treatment advice.
- No dosing advice.
- No patient-specific guidance.
- No clinical actionability claim.
- No wet-lab promotion from Tier-0 outputs.
- No claim that a mechanism is proven from static bulk data alone.
- No synthetic data or fake replication.
- No pan-cancer or pan-pediatric-tumor generalization from one cohort.
- No “AI discovered a cure” language.
- No strong claim without replication, comparator alignment, source/probe audit, confounder handling, and falsifier survival.

Preferred language:

- “Killed as written.”
- “Blocked by missing evidence.”
- “Invest in data only.”
- “Review-only directional screen.”
- “Not measurable with current data.”
- “Tier-0 replayability only.”
- “No wet-lab candidacy.”

---

## Main Workflow

1. Researcher enters a biomedical hypothesis.
2. Engine parses structured intent and biological route.
3. Available evidence and route-specific constraints are checked.
4. Uploaded files may provide additional routing context.
5. Claim guards and falsification gates are applied.
6. Report title is derived from the hypothesis.
7. A Vraimony-powered falsification receipt is created.
8. The report is stored in history and calibration set.
9. The researcher can open, copy, download, or print the report.

---

## Repository Structure

```text
app/
  src/main/java/com/immunesignal/app/
    ResearchAutopilotActivity.kt
    ResearchReportHistoryRendererV30694.kt
    ResearchReportTitleDeriverV30698.kt
    HypothesisCalibrationSetV30696.kt
    VraimonyFalsificationProtocolReceiptV30697.kt
    PediatricApmMultiCohortFuelV30696.kt
    PediatricMultiTumorCohortExpansionV30695.kt
    UserUploadedFileSmartReaderV30691.kt
    PublicationPreprintReadinessV30680.kt
    PublicationDataFuelPackV30690.kt
    ...
  src/main/assets/protocols/
    immuneerrorradar_falsification_protocol_v30697.json
  src/main/res/layout/
    activity_research_autopilot.xml
scripts/
  run_static_checks_fast.sh
  static_checks/
    audit_research_engine_v30692_ui_upload_history_final.py
    audit_research_engine_v30693_progress_audit_compat.py
    audit_research_engine_v30694_activity_size_extraction.py
    audit_research_engine_v30695_pediatric_multi_tumor_guard.py
    audit_research_engine_v30696_history_calibration_apm_multicohort.py
    audit_research_engine_v30697_vraimony_falsification_protocol.py
    audit_research_engine_v30698_history_titles_privacy.py
docs/
  IMMUNEERRORRADAR_FALSIFICATION_PROTOCOL.md
  PREPRINT_DATA_FUEL_v3.0.6.9.md
```

---

## Local Static Checks

Run the fast static checks:

```bash
bash scripts/run_static_checks_fast.sh
```

Important checks include:

- Kotlin delimiter audit
- JSON validation
- XML parse/layout checks
- UI/upload/history audit
- progress audit compatibility
- activity-size reduction audit
- publication data fuel audit
- pediatric multi-tumor guard audit
- history/calibration/APM multi-cohort audit
- Vraimony falsification protocol audit
- history title/privacy audit

---

## Android Build

Debug build:

```bash
./gradlew :app:assembleDebug
```

Kotlin compile check:

```bash
./gradlew :app:compileDebugKotlin
```

If Gradle cannot download dependencies, verify network/DNS access to Gradle distribution services or use a cached Gradle wrapper environment.

---

## Preprint-Readiness Policy

Default policy:

```text
DO_NOT_INVEST_CLAIM_KILLED -> no experimental promotion
WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB -> no experimental promotion
WATCHLIST_METHOD_COUNTERSIGNAL_NO_INVEST -> no experimental promotion
NOT_MEASURABLE_PROBE_AND_CONTEXT_BLOCKED -> no promotion
INVEST_IN_DATA_ONLY -> data acquisition and replication only; no wet-lab claim
```

Stronger promotion requires Tier-2 evidence: independent cohort replication with suitable outcome, comparator/covariate alignment, source/probe validation, and stable direction after falsifier checks.

---

## What This Project Is Not

This project is not:

- a clinical diagnostic product
- a medical app for patients
- a treatment recommendation engine
- a substitute for laboratory validation
- a substitute for expert biomedical review
- a certified scientific study
- a claim that AI has discovered a cure or proven a mechanism

---

## Intended Users

Intended users include:

- biomedical researchers
- computational biology reviewers
- immunology and oncology research teams
- preprint authors evaluating claim readiness
- labs that need a stricter evidence gate before spending experimental resources

---

## License

Add your chosen license before public release.

Recommended options:

- `Apache-2.0` for permissive open-source adoption.
- `MIT` for a simple permissive release.
- Custom/private license if the repository is not ready for open public reuse.

---

## Maintainer Note

The core rule is simple:

> Evidence gates the claim. The engine may route, stress-test, document, and falsify; it must not overclaim biological proof.
