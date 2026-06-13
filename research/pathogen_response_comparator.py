#!/usr/bin/env python3
"""Compare protective vs damaging antiviral response themes."""
from __future__ import annotations
import json, sys
from immune_axis_mapper import map_text


def compare(text: str) -> dict:
    axes = set(map_text(text))
    notes = []
    if "interferon_antiviral_axis" in axes:
        notes.append("Interferon timing should be evaluated against viral load and recovery/deterioration labels.")
    if "regulatory_brake_axis" in axes:
        notes.append("Regulatory brake markers should be checked as resolution vs runaway amplification signals.")
    if "tissue_damage_axis" in axes:
        notes.append("Separate pathogen control from host tissue damage; do not treat stronger inflammation as better immunity.")
    if not notes:
        notes.append("No antiviral-response axis detected; collect viral-response data first.")
    return {"axes": sorted(axes), "notes": notes}

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "interferon il10 tissue damage viral recovery"
    print(json.dumps(compare(text), indent=2))
