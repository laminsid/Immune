#!/usr/bin/env python3
"""DNA/RNA/omics bridge helper for Immune Error Radar.

Reads a matrix CSV and annotates cases with omics-axis hints. This is deliberately
simple: it is a research aide, not a clinical model.

v1.1.1 fix:
- A column name alone no longer counts as an omics signal.
- `no`, `unknown`, `none`, blank, and equivalent values are treated as absent.
- Strong hits require an affirmative/measured value in the row value.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable

DNA_TERMS = {"dna", "genome", "genomic", "snp", "variant", "methylation", "epigenetic"}
RNA_TERMS = {"rna", "rna_seq", "rnaseq", "transcriptomic", "transcriptome", "gene_expression", "mirna", "scrna"}
IMMUNE_TERMS = {"ige", "eosinophils", "histamine", "il6", "tnf_alpha", "il10", "crp", "ferritin"}

NEGATIVE_VALUES = {
    "", "0", "0.0", "false", "no", "none", "null", "na", "n/a", "not_available",
    "not available", "unknown", "unk", "negative", "absent", "missing", "not_measured",
    "not measured",
}
AFFIRMATIVE_VALUES = {
    "1", "1.0", "true", "yes", "y", "present", "positive", "detected", "measured",
    "available", "high", "medium", "moderate", "low", "elevated", "reduced", "abnormal",
}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize(value: object) -> str:
    return str(value or "").strip().lower().replace("-", "_")


def has_meaningful_value(value: object) -> bool:
    v = normalize(value)
    if v in NEGATIVE_VALUES:
        return False
    if v in AFFIRMATIVE_VALUES:
        return True
    try:
        return float(v) != 0.0
    except ValueError:
        pass
    return len(v) >= 3


def matching_terms(name: str, terms: Iterable[str]) -> list[str]:
    n = normalize(name)
    return sorted(term for term in terms if term in n)


def row_hits(row: dict[str, str], terms: set[str]) -> list[str]:
    hits: set[str] = set()
    for key, value in row.items():
        key_hits = matching_terms(key, terms)
        if not key_hits:
            continue
        if has_meaningful_value(value):
            hits.update(key_hits)
    return sorted(hits)


def immune_hits(row: dict[str, str]) -> list[str]:
    return row_hits(row, IMMUNE_TERMS)


def score_row(row: dict[str, str]) -> dict[str, object]:
    dna_hits = row_hits(row, DNA_TERMS)
    rna_hits = row_hits(row, RNA_TERMS)
    immune = immune_hits(row)

    pattern = "low_omics_signal"
    if dna_hits and rna_hits and immune:
        pattern = "dna_rna_immune_bridge_candidate"
    elif rna_hits and immune:
        pattern = "rna_immune_expression_candidate"
    elif dna_hits and immune:
        pattern = "dna_epigenetic_immune_candidate"

    return {
        "case_id": row.get("case_id") or row.get("id") or "unknown",
        "pattern": pattern,
        "dna_hits": dna_hits,
        "rna_hits": rna_hits,
        "immune_hits": immune,
    }


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("research/examples/sample_cases.csv")
    rows = load_rows(path)
    result = [score_row(row) for row in rows]
    print(json.dumps({"input": str(path), "rows": len(rows), "omics_bridge": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
