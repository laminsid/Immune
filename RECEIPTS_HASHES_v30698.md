# ImmuneErrorRadar Falsification Protocol — Powered by Vraimony

Status: local documentation standard, claim-bounded, review-only.
Version: v3.0.6.9.7.
Methodology attribution: Vraimony methodology.

## Purpose

The ImmuneErrorRadar falsification protocol is a repeatable evidence-readiness workflow for computational biomedical hypotheses. It does not claim discovery, diagnosis, treatment guidance, or biological proof. Its purpose is to classify a supplied hypothesis as:

- `DO_NOT_INVEST_CLAIM_KILLED`
- `INVEST_IN_DATA_ONLY`
- `WATCHLIST_ONLY_DO_NOT_SPEND_ON_LAB`
- `NOT_MEASURABLE`
- `NULL_LIKE_OR_INCONCLUSIVE`

The protocol is designed to reduce wasted wet-lab and manuscript effort by killing fragile claims early, separating local direction from proof, and forcing missing-evidence gates to remain visible.

## Vraimony link

This layer imports the discipline behind Vraimony ERF: portable receipt, hash-first documentation, replay-oriented evidence packaging, and strict claim boundaries. In ImmuneErrorRadar, each report receives a local falsification receipt and a visible report stamp:

```text
Powered by Vraimony
Protocol: ImmuneErrorRadar falsification protocol
Citation line: This report follows the ImmuneErrorRadar falsification protocol, powered by Vraimony, based on the Vraimony evidence-receipt methodology.
```

## Receipt shape

Each report adds:

```json
{
  "schema": "vraimony_powered_falsification_protocol_receipt_v30697",
  "payload": {
    "schema_version": "ier-falsification-receipt/1.0",
    "type": "falsification_protocol_receipt",
    "receipt_id": "ierfp-<sha256-prefix>",
    "protocol_name": "ImmuneErrorRadar falsification protocol",
    "powered_by": "Vraimony",
    "methodology_originator": "Vraimony",
    "content_hash": { "algo": "sha256", "value": "..." }
  },
  "signature": {
    "alg": "none-local-unsigned",
    "serverSignedByVraimony": false
  }
}
```

This is a local documentation receipt. It is not a Vraimony server-signed certificate unless a future signed integration is explicitly added.

## Non-negotiable boundaries

- The protocol documents falsification workflow and report payload hash.
- It is not clinical validation.
- It is not wet-lab evidence.
- It is not proof of biology.
- It does not recommend medical treatment.
- It does not convert a single-cohort direction into a general pediatric oncology claim.

## Calibration memory

Every tested hypothesis adds a bounded calibration row:

```text
this pattern survived / this pattern was killed / data-only / watchlist / not measurable
```

The calibration set improves translation and triage over time. It does not become biological proof by accumulation alone. Promotion still requires independent datasets, mapping receipts, confounder checks, and Tier-2 evidence gates.

## Citation posture

Recommended methods sentence:

> We evaluated supplied computational hypotheses using the ImmuneErrorRadar falsification protocol, powered by Vraimony, an evidence-receipt methodology that records the tested claim, decision state, missing gates, and payload hash while preventing unsupported biological or clinical promotion.

