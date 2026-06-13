#!/usr/bin/env python3
"""Map marker/gene words into the canonical global immune axes."""
from __future__ import annotations
import json, sys

RULES = {
    "type2_allergy_axis": ["ige", "eosinophil", "mast", "histamine", "il4", "il-4", "il5", "il-5", "il13", "il-13"],
    "interferon_antiviral_axis": ["ifn", "interferon", "isg", "mx1", "oas", "viral", "virus"],
    "tnf_il6_autoimmune_axis": ["tnf", "il6", "il-6", "il1b", "il-1b", "rheumatoid"],
    "regulatory_brake_axis": ["il10", "il-10", "foxp3", "treg", "regulatory"],
    "tcell_activation_axis": ["cd4", "cd8", "t cell", "t-cell", "th1", "th17"],
    "bcell_antibody_axis": ["b cell", "b-cell", "antibody", "plasma", "igg", "igm", "iga"],
    "tissue_damage_axis": ["ldh", "damage", "injury", "fibrosis", "endothelial"],
    "resolution_recovery_axis": ["resolution", "recovery", "repair", "remission"],
}

def map_text(text: str) -> list[str]:
    t = text.lower()
    return [axis for axis, keys in RULES.items() if any(k in t for k in keys)]

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "interferon IL6 IL10 CD8 antibody tissue damage recovery"
    print(json.dumps({"text": text, "axes": map_text(text)}, indent=2))
