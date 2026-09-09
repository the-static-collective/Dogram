"""Bounded exact research kernel for CRITICAL-HESSIAN-INERTIA-001.

This module is internal research surface. It checks a two-dimensional Hessian
change-of-coordinates specimen with exact rational arithmetic. It does not
promote a public Dogram operator or infer occurrence, evidence, causation, or
semantic importance from critical-point type.
"""

from fractions import Fraction


def _fraction(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def _vector2(values, name):
    result = tuple(_fraction(value) for value in values)
    if len(result) != 2:
        raise ValueError(f"{name} must have exactly two entries")
    return result


def _matrix2(values, name, *, symmetric=False):
    rows = tuple(tuple(_fraction(value) for value in row) for row in values)
    if len(rows) != 2 or any(len(row) != 2 for row in rows):
        raise ValueError(f"{name} must be a 2x2 matrix")
    if symmetric and rows[0][1] != rows[1][0]:
        raise ValueError(f"{name} must be symmetric")
    return rows


def _transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(2)) for i in range(2))


def _matmul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def _add(left, right):
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(2))
        for i in range(2)
    )


def _scale(scalar, matrix):
    return tuple(tuple(scalar * matrix[i][j] for j in range(2)) for i in range(2))


def _determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def _trace(matrix):
    return matrix[0][0] + matrix[1][1]


def _characteristic_coefficients(matrix):
    return (Fraction(1), -_trace(matrix), _determinant(matrix))


def _inertia_2x2_symmetric(matrix):
    """Return (positive, negative, zero) using exact 2x2 invariants."""
    determinant = _determinant(matrix)
    trace = _trace(matrix)

    if determinant < 0:
        return (1, 1, 0)
    if determinant > 0:
        if trace > 0:
            return (2, 0, 0)
        if trace < 0:
            return (0, 2, 0)
        raise ValueError("nonzero determinant with zero trace is impossible for real symmetric 2x2")

    if matrix == ((0, 0), (0, 0)):
        return (0, 0, 2)
    if trace > 0:
        return (1, 0, 1)
    if trace < 0:
        return (0, 1, 1)
    raise ValueError("rank-one real symmetric 2x2 matrix cannot have zero trace")


def critical_hessian_receipt(base_hessian, base_gradient, jacobian, component_hessians):
    """Return an exact 2D second-order coordinate-change receipt.

    For x = phi(z), the raw coordinate Hessian satisfies

        H_z(f o phi) = J^T H_x(f) J + sum_a (partial_a f) H_z(phi_a).

    At a critical point the gradient-weighted correction vanishes, leaving an
    invertible congruence when ``J`` is nonsingular. Sylvester inertia is then
    preserved even though matrix entries, determinant, and eigenvalues need not
    be preserved.
    """
    hessian = _matrix2(base_hessian, "base Hessian", symmetric=True)
    gradient = _vector2(base_gradient, "base gradient")
    transform = _matrix2(jacobian, "Jacobian")
    map_hessians = tuple(
        _matrix2(matrix, f"component Hessian {index}", symmetric=True)
        for index, matrix in enumerate(component_hessians)
    )
    if len(map_hessians) != 2:
        raise ValueError("component_hessians must contain exactly two 2x2 matrices")

    jacobian_determinant = _determinant(transform)
    if jacobian_determinant == 0:
        raise ValueError("Jacobian must be invertible")

    pullback = _matmul(_transpose(transform), _matmul(hessian, transform))
    correction = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    for gradient_component, map_hessian in zip(gradient, map_hessians):
        correction = _add(correction, _scale(gradient_component, map_hessian))
    transformed = _add(pullback, correction)

    base_inertia = _inertia_2x2_symmetric(hessian)
    transformed_inertia = _inertia_2x2_symmetric(transformed)
    critical_point = all(component == 0 for component in gradient)

    return {
        "critical_point": critical_point,
        "base_hessian": hessian,
        "jacobian": transform,
        "jacobian_determinant": jacobian_determinant,
        "congruence_pullback": pullback,
        "second_order_correction": correction,
        "transformed_hessian": transformed,
        "base_characteristic_coefficients": _characteristic_coefficients(hessian),
        "transformed_characteristic_coefficients": _characteristic_coefficients(transformed),
        "base_determinant": _determinant(hessian),
        "transformed_determinant": _determinant(transformed),
        "base_inertia": base_inertia,
        "transformed_inertia": transformed_inertia,
        "base_morse_index": base_inertia[1],
        "transformed_morse_index": transformed_inertia[1],
        "critical_congruence_closed": critical_point and transformed == pullback,
    }
