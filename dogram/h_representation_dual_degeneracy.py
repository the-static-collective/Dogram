"""Bounded exact research kernel for H-REPRESENTATION-DUAL-DEGENERACY-001.

This module handles only the frozen two-dimensional triangle specimen used by the
research receipt. It is not a general LP, polyhedral, or duality engine.
"""

from fractions import Fraction


def _q(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def _normalize_constraints(constraints):
    rows = []
    for a, b in constraints:
        if len(a) != 2:
            raise ValueError("frozen specimen is two-dimensional")
        rows.append((tuple(_q(v) for v in a), _q(b)))
    return tuple(rows)


def verify_redundant_constraint(base_constraints, extra_constraint):
    base = _normalize_constraints(base_constraints)
    extra = _normalize_constraints((extra_constraint,))[0]
    expected = (
        ((Fraction(-1), Fraction(0)), Fraction(0)),
        ((Fraction(0), Fraction(-1)), Fraction(0)),
        ((Fraction(1), Fraction(1)), Fraction(2)),
    )
    expected_extra = ((Fraction(1), Fraction(0)), Fraction(2))
    if base != expected or extra != expected_extra:
        raise ValueError("only the frozen triangle and x<=2 redundancy witness are supported")
    return {
        "same_feasible_triangle": True,
        "witness": "x<=x+y<=2 because y>=0",
    }


def dual_residual(constraints, objective, multipliers):
    rows = _normalize_constraints(constraints)
    c = tuple(_q(v) for v in objective)
    lam = tuple(_q(v) for v in multipliers)
    if len(c) != 2:
        raise ValueError("objective must be two-dimensional")
    if len(lam) != len(rows):
        raise ValueError("one multiplier is required per constraint")
    if any(value < 0 for value in lam):
        raise ValueError("dual multipliers must be nonnegative")
    lhs = tuple(
        sum(lam[i] * rows[i][0][j] for i in range(len(rows)))
        for j in range(2)
    )
    return tuple(lhs[j] - c[j] for j in range(2))


def dual_objective(constraints, multipliers):
    rows = _normalize_constraints(constraints)
    lam = tuple(_q(v) for v in multipliers)
    if len(lam) != len(rows):
        raise ValueError("one multiplier is required per constraint")
    if any(value < 0 for value in lam):
        raise ValueError("dual multipliers must be nonnegative")
    return sum(lam[i] * rows[i][1] for i in range(len(rows)))


def redundant_dual_family(t):
    t = _q(t)
    if t < 0 or t > 1:
        raise ValueError("t must lie in [0,1]")
    return (Fraction(0), t, t, Fraction(1) - t)
