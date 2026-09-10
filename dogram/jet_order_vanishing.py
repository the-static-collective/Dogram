"""Bounded exact research kernel for JET-ORDER-VANISHING-001.

This module compares finite polynomial germs at zero, their declared truncated
jets, and the first nonzero derivative order before and after an explicitly
supplied one-variable local reparameterization. It does not promote a public
Dogram operator or infer occurrence, evidence, causation, importance, or
semantic equivalence from a jet or singularity classification.
"""

from fractions import Fraction
from math import factorial


def _fraction(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def _polynomial(values, name):
    coefficients = tuple(_fraction(value) for value in values)
    if not coefficients:
        raise ValueError(f"{name} must contain at least one coefficient")
    return coefficients


def _trim(coefficients):
    values = list(coefficients)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def _multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return _trim(result)


def _add(left, right):
    size = max(len(left), len(right))
    result = [Fraction(0)] * size
    for index in range(size):
        if index < len(left):
            result[index] += left[index]
        if index < len(right):
            result[index] += right[index]
    return _trim(result)


def _scale(scalar, polynomial):
    return _trim(tuple(scalar * value for value in polynomial))


def _compose(outer, inner):
    """Return outer(inner(z)) for finite ascending coefficient tuples."""
    result = (Fraction(0),)
    power = (Fraction(1),)
    for coefficient in outer:
        result = _add(result, _scale(coefficient, power))
        power = _multiply(power, inner)
    return _trim(result)


def _jet(coefficients, order):
    return tuple(
        coefficients[index] if index < len(coefficients) else Fraction(0)
        for index in range(order + 1)
    )


def _first_nonzero_order(coefficients):
    for order, coefficient in enumerate(coefficients):
        if coefficient != 0:
            return order
    return None


def _derivative_at_zero(coefficients, order):
    if order >= len(coefficients):
        return Fraction(0)
    return coefficients[order] * factorial(order)


def jet_order_vanishing_receipt(left_coefficients, right_coefficients, jet_order, coordinate_map):
    """Return an exact one-variable jet/order-of-vanishing receipt.

    Coefficients are supplied in ascending order. The coordinate map must fix
    zero and have nonzero linear coefficient, so it is a valid formal/local
    diffeomorphism germ at zero for this bounded specimen.
    """
    if not isinstance(jet_order, int) or isinstance(jet_order, bool) or jet_order < 0:
        raise ValueError("jet_order must be a nonnegative integer")

    left = _trim(_polynomial(left_coefficients, "left polynomial"))
    right = _trim(_polynomial(right_coefficients, "right polynomial"))
    phi = _trim(_polynomial(coordinate_map, "coordinate map"))

    if phi[0] != 0:
        raise ValueError("coordinate map must fix zero")
    linear_term = phi[1] if len(phi) > 1 else Fraction(0)
    if linear_term == 0:
        raise ValueError("coordinate map must have nonzero linear term")

    left_order = _first_nonzero_order(left)
    right_order = _first_nonzero_order(right)
    if left_order is None or right_order is None:
        raise ValueError("zero polynomial has no finite first nonzero order in this kernel")

    left_transformed = _compose(left, phi)
    right_transformed = _compose(right, phi)
    left_transformed_order = _first_nonzero_order(left_transformed)
    right_transformed_order = _first_nonzero_order(right_transformed)

    left_leading_derivative = _derivative_at_zero(left, left_order)
    right_leading_derivative = _derivative_at_zero(right, right_order)
    left_transformed_leading_derivative = _derivative_at_zero(
        left_transformed, left_transformed_order
    )
    right_transformed_leading_derivative = _derivative_at_zero(
        right_transformed, right_transformed_order
    )

    left_jet = _jet(left, jet_order)
    right_jet = _jet(right, jet_order)

    return {
        "declared_jet_order": jet_order,
        "left_truncated_jet": left_jet,
        "right_truncated_jet": right_jet,
        "truncated_jets_equal": left_jet == right_jet,
        "left_first_nonzero_order": left_order,
        "right_first_nonzero_order": right_order,
        "left_first_nonzero_derivative": left_leading_derivative,
        "right_first_nonzero_derivative": right_leading_derivative,
        "coordinate_map": phi,
        "coordinate_linear_term": linear_term,
        "left_transformed_coefficients": left_transformed,
        "right_transformed_coefficients": right_transformed,
        "left_transformed_first_nonzero_order": left_transformed_order,
        "right_transformed_first_nonzero_order": right_transformed_order,
        "left_transformed_first_nonzero_derivative": left_transformed_leading_derivative,
        "right_transformed_first_nonzero_derivative": right_transformed_leading_derivative,
        "left_order_preserved": left_order == left_transformed_order,
        "right_order_preserved": right_order == right_transformed_order,
        "left_leading_derivative_scaling_closed": (
            left_transformed_leading_derivative
            == left_leading_derivative * linear_term ** left_order
        ),
        "right_leading_derivative_scaling_closed": (
            right_transformed_leading_derivative
            == right_leading_derivative * linear_term ** right_order
        ),
    }
