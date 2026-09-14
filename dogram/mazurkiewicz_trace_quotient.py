"""Bounded Mazurkiewicz-trace quotient research kernel.

This module intentionally stays below Dogram's public operator floor.  It computes
only a finite word-equivalence receipt under a declared symmetric independence
relation.  Trace equivalence is not treated as occurrence, causation, evidence,
or semantic identity.
"""

from collections import Counter, deque
from typing import FrozenSet, Iterable, Tuple


Pair = Tuple[str, str]
Independence = FrozenSet[Pair]


def frozen_specimen():
    """Return the two-letter hostile control used by the research slice."""
    return {
        "alphabet": ("a", "b"),
        "words": ("ab", "ba"),
        "parallel_independence": frozenset({("a", "b"), ("b", "a")}),
        "ordered_independence": frozenset(),
    }


def parikh_vector(word: str):
    """Return an exact order-insensitive event-count receipt."""
    counts = Counter(word)
    return tuple(sorted(counts.items()))


def _one_swap_neighbors(word: str, independence: Independence):
    for i in range(len(word) - 1):
        left, right = word[i], word[i + 1]
        if (left, right) in independence:
            yield word[:i] + right + left + word[i + 2 :]


def trace_class(word: str, independence: Independence):
    """Enumerate the finite trace class reachable by adjacent independent swaps."""
    seen = {word}
    queue = deque([word])
    while queue:
        current = queue.popleft()
        for neighbor in _one_swap_neighbors(current, independence):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return frozenset(seen)


def trace_partition(words: Iterable[str], independence: Independence):
    """Partition a declared finite language by Mazurkiewicz trace equivalence."""
    remaining = set(words)
    classes = []
    while remaining:
        seed = min(remaining)
        cls = trace_class(seed, independence) & remaining
        classes.append(frozenset(cls))
        remaining -= cls
    return tuple(sorted(classes, key=lambda cls: tuple(sorted(cls))))
