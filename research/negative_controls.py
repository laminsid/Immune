#!/usr/bin/env python3
"""Permutation-based negative-control v1.0.

v0.9.0 used a single random shuffle, which produces noise rather than evidence.
v1.0 runs N permutations (default 1000), computes empirical p-value as
  p = (extreme_count + 1) / (n_perm + 1)

with the +1 add-one correction (Phipson & Smyth 2010) so p > 0 even when no
permutation exceeds the observed correlation.

Interpretation:
  p < 0.01      strong negative-control resistance
  p < 0.05      moderate
  p >= 0.05     forward correlation is not distinguishable from chance shuffle
                AT THIS SAMPLE SIZE — does NOT prove no effect.

Sample-size gate:
  n < 14        flag INSUFFICIENT_DATA (correlation unstable below ~14)
  14 <= n < 30  flag LOW_POWER
  n >= 30       no flag
"""
import csv
import json
import random
import statistics
import sys
from pathlib import Path


def corr(xs, ys):
    n = len(xs)
    if n < 3 or n != len(ys):
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = sum((x - mx) ** 2 for x in xs) ** 0.5
    deny = sum((y - my) ** 2 for y in ys) ** 0.5
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def permutation_pvalue(xs, ys, n_perm=1000, seed=42):
    """Two-sided permutation p-value for absolute correlation.

    Returns (observed_corr, p_value) or (observed_corr, None) if observed
    correlation cannot be computed.
    """
    observed = corr(xs, ys)
    if observed is None:
        return None, None
    obs_abs = abs(observed)
    rng = random.Random(seed)
    ys_copy = list(ys)
    extreme = 0
    valid_perms = 0
    for _ in range(n_perm):
        rng.shuffle(ys_copy)
        c = corr(xs, ys_copy)
        if c is None:
            continue
        valid_perms += 1
        if abs(c) >= obs_abs:
            extreme += 1
    if valid_perms == 0:
        return observed, None
    # Phipson & Smyth (2010) add-one correction
    p = (extreme + 1) / (valid_perms + 1)
    return observed, p


def sample_size_flag(n):
    if n < 14:
        return "INSUFFICIENT_DATA"
    if n < 30:
        return "LOW_POWER"
    return "OK"


def interpret(p):
    if p is None:
        return "no_p_value_available"
    if p < 0.01:
        return "strong_resistance_to_chance"
    if p < 0.05:
        return "moderate_resistance_to_chance"
    return "not_distinguishable_from_chance_at_this_n"


def run(path, exposure, outcome, n_perm=1000, max_lag=2):
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8")))
    xs_full = [float(r.get(exposure, 0) or 0) for r in rows]
    ys_full = [float(r.get(outcome, 0) or 0) for r in rows]
    n = len(xs_full)
    flag = sample_size_flag(n)

    # Forward lag analysis: x predicts y at +1 lag (canonical hypothesis test)
    forward = None
    forward_p = None
    if n > 3:
        forward, forward_p = permutation_pvalue(xs_full[:-1], ys_full[1:], n_perm)

    # Reverse-time control: y predicts x at +1 lag (should be weaker if x→y is real)
    reverse = None
    reverse_p = None
    if n > 3:
        reverse, reverse_p = permutation_pvalue(ys_full[:-1], xs_full[1:], n_perm)

    # Same-day correlation (lag 0) — useful baseline
    same_day = corr(xs_full, ys_full)

    return {
        "n": n,
        "sample_size_flag": flag,
        "n_permutations": n_perm,
        "exposure": exposure,
        "outcome": outcome,
        "lag_0_correlation": same_day,
        "forward_lag_1": {
            "correlation": forward,
            "p_value": forward_p,
            "interpretation": interpret(forward_p),
        },
        "reverse_time_lag_1": {
            "correlation": reverse,
            "p_value": reverse_p,
            "interpretation": interpret(reverse_p),
        },
        "verdict": _verdict(forward, forward_p, reverse, reverse_p, flag),
        "method": "permutation_pvalue_phipson_smyth_2010",
        "version": "v1.0",
    }


def _verdict(forward, forward_p, reverse, reverse_p, flag):
    if flag == "INSUFFICIENT_DATA":
        return "withhold_judgement_collect_more_data"
    if forward is None:
        return "cannot_compute"
    if forward_p is not None and forward_p < 0.05 and (
        reverse is None or reverse_p is None or abs(forward) > abs(reverse)
    ):
        return "forward_signal_passes_negative_control"
    if reverse is not None and abs(reverse) >= abs(forward) * 0.9:
        return "reverse_time_just_as_strong_likely_confound"
    return "forward_signal_does_not_clearly_beat_chance"


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({
            "usage": "negative_controls.py series.csv exposure_col outcome_col [n_perm]",
            "default_n_perm": 1000,
        }, indent=2))
    else:
        n_perm = int(sys.argv[4]) if len(sys.argv) >= 5 else 1000
        print(json.dumps(run(sys.argv[1], sys.argv[2], sys.argv[3], n_perm=n_perm), indent=2))
