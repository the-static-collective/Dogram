"""Bounded Foata-normal-form profile collision research kernel.

This stays below Dogram's public operator floor. It computes exact finite
Mazurkiewicz trace classes and occurrence-dependence layers under a declared
symmetric independence relation. Normalization is not occurrence, evidence,
causation, or semantic identity.
"""

from collections import Counter, deque


def frozen_specimen():
    """Return the four-event hostile specimen."""
    independence = frozenset({("a", "b"), ("b", "a")})
    return {
        "alphabet": ("a", "b", "c", "d"),
        "independence": independence,
        "left_word": "abcd",
        "right_word": "abdc",
    }


def parikh_vector(word):
    return tuple(sorted(Counter(word).items()))


def trace_class(word, independence):
    """Enumerate words reachable by adjacent independent swaps."""
    seen = {word}
    queue = deque([word])
    while queue:
        current = queue.popleft()
        for i in range(len(current) - 1):
            if (current[i], current[i + 1]) not in independence:
                continue
            neighbor = current[:i] + current[i + 1] + current[i] + current[i + 2 :]
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return frozenset(seen)


def dependence_edges(word, independence):
    """Return ordered occurrence dependencies induced by the word."""
    edges = set()
    for i in range(len(word)):
        for j in range(i + 1, len(word)):
            if word[i] == word[j] or (word[i], word[j]) not in independence:
                edges.add((i, j))
    return frozenset(edges)


def foata_layers(word, independence):
    """Greedily peel minimal occurrences from the dependence poset."""
    edges = dependence_edges(word, independence)
    remaining = set(range(len(word)))
    layers = []
    while remaining:
        minimal = tuple(
            i for i in sorted(remaining)
            if not any((j, i) in edges for j in remaining)
        )
        layers.append(tuple(word[i] for i in minimal))
        remaining.difference_update(minimal)
    return tuple(layers)


def layer_size_profile(word, independence):
    return tuple(len(layer) for layer in foata_layers(word, independence))
