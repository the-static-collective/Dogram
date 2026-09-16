from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


Edge = tuple[int, int]
Matrix = tuple[tuple[int, ...], ...]

BASE_EDGES: tuple[Edge, ...] = (
    (0, 1), (0, 4), (0, 5), (1, 4), (1, 5),
    (2, 4), (2, 5), (3, 4), (3, 5), (4, 5),
)

SIGNING_A = {edge: 1 for edge in BASE_EDGES}
SIGNING_A[(2, 5)] = -1
SIGNING_A[(3, 5)] = -1

SIGNING_B = {edge: 1 for edge in BASE_EDGES}
SIGNING_B[(2, 5)] = -1
SIGNING_B[(3, 5)] = -1
SIGNING_B[(4, 5)] = -1


@dataclass(frozen=True)
class SheafCospectralGluingReceipt:
    laplacian_a: Matrix
    laplacian_b: Matrix
    charpoly_a: tuple[int, ...]
    charpoly_b: tuple[int, ...]
    determinant_a: int
    determinant_b: int
    h0_dimension_a: int
    h0_dimension_b: int
    negative_triangle_degree_profiles_a: tuple[tuple[int, int, int], ...]
    negative_triangle_degree_profiles_b: tuple[tuple[int, int, int], ...]


def _degrees() -> tuple[int, ...]:
    out = [0] * 6
    for u, v in BASE_EDGES:
        out[u] += 1
        out[v] += 1
    return tuple(out)


def _signed_laplacian(signing: dict[Edge, int]) -> Matrix:
    degrees = _degrees()
    rows = [[0] * 6 for _ in range(6)]
    for i, degree in enumerate(degrees):
        rows[i][i] = degree
    for u, v in BASE_EDGES:
        sign = signing[(u, v)]
        rows[u][v] = -sign
        rows[v][u] = -sign
    return tuple(tuple(row) for row in rows)


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    n = len(left)
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def _trace(matrix: Matrix) -> int:
    return sum(matrix[i][i] for i in range(len(matrix)))


def _charpoly_via_newton(matrix: Matrix) -> tuple[int, ...]:
    """Return monic characteristic-polynomial coefficients using exact Newton identities."""
    n = len(matrix)
    powers: list[Matrix] = [matrix]
    for _ in range(2, n + 1):
        powers.append(_matmul(powers[-1], matrix))
    traces = [0] + [_trace(power) for power in powers]
    coeffs = [1]
    for k in range(1, n + 1):
        numerator = sum(coeffs[k - i] * traces[i] for i in range(1, k + 1))
        if numerator % k:
            raise ArithmeticError("Newton identity failed to remain integral")
        coeffs.append(-numerator // k)
    return tuple(coeffs)


def _rank(matrix: Matrix) -> int:
    from fractions import Fraction

    work = [[Fraction(x) for x in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pv = work[rank][col]
        work[rank] = [x / pv for x in work[rank]]
        for r in range(rows):
            if r == rank or not work[r][col]:
                continue
            factor = work[r][col]
            work[r] = [work[r][j] - factor * work[rank][j] for j in range(cols)]
        rank += 1
    return rank


def _negative_triangle_degree_profiles(signing: dict[Edge, int]) -> tuple[tuple[int, int, int], ...]:
    edge_set = set(BASE_EDGES)
    degrees = _degrees()
    profiles: list[tuple[int, int, int]] = []
    for a, b, c in combinations(range(6), 3):
        tri = ((a, b), (a, c), (b, c))
        if not all(edge in edge_set for edge in tri):
            continue
        sign = signing[(a, b)] * signing[(a, c)] * signing[(b, c)]
        if sign == -1:
            profiles.append(tuple(sorted((degrees[a], degrees[b], degrees[c]))))
    return tuple(sorted(profiles))


def analyze_sheaf_cospectral_gluing() -> SheafCospectralGluingReceipt:
    """Exact bounded rank-one signed-gluing comparison on one fixed base graph.

    Signed Laplacian cospectrality is treated only as a mathematical quotient.
    It is not occurrence, evidence, identity, causation, or semantic agreement.
    """
    lap_a = _signed_laplacian(SIGNING_A)
    lap_b = _signed_laplacian(SIGNING_B)
    cp_a = _charpoly_via_newton(lap_a)
    cp_b = _charpoly_via_newton(lap_b)
    rank_a = _rank(lap_a)
    rank_b = _rank(lap_b)
    return SheafCospectralGluingReceipt(
        laplacian_a=lap_a,
        laplacian_b=lap_b,
        charpoly_a=cp_a,
        charpoly_b=cp_b,
        determinant_a=cp_a[-1],
        determinant_b=cp_b[-1],
        h0_dimension_a=6 - rank_a,
        h0_dimension_b=6 - rank_b,
        negative_triangle_degree_profiles_a=_negative_triangle_degree_profiles(SIGNING_A),
        negative_triangle_degree_profiles_b=_negative_triangle_degree_profiles(SIGNING_B),
    )
