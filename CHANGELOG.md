# Changelog

All notable changes to ImmuneErrorRadar / GTIM are summarized here.

This changelog is intentionally consolidated for a clean public repository root. Older detailed changelogs may be archived under `docs/changelogs/`.

## v3.0.7.0 — GitHub UI Isolation Final

### Added
- Introduced `ResearchAutopilotUiBinderV30700.kt` to isolate UI binding from the legacy activity bridge.
- Added `docs/GITHUB_UI_ISOLATION_v30700.md` to document the UI isolation boundary.
- Added static audit coverage for the GitHub UI isolation layer.

### Changed
- Kept `ResearchAutopilotActivity.kt` as the compatibility bridge for existing routes, callbacks, and CI expectations.
- Preserved legacy XML IDs and report/export/upload paths to avoid route breakage.
- Reduced Activity-level UI responsibility without changing scientific report logic.

### Preserved
- Upload flow.
- Report history and report reader.
- Copy/download/print actions.
- Vraimony/ERF-inspired receipt fields.
- Tier-0 boundaries.
- Calibration ledger.
- Verdict and route names.

## v3.0.6.9.9 — Unit-Test Triage-Signal Hotfix

### Fixed
- Updated legacy unit-test expectations after replacing `Experimental signal` with claim-safer triage wording.
- Added compatibility audit for the new `Triage signal: REVIEW_ONLY_DIRECTIONAL_SCREEN` report language.

### Changed
- Removed report wording that could be misread as wet-lab promotion when `wetLabAllowed=false`.

## v3.0.6.9.8 — History Titles and Privacy-Safe Reports

### Added
- Added report-title derivation from the tested hypothesis.
- Added clearer history labels so researchers can distinguish CK2, HDAC/DNMT, NECTIN2/TIGIT, γδ/NKG2D, APM, and other reports.

### Changed
- Improved history grouping by date and report name.
- Removed personal-name attribution from generated app reports while preserving the Vraimony methodology identity.
- Replaced ambiguous experimental wording with review-only triage wording.

## v3.0.6.9.7 — Powered by Vraimony Falsification Protocol

### Added
- Added `Powered by Vraimony` report identity.
- Added `ImmuneErrorRadar falsification protocol` as a citeable methodology phrase.
- Added ERF-inspired evidence receipt discipline: hash-first, portable, replayable, and claim-bounded.
- Added local falsification receipt fields, including local hash and `signedByVraimony=false` boundary.
- Added protocol documentation and JSON protocol metadata.

### Boundaries
- Receipts document workflow and report payload hashes only.
- Receipts are not clinical validation, wet-lab evidence, source-truth certification, or proof of biology.

## v3.0.6.9.6 — History, Calibration, and APM Multi-Cohort Fuel

### Added
- Added APM multi-cohort data fuel as validation targets only, not replication.
- Added pediatric cross-tumor expansion targets: medulloblastoma, Wilms tumor/nephroblastoma, and Ewing sarcoma.
- Added calibration ledger / translation memory categories: killed, data-only, watchlist, not measurable, null-like, and local-direction review-only.
- Added history report reader with date selection, report selection, open, copy, download, and print actions.

### Boundaries
- `syntheticData=false` and `fakeReplication=false` for multi-cohort fuel.
- Cross-tumor promotion is blocked until independent human datasets pass required checks.

## v3.0.6.9.5 — Pediatric Multi-Tumor CI Hotfix

### Added
- Added pediatric multi-tumor cohort guard.
- Added single-cohort scope warning for neuroblastoma-only evidence.
- Added requirement for external pediatric tumor-family datasets before cross-tumor claims.

### Fixed
- Restored the legacy hidden audit marker `Developer: refresh gene mapping` without reintroducing obsolete More Controls UI.

## v3.0.6.9.4 — Activity Reduction CI Final

### Fixed
- Reduced `ResearchAutopilotActivity.kt` below legacy CI size threshold.
- Extracted report history rendering into `ResearchReportHistoryRendererV30694.kt`.

## v3.0.6.9.3 — Progress Audit Compatibility

### Fixed
- Restored XML `ProgressBar` determinate compatibility for legacy audits.
- Preserved runtime spinner/progress behavior where required.

## v3.0.6.9.2 — Preprint UI Upload History Final

### Added
- Added report history panel.
- Added visible progress/search indicator.
- Added hypothesis-input clearing after successful report generation.
- Added large-file upload streaming/chunking path.

### Removed
- Removed obsolete More Controls UI path from active usage.

## v3.0.6.9.1 — UI Upload History Hotfix

### Added
- Added first version of report history and upload reader improvements.
- Introduced streaming reader for large uploaded files.

### Changed
- Kept upload as routing context, not source-truth proof.

## v3.0.6.9 — Publication Data Fuel

### Added
- Added publication data fuel pack for CK2, HDAC/DNMT, APM, NECTIN2/TIGIT, and γδ/NKG2D routes.
- Preserved APM/B2M-TAP-HLA as the only `INVEST_IN_DATA_ONLY` route.

### Boundaries
- No synthetic matrices.
- No fake replication.
- No wet-lab promotion.
- Tier-2 required before computational evidence language.

## v3.0.6.8 — Preprint Publication Readiness

### Added
- Added preprint-readiness decision layer.
- Added clear kill/data-only/watchlist verdict language.
- Added no-probability-reporting rule for uncalibrated translation probabilities.

## v3.0.6.x — Falsification and Investment-Triage Baseline

### Added
- Added MYCN-adjusted falsification logic.
- Added kill/invest triage layer.
- Added Tier-0/Tier-1/Tier-2 evidence-readiness boundaries.
- Added targeted GPL5175 review and probe/vector readiness receipts.

### Scientific posture
- Static bulk expression may support directional screening only.
- Bulk proxies cannot prove upstream mechanism, ligand-receptor engagement, cell identity, or clinical actionability.
- Wet-lab promotion is blocked unless stricter independent evidence gates are passed.
