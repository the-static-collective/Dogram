from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable


Edge = tuple[int, int]
Polynomial = tuple[int, ...]
JointDegreeCount = tuple[int, int, int]


@dataclass(frozen=True)
class JointDegreeIncidenceReceipt:
    degree_sequence: tuple[int, ...]
    laplacian_characteristic_polynomial: Polynomial
    joint_degree_counts: tuple[JointDegreeCount, ...]


def _matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def _charpoly(matrix: list[list[int]]) -> Polynomial:
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


def _normalize_edges(edges: Iterable[Edge]) -> tuple[tuple[int, ...], tuple[Edge, ...]]:
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
    return nodes, ordered


def analyze_graph(edges: Iterable[Edge]) -> JointDegreeIncidenceReceipt:
    nodes, ordered_edges = _normalize_edges(edges)
    degrees = {node: 0 for node in nodes}
    for u, v in ordered_edges:
        degrees[u] += 1
        degrees[v] += 1

    laplacian = [[0 for _ in nodes] for _ in nodes]
    for u, v in ordered_edges:
        laplacian[u][u] += 1
        laplacian[v][v] += 1
        laplacian[u][v] -= 1
        laplacian[v][u] -= 1

    incidence = Counter(
        (max(degrees[u], degrees[v]), min(degrees[u], degrees[v]))
        for u, v in ordered_edges
    )
    joint_degree_counts = tuple(
        (high, low, count)
        for (high, low), count in sorted(incidence.items(), reverse=True)
    )

    return JointDegreeIncidenceReceipt(
        degree_sequence=tuple(sorted(degrees.values(), reverse=True)),
        laplacian_characteristic_polynomial=_charpoly(laplacian),
        joint_degree_counts=joint_degree_counts,
    )
