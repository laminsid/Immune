#!/usr/bin/env python3
"""Canonical parity fixtures v0.9.1.

Run this from Python to emit expected scores. Paste the same inputs into a
Kotlin unit test against CausalityScorer.kt and HypothesisRankingEngine.kt;
every value MUST match. Any divergence is a bug per
docs/CANONICAL_SCORING_FORMULA_v0.9.1.md.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from research.causality_scorer import score as causality_score
from research.hypothesis_ranker import overall_score, status_for


CAUSALITY_FIXTURES = [
    {
        "name": "stress_allergy_human_cohort_repeated_no_control",
        "input": {
            "text": "stress before allergy histamine blood pressure mast cell mechanism",
            "evidence_quality": 74,
            "repeatability": 3,
            "study_design": "human_cohort",
            "axes": ["psychoneuroimmune_axis", "type2_allergy_axis", "autonomic_vascular_axis"],
            "negative_control_status": "control_required_before_strong",
        },
    },
    {
        "name": "animal_model_no_temporal_no_repeats",
        "input": {
            "text": "mouse il-6 inflammation pathway",
            "evidence_quality": 30,
            "repeatability": 0,
            "study_design": "animal_study",
            "axes": ["tnf_il6_autoimmune_axis"],
            "negative_control_status": "weak_no_control_possible",
        },
    },
    {
        "name": "rct_strong_negative_finding",
        "input": {
            "text": "randomized clinical trial showed no association testosterone allergy",
            "evidence_quality": 88,
            "repeatability": 2,
            "study_design": "human_randomized_trial",
            "axes": ["testosterone_immune_axis", "type2_allergy_axis"],
            "negative_control_status": "watch_requires_controls",
        },
    },
]

RANKING_FIXTURES = [
    {"name": "ev74_ca65_nv60_rep3", "ev": 74, "ca": 65, "nv": 60, "rep": 3, "neg": "watch_requires_controls"},
    {"name": "ev30_ca20_nv10_rep0", "ev": 30, "ca": 20, "nv": 10, "rep": 0, "neg": "weak_no_control_possible"},
    {"name": "ev88_ca78_nv70_rep4_blocked", "ev": 88, "ca": 78, "nv": 70, "rep": 4, "neg": "control_required_before_strong"},
    {"name": "ev88_ca78_nv70_rep4_passed", "ev": 88, "ca": 78, "nv": 70, "rep": 4, "neg": "watch_requires_controls"},
]


def run():
    out = {"formula_version": "v0.9.1", "causality": [], "ranking": []}
    for fx in CAUSALITY_FIXTURES:
        result = causality_score(**fx["input"])
        out["causality"].append({"name": fx["name"], "input": fx["input"], "expected": result})
    for fx in RANKING_FIXTURES:
        score_val = overall_score(fx["ev"], fx["ca"], fx["nv"], fx["rep"])
        st = status_for(score_val, fx["rep"], fx["neg"])
        out["ranking"].append({
            "name": fx["name"],
            "input": {"ev": fx["ev"], "ca": fx["ca"], "nv": fx["nv"], "rep": fx["rep"], "neg": fx["neg"]},
            "expected": {"overall_score": score_val, "status": st},
        })
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    run()
