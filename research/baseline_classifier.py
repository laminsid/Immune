#!/usr/bin/env python3
"""Baseline classifier for immune-axis matrix.

No external ML dependency: this creates an interpretable first-pass rule baseline.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path


def n(row: dict[str, str], key: str) -> int:
    try:
        return int(float(row.get(key) or 0))
    except ValueError:
        return 0


def classify(row: dict[str, str]) -> str:
    type2 = n(row, "type2_axis")
    tnf = n(row, "tnf_il6_axis")
    hyper = n(row, "hyperinflammatory_axis")
    brake = n(row, "regulatory_brake_weakness")
    stress_musc = max(n(row, "psychoneuroimmune_axis"), n(row, "psychomusculoskeletal_axis"))

    if max(type2, tnf, hyper, brake, stress_musc) < 35:
        return "low_signal_or_incomplete"
    if hyper >= 75 or (hyper >= 60 and brake >= 65):
        return "hyperinflammatory_dominant"
    if tnf >= 65:
        return "autoimmune_inflammatory_dominant"
    if type2 >= 65 and tnf < 60:
        return "type2_allergy_dominant"
    if stress_musc >= 70 and max(type2, tnf, hyper) < 65:
        return "stress_musculoskeletal_dominant"
    scores = {
        "type2_allergy_dominant": type2,
        "autoimmune_inflammatory_dominant": tnf,
        "hyperinflammatory_dominant": hyper,
        "stress_musculoskeletal_dominant": stress_musc,
    }
    return max(scores, key=scores.get)


def run(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print("case_id,known_condition,predicted_pattern,match_hint")
    for r in rows:
        pred = classify(r)
        known = r.get("condition", "unknown")
        match = "REVIEW"
        if known == "allergy" and pred == "type2_allergy_dominant": match = "HIT"
        elif known == "ra" and pred == "autoimmune_inflammatory_dominant": match = "HIT"
        elif known == "hyperinflammation" and pred == "hyperinflammatory_dominant": match = "HIT"
        elif known == "back_stress" and pred == "stress_musculoskeletal_dominant": match = "HIT"
        print(f"{r.get('case_id')},{known},{pred},{match}")


if __name__ == "__main__":
    run(Path(sys.argv[1] if len(sys.argv) > 1 else "research/examples/sample_matrix.csv"))
