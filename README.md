# ImmuneErrorRadar / GTIM

**Hypothesis Stress-Test & Evidence Readiness Gate for Immunology and Oncology Research**

ImmuneErrorRadar / GTIM is a research-oriented Android/Kotlin engine for evaluating biomedical hypotheses before expensive experimental follow-up. It is designed to stress-test claims against available evidence, detect weak or confounded computational signals, and produce reviewer-readable reports with explicit boundaries.

This project is **not** a medical device, not a diagnostic tool, not a treatment recommendation system, and not a clinical decision-support product. It is a research software prototype for hypothesis triage, falsification, evidence-readiness review, and publication-preparation workflows.

---

## Current Release

**Version:** `v3.0.6.9.4-activity-reduction-ci-final`

This release focuses on preprint-readiness, UI cleanup, upload handling, report history, and CI compatibility.

Key additions:

- Preprint-oriented verdict layer for biomedical hypothesis stress-testing.
- APM / B2M-TAP-HLA remains the only `INVEST_IN_DATA_ONLY` route in the current neuroblastoma publication-data fuel pack.
- CK2, HDAC/DNMT, NECTIN2/TIGIT, γδ/NKG2D, ODC1/polyamine, and CD276/B7-H3 routes are constrained to killed/watchlist states unless stronger independent evidence is provided.
- Mesenchymal/stromal counter-signal routing is separated from generic hypothesis routing.
- `experimentalPromotionAllowed=false` is enforced for killed and watchlist decisions.
- Upload button remains directly visible; obsolete “More controls” UI path was removed.
- Search/progress feedback was restored with CI-compatible progress behavior.
- Hypothesis input is cleared after successful report generation.
- Report history panel was added and indexed by date.
- Large uploaded files are processed through streaming/chunked reading instead of loading the full file into memory.
- `ResearchAutopilotActivity` was reduced by extracting report history rendering into a separate class.

---

## Research Purpose

The core question this engine asks is not:

> “Can AI generate a new biomedical hypothesis?”

The core question is:

> “Does this hypothesis survive first-pass computational falsification well enough to justify further data work?”

The engine is designed to help researchers identify whether a claim is:

- **Killed** by current data or confounder adjustment.
- **Null-like** or too weak to promote.
- **Watchlist only** and not worth lab spending yet.
- **Not measurable** with the available data.
- **Invest in data only** when the route deserves more mapping, replication, or comparator evidence.
- **Computational evidence candidate** only after stricter evidence gates are passed.

---

## Scientific Boundaries

This project follows strict claim boundaries:

- No diagnosis.
- No treatment advice.
- No dosing advice.
- No patient-specific medical guidance.
- No claim that a mechanism is biologically proven from static bulk data alone.
- No wet-lab promotion from killed, watchlist, surrogate-only, or underpowered results.
- No “AI discovered a cure” or equivalent language.
- No strong claim without replication, comparator alignment, platform/probe audit, and falsifier checks.

Preferred language:

- “Survives first falsification.”
- “Blocked by missing comparator/probe/confounder evidence.”
- “Review-ready computational evidence.”
- “Invest in data only.”
- “Do not invest; claim killed as currently formulated.”
- “Not discovery yet.”

---

## Current Biomedical Focus

The current publication-readiness track focuses mainly on pediatric neuroblastoma hypothesis stress-testing.

Primary evidence route:

- Antigen presentation / APM axis.
- B2M / TAP / HLA-related signal review.
- NK and immune-effector context.
- MYCN-aware interpretation.
- Replication requirement through external datasets such as GSE49710 or TARGET-NBL before promotion.

Current publication-data fuel rule:

- APM / B2M-TAP-HLA may remain `INVEST_IN_DATA_ONLY`.
- CK2 and HDAC/DNMT are not promoted without perturbation/protein/chromatin/IFN-context evidence.
- NECTIN2/TIGIT is not promoted from bulk-testability alone.
- γδ/NKG2D is not promoted without true gamma-delta evidence such as TRGC/TRDV/TCR/single-cell support.
- ODC1/polyamine and CD276/B7-H3 remain watchlist/subgroup routes unless stronger independent evidence appears.

---

## Main Workflow

1. Researcher enters a biomedical hypothesis.
2. Engine parses structured intent and biological route.
3. Available evidence and route-specific constraints are checked.
4. Uploaded files may provide additional routing context.
5. The engine applies claim guards, falsification gates, and preprint-readiness logic.
6. A report is generated with:
   - Final verdict.
   - Decision route.
   - Evidence state.
   - What was tested.
   - What was not proven.
   - Missing evidence.
   - Next data-only action, if justified.

---

## Uploaded File Handling

Large uploaded files are treated as **routing context**, not automatic proof.

