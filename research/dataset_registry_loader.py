#!/usr/bin/env python3
"""Load and sanity-check a dataset registry CSV for Immune Error Radar.

Expected columns:
dataset_id,condition,source,url,sample_count,data_type,available_markers,license_access,quality_score,notes
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REQUIRED = [
    "dataset_id", "condition", "source", "url", "sample_count", "data_type",
    "available_markers", "license_access", "quality_score", "notes",
]


def load_registry(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in REQUIRED if c not in (rows[0].keys() if rows else [])]
    if missing:
        raise SystemExit(f"Missing columns: {missing}")
    return rows


def score_summary(rows: list[dict[str, str]]) -> None:
    print(f"datasets={len(rows)}")
    by_condition: dict[str, int] = {}
    for r in rows:
        by_condition[r["condition"]] = by_condition.get(r["condition"], 0) + 1
    for condition, count in sorted(by_condition.items()):
        print(f"{condition}: {count}")
    weak = [r for r in rows if int(float(r.get("quality_score") or 0)) < 60]
    if weak:
        print("\nWeak/needs-review datasets:")
        for r in weak:
            print(f"- {r['dataset_id']} ({r['condition']}): quality={r['quality_score']}")


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/DATASET_REGISTRY_v0.3.csv")
    rows = load_registry(path)
    score_summary(rows)
