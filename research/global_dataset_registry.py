#!/usr/bin/env python3
"""v1.3 Global dataset registry helper.

Reads a lightweight CSV of public dataset candidates and scores whether they are
useful for trigger -> immune response -> outcome research. This is intentionally
simple and offline; Android uses PubMed metadata, while this script is for
research-side curation.
"""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

REQUIRED = ["dataset_id", "condition", "data_type", "species", "sample_count", "outcome_labels"]


def score(row: dict) -> int:
    s = 20
    if row.get("species", "").lower() == "human": s += 25
    if any(x in row.get("data_type", "").lower() for x in ["rna", "single", "transcript", "cytokine"]): s += 20
    try:
        n = int(float(row.get("sample_count", "0") or 0))
    except ValueError:
        n = 0
    if n >= 100: s += 15
    elif n >= 30: s += 8
    if row.get("outcome_labels", "").lower() in {"yes", "true", "1"}: s += 20
    return max(0, min(100, s))


def load(path: str) -> list[dict]:
    rows = list(csv.DictReader(Path(path).open(newline='', encoding='utf-8')))
    out = []
    for r in rows:
        missing = [k for k in REQUIRED if not r.get(k)]
        r["quality_score"] = score(r)
        r["missing_required"] = missing
        r["status"] = "READY_CANDIDATE" if r["quality_score"] >= 70 and not missing else "NEEDS_REVIEW"
        out.append(r)
    return sorted(out, key=lambda x: x["quality_score"], reverse=True)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "research/examples/global_dataset_candidates.csv"
    print(json.dumps(load(path), indent=2, ensure_ascii=False))
