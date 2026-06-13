#!/usr/bin/env python3
"""Simple lagged association scanner for private repeated observations."""
import csv
import json
import statistics
import sys
from pathlib import Path


def corr(xs, ys):
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    denx = sum((x-mx)**2 for x in xs) ** 0.5
    deny = sum((y-my)**2 for y in ys) ** 0.5
    if denx == 0 or deny == 0:
        return None
    return num/(denx*deny)


def scan(path: str, exposure: str, outcome: str, max_lag: int = 2):
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8")))
    xs = [float(r.get(exposure, 0) or 0) for r in rows]
    ys = [float(r.get(outcome, 0) or 0) for r in rows]
    out = []
    for lag in range(max_lag + 1):
        if lag == 0:
            c = corr(xs, ys)
        else:
            c = corr(xs[:-lag], ys[lag:])
        out.append({"lag_days": lag, "correlation": c})
    return out


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"usage": "personal_time_series.py personal_series.csv exposure_col outcome_col"}, indent=2))
    else:
        print(json.dumps(scan(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2))
