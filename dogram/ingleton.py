from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Mapping


@dataclass
class IngletonInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class IngletonAnalysis:
    left: int
    right: int
    slack: int
    violates: bool
    consumed_subsets: tuple[tuple[Hashable, ...], ...]

    def to_data(self) -> dict[str, object]:
        return {
            "left": self.left,
            "right": self.right,
            "slack": self.slack,
            "violates": self.violates,
            "consumed_subsets": [list(values) for values in self.consumed_subsets],
        }


def _stable_subset(values: frozenset[Hashable]) -> tuple[Hashable, ...]:
    return tuple(sorted(values, key=lambda value: (type(value).__name__, repr(value))))


def evaluate_ingleton(
    rank_table: Mapping[frozenset[Hashable], int],
    y1: frozenset[Hashable],
    y2: frozenset[Hashable],
    y3: frozenset[Hashable],
    y4: frozenset[Hashable],
) -> IngletonAnalysis:
    """Evaluate the Ingleton necessary condition on four declared subsets.

    A negative slack certifies failure of this necessary condition for linear
    representability. Nonnegative slack does not certify representability.
    This function does not validate the matroid rank axioms.
    """

    groups = (y1, y2, y3, y4)
    if not all(isinstance(group, frozenset) for group in groups):
        raise IngletonInputError("INVALID_SUBSET", "all Y groups must be frozensets")

    left_sets = (
        y1,
        y2,
        y1 | y2 | y3,
        y1 | y2 | y4,
        y3 | y4,
    )
    right_sets = (
        y1 | y2,
        y1 | y3,
        y1 | y4,
        y2 | y3,
        y2 | y4,
    )
    consumed = left_sets + right_sets

    values: list[int] = []
    for subset in consumed:
        if subset not in rank_table:
            raise IngletonInputError(
                "MISSING_RANK", f"missing rank for consumed subset {_stable_subset(subset)!r}"
            )
        rank = rank_table[subset]
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 0:
            raise IngletonInputError(
                "INVALID_RANK", f"rank must be a nonnegative integer for {_stable_subset(subset)!r}"
            )
        values.append(rank)

    left = sum(values[:5])
    right = sum(values[5:])
    slack = right - left
    return IngletonAnalysis(
        left=left,
        right=right,
        slack=slack,
        violates=slack < 0,
        consumed_subsets=tuple(_stable_subset(subset) for subset in consumed),
    )


__all__ = ["IngletonAnalysis", "IngletonInputError", "evaluate_ingleton"]
