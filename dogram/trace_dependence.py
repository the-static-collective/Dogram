from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TraceInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class TracePairAnalysis:
    left: tuple[str, ...]
    right: tuple[str, ...]
    left_canonical: tuple[str, ...]
    right_canonical: tuple[str, ...]
    equivalent: bool

    def to_data(self) -> dict[str, object]:
        return {
            "left": list(self.left),
            "right": list(self.right),
            "left_canonical": list(self.left_canonical),
            "right_canonical": list(self.right_canonical),
            "equivalent": self.equivalent,
        }


def _validate_word(word: tuple[str, ...]) -> None:
    if not isinstance(word, tuple):
        raise TraceInputError("INVALID_WORD", "word must be a tuple of event labels")
    for label in word:
        if not isinstance(label, str) or not label:
            raise TraceInputError(
                "INVALID_LABEL", "event labels must be non-empty strings"
            )


def _validate_independence(
    independence: set[tuple[str, str]], labels: set[str]
) -> None:
    if not isinstance(independence, set):
        raise TraceInputError(
            "INVALID_INDEPENDENCE", "independence must be a set of label pairs"
        )

    for pair in independence:
        if (
            not isinstance(pair, tuple)
            or len(pair) != 2
            or not all(isinstance(label, str) and label for label in pair)
        ):
            raise TraceInputError(
                "INVALID_INDEPENDENCE", "independence entries must be label pairs"
            )
        left, right = pair
        if left == right:
            raise TraceInputError(
                "REFLEXIVE_INDEPENDENCE", "independence must be irreflexive"
            )
        if left not in labels or right not in labels:
            raise TraceInputError(
                "UNUSED_INDEPENDENCE_LABEL",
                "independence may mention only labels consumed by the analyzed word(s)",
            )
        if (right, left) not in independence:
            raise TraceInputError(
                "ASYMMETRIC_INDEPENDENCE", "independence must be symmetric"
            )


def _canonical_from_validated(
    word: tuple[str, ...], independence: set[tuple[str, str]]
) -> tuple[str, ...]:
    size = len(word)
    outgoing: list[list[int]] = [[] for _ in range(size)]
    indegree = [0] * size

    for source in range(size):
        for target in range(source + 1, size):
            left = word[source]
            right = word[target]
            dependent = left == right or (left, right) not in independence
            if dependent:
                outgoing[source].append(target)
                indegree[target] += 1

    available = {index for index, degree in enumerate(indegree) if degree == 0}
    canonical: list[str] = []

    while available:
        chosen = min(available, key=lambda index: (word[index], index))
        available.remove(chosen)
        canonical.append(word[chosen])
        for target in outgoing[chosen]:
            indegree[target] -= 1
            if indegree[target] == 0:
                available.add(target)

    if len(canonical) != size:
        raise AssertionError("dependence graph must be acyclic")
    return tuple(canonical)


def canonical_trace(
    word: tuple[str, ...], independence: set[tuple[str, str]]
) -> tuple[str, ...]:
    """Return a deterministic representative of a Mazurkiewicz trace class.

    The independence relation is declared input. Dogram does not infer independence
    from endpoints, labels, reachability, timestamps, or observed commutation.
    """

    _validate_word(word)
    _validate_independence(independence, set(word))
    return _canonical_from_validated(word, independence)


def analyze_trace_pair(
    left: tuple[str, ...],
    right: tuple[str, ...],
    independence: set[tuple[str, str]],
) -> TracePairAnalysis:
    """Compare two finite words modulo adjacent swaps of declared independent events."""

    _validate_word(left)
    _validate_word(right)
    labels = set(left) | set(right)
    _validate_independence(independence, labels)
    left_canonical = _canonical_from_validated(left, independence)
    right_canonical = _canonical_from_validated(right, independence)
    return TracePairAnalysis(
        left=left,
        right=right,
        left_canonical=left_canonical,
        right_canonical=right_canonical,
        equivalent=left_canonical == right_canonical,
    )


__all__ = [
    "TraceInputError",
    "TracePairAnalysis",
    "analyze_trace_pair",
    "canonical_trace",
]
