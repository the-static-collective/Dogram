from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Mapping, Sequence


@dataclass
class VectorMatroidInputError(ValueError):
    residual: str

    def __str__(self) -> str:
        return self.residual


def _matrix_rank(columns: Sequence[Sequence[int]]) -> int:
    if not columns:
        return 0

    rows = [
        [Fraction(columns[column][row]) for column in range(len(columns))]
        for row in range(len(columns[0]))
    ]
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    pivot_column = 0

    while rank < row_count and pivot_column < column_count:
        pivot = next(
            (row for row in range(rank, row_count) if rows[row][pivot_column] != 0),
            None,
        )
        if pivot is None:
            pivot_column += 1
            continue

        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][pivot_column]
        rows[rank] = [value / pivot_value for value in rows[rank]]

        for row in range(row_count):
            if row == rank:
                continue
            factor = rows[row][pivot_column]
            if factor == 0:
                continue
            rows[row] = [
                current - factor * pivot_entry
                for current, pivot_entry in zip(rows[row], rows[rank], strict=True)
            ]

        rank += 1
        pivot_column += 1

    return rank


@dataclass(frozen=True)
class VectorMatroidAnalysis:
    _vectors: tuple[tuple[str, tuple[int, ...]], ...]
    ambient_dimension: int
    circuits: tuple[tuple[str, ...], ...]

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(label for label, _ in self._vectors)

    def _selected_columns(self, labels: Sequence[str]) -> tuple[tuple[int, ...], ...]:
        requested = tuple(labels)
        if len(set(requested)) != len(requested):
            raise VectorMatroidInputError("rank labels must form a set without duplicates")

        by_label = dict(self._vectors)
        unknown = [label for label in requested if label not in by_label]
        if unknown:
            raise VectorMatroidInputError(f"unknown labels: {unknown}")
        return tuple(by_label[label] for label in requested)

    def rank(self, labels: Sequence[str]) -> int:
        return _matrix_rank(self._selected_columns(labels))

    def rank_defect(self, labels: Sequence[str]) -> int:
        requested = tuple(labels)
        return len(requested) - self.rank(requested)

    @property
    def full_rank(self) -> int:
        return self.rank(self.labels)

    @property
    def full_rank_defect(self) -> int:
        return len(self.labels) - self.full_rank

    def to_data(self) -> dict[str, object]:
        return {
            "ambient_dimension": self.ambient_dimension,
            "labels": list(self.labels),
            "full_rank": self.full_rank,
            "full_rank_defect": self.full_rank_defect,
            "circuits": [list(circuit) for circuit in self.circuits],
        }


def analyze_vector_matroid(
    vectors: Mapping[str, Sequence[int]],
) -> VectorMatroidAnalysis:
    """Analyze exact finite vector-matroid rank/circuit structure over Q.

    This research floor is intentionally loopless: zero vectors are refused rather
    than silently admitted as one-element circuits.
    """

    if not vectors:
        raise VectorMatroidInputError("at least one labeled vector is required")

    ordered = tuple(sorted(vectors.items()))
    ambient_dimension = len(ordered[0][1])
    if ambient_dimension == 0:
        raise VectorMatroidInputError("vectors must have positive dimension")

    normalized: list[tuple[str, tuple[int, ...]]] = []
    for label, vector in ordered:
        if not isinstance(label, str) or not label:
            raise VectorMatroidInputError("labels must be non-empty strings")
        if len(vector) != ambient_dimension:
            raise VectorMatroidInputError("all vectors must have the same dimension")

        coordinates = tuple(vector)
        if any(not isinstance(value, int) or isinstance(value, bool) for value in coordinates):
            raise VectorMatroidInputError("coordinates must be integers")
        if all(value == 0 for value in coordinates):
            raise VectorMatroidInputError("zero vectors are outside the loopless research floor")
        normalized.append((label, coordinates))

    frozen_vectors = tuple(normalized)
    labels = tuple(label for label, _ in frozen_vectors)
    by_label = dict(frozen_vectors)
    circuits: list[tuple[str, ...]] = []

    for size in range(2, len(labels) + 1):
        for subset in combinations(labels, size):
            columns = tuple(by_label[label] for label in subset)
            if _matrix_rank(columns) == size:
                continue
            if any(set(circuit).issubset(subset) for circuit in circuits):
                continue
            circuits.append(subset)

    return VectorMatroidAnalysis(
        _vectors=frozen_vectors,
        ambient_dimension=ambient_dimension,
        circuits=tuple(circuits),
    )


__all__ = [
    "VectorMatroidAnalysis",
    "VectorMatroidInputError",
    "analyze_vector_matroid",
]
