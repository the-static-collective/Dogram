from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


@dataclass(frozen=True)
class OrientationSignature:
    labels: tuple[str, ...]
    rank: int
    nonzero_bases: tuple[tuple[str, ...], ...]
    determinants: tuple[Fraction, ...]
    signs: tuple[int, ...]


def _determinant(matrix: list[list[Fraction]]) -> Fraction:
    n = len(matrix)
    work = [row[:] for row in matrix]
    determinant = Fraction(1)

    for column in range(n):
        pivot = next(
            (row for row in range(column, n) if work[row][column] != 0), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant *= -1

        pivot_value = work[column][column]
        determinant *= pivot_value
        for index in range(column, n):
            work[column][index] /= pivot_value

        for row in range(column + 1, n):
            factor = work[row][column]
            if factor == 0:
                continue
            for index in range(column, n):
                work[row][index] -= factor * work[column][index]

    return determinant


def analyze_orientation_signature(
    vectors: dict[str, tuple[int, ...]], rank: int
) -> OrientationSignature:
    """Return exact determinant signs for all nonzero rank-sized bases.

    This is a bounded realizable-oriented-matroid research kernel. It reports the
    sign layer supplied by a declared rational vector realization. It does not
    infer geometry, causality, evidence, truth, or meaning from that layer.
    """

    if not isinstance(rank, int) or isinstance(rank, bool) or rank <= 0:
        raise ValueError("rank must be a positive integer")

    labels = tuple(sorted(vectors))
    if len(labels) < rank:
        raise ValueError("need at least rank vectors")

    widths = {len(vectors[label]) for label in labels}
    if widths != {rank}:
        raise ValueError("each vector must have exactly rank coordinates")

    bases: list[tuple[str, ...]] = []
    determinants: list[Fraction] = []
    signs: list[int] = []

    for basis in combinations(labels, rank):
        matrix = [
            [Fraction(vectors[label][row]) for label in basis]
            for row in range(rank)
        ]
        determinant = _determinant(matrix)
        if determinant == 0:
            continue
        bases.append(basis)
        determinants.append(determinant)
        signs.append(1 if determinant > 0 else -1)

    return OrientationSignature(
        labels=labels,
        rank=rank,
        nonzero_bases=tuple(bases),
        determinants=tuple(determinants),
        signs=tuple(signs),
    )


__all__ = ["OrientationSignature", "analyze_orientation_signature"]
