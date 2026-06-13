#!/usr/bin/env python3
"""Prototype allergy-aging-autonomic bridge.

This script is intentionally heuristic. It tests competing research hypotheses:
1) allergy reactivity may reflect preserved responsiveness when aging-load is low;
2) chronic allergy + inflammatory burden may reflect inflammaging load;
3) stress/allergy/BP timing may reveal autonomic-mast-cell vascular instability.
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


def b(row: dict[str, str], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"1", "true", "yes", "y"}


def score(row: dict[str, str]) -> dict[str, int | str]:
    allergy = clamp((f(row, "IgE_IU_mL") / 250) * 40 + (f(row, "Eosinophils_cells_uL") / 600) * 35 + f(row, "allergy_intensity_0_10") * 5)
    inflammaging = clamp((f(row, "CRP_mg_L") / 10) * 20 + (f(row, "IL6_pg_mL") / 20) * 20 + (f(row, "TNF_alpha_pg_mL") / 20) * 15 + max(0, 5 - f(row, "sleep_quality_0_10")) * 6)
    immunosenescence = clamp(f(row, "age") * 0.35 + f(row, "recovery_slow_0_10") * 6 + (18 if b(row, "frequent_infections") else 0))
    resilience = clamp(50 + f(row, "exercise_recovery_0_10") * 4 + (f(row, "sleep_quality_0_10") - 5) * 5 - f(row, "recovery_slow_0_10") * 4)
    sympathetic_up = clamp(f(row, "stress_0_10") * 7 + max(0, f(row, "resting_pulse_bpm") - 80) * 1.2 + max(0, f(row, "systolic_bp") - 120) * 0.8)
    histamine_down = clamp(allergy * 0.35 + (18 if b(row, "flushing") else 0) + (18 if b(row, "faintness_during_allergy") else 0) + max(0, 105 - f(row, "systolic_bp")) * 0.9)
    bp_instability = clamp((20 if b(row, "dizziness_standing") else 0) + (20 if b(row, "faintness_during_allergy") else 0) + max(0, 95 - f(row, "systolic_bp")) + max(0, f(row, "systolic_bp") - 150) * 0.5)
    aging_load = clamp((inflammaging + immunosenescence) / 2)

    if allergy >= 55 and aging_load < 35 and resilience >= 55:
        pattern = "preserved_responsiveness_candidate"
    elif allergy >= 55 and inflammaging >= 45:
        pattern = "chronic_irritation_inflammaging_candidate"
    elif allergy < 30 and immunosenescence >= 45:
        pattern = "weak_responsiveness_candidate"
    elif sympathetic_up >= 55 and histamine_down >= 40:
        pattern = "autonomic_mast_cell_bp_competition_candidate"
    else:
        pattern = "mixed_or_undermeasured"

    return {
        "allergy_reactivity": allergy,
        "inflammaging": inflammaging,
        "immunosenescence": immunosenescence,
        "resilience": resilience,
        "sympathetic_up": sympathetic_up,
        "histamine_down": histamine_down,
        "bp_instability": bp_instability,
        "pattern": pattern,
    }


def run(path: Path) -> None:
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    fields = ["case_id", "condition", "allergy_reactivity", "inflammaging", "immunosenescence", "resilience", "sympathetic_up", "histamine_down", "bp_instability", "pattern"]
    print(",".join(fields))
    for row in rows:
        out = score(row)
        print(",".join(str(row.get(k, out.get(k, ""))) for k in fields))


if __name__ == "__main__":
    run(Path(sys.argv[1] if len(sys.argv) > 1 else "research/examples/sample_cases.csv"))
