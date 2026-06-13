#!/usr/bin/env python3
"""Minimal unit normalizer for immune marker tables.

This deliberately refuses unknown conversions rather than inventing them.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path
from marker_dictionary import MARKERS

ALIASES = {k.lower(): k for k in MARKERS}
ALIASES.update({"tnf-α": "TNF_alpha", "tnf_alpha": "TNF_alpha", "il-6": "IL6", "il-10": "IL10", "total ige": "IgE"})


def normalize_marker(marker: str, value: str, unit: str) -> tuple[str, float, str, str]:
    key = ALIASES.get(marker.strip().lower())
    if not key:
        return marker, float(value), unit, "UNKNOWN_MARKER"
    meta = MARKERS[key]
    if unit not in meta["accepted_units"]:
        return meta["canonical"], float(value), unit, "UNVERIFIED_UNIT"
    # IU/mL and kU/L are numerically equivalent for specific IgE contexts, but total IgE conventions vary; do not convert blindly.
    return meta["canonical"], float(value), unit, "OK"


def normalize_csv(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print("canonical_marker,value,unit,status")
    for r in rows:
        marker, value, unit, status = normalize_marker(r["marker"], r["value"], r["unit"])
        print(f"{marker},{value},{unit},{status}")


if __name__ == "__main__":
    normalize_csv(Path(sys.argv[1] if len(sys.argv) > 1 else "research/examples/sample_markers.csv"))
