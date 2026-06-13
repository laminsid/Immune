#!/usr/bin/env python3
"""Find bridge candidates across immune-axis patterns.

Bridge = axes that are high across different labeled conditions or unusual co-activation pairs.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

AXES = ["type2_axis", "tnf_il6_axis", "hyperinflammatory_axis", "regulatory_brake_weakness", "psychoneuroimmune_axis", "psychomusculoskeletal_axis"]


def n(row: dict[str, str], key: str) -> int:
    try:
        return int(float(row.get(key) or 0))
    except ValueError:
        return 0


def run(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print("Bridge candidates")
    for r in rows:
        high = [a for a in AXES if n(r, a) >= 65]
        if len(high) >= 2:
            print(f"- {r.get('case_id')} ({r.get('condition')}): {' + '.join(high)}")
    print("\nCross-condition axis averages")
    groups: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        groups.setdefault(r.get("condition", "unknown"), []).append(r)
    for cond, items in groups.items():
        vals = []
        for axis in AXES:
            avg = sum(n(r, axis) for r in items) / max(1, len(items))
            vals.append(f"{axis}={avg:.1f}")
        print(f"{cond}: " + ", ".join(vals))


if __name__ == "__main__":
    run(Path(sys.argv[1] if len(sys.argv) > 1 else "research/examples/sample_matrix.csv"))
