#!/usr/bin/env python3
"""Evidence quality utilities for Immune Error Radar v0.9.

Classifies study evidence before the research engine learns from it.
This script is intentionally conservative: unknown metadata stays low-confidence.
"""
import csv
import json
import re
import sys
from pathlib import Path

DESIGN_WEIGHTS = {
    "systematic_review_meta_analysis": 82,
    "human_randomized_trial": 88,
    "human_cohort": 74,
    "human_case_control": 66,
    "human_case_report_or_series": 48,
    "animal_study": 38,
    "cell_in_vitro": 30,
    "mechanistic_review": 42,
    "unknown_design": 35,
}
SPECIES_PENALTY = {"human": 0, "mixed_human_animal": 8, "animal": 22, "cell_only": 28, "unknown": 15}


def classify_species(text: str) -> str:
    t = text.lower()
    has_human = any(x in t for x in ["human", "patient", "patients", "cohort", "clinical", "volunteer"])
    has_animal = any(x in t for x in ["mouse", "mice", "murine", "rat", "animal model", "zebrafish"])
    has_cell = any(x in t for x in ["in vitro", "cell line", "cultured", "organoid", "pbmc"])
    if has_human and has_animal:
        return "mixed_human_animal"
    if has_human:
        return "human"
    if has_animal:
        return "animal"
    if has_cell:
        return "cell_only"
    return "unknown"


def classify_design(text: str) -> str:
    t = text.lower()
    if "meta-analysis" in t or "systematic review" in t:
        return "systematic_review_meta_analysis"
    if "randomized" in t or "randomised" in t or "clinical trial" in t:
        return "human_randomized_trial"
    if "cohort" in t or "longitudinal" in t or "prospective" in t:
        return "human_cohort"
    if "case-control" in t or "case control" in t:
        return "human_case_control"
    if "case report" in t or "case series" in t:
        return "human_case_report_or_series"
    if re.search(r"\b(mouse|mice|murine|rat)\b", t):
        return "animal_study"
    if "in vitro" in t or "cell line" in t or "cultured" in t:
        return "cell_in_vitro"
    if "review" in t:
        return "mechanistic_review"
    return "unknown_design"


def score(text: str) -> dict:
    design = classify_design(text)
    species = classify_species(text)
    base = DESIGN_WEIGHTS[design]
    q = max(5, min(100, base - SPECIES_PENALTY[species]))
    return {"study_design": design, "species": species, "evidence_quality_score": q}


def main(path: str) -> None:
    p = Path(path)
    rows = []
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = " ".join(str(v) for v in row.values())
            rows.append({**row, **score(text)})
    print(json.dumps(rows, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps(score("human cohort allergy histamine blood pressure"), indent=2))
    else:
        main(sys.argv[1])
