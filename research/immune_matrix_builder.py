#!/usr/bin/env python3
"""Build a simple immune-axis matrix from normalized case rows.

This is a baseline heuristic, not a validated model.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path


def clamp(x: float) -> int:
    return int(max(0, min(100, round(x))))


def f(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except ValueError:
        return 0.0


def axes(row: dict[str, str]) -> dict[str, int]:
    type2 = clamp((f(row, "IgE_IU_mL") / 250) * 50 + (f(row, "Eosinophils_cells_uL") / 600) * 45)
    tnf_il6 = clamp((f(row, "IL6_pg_mL") / 40) * 35 + (f(row, "TNF_alpha_pg_mL") / 35) * 35 + (f(row, "CRP_mg_L") / 25) * 20 + (f(row, "ESR_mm_h") / 60) * 10)
    hyper = clamp((f(row, "IL6_pg_mL") / 160) * 35 + (f(row, "TNF_alpha_pg_mL") / 100) * 30 + (f(row, "Ferritin_ng_mL") / 1000) * 35 + (f(row, "CRP_mg_L") / 100) * 10)
    brake = clamp(100 - min(100, f(row, "IL10_pg_mL") * 8))
    stress = clamp(f(row, "stress_0_10") * 10 + max(0, 5 - f(row, "sleep_quality_0_10")) * 8)
    musc = clamp(f(row, "mechanical_load_0_10") * 10)
    return {
        "type2_axis": type2,
        "tnf_il6_axis": tnf_il6,
        "hyperinflammatory_axis": hyper,
        "regulatory_brake_weakness": brake,
        "psychoneuroimmune_axis": stress,
        "psychomusculoskeletal_axis": musc,
    }


def build(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    headers = ["case_id", "condition", "type2_axis", "tnf_il6_axis", "hyperinflammatory_axis", "regulatory_brake_weakness", "psychoneuroimmune_axis", "psychomusculoskeletal_axis"]
    print(",".join(headers))
    for r in rows:
        a = axes(r)
        print(",".join([r.get("case_id", "case"), r.get("condition", "unknown")] + [str(a[h]) for h in headers[2:]]))


if __name__ == "__main__":
    build(Path(sys.argv[1] if len(sys.argv) > 1 else "research/examples/sample_cases.csv"))
