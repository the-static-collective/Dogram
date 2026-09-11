"""Bounded exact research kernel for COORDINATE-COVARIANCE-001.

This module is intentionally internal research surface. It does not promote a
public Dogram operator or attach semantic meaning to coordinate changes,
dual variables, or optimization geometry.
"""

from fractions import Fraction


def _fraction(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def _matrix(matrix):
    rows = tuple(tuple(_fraction(value) for value in row) for row in matrix)
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("coordinate map must be a non-empty square matrix")
    return rows


def _vector(vector, dimension, name):
    result = tuple(_fraction(value) for value in vector)
    if len(result) != dimension:
        raise ValueError(f"{name} dimension differs from coordinate map")
    return result


def _matvec(matrix, vector):
    return tuple(
        sum((entry * value for entry, value in zip(row, vector)), Fraction(0))
        for row in matrix
    )


def _row_times_matrix(row, matrix):
    dimension = len(matrix)
    return tuple(
        sum((row[k] * matrix[k][j] for k in range(dimension)), Fraction(0))
        for j in range(dimension)
    )


def _matmul(left, right):
    dimension = len(left)
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(dimension)), Fraction(0))
            for j in range(dimension)
        )
        for i in range(dimension)
    )


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def stationarity_residual(constraints, objective, multipliers):
    """Return exact A^T lambda - c for a declared inequality presentation."""
    objective = tuple(_fraction(value) for value in objective)
    dimension = len(objective)
    if not dimension:
        raise ValueError("objective must be non-empty")
    if len(constraints) != len(multipliers):
        raise ValueError("one multiplier is required per constraint")

    parsed_constraints = []
    for normal, bound in constraints:
        parsed_constraints.append(
            (_vector(normal, dimension, "constraint"), _fraction(bound))
        )
    parsed_multipliers = tuple(_fraction(value) for value in multipliers)

    return tuple(
        sum(
            (lam * normal[j] for lam, (normal, _) in zip(parsed_multipliers, parsed_constraints)),
            Fraction(0),
        )
        - objective[j]
        for j in range(dimension)
    )


def coordinate_change_receipt(constraints, objective, transform, inverse, base_point):
    """Replay one exact invertible coordinate change x = T z.

    Constraint rows and the objective are covectors, so their coordinates are
    pulled back by right multiplication with T. A primal point is carried to z
    coordinates by T^{-1}. The returned booleans are algebraic witnesses only.
    """
    transform = _matrix(transform)
    inverse = _matrix(inverse)
    dimension = len(transform)
    if len(inverse) != dimension:
        raise ValueError("inverse dimension differs from coordinate map")

    objective = _vector(objective, dimension, "objective")
    base_point = _vector(base_point, dimension, "base point")

    parsed_constraints = []
    for normal, bound in constraints:
        parsed_constraints.append(
            (_vector(normal, dimension, "constraint"), _fraction(bound))
        )
    parsed_constraints = tuple(parsed_constraints)

    identity = tuple(
        tuple(Fraction(int(i == j)) for j in range(dimension))
        for i in range(dimension)
    )
    inverse_witness = (
        _matmul(transform, inverse) == identity
        and _matmul(inverse, transform) == identity
    )
    if not inverse_witness:
        raise ValueError("declared inverse does not invert coordinate map")

    transformed_objective = _row_times_matrix(objective, transform)
    transformed_constraints = tuple(
        (_row_times_matrix(normal, transform), bound)
        for normal, bound in parsed_constraints
    )
    transformed_optimum = _matvec(inverse, base_point)
    replayed_base_optimum = _matvec(transform, transformed_optimum)

    return {
        "transformed_objective": transformed_objective,
        "transformed_constraints": transformed_constraints,
        "transformed_optimum": transformed_optimum,
        "replayed_base_optimum": replayed_base_optimum,
        "inverse_witness": inverse_witness,
        "base_objective_value": _dot(objective, base_point),
        "transformed_objective_value": _dot(
            transformed_objective, transformed_optimum
        ),
    }
