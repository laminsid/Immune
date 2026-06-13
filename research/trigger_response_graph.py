#!/usr/bin/env python3
"""Build a small trigger -> response -> outcome graph from mapped axes."""
from __future__ import annotations
import json, sys
from immune_axis_mapper import map_text

EDGE_TEMPLATES = [
    ("allergen", "type2_allergy_axis", "airway/skin/gut irritation"),
    ("virus", "interferon_antiviral_axis", "viral control vs deterioration"),
    ("self-antigen", "tnf_il6_autoimmune_axis", "chronic inflammatory burden"),
    ("response shutdown", "regulatory_brake_axis", "resolution vs runaway amplification"),
    ("immune collateral damage", "tissue_damage_axis", "organ/tissue injury"),
]

def build(text: str) -> list[dict]:
    axes = set(map_text(text))
    out = []
    for trig, axis, outcome in EDGE_TEMPLATES:
        if axis in axes:
            out.append({"trigger": trig, "response_axis": axis, "outcome": outcome, "status": "WATCH"})
    return out

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "virus interferon il10 tissue damage recovery"
    print(json.dumps(build(text), indent=2))
