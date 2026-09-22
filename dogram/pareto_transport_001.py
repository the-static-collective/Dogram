"""PARETO-TRANSPORT-001: finite vector-cost and declared scalarization receipts.

Research-only. A cost vector is structural input, not ontology, preference, evidence,
or authority. Pareto incomparability is a calculation result, not indecision.
"""
from fractions import Fraction


def dominates(left, right):
    """True iff left Pareto-dominates right for minimization."""
    if len(left) != len(right) or not left:
        raise ValueError("cost vectors must have the same nonzero dimension")
    return all(a <= b for a, b in zip(left, right)) and any(
        a < b for a, b in zip(left, right)
    )


def compare(left, right):
    """Return the componentwise Pareto relation without choosing a winner."""
    if dominates(left, right):
        return "left_dominates"
    if dominates(right, left):
        return "right_dominates"
    if tuple(left) == tuple(right):
        return "equal_cost_vector"
    return "incomparable"


def scalar_cost(cost_vector, weights):
    """Apply caller-declared nonnegative normalized rational weights."""
    if len(cost_vector) != len(weights) or not cost_vector:
        raise ValueError("cost vector and weights must have same nonzero dimension")
    ws = tuple(Fraction(w) for w in weights)
    if any(w < 0 for w in ws) or sum(ws, Fraction(0)) != 1:
        raise ValueError("weights must be nonnegative and sum exactly to one")
    return sum((w * Fraction(c) for w, c in zip(ws, cost_vector)), Fraction(0))


def frozen_specimen():
    """Replay the vector costs exposed by TRANSPORT-METRIC-RANKING-001."""
    pi = (Fraction(2), Fraction(2))
    rho = (Fraction(3), Fraction(1))
    weights = {
        "favor_metric_1": (Fraction(3, 4), Fraction(1, 4)),
        "balanced": (Fraction(1, 2), Fraction(1, 2)),
        "favor_metric_2": (Fraction(1, 4), Fraction(3, 4)),
    }
    return {
        "pi": pi,
        "rho": rho,
        "pareto_relation": compare(pi, rho),
        "scalarizations": {
            name: {"weights": w, "pi": scalar_cost(pi, w), "rho": scalar_cost(rho, w)}
            for name, w in weights.items()
        },
    }
