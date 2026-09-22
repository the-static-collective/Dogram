"""SCALARIZATION-VISIBILITY-001: finite research kernel.

Receipts method-relative visibility of finite biobjective minimization points.
No semantic preference, occurrence, evidence, or authority is inferred.
"""
from fractions import Fraction


def dominates(a, b):
    """Strict Pareto dominance for minimization."""
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))


def pareto_minimal(points, name):
    target = points[name]
    return not any(other != name and dominates(value, target) for other, value in points.items())


def weighted_cost(point, w):
    w = Fraction(w)
    return w * point[0] + (1 - w) * point[1]


def weighted_winners(points, w):
    costs = {name: weighted_cost(point, w) for name, point in points.items()}
    best = min(costs.values())
    return tuple(sorted(name for name, cost in costs.items() if cost == best))


def epsilon_constraint_winners(points, epsilon):
    """Minimize objective 1 subject to objective 2 <= declared epsilon."""
    epsilon = Fraction(epsilon)
    feasible = {name: point for name, point in points.items() if point[1] <= epsilon}
    if not feasible:
        return (), {}
    best = min(point[0] for point in feasible.values())
    winners = tuple(sorted(name for name, point in feasible.items() if point[0] == best))
    return winners, feasible


def frozen_receipt():
    points = {"A": (Fraction(0), Fraction(4)), "B": (Fraction(2), Fraction(3)), "C": (Fraction(4), Fraction(0))}
    # Exact breakpoints suffice to partition every normalized nonnegative weighted sum.
    probes = (Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(3, 5), Fraction(1))
    weighted = {str(w): weighted_winners(points, w) for w in probes}
    eps_winners, feasible = epsilon_constraint_winners(points, Fraction(3))
    return {
        "points": points,
        "pareto_minimal": {name: pareto_minimal(points, name) for name in points},
        "weighted_probe_winners": weighted,
        "B_weighted_sum_selectable": False,  # proved by incompatible exact inequalities in research note/tests
        "epsilon": Fraction(3),
        "epsilon_feasible": tuple(sorted(feasible)),
        "epsilon_winners": eps_winners,
        "B_epsilon_selectable": "B" in eps_winners,
        "seal": "INVISIBLE_TO_ONE_DECLARED_SCALARIZATION_FAMILY != ABSENT_FROM_THE_PARETO_SET",
        "authority": "none",
    }
