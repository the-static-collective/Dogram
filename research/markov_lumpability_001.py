"""MARKOV-LUMPABILITY-001: exact finite partition/lumpability receipt.

Research only. Support reachability is kept distinct from transition mass.
Probabilities are parsed as Fractions for exact arithmetic.
"""
from fractions import Fraction


def _f(x):
    return x if isinstance(x, Fraction) else Fraction(str(x))


def analyze(states, block_of, transition):
    states = tuple(states)
    blocks = tuple(sorted(set(block_of.values())))
    if set(block_of) != set(states) or set(transition) != set(states):
        raise ValueError("states, block_of, and transition rows must have identical state IDs")
    rows = {}
    for s in states:
        if set(transition[s]) != set(states):
            raise ValueError("each transition row must name every state")
        row = {t: _f(transition[s][t]) for t in states}
        if any(v < 0 for v in row.values()) or sum(row.values(), Fraction()) != 1:
            raise ValueError("transition rows must be nonnegative and sum exactly to 1")
        rows[s] = row

    aggregate = {
        s: {b: sum((rows[s][t] for t in states if block_of[t] == b), Fraction()) for b in blocks}
        for s in states
    }
    support = {s: tuple(b for b in blocks if aggregate[s][b] > 0) for s in states}
    witness = None
    support_witness = None
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            if block_of[x] != block_of[y]:
                continue
            if support[x] != support[y] and support_witness is None:
                support_witness = (x, y, support[x], support[y])
            for b in blocks:
                if aggregate[x][b] != aggregate[y][b] and witness is None:
                    witness = (x, y, b, aggregate[x][b], aggregate[y][b])
    lumpable = witness is None
    quotient = None
    if lumpable:
        quotient = {}
        for b in blocks:
            representative = next(s for s in states if block_of[s] == b)
            quotient[b] = aggregate[representative]
    return {
        "strong_lumpable": lumpable,
        "aggregate_block_mass": aggregate,
        "quotient_support": support,
        "mass_counterexample": witness,
        "support_counterexample": support_witness,
        "induced_transition": quotient,
        "non_claims": (
            "positive support is not occurrence",
            "same quotient support is not lumpability",
            "transition probability is not evidentiary confidence",
            "lumpability is not causal equivalence",
        ),
    }
