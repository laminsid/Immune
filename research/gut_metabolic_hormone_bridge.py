#!/usr/bin/env python3
"""Gut / nutrition / muscle / testosterone bridge prototype.

Reads a CSV with optional columns:
case_id,reflux_heartburn,bloating_dyspepsia,diet_diversity,protein_g,body_weight_kg,
muscle_low,strength_training,testosterone_ng_dl,type2_axis,tnf_il6_axis,recovery_slow
"""
import csv
import sys
from pathlib import Path


def f(row, key, default=0.0):
    try:
        raw = str(row.get(key, "")).strip()
        return float(raw) if raw else default
    except Exception:
        return default


def b(row, key):
    return str(row.get(key, "")).strip().lower() in {"1", "true", "yes", "y"}


def classify(row):
    reflux = f(row, "reflux_heartburn")
    dys = f(row, "bloating_dyspepsia")
    diet = f(row, "diet_diversity", 5)
    protein = f(row, "protein_g")
    weight = f(row, "body_weight_kg")
    ppkg = protein / weight if protein > 0 and weight > 0 else None
    testosterone = f(row, "testosterone_ng_dl")
    type2 = f(row, "type2_axis")
    inflam = f(row, "tnf_il6_axis")
    recovery = f(row, "recovery_slow")

    labels = []
    if (reflux >= 6 or dys >= 6) and type2 >= 40:
        labels.append("gastric_acid_allergy_bridge_candidate")
    if diet <= 3 and type2 >= 35:
        labels.append("gut_barrier_microbiome_allergy_candidate")
    if ppkg is not None and ppkg < 0.8 and (recovery >= 6 or b(row, "muscle_low")):
        labels.append("protein_muscle_recovery_candidate")
    if b(row, "muscle_low") and inflam >= 35:
        labels.append("muscle_inflammation_reserve_candidate")
    if testosterone and (testosterone < 350 or testosterone > 900):
        labels.append("testosterone_immune_modulation_candidate")
    return labels or ["mixed_or_undermeasured"]


def main(path):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            print(row.get("case_id", "case"), ",".join(classify(row)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "research/examples/sample_cases.csv")
