from __future__ import annotations

from itertools import combinations


def hamming(left: str, right: str) -> int:
    if len(left) != len(right):
        raise ValueError("signatures must have equal length")
    return sum(a != b for a, b in zip(left, right))


def minimum_distance(signatures: tuple[str, ...]) -> int:
    return min(hamming(a, b) for a, b in combinations(signatures, 2))


def survives_erasure(signatures: tuple[str, ...], erased: frozenset[int]) -> bool:
    projected = {
        tuple(bit for index, bit in enumerate(signature) if index not in erased)
        for signature in signatures
    }
    return len(projected) == len(signatures)


def collapsed_pairs(signatures: tuple[str, ...], erased: frozenset[int]) -> tuple[tuple[int, int], ...]:
    collisions = []
    for i, j in combinations(range(len(signatures)), 2):
        remaining = [k for k in range(len(signatures[i])) if k not in erased]
        if all(signatures[i][k] == signatures[j][k] for k in remaining):
            collisions.append((i, j))
    return tuple(collisions)


def specimen() -> dict[str, object]:
    resilient = ("0000", "0011", "0101", "0110")
    fragile = ("0000", "0011", "0101", "1001")
    declared_failure = frozenset({0, 1})
    alternate_same_cardinality_failure = frozenset({2, 3})
    return {
        "resilient": resilient,
        "fragile": fragile,
        "minimum_distance": {
            "resilient": minimum_distance(resilient),
            "fragile": minimum_distance(fragile),
        },
        "declared_failure": sorted(declared_failure),
        "survives_declared_failure": {
            "resilient": survives_erasure(resilient, declared_failure),
            "fragile": survives_erasure(fragile, declared_failure),
        },
        "fragile_collisions": collapsed_pairs(fragile, declared_failure),
        "alternate_same_cardinality_failure": sorted(alternate_same_cardinality_failure),
        "resilient_collisions_after_alternate_failure": collapsed_pairs(
            resilient, alternate_same_cardinality_failure
        ),
    }
