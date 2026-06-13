# ImmuneErrorRadar Receipts / Hashes Index v3.0.6.9.8

**Powered by Vraimony**  
**Protocol:** ImmuneErrorRadar falsification protocol  
**Receipt discipline:** ERF-inspired evidence receipt discipline — hash-first, portable, replayable, claim-bounded.

## Boundary

These receipts document local report payloads, source artifacts, and replay metadata. They are **not** medical advice, not clinical validation, not wet-lab evidence, not source-truth certification, and not proof of biology. `signedByVraimony=false` means the receipt is local/unsigned and has not been sealed by a Vraimony server-side signature flow.

## Source artifact SHA-256 hashes

| File | Role | SHA-256 | Size bytes |
|---|---|---:|---:|
| `ImmuneErrorRadar-v3.0.6.9.8-history-titles-privacy-final.zip` | `source_code_release` | `7b5ea2717505b48b46e28202c7b4416fbbbaa6fcd09c562efc95f66410bec8c2` | 4362329 |
| `README_ImmuneErrorRadar_v30698.md` | `preprint_or_readme` | `648a1079fa154f13484a3de187dcc446db609ccbafa0c8e1ec836b0da59a8142` | 13865 |
| `ImmuneErrorRadar_Preprint_v5_Vraimony_ERF_3Cohort.docx` | `preprint_or_readme` | `2416c0fb470718bcff509f8ddb1058a53c3da59f96438bb96d498cd4e0487655` | 48313 |
| `ImmuneErrorRadar_Preprint_v5_Vraimony_ERF_3Cohort.pdf` | `preprint_or_readme` | `7d1eb693617338b84cc9ce62489c69659e1721c892618366b9d834ae00aea8e5` | 147091 |
| `immune_discovery_2026-06-13_14-25.pdf` | `generated_report_pdf` | `0f146f26f933fa449be76e8c86b8e203465ec0599dbdbf8990ea27dcd4885b1c` | 219480 |
| `immune_discovery_2026-06-13_14-27.pdf` | `generated_report_pdf` | `e2d5d14ca024ea7e6712880599fd882421c82a5297edc115536b6aabade729d9` | 217919 |
| `immune_discovery_2026-06-13_14-34.pdf` | `generated_report_pdf` | `e4c394c838c6952823594324dfcc7d5e80c428f916a284c45c4c3f4354ff9b5e` | 219487 |
| `immune_discovery_2026-06-13_14-37.pdf` | `generated_report_pdf` | `3c6a0b17ef4a12a256003e46bac88422dd91ab49ebb55679a6e0b73914ae865e` | 219617 |

## Report receipt index

| Report title | Route | Final decision | Calibration outcome | Protocol receipt id | Run replay SHA-256 | Vraimony-signed |
|---|---|---|---|---|---|---|
| CK2/CSNK2A1 to APM mechanism claim | `CK2_CSNK2A1_IFN_APM_PFS_MYCN_GSE85047` | `DO_NOT_INVEST_CLAIM_KILLED` | `KILLED` | `ierfp-fb5f8d434c24e4e625c36ccd` | `10db8cba673903013b41322b887fd71322856ec207e4f1a7e7d8d360e180c006` | false |
| NECTIN2/TIGIT bulk checkpoint testability claim | `NECTIN2_TIGIT_CHECKPOINT_PFS_MYCN_GSE85047` | `DO_NOT_INVEST_CLAIM_KILLED` | `KILLED` | `ierfp-c823aa840ffb6987580217e2` | `835e4db3f313e90e23f56594e808185d3fef2ba457647423aaaf415be61f001f` | false |
| HDAC/DNMT to APM epigenetic repression claim | `HDAC2_DNMT1_APM_REPRESSION_PFS_MYCN_GSE85047` | `DO_NOT_INVEST_CLAIM_KILLED` | `KILLED` | `ierfp-84aa42b01983fe44cd0ac899` | `4c7a5c79e5a0556c1b9ba36554ced900fea294080580b76197be2336fc44a066` | false |
| γδ/NKG2D surrogate claim | `GAMMA_DELTA_NKG2D_MICA_SURVEILLANCE_PFS_MYCN_GSE85047` | `DO_NOT_INVEST_CLAIM_KILLED` | `KILLED` | `ierfp-4776ab5f9ab87c66d0ee603b` | `c198165194c3be812b1f5f2d5d6c57dcb872f9a0e1eff1da7d6b9ad268494c53` | false |
| APM/B2M–TAP–HLA data axis | `APM_COMPOSITE_PFS_MYCN_GSE85047` | `INVEST_IN_DATA_ONLY` | `DATA_ONLY_SURVIVED_FIRST_TRIAGE` | `not_available_in_current_uploaded_report_batch` | `694025f7f14bf5da5ad2fbec5aaa7a283152de5b17fa696222d50e39826a5a2c` | false |
| ODC1/polyamine primary-driver claim | `ODC1_POLYAMINE_AXIS_REFERENCE` | `WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB` | `WATCHLIST_OR_WEAK_SECONDARY` | `not_available_in_current_uploaded_report_batch` | `3030ed6e2c34890552b1660dcfec0bcd7b2e6852de6d26400aea50018dcab01d` | false |

## Practical use

1. Keep this file with the preprint and generated reports.
2. When a report is regenerated, compare the run replay SHA-256 and source artifact SHA-256 values.
3. A mismatch does not automatically mean fraud; it means the report must be treated as a different replay state and must receive a new receipt.
4. Do not cite these receipts as biological proof. Cite them as workflow/replay documentation.
