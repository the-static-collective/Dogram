"""MARKOV-LUMPABILITY-RESIDUAL-001: exact finite residual for partitioned Markov rows.

Research only. A residual measures structural stochastic mismatch; it does not turn
an undeclared tolerance into equivalence, evidence, occurrence, or authority.
"""
from fractions import Fraction

from research.markov_lumpability_001 import analyze


def _f(x):
    return x if isinstance(x, Fraction) else Fraction(str(x))


def analyze_residual(states, block_of, transition, tolerance=None):
    base = analyze(states, block_of, transition)
    states = tuple(states)
    blocks = tuple(sorted(set(block_of.values())))
    agg = base["aggregate_block_mass"]

    pair_receipts = []
    maximum = None
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            if block_of[x] != block_of[y]:
                continue
            delta = {b: agg[x][b] - agg[y][b] for b in blocks}
            abs_delta = {b: abs(v) for b, v in delta.items()}
            max_block = max(abs_delta, key=lambda b: (abs_delta[b], str(b)))
            tv = sum(abs_delta.values(), Fraction()) / 2
            receipt = {
                "pair": (x, y),
                "source_block": block_of[x],
                "signed_block_delta": delta,
                "max_block": max_block,
                "max_block_discrepancy": abs_delta[max_block],
                "total_variation": tv,
            }
            pair_receipts.append(receipt)
            key = (tv, abs_delta[max_block], str(x), str(y))
            if maximum is None or key > maximum[0]:
                maximum = (key, receipt)

    tol = None if tolerance is None else _f(tolerance)
    if tol is not None and (tol < 0 or tol > 1):
        raise ValueError("tolerance must be in [0,1]")

    max_tv = Fraction() if maximum is None else maximum[1]["total_variation"]
    within_declared_tolerance = None if tol is None else max_tv <= tol
    return {
        "strong_lumpable": base["strong_lumpable"],
        "pair_receipts": tuple(pair_receipts),
        "maximum_total_variation": max_tv,
        "maximum_witness": None if maximum is None else maximum[1],
        "declared_tolerance": tol,
        "within_declared_tolerance": within_declared_tolerance,
        "non_claims": (
            "small residual is not exact lumpability",
            "within declared tolerance is not semantic equivalence",
            "transition probability is not evidentiary confidence",
            "positive probability is not occurrence",
            "residual magnitude is not causal distance",
        ),
    }
