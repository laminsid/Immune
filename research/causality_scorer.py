#!/usr/bin/env python3
"""Canonical causality scoring v0.9.1.

Matches CausalityScorer.kt exactly. See docs/CANONICAL_SCORING_FORMULA_v0.9.1.md.
The score ranks hypotheses; it does not prove causality.

Changes from v0.9.0:
- Adds design_boost (was missing, caused divergence with Kotlin).
- Adds negative_control_penalty (was missing, contradicted v0.9 README claim).
- Repeatability bucketing aligned to Kotlin (10/25/48/70 instead of linear).
"""
import json
import sys

MEASURABLE = [
    "ige", "eosinophil", "histamine", "crp", "il-6", "tnf", "il-10",
    "blood pressure", "heart rate", "rna", "gene expression",
    "dna methylation", "testosterone", "protein", "muscle mass",
]
TEMPORAL = [
    "before", "after", "preced", "follow-up", "longitudinal",
    "prospective", "time course", "lag",
]


def temporality_score(text, study_design=""):
    t = text.lower()
    if any(x in t for x in TEMPORAL):
        return 55
    if "cohort" in study_design or "trial" in study_design:
        return 50
    return 20


def measurable_score(text, axes=None):
    t = text.lower()
    axes = axes or []
    s = 15 + 8 * sum(1 for x in MEASURABLE if x in t)
    if "autonomic_vascular_axis" in axes:
        s += 8
    if "rna_transcriptomic_axis" in axes or "dna_genomic_axis" in axes:
        s += 10
    return max(0, min(100, s))


def repeatability_score(count):
    """Aligned to Kotlin buckets (was linear in v0.9.0)."""
    if count >= 3:
        return 70
    if count == 2:
        return 48
    if count == 1:
        return 25
    return 10


def contradiction_penalty(text):
    t = text.lower()
    if "no association" in t or "not associated" in t:
        return 25
    if any(x in t for x in ["conflicting", "inconsistent", "controversial"]):
        return 18
    return 5


def design_boost(study_design):
    if "randomized" in study_design:
        return 10
    if "cohort" in study_design:
        return 8
    if "case_control" in study_design:
        return 3
    return 0


def negative_control_penalty(status):
    """NEW in v0.9.1: integrate negative-control into the score itself.

    Closes the gap where v0.9.0 claimed negative-control resistance was
    part of the rule but never multiplied into the numeric score.
    """
    if status == "control_required_before_strong":
        return 12
    if status == "watch_requires_controls":
        return 6
    return 0


def score(
    text,
    evidence_quality=35,
    repeatability=0,
    study_design="",
    axes=None,
    negative_control_status="weak_no_control_possible",
):
    """Canonical causality scoring matching Kotlin CausalityScorer.kt."""
    t = text.lower()
    axes = axes or []
    temporality = temporality_score(t, study_design)
    measurable = measurable_score(t, axes)
    plausibility = 60 if any(
        x in t for x in ["mechanism", "pathway", "receptor", "cytokine", "mast cell", "autonomic"]
    ) else 30
    rep = repeatability_score(repeatability)
    contradiction = contradiction_penalty(t)
    boost = design_boost(study_design)
    neg_pen = negative_control_penalty(negative_control_status)

    total = int(
        temporality * 0.22
        + plausibility * 0.26
        + measurable * 0.18
        + rep * 0.18
        + evidence_quality * 0.16
        + boost
        - contradiction
        - neg_pen
    )
    return {
        "causality_score": max(0, min(100, total)),
        "temporality": temporality,
        "biological_plausibility": plausibility,
        "measurable_marker": measurable,
        "repeatability": rep,
        "contradiction_penalty": contradiction,
        "design_boost": boost,
        "negative_control_penalty": neg_pen,
        "formula_version": "v0.9.1",
    }


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "stress before allergy histamine blood pressure mast cell mechanism"
    print(json.dumps(score(text), indent=2))
