"""Bounded exact research kernel for FACET-SCALING-MULTIPLIER-001.

This module is intentionally internal research surface. It does not promote a
public Dogram operator or attach semantic meaning to dual multipliers.
"""

from fractions import Fraction


def _fraction(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def positive_row_scaling_witness(base_constraint, scaled_constraint):
    base_normal, base_bound = base_constraint
    scaled_normal, scaled_bound = scaled_constraint
    if len(base_normal) != len(scaled_normal):
        raise ValueError("constraint dimensions differ")

    candidates = []
    for a, b in zip(base_normal, scaled_normal):
        a = _fraction(a)
        b = _fraction(b)
        if a == 0:
            if b != 0:
                raise ValueError("rows are not scalar multiples")
            continue
        candidates.append(b / a)

    if _fraction(base_bound) != 0:
        candidates.append(_fraction(scaled_bound) / _fraction(base_bound))
    elif _fraction(scaled_bound) != 0:
        raise ValueError("rows are not scalar multiples")

    if not candidates:
        raise ValueError("zero constraint has no declared positive scaling")
    scale = candidates[0]
    if scale <= 0 or any(candidate != scale for candidate in candidates[1:]):
        raise ValueError("constraint scaling must be one positive scalar")

    return {"scale": scale, "same_halfspace": True}


def dual_residual(constraints, objective, multipliers):
    if len(constraints) != len(multipliers):
        raise ValueError("one multiplier is required per constraint")
    dimension = len(objective)
    if any(len(normal) != dimension for normal, _ in constraints):
        raise ValueError("constraint and objective dimensions differ")
    return tuple(
        sum(_fraction(lam) * _fraction(normal[j]) for lam, (normal, _) in zip(multipliers, constraints))
        - _fraction(objective[j])
        for j in range(dimension)
    )


def dual_objective(constraints, multipliers):
    if len(constraints) != len(multipliers):
        raise ValueError("one multiplier is required per constraint")
    return sum(
        (_fraction(lam) * _fraction(bound) for lam, (_, bound) in zip(multipliers, constraints)),
        Fraction(0),
    )


def facet_contribution(constraint, multiplier):
    normal, bound = constraint
    lam = _fraction(multiplier)
    return {
        "weighted_normal": tuple(lam * _fraction(component) for component in normal),
        "weighted_bound": lam * _fraction(bound),
    }