The current reader avoids loading full large files into memory. Instead, it uses streaming/chunked reading and extracts only relevant text slices, including:

- File head sample.
- File tail sample.
- Route-relevant lines.
- Dataset/accession markers.
- Gene/pathway/platform terms relevant to the active research route.
- Partition summaries.

This is intended to support large files, including very large text-like inputs, while reducing memory pressure.

Important boundary:

> A user-uploaded file can support routing and review context, but it does not certify provenance, biological truth, or statistical validity by itself.

---

## UI Changes in Current Release

The latest release includes:

- Visible upload button.
- Removed “More controls” path.
- Search/progress indicator restored.
- Hypothesis input clears after successful report completion.
- Report history panel with date-indexed entries.
- Large-file reading through smart streaming/chunking.

---

## Repository Structure

Typical project structure:

```text
app/
  src/main/java/com/immunesignal/app/
    ResearchAutopilotActivity.kt
    ResearchReportHistoryRendererV30694.kt
    UserUploadedFileSmartReaderV30691.kt
    PublicationPreprintReadinessV30680.kt
    PublicationDataFuelPackV30690.kt
    ...
  src/main/res/layout/
    activity_research_autopilot.xml
scripts/
  run_static_checks_fast.sh
  static_checks/
    audit_research_engine_v30692_ui_upload_history_final.py
    audit_research_engine_v30693_progress_audit_compat.py
    audit_research_engine_v30694_activity_size_extraction.py
    ...
docs/
  PREPRINT_DATA_FUEL_v3.0.6.9.md
  ...
```

---

## Local Static Checks

Run the fast static checks:

```bash
bash scripts/run_static_checks_fast.sh
```

Important checks include:

- Kotlin delimiter audit.
- JSON validation.
- XML parse/layout checks.
- UI/upload/history audit.
- Progress audit compatibility.
- Activity-size reduction audit.
- Publication data fuel audit.
- Preprint readiness audit.

---

## Android Build

Typical debug build command:

```bash
./gradlew :app:assembleDebug
```

Typical Kotlin compile check:

```bash
./gradlew :app:compileDebugKotlin
```

If Gradle cannot download dependencies, verify network/DNS access to Gradle distribution services or use a cached Gradle wrapper environment.

---

## CI Notes

This repository relies heavily on static checks to prevent regression in:

- Scientific claim boundaries.
- UI behavior.
- Upload safety.
- Version identity.
- Report routes.
- Evidence promotion rules.
- Activity size / modularization.

Recent CI compatibility fixes:

- ProgressBar layout remains determinate for legacy audit compatibility.
- Runtime can still switch progress behavior when needed.
- `ResearchAutopilotActivity` was reduced below the legacy size threshold by extracting history rendering.

---

## Preprint-Readiness Policy

A route may be promoted only when the evidence state supports it.

Current default policy:

- `DO_NOT_INVEST_CLAIM_KILLED` → no experimental promotion.
- `WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB` → no experimental promotion.
- `WATCHLIST_METHOD_COUNTERSIGNAL_NO_INVEST` → no experimental promotion.
- `INVEST_IN_DATA_ONLY` → data work only; no wet-lab claim.
- Stronger promotion requires independent replication, comparator alignment, platform/probe validation, and falsifier survival.

---

## Example Verdict Language

Acceptable verdict language:

```text
FINAL INVESTMENT DECISION: INVEST_IN_DATA_ONLY
```

```text
FINAL INVESTMENT DECISION: DO_NOT_INVEST_CLAIM_KILLED
```

```text
FINAL INVESTMENT DECISION: WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB
```

```text
ROUTE: MESENCHYMAL_STROMAL_COUNTER_SIGNAL_REINTERPRET
VERDICT: WATCHLIST_METHOD_COUNTERSIGNAL_NO_INVEST
```

---

## What This Project Is Not

This project is not:

- A clinical diagnostic product.
- A medical app for patients.
- A treatment recommendation engine.
- A substitute for laboratory validation.
- A substitute for expert biomedical review.
- A certified scientific study.
- A claim that AI has discovered a cure or proven a mechanism.

---

## Intended Users

Intended users include:

- Biomedical researchers.
- Immunology and oncology research teams.
- Computational biology reviewers.
- Professors and lab teams evaluating hypothesis quality.
- Preprint authors who need a stricter evidence-readiness gate before publishing claims.

---

## License

Add your chosen license here before public release.

Recommended options depend on your strategy:

- `Apache-2.0` for permissive open-source adoption.
- `MIT` for simple permissive release.
- Custom/private license if this repository is not ready for open public reuse.

---

## Maintainer Note

This repository is under active research development. The most important principle is not to make the software look more certain than the evidence allows.

Core rule:

> Evidence gates the claim. The engine may route, stress-test, and falsify; it must not overclaim biological proof.
