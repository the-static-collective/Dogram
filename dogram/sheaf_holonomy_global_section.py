from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


Matrix = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class SheafHolonomyGlobalSectionReceipt:
    transports: tuple[int, int, int]
    transport_product: int
    constraint_matrix: Matrix
    constraint_rank: int
    global_section_dimension: int
    laplacian: Matrix
    laplacian_charpoly: tuple[int, ...]
    laplacian_determinant: int


def _rank(matrix: Matrix) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][col]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                work[row][j] - factor * work[rank][j]
                for j in range(cols)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[row][col] for row in range(len(matrix))) for col in range(len(matrix[0])))


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def _charpoly_3x3(matrix: Matrix) -> tuple[int, int, int, int]:
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("bounded specimen requires a 3x3 matrix")
    trace = sum(matrix[i][i] for i in range(3))
    square = _matmul(matrix, matrix)
    trace_square = sum(square[i][i] for i in range(3))
    second = (trace * trace - trace_square) // 2
    determinant = (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )
    return (1, -trace, second, -determinant)


def analyze_rank_one_triangle(transports: tuple[int, int, int]) -> SheafHolonomyGlobalSectionReceipt:
    """Analyze a rank-one signed transport sheaf on the oriented triangle 0->1->2->0.

    Each vertex and edge stalk is one-dimensional.  The edge equations are
    x1=t01*x0, x2=t12*x1, x0=t20*x2.  This bounded research kernel records
    linear compatibility only; it assigns no evidential, causal, or semantic
    meaning to a section or obstruction.
    """
    if len(transports) != 3 or any(value not in (-1, 1) for value in transports):
        raise ValueError("transports must be exactly three signs in {-1, +1}")

    t01, t12, t20 = transports
    constraint: Matrix = (
        (-t01, 1, 0),
        (0, -t12, 1),
        (1, 0, -t20),
    )
    rank = _rank(constraint)
    laplacian = _matmul(_transpose(constraint), constraint)
    charpoly = _charpoly_3x3(laplacian)

    return SheafHolonomyGlobalSectionReceipt(
        transports=transports,
        transport_product=t01 * t12 * t20,
        constraint_matrix=constraint,
        constraint_rank=rank,
        global_section_dimension=3 - rank,
        laplacian=laplacian,
        laplacian_charpoly=charpoly,
        laplacian_determinant=-charpoly[-1],
    )
