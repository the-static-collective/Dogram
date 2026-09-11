from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable


Edge = tuple[int, int]
SpectrumEntry = tuple[int, int]
JointDegreeCount = tuple[int, int, int]


@dataclass(frozen=True)
class StronglyRegularCliqueCollisionReceipt:
    degree_sequence: tuple[int, ...]
    joint_degree_counts: tuple[JointDegreeCount, ...]
    laplacian_spectrum: tuple[SpectrumEntry, ...]
    triangle_count: int
    k4_count: int
    clique_number: int


def _matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def _charpoly(matrix: list[list[int]]) -> tuple[int, ...]:
    n = len(matrix)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    b = identity
    coeffs = [1]
    for k in range(1, n + 1):
        ab = _matmul(matrix, b)
        trace = sum(ab[i][i] for i in range(n))
        if trace % k:
            raise ArithmeticError("exact characteristic-polynomial division failed")
        coefficient = -(trace // k)
        coeffs.append(coefficient)
        b = [
            [ab[i][j] + (coefficient if i == j else 0) for j in range(n)]
            for i in range(n)
        ]
    return tuple(coeffs)


def _synthetic_divide(coeffs: tuple[int, ...], root: int) -> tuple[tuple[int, ...], int]:
    out = [coeffs[0]]
    for coefficient in coeffs[1:]:
        out.append(coefficient + root * out[-1])
    return tuple(out[:-1]), out[-1]


def _integer_spectrum(coeffs: tuple[int, ...], n: int) -> tuple[SpectrumEntry, ...]:
    remaining = coeffs
    entries: list[SpectrumEntry] = []
    for root in range(n + 1):
        multiplicity = 0
        while len(remaining) > 1:
            quotient, remainder = _synthetic_divide(remaining, root)
            if remainder != 0:
                break
            remaining = quotient
            multiplicity += 1
        if multiplicity:
            entries.append((root, multiplicity))
    if len(remaining) != 1:
        raise ValueError("bounded specimen requires an integral Laplacian spectrum")
    return tuple(entries)


def _normalize_edges(edges: Iterable[Edge]) -> tuple[tuple[int, ...], tuple[Edge, ...], dict[int, set[int]]]:
    raw = tuple(edges)
    if not raw:
        raise ValueError("at least one edge is required")
    normalized: set[Edge] = set()
    max_vertex = -1
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
        max_vertex = max(max_vertex, u, v)

    nodes = tuple(range(max_vertex + 1))
    if len(nodes) > 16:
        raise ValueError("bounded specimen supports at most 16 vertices")
    if set(vertex for edge in normalized for vertex in edge) != set(nodes):
        raise ValueError("vertices must be consecutive and incident")

    ordered = tuple(sorted(normalized))
    adjacency = {node: set() for node in nodes}
    for u, v in ordered:
        adjacency[u].add(v)
        adjacency[v].add(u)

    seen = {nodes[0]}
    stack = [nodes[0]]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    if len(seen) != len(nodes):
        raise ValueError("graph must be connected")
    return nodes, ordered, adjacency


def _is_clique(vertices: tuple[int, ...], adjacency: dict[int, set[int]]) -> bool:
    return all(v in adjacency[u] for u, v in combinations(vertices, 2))


def analyze_graph(edges: Iterable[Edge]) -> StronglyRegularCliqueCollisionReceipt:
    nodes, ordered_edges, adjacency = _normalize_edges(edges)
    degrees = {node: len(adjacency[node]) for node in nodes}

    laplacian = [[0 for _ in nodes] for _ in nodes]
    for node in nodes:
        laplacian[node][node] = degrees[node]
    for u, v in ordered_edges:
        laplacian[u][v] = -1
        laplacian[v][u] = -1

    incidence = Counter(
        (max(degrees[u], degrees[v]), min(degrees[u], degrees[v]))
        for u, v in ordered_edges
    )
    joint_degree_counts = tuple(
        (high, low, count)
        for (high, low), count in sorted(incidence.items(), reverse=True)
    )

    triangle_count = sum(
        1 for triple in combinations(nodes, 3) if _is_clique(triple, adjacency)
    )
    k4_count = sum(
        1 for quartet in combinations(nodes, 4) if _is_clique(quartet, adjacency)
    )

    clique_number = 1
    for size in range(2, len(nodes) + 1):
        if any(_is_clique(group, adjacency) for group in combinations(nodes, size)):
            clique_number = size
        else:
            break

    return StronglyRegularCliqueCollisionReceipt(
        degree_sequence=tuple(sorted(degrees.values(), reverse=True)),
        joint_degree_counts=joint_degree_counts,
        laplacian_spectrum=_integer_spectrum(_charpoly(laplacian), len(nodes)),
        triangle_count=triangle_count,
        k4_count=k4_count,
        clique_number=clique_number,
    )
