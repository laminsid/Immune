#!/usr/bin/env python3
"""Verify the public ImmuneErrorRadar evidence package.

This checker is intentionally conservative. It verifies that the repository contains the
research artifacts needed for review. It does not certify biological truth, source truth,
or clinical validity.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "LICENSE",
    "NOTICE",
    "RESEARCHER_QUICKSTART.md",
    "docs/RECEIPTS_HASHES_v30698.md",
    "docs/TARGETED_GPL5175_REVIEW_MANIFEST_v30698.md",
    "docs/TIER0_BOUNDARIES_v30698.md",
    "docs/REPLAY_DESCRIPTION_v30698.md",
    "assets/receipts/receipts_hashes_index_v30698.json",
    "assets/receipts/receipts_hashes_index_v30698.csv",
    "assets/manifests/targeted_GPL5175_review_manifest_v30698.csv",
    "assets/manifests/gpl5175_targeted_probe_manifest_v1.source.json",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    print("ImmuneErrorRadar evidence package check v3.0.7.4")
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        for p in missing:
            print(f"MISSING {p}")
        fail("required evidence package files are missing")

    receipt_json = ROOT / "assets/receipts/receipts_hashes_index_v30698.json"
    try:
        receipt_data = json.loads(receipt_json.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"receipt JSON parse failed: {exc}")

    receipt_csv = ROOT / "assets/receipts/receipts_hashes_index_v30698.csv"
    try:
        with receipt_csv.open("r", encoding="utf-8", newline="") as fh:
            receipt_rows = list(csv.DictReader(fh))
    except Exception as exc:
        fail(f"receipt CSV parse failed: {exc}")

    manifest_csv = ROOT / "assets/manifests/targeted_GPL5175_review_manifest_v30698.csv"
    try:
        with manifest_csv.open("r", encoding="utf-8", newline="") as fh:
            manifest_rows = list(csv.DictReader(fh))
    except Exception as exc:
        fail(f"targeted manifest CSV parse failed: {exc}")

    source_manifest = ROOT / "assets/manifests/gpl5175_targeted_probe_manifest_v1.source.json"
    try:
        source_data = json.loads(source_manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"source manifest JSON parse failed: {exc}")

    print(f"PASS required files: {len(REQUIRED)}")
    print(f"PASS receipt json type: {type(receipt_data).__name__}")
    print(f"PASS receipt csv rows: {len(receipt_rows)}")
    print(f"PASS targeted manifest rows: {len(manifest_rows)}")
    print(f"PASS source manifest type: {type(source_data).__name__}")
    print("BOUNDARY: This verifies package structure and UTF-8 parseability only.")
    print("BOUNDARY: It does not certify biology, clinical validity, source truth, or wet-lab evidence.")


if __name__ == "__main__":
    main()
