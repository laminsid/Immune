# Replay Description v3.0.6.9.8

**Powered by Vraimony**  
**Protocol:** ImmuneErrorRadar falsification protocol  
**Scope:** replay description for report reproduction and auditability.

## Minimum replay package

A reproducible replay package should include:

1. Source code release ZIP or Git commit hash.
2. README version and preprint version.
3. Report PDF or report text.
4. Receipt/hash index.
5. Targeted GPL5175 review manifest.
6. Input hypothesis text.
7. Dataset/outcome context.
8. Engine version and schema version.

## Current source release

- Release ZIP: `ImmuneErrorRadar-v3.0.6.9.8-history-titles-privacy-final.zip`
- SHA-256: `7b5ea2717505b48b46e28202c7b4416fbbbaa6fcd09c562efc95f66410bec8c2`
- GitHub repository: `https://github.com/laminsid/Immune`

## Replay steps

1. Clone the repository or unpack the release ZIP.
2. Verify the source release SHA-256 against `assets/receipts/receipts_hashes_index_v30698.json`.
3. Confirm the targeted GPL5175 manifest exists at the expected path or use the copy in `assets/manifests/`.
4. Run static checks:

```bash
bash scripts/run_static_checks_fast.sh
```

5. Build or run the Android application if the Gradle environment is available:

```bash
./gradlew :app:assembleDebug
```

6. Enter the exact hypothesis text into the Research Autopilot input.
7. Run the report.
8. Compare the report route, final decision, protocol receipt id, content hash, and replay SHA-256 with the receipt index.

## Expected route examples

- CK2 mechanism claim → `CK2_CSNK2A1_IFN_APM_PFS_MYCN_GSE85047` → `DO_NOT_INVEST_CLAIM_KILLED`.
- HDAC/DNMT epigenetic mechanism claim → `HDAC2_DNMT1_APM_REPRESSION_PFS_MYCN_GSE85047` → `DO_NOT_INVEST_CLAIM_KILLED`.
- NECTIN2/TIGIT bulk checkpoint claim → `NECTIN2_TIGIT_CHECKPOINT_PFS_MYCN_GSE85047` → `DO_NOT_INVEST_CLAIM_KILLED` for current bulk data.
- γδ/NKG2D surrogate claim → `GAMMA_DELTA_NKG2D_MICA_SURVEILLANCE_PFS_MYCN_GSE85047` → killed as true gamma-delta evidence from bulk surrogate.
- APM/B2M–TAP–HLA → `APM_COMPOSITE_PFS_MYCN_GSE85047` → `INVEST_IN_DATA_ONLY`.

## What counts as a successful replay

A replay is acceptable when the following match or are explainably versioned:

- Same hypothesis parsing route.
- Same final bounded decision.
- Same claim guard posture.
- Same Tier-0 boundary.
- Same or newly versioned receipt/hash.
- No promotion from killed/watchlist/not-measurable to wet-lab without new independent evidence.

## What does not count as proof

A replay does not certify biology, clinical actionability, source truth, or wet-lab validity. It confirms the report-generation state and bounded falsification workflow.
