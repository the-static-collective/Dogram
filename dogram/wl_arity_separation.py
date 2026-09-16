from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Iterable


Edge = tuple[int, int]
TupleVertex = tuple[int, ...]


@dataclass(frozen=True)
class WLArityReceipt:
    dimension: int
    left_initial_class_sizes: tuple[int, ...]
    right_initial_class_sizes: tuple[int, ...]
    left_one_round_class_sizes: tuple[int, ...]
    right_one_round_class_sizes: tuple[int, ...]
    left_stable_after_one_round: bool
    right_stable_after_one_round: bool
    distinguished_after_one_round: bool


def _normalize_edges(edges: Iterable[Edge]) -> tuple[int, frozenset[Edge]]:
    raw = tuple(edges)
    if not raw:
        raise ValueError("at least one edge is required")
    normalized: set[Edge] = set()
    maximum = -1
    for edge in raw:
        if len(edge) != 2:
            raise ValueError("each edge must have two endpoints")
        u, v = edge
        if not isinstance(u, int) or not isinstance(v, int) or u < 0 or v < 0 or u == v:
            raise ValueError("edges must join distinct nonnegative integer vertices")
        pair = (u, v) if u < v else (v, u)
        if pair in normalized:
            raise ValueError("duplicate undirected edge")
        normalized.add(pair)
        maximum = max(maximum, u, v)

    vertex_count = maximum + 1
    if vertex_count > 16:
        raise ValueError("bounded specimen supports at most 16 vertices")
    incident = {vertex for edge in normalized for vertex in edge}
    if incident != set(range(vertex_count)):
        raise ValueError("vertices must be consecutive and incident")
    return vertex_count, frozenset(normalized)


def _atomic_type(vertices: TupleVertex, edges: frozenset[Edge]) -> tuple[int, ...]:
    signature: list[int] = []
    for left in vertices:
        for right in vertices:
            if left == right:
                signature.append(0)
            elif (min(left, right), max(left, right)) in edges:
                signature.append(1)
            else:
                signature.append(2)
    return tuple(signature)


def _canonical_ids(signatures: list[object]) -> dict[object, int]:
    ordered = sorted(set(signatures), key=repr)
    return {signature: color for color, signature in enumerate(ordered)}


def _class_sizes(colors: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(Counter(colors).values()))


def _same_partition(old: tuple[int, ...], new: tuple[int, ...]) -> bool:
    old_to_new: dict[int, set[int]] = defaultdict(set)
    new_to_old: dict[int, set[int]] = defaultdict(set)
    for old_color, new_color in zip(old, new, strict=True):
        old_to_new[old_color].add(new_color)
        new_to_old[new_color].add(old_color)
    return all(len(values) == 1 for values in old_to_new.values()) and all(
        len(values) == 1 for values in new_to_old.values()
    )


def analyze_pair(
    left_edges: Iterable[Edge],
    right_edges: Iterable[Edge],
    *,
    dimension: int,
) -> WLArityReceipt:
    """Run one exact joint k-WL refinement round on a bounded graph pair.

    Colors are assigned jointly across the two carriers so color identifiers are
    directly comparable. The refinement uses the standard k-WL replacement
    signature: for each candidate vertex w, collect the vector of colors obtained
    by replacing each coordinate of the current k-tuple by w, then take the
    multiset of those vectors.
    """

    if dimension not in (2, 3):
        raise ValueError("dimension must be 2 or 3")

    left_n, left = _normalize_edges(left_edges)
    right_n, right = _normalize_edges(right_edges)
    if left_n != right_n:
        raise ValueError("graph pair must have the same vertex count")
    n = left_n

    tuples = tuple(product(range(n), repeat=dimension))
    index = {vertices: position for position, vertices in enumerate(tuples)}

    left_atomic = [_atomic_type(vertices, left) for vertices in tuples]
    right_atomic = [_atomic_type(vertices, right) for vertices in tuples]
    initial_ids = _canonical_ids(left_atomic + right_atomic)
    left_initial = tuple(initial_ids[signature] for signature in left_atomic)
    right_initial = tuple(initial_ids[signature] for signature in right_atomic)

    def refinement_signatures(colors: tuple[int, ...]) -> list[object]:
        signatures: list[object] = []
        for vertices in tuples:
            replacement_vectors = []
            for replacement in range(n):
                vector = []
                for coordinate in range(dimension):
                    changed = list(vertices)
                    changed[coordinate] = replacement
                    vector.append(colors[index[tuple(changed)]])
                replacement_vectors.append(tuple(vector))
            signatures.append(
                (
                    colors[index[vertices]],
                    tuple(sorted(replacement_vectors)),
                )
            )
        return signatures

    left_signatures = refinement_signatures(left_initial)
    right_signatures = refinement_signatures(right_initial)
    refined_ids = _canonical_ids(left_signatures + right_signatures)
    left_refined = tuple(refined_ids[signature] for signature in left_signatures)
    right_refined = tuple(refined_ids[signature] for signature in right_signatures)

    return WLArityReceipt(
        dimension=dimension,
        left_initial_class_sizes=_class_sizes(left_initial),
        right_initial_class_sizes=_class_sizes(right_initial),
        left_one_round_class_sizes=_class_sizes(left_refined),
        right_one_round_class_sizes=_class_sizes(right_refined),
        left_stable_after_one_round=_same_partition(left_initial, left_refined),
        right_stable_after_one_round=_same_partition(right_initial, right_refined),
        distinguished_after_one_round=Counter(left_refined) != Counter(right_refined),
    )
