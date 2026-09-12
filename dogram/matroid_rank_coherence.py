from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping


Subset = frozenset[str]


@dataclass(frozen=True)
class RankViolation:
    kind: str
    left: tuple[str, ...]
    right: tuple[str, ...] = ()
    intersection: tuple[str, ...] = ()
    union: tuple[str, ...] = ()
    residual: int = 0


@dataclass(frozen=True)
class MatroidRankAnalysis:
    ground_set: tuple[str, ...]
    is_matroid_rank: bool
    violations: tuple[RankViolation, ...]


def _subset_key(subset: Subset) -> tuple[int, tuple[str, ...]]:
    return (len(subset), tuple(sorted(subset)))


def _powerset(ground_set: tuple[str, ...]) -> tuple[Subset, ...]:
    items: list[Subset] = []
    for size in range(len(ground_set) + 1):
        for combo in combinations(ground_set, size):
            items.append(frozenset(combo))
    return tuple(items)


def analyze_rank_table(
    ground_set: tuple[str, ...], ranks: Mapping[Subset, int]
) -> MatroidRankAnalysis:
    """Check whether a complete finite set-function is a matroid rank function.

    This research kernel checks only the conventional finite rank axioms. It does
    not infer that the supplied ground elements encode causal, statistical,
    historical, semantic, or evidentiary independence.
    """

    if len(set(ground_set)) != len(ground_set):
        raise ValueError("ground_set labels must be unique")
    if any(not isinstance(label, str) for label in ground_set):
        raise ValueError("ground_set labels must be strings")

    expected = set(_powerset(ground_set))
    supplied = set(ranks)
    if supplied != expected:
        missing = sorted(expected - supplied, key=_subset_key)
        extra = sorted(supplied - expected, key=_subset_key)
        raise ValueError(f"rank table must be complete; missing={missing!r} extra={extra!r}")

    for subset, value in ranks.items():
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"rank for {sorted(subset)!r} must be an integer")

    subsets = sorted(expected, key=_subset_key)
    violations: list[RankViolation] = []

    empty = frozenset()
    if ranks[empty] != 0:
        violations.append(
            RankViolation(
                kind="NORMALIZATION",
                left=(),
                residual=abs(ranks[empty]),
            )
        )

    for subset in subsets:
        value = ranks[subset]
        if value < 0 or value > len(subset):
            residual = -value if value < 0 else value - len(subset)
            violations.append(
                RankViolation(
                    kind="SUBCARDINALITY",
                    left=tuple(sorted(subset)),
                    residual=residual,
                )
            )

    for left in subsets:
        for right in subsets:
            if left < right and ranks[left] > ranks[right]:
                violations.append(
                    RankViolation(
                        kind="MONOTONICITY",
                        left=tuple(sorted(left)),
                        right=tuple(sorted(right)),
                        residual=ranks[left] - ranks[right],
                    )
                )

    for i, left in enumerate(subsets):
        for right in subsets[i + 1 :]:
            intersection = left & right
            union = left | right
            lhs = ranks[left] + ranks[right]
            rhs = ranks[intersection] + ranks[union]
            if lhs < rhs:
                violations.append(
                    RankViolation(
                        kind="SUBMODULARITY",
                        left=tuple(sorted(left)),
                        right=tuple(sorted(right)),
                        intersection=tuple(sorted(intersection)),
                        union=tuple(sorted(union)),
                        residual=rhs - lhs,
                    )
                )

    violations.sort(
        key=lambda v: (
            v.kind,
            len(v.left),
            v.left,
            len(v.right),
            v.right,
            v.intersection,
            v.union,
            v.residual,
        )
    )
    return MatroidRankAnalysis(
        ground_set=ground_set,
        is_matroid_rank=not violations,
        violations=tuple(violations),
    )


__all__ = ["MatroidRankAnalysis", "RankViolation", "analyze_rank_table"]
