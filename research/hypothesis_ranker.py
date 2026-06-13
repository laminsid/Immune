#!/usr/bin/env python3
"""Hypothesis ranking v0.9.1.

Matches HypothesisRankingEngine.kt exactly. See docs/CANONICAL_SCORING_FORMULA_v0.9.1.md.

Changes from v0.9.0:
- Adds novelty term (was missing, caused divergence with Kotlin).
- Negative-control hard gate aligned to Kotlin status string.
"""
import csv
import json
import sys
from pathlib import Path


def overall_score(evidence, causality, novelty, repeatability):
    """Aligned to Kotlin formula:
    0.32*evidence + 0.34*causality + 0.18*novelty + 0.16*min(60, rep*12)
    """
    rep_term = min(60, repeatability * 12)
    raw = (
        evidence * 0.32
        + causality * 0.34
        + novelty * 0.18
        + rep_term * 0.16
    )
    return max(0, min(100, int(raw)))


def status_for(score, repeatability, neg_status):
    """Status thresholds match Kotlin HypothesisRankingEngine.kt."""
    blocked_neg = {"control_required_before_strong"}
    if score >= 72 and repeatability >= 3 and neg_status not in blocked_neg:
        return "STRONG_SIGNAL"
    if score >= 55:
        return "WATCH"
    if score >= 35:
        return "WEAK"
    return "NOISE_OR_UNKNOWN"


def rank(path):
    rows = []
    for row in csv.DictReader(Path(path).open(encoding="utf-8")):
        ev = int(float(row.get("evidence_quality_score", 0) or 0))
        ca = int(float(row.get("causality_score", 0) or 0))
        # novelty is optional in older CSVs; default to 0 keeps backward compat
        nv = int(float(row.get("novelty_score", 0) or 0))
        rep = int(float(row.get("repeatability", 0) or 0))
        neg = row.get("negative_control", "unknown")
        total = overall_score(ev, ca, nv, rep)
        rows.append({
            **row,
            "overall_score": total,
            "status": status_for(total, rep, neg),
            "formula_version": "v0.9.1",
        })
    print(json.dumps(
        sorted(rows, key=lambda r: r["overall_score"], reverse=True),
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "hypothesis_ranker.py hypotheses.csv"}, indent=2))
    else:
        rank(sys.argv[1])
