from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import Iterable


Edge = tuple[int, int]


@dataclass(frozen=True)
class WLComparisonReceipt:
    dimension: int
    distinguished: bool
    first_distinguishing_round: int | None
    stable_round: int | None
    rounds_run: int
    left_color_class_sizes: tuple[int, ...]
    right_color_class_sizes: tuple[int, ...]


def _adjacency(edges: Iterable[Edge]) -> list[list[bool]]:
    raw = tuple(edges)
    vertices = sorted({vertex for edge in raw for vertex in edge})
    if vertices != list(range(16)):
        raise ValueError("bounded specimen requires exactly vertices 0..15")

    adjacency = [[False] * 16 for _ in range(16)]
    seen: set[Edge] = set()
    for edge in raw:
        if len(edge) != 2:
            raise ValueError("each edge must have two endpoints")
        u, v = edge
        if not isinstance(u, int) or not isinstance(v, int) or u == v:
            raise ValueError("edges must join distinct integer vertices")
        pair = (u, v) if u < v else (v, u)
        if pair in seen:
            raise ValueError("duplicate undirected edge")
        seen.add(pair)
        adjacency[u][v] = True
        adjacency[v][u] = True
    return adjacency


def _class_sizes(colors: list[int]) -> tuple[int, ...]:
    return tuple(sorted(Counter(colors).values()))


def compare_graphs_wl(
    left_edges: Iterable[Edge],
    right_edges: Iterable[Edge],
    *,
    dimension: int,
) -> WLComparisonReceipt:
    if dimension not in (3, 4):
        raise ValueError("bounded specimen supports only dimensions 3 and 4")

    left = _adjacency(left_edges)
    right = _adjacency(right_edges)
    n = 16
    k = dimension
    tuples = list(product(range(n), repeat=k))

    def atomic_type(adjacency: list[list[bool]], item: tuple[int, ...]) -> tuple[int, ...]:
        signature: list[int] = []
        for i in range(k):
            for j in range(i + 1, k):
                if item[i] == item[j]:
                    signature.append(0)
                elif adjacency[item[i]][item[j]]:
                    signature.append(1)
                else:
                    signature.append(2)
        return tuple(signature)

    def assign_colors(
        left_signatures: list[object], right_signatures: list[object]
    ) -> tuple[list[int], list[int], int]:
        signatures = sorted(set(left_signatures + right_signatures), key=repr)
        color_of = {signature: color for color, signature in enumerate(signatures)}
        return (
            [color_of[signature] for signature in left_signatures],
            [color_of[signature] for signature in right_signatures],
            len(signatures),
        )

    left_colors, right_colors, color_count = assign_colors(
        [atomic_type(left, item) for item in tuples],
        [atomic_type(right, item) for item in tuples],
    )

    left_sizes = _class_sizes(left_colors)
    right_sizes = _class_sizes(right_colors)
    if left_sizes != right_sizes:
        return WLComparisonReceipt(
            dimension=k,
            distinguished=True,
            first_distinguishing_round=0,
            stable_round=None,
            rounds_run=0,
            left_color_class_sizes=left_sizes,
            right_color_class_sizes=right_sizes,
        )

    powers = [n ** (k - 1 - position) for position in range(k)]

    def refine(colors: list[int]) -> list[object]:
        refined: list[object] = []
        for tuple_index, item in enumerate(tuples):
            coordinate_multisets: list[tuple[int, ...]] = []
            for position in range(k):
                base = tuple_index - item[position] * powers[position]
                replacement_colors = [
                    colors[base + vertex * powers[position]] for vertex in range(n)
                ]
                coordinate_multisets.append(tuple(sorted(replacement_colors)))
            refined.append((colors[tuple_index], tuple(coordinate_multisets)))
        return refined

    previous_color_count = color_count
    for round_index in range(1, 17):
        left_colors, right_colors, color_count = assign_colors(
            refine(left_colors), refine(right_colors)
        )
        left_sizes = _class_sizes(left_colors)
        right_sizes = _class_sizes(right_colors)
        if left_sizes != right_sizes:
            return WLComparisonReceipt(
                dimension=k,
                distinguished=True,
                first_distinguishing_round=round_index,
                stable_round=None,
                rounds_run=round_index,
                left_color_class_sizes=left_sizes,
                right_color_class_sizes=right_sizes,
            )
        if color_count == previous_color_count:
            return WLComparisonReceipt(
                dimension=k,
                distinguished=False,
                first_distinguishing_round=None,
                stable_round=round_index,
                rounds_run=round_index,
                left_color_class_sizes=left_sizes,
                right_color_class_sizes=right_sizes,
            )
        previous_color_count = color_count

    raise RuntimeError("bounded refinement did not stabilize within 16 rounds")
