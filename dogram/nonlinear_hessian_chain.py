"""Bounded exact research kernel for NONLINEAR-HESSIAN-CHAIN-001.

This module is intentionally internal research surface. It verifies a scalar
second-order chain-rule specimen with exact rational arithmetic. It does not
promote a public Dogram operator or infer occurrence, evidence, causation, or
semantic equivalence from a coordinate reparameterization.
"""

from fractions import Fraction


def _fraction(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def _coefficients(values, name):
    result = tuple(_fraction(value) for value in values)
    if not result:
        raise ValueError(f"{name} coefficients must be non-empty")
    return result


def _evaluate(coefficients, point):
    point = _fraction(point)
    total = Fraction(0)
    power = Fraction(1)
    for coefficient in coefficients:
        total += coefficient * power
        power *= point
    return total


def _derivative(coefficients):
    if len(coefficients) <= 1:
        return (Fraction(0),)
    return tuple(
        Fraction(power) * coefficient
        for power, coefficient in enumerate(coefficients)
        if power > 0
    )


def _poly_add(left, right):
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else Fraction(0))
        + (right[i] if i < len(right) else Fraction(0))
        for i in range(size)
    )


def _poly_mul(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return tuple(result)


def _compose(outer, inner):
    """Return exact coefficients of outer(inner(z)), low degree to high."""
    result = (Fraction(0),)
    power = (Fraction(1),)
    for coefficient in outer:
        result = _poly_add(result, tuple(coefficient * value for value in power))
        power = _poly_mul(power, inner)
    return result


def nonlinear_hessian_receipt(objective_coefficients, map_coefficients, z):
    """Replay first- and second-order chain rules for f(phi(z)) exactly.

    Coefficients are ordered from degree zero upward. The returned
    ``naive_hessian_pullback`` is the scalar analogue of J^T H J. The
    ``second_order_correction`` is f'(phi(z)) * phi''(z), which vanishes at a
    critical point but need not vanish elsewhere.
    """
    objective = _coefficients(objective_coefficients, "objective")
    coordinate_map = _coefficients(map_coefficients, "coordinate map")
    z = _fraction(z)

    objective_prime = _derivative(objective)
    objective_second = _derivative(objective_prime)
    map_prime = _derivative(coordinate_map)
    map_second = _derivative(map_prime)

    x = _evaluate(coordinate_map, z)
    base_gradient = _evaluate(objective_prime, x)
    base_hessian = _evaluate(objective_second, x)
    jacobian = _evaluate(map_prime, z)
    map_second_derivative = _evaluate(map_second, z)

    transformed_gradient = base_gradient * jacobian
    naive_hessian_pullback = base_hessian * jacobian * jacobian
    second_order_correction = base_gradient * map_second_derivative
    transformed_hessian = naive_hessian_pullback + second_order_correction

    composite = _compose(objective, coordinate_map)
    composite_prime = _derivative(composite)
    composite_second = _derivative(composite_prime)

    return {
        "x": x,
        "base_gradient": base_gradient,
        "base_hessian": base_hessian,
        "jacobian": jacobian,
        "map_second_derivative": map_second_derivative,
        "transformed_gradient": transformed_gradient,
        "naive_hessian_pullback": naive_hessian_pullback,
        "second_order_correction": second_order_correction,
        "transformed_hessian": transformed_hessian,
        "direct_composite_gradient": _evaluate(composite_prime, z),
        "direct_composite_hessian": _evaluate(composite_second, z),
        "critical_point": base_gradient == 0,
    }
