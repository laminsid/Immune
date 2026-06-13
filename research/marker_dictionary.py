#!/usr/bin/env python3
"""Canonical marker dictionary for research-side normalization."""
from __future__ import annotations
import json

MARKERS = {
    "CRP": {"canonical": "CRP_mg_L", "axis": ["systemic_damage", "tnf_il6"], "accepted_units": ["mg/L"]},
    "ESR": {"canonical": "ESR_mm_h", "axis": ["systemic_inflammation"], "accepted_units": ["mm/h", "mm/hr"]},
    "IgE": {"canonical": "IgE_IU_mL", "axis": ["type2_allergy"], "accepted_units": ["IU/mL", "kU/L"]},
    "Eosinophils": {"canonical": "Eosinophils_cells_uL", "axis": ["type2_allergy", "eosinophil"], "accepted_units": ["cells/uL", "cells/µL"]},
    "IL6": {"canonical": "IL6_pg_mL", "axis": ["tnf_il6", "hyperinflammatory"], "accepted_units": ["pg/mL"]},
    "TNF_alpha": {"canonical": "TNF_alpha_pg_mL", "axis": ["tnf_il6", "hyperinflammatory"], "accepted_units": ["pg/mL"]},
    "IL10": {"canonical": "IL10_pg_mL", "axis": ["regulatory_brake"], "accepted_units": ["pg/mL"]},
    "Ferritin": {"canonical": "Ferritin_ng_mL", "axis": ["systemic_damage", "hyperinflammatory"], "accepted_units": ["ng/mL"]},
    "Histamine": {"canonical": "Histamine", "axis": ["mast_cell"], "accepted_units": ["ng/mL", "nmol/L", "unknown"]},
}

if __name__ == "__main__":
    print(json.dumps(MARKERS, indent=2, ensure_ascii=False))
