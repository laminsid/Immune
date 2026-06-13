# Tier-0 Boundaries v3.0.6.9.8

**Powered by Vraimony**  
**Protocol:** ImmuneErrorRadar falsification protocol  
**Purpose:** protect the preprint and reports from overclaiming.

## What Tier-0 means

Tier-0 means the engine can produce a local, replayable, review-only falsification/triage result. It can say that a supplied claim is killed as written, watchlist-only, not measurable, null-like, or data-only. Tier-0 does **not** allow claims of biological proof.

## Tier-0 allowed outputs

- `DO_NOT_INVEST_CLAIM_KILLED`
- `WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB`
- `WATCHLIST_METHOD_COUNTERSIGNAL_NO_INVEST`
- `NOT_MEASURABLE_PROBE_AND_CONTEXT_BLOCKED`
- `NULL_LIKE_OR_INCONCLUSIVE`
- `INVEST_IN_DATA_ONLY`

## Tier-0 may support

- Directional screening.
- Claim-as-written falsification.
- MYCN-aware attenuation checks.
- Review-only Cox/event-rate summaries.
- Probe readiness warnings.
- Replay/hash receipt documentation.
- Calibration ledger entries such as `KILLED`, `WATCHLIST`, `DATA_ONLY_SURVIVED_FIRST_TRIAGE`, or `NOT_MEASURABLE`.

## Tier-0 must not claim

- Diagnosis, treatment advice, clinical actionability, or dosing.
- Wet-lab candidacy.
- Mechanistic proof from static bulk expression.
- Ligand-receptor checkpoint function from bulk expression alone.
- Gamma-delta T-cell identity from surrogate bulk markers alone.
- Cross-pediatric-tumor generalization from neuroblastoma-only evidence.
- Pan-cancer or pan-pediatric oncology claim.
- Vraimony server signature if `signedByVraimony=false`.

## APM-specific boundary

APM/B2M–TAP–HLA is retained only as `INVEST_IN_DATA_ONLY`. This means data work may continue: full GPL5175 mapping, vector binding, source-certified tiles, GSE49710/TARGET-NBL replication, MYCN interaction/stability checks, and cross-tumor stress-test templates. It does not permit wet-lab promotion or evidence language.

## 3-cohort / cross-tumor boundary

Current pediatric oncology evidence is neuroblastoma-scoped unless independent datasets pass the same protocol. The intended expansion targets are:

1. Neuroblastoma primary/replication lane: GSE85047 → GSE49710 / TARGET-NBL.
2. Medulloblastoma.
3. Wilms tumor / nephroblastoma.
4. Ewing sarcoma.

Before any cross-tumor claim, each tumor family must receive a separate receipt and one of the bounded outcomes: `KILLED`, `NULL-LIKE`, `SURVIVING_REVIEW_ONLY`, `DATA_ONLY`, or `NOT_MEASURABLE`.
