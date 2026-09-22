"""UNSUPPORTED-PARETO-001: Pareto-valid does not imply linearly supported.

Research only. Objective vectors and scalarization weights are declared calculation
inputs, not ontology, preference, evidence, occurrence, or authority.
"""
from fractions import Fraction


def dominates(left, right):
    if len(left) != len(right) or not left:
        raise ValueError("cost vectors must have the same nonzero dimension")
    return all(a <= b for a, b in zip(left, right)) and any(a < b for a, b in zip(left, right))


def pareto_minima(points):
    """Return names whose vectors are nondominated for minimization."""
    items = list(points.items())
    return tuple(name for name, point in items if not any(
        other_name != name and dominates(other, point)
        for other_name, other in items
    ))


def scalar_cost(point, w):
    """Biobjective weighted sum with declared w in [0,1]."""
    w = Fraction(w)
    if w < 0 or w > 1:
        raise ValueError("w must lie in [0,1]")
    if len(point) != 2:
        raise ValueError("this bounded specimen is biobjective")
    return w * Fraction(point[0]) + (1 - w) * Fraction(point[1])


def support_interval(name, points):
    """Exact feasible interval of w for which name weakly minimizes weighted sum.

    Each comparison is linear in w; intersect its exact rational interval with [0,1].
    Returns None when no nonnegative normalized linear scalarization supports the point.
    """
    target = points[name]
    lo, hi = Fraction(0), Fraction(1)
    for other_name, other in points.items():
        if other_name == name:
            continue
        # target_cost <= other_cost gives a*w + b <= 0.
        a = Fraction(target[0] - target[1] - other[0] + other[1])
        b = Fraction(target[1] - other[1])
        if a == 0:
            if b > 0:
                return None
            continue
        bound = -b / a
        if a > 0:
            hi = min(hi, bound)
        else:
            lo = max(lo, bound)
        if lo > hi:
            return None
    return (max(lo, Fraction(0)), min(hi, Fraction(1))) if max(lo, Fraction(0)) <= min(hi, Fraction(1)) else None


def frozen_specimen():
    # B lies above the lower convex envelope joining A and C: nondominated but unsupported.
    points = {
        "A": (Fraction(0), Fraction(4)),
        "B": (Fraction(2), Fraction(3)),
        "C": (Fraction(4), Fraction(0)),
    }
    return {
        "points": points,
        "pareto_minima": pareto_minima(points),
        "support_intervals": {name: support_interval(name, points) for name in points},
        "B_vs_A_requires": "w <= 1/3",
        "B_vs_C_requires": "w >= 3/5",
    }
