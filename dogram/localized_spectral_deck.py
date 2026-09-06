from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from typing import Iterable


Edge = tuple[int, int]
Polynomial = tuple[int, ...]


@dataclass(frozen=True)
class LocalizedSpectralDeckReceipt:
    degree_sequence: tuple[int, ...]
    laplacian_characteristic_polynomial: Polynomial
    articulation_count: int
    bridge_count: int
    diameter: int
    distance_histogram: tuple[tuple[int, int], ...]
    triangle_count: int
    vertex_deleted_laplacian_deck: tuple[Polynomial, ...]


def _matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def _charpoly(matrix: list[list[int]]) -> Polynomial:
    n = len(matrix)
    if n == 0:
        return (1,)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    b = identity
    coeffs = [1]
    for k in range(1, n + 1):
        ab = _matmul(matrix, b)
        trace = sum(ab[i][i] for i in range(n))
        if trace % k:
            raise ArithmeticError("exact characteristic-polynomial division failed")
        c = -(trace // k)
        coeffs.append(c)
        b = [
            [ab[i][j] + (c if i == j else 0) for j in range(n)]
            for i in range(n)
        ]
    return tuple(coeffs)


def _adjacency(nodes: tuple[int, ...], edges: tuple[Edge, ...]) -> dict[int, set[int]]:
    adj = {node: set() for node in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def _connected(adj: dict[int, set[int]]) -> bool:
    if not adj:
        return True
    start = next(iter(adj))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(adj)


def _laplacian(nodes: tuple[int, ...], edges: tuple[Edge, ...]) -> list[list[int]]:
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for u, v in edges:
        i, j = index[u], index[v]
        matrix[i][i] += 1
        matrix[j][j] += 1
        matrix[i][j] -= 1
        matrix[j][i] -= 1
    return matrix


def _distances(adj: dict[int, set[int]], start: int) -> dict[int, int]:
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


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
    if set(node for edge in normalized for node in edge) != set(nodes):
        raise ValueError("vertices must be consecutive and incident")
    ordered = tuple(sorted(normalized))
    if not _connected(_adjacency(nodes, ordered)):
        raise ValueError("graph must be connected")
    return nodes, ordered


def _deleted(nodes: tuple[int, ...], edges: tuple[Edge, ...], vertex: int) -> tuple[tuple[int, ...], tuple[Edge, ...]]:
    kept_nodes = tuple(node for node in nodes if node != vertex)
    kept_edges = tuple(edge for edge in edges if vertex not in edge)
    return kept_nodes, kept_edges


def analyze_graph(edges: Iterable[Edge]) -> LocalizedSpectralDeckReceipt:
    nodes, ordered_edges = _normalize_edges(edges)
    adj = _adjacency(nodes, ordered_edges)
    degrees = tuple(sorted((len(adj[node]) for node in nodes), reverse=True))
    charpoly = _charpoly(_laplacian(nodes, ordered_edges))

    articulation_count = 0
    for vertex in nodes:
        kept_nodes, kept_edges = _deleted(nodes, ordered_edges, vertex)
        if kept_nodes and not _connected(_adjacency(kept_nodes, kept_edges)):
            articulation_count += 1

    bridge_count = 0
    for edge in ordered_edges:
        kept_edges = tuple(candidate for candidate in ordered_edges if candidate != edge)
        if not _connected(_adjacency(nodes, kept_edges)):
            bridge_count += 1

    pair_distances: list[int] = []
    diameter = 0
    for i, u in enumerate(nodes):
        dist = _distances(adj, u)
        diameter = max(diameter, max(dist.values()))
        for v in nodes[i + 1 :]:
            pair_distances.append(dist[v])
    distance_histogram = tuple(sorted(Counter(pair_distances).items()))

    triangle_count = 0
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes[i + 1 :], start=i + 1):
            if v not in adj[u]:
                continue
            for w in nodes[j + 1 :]:
                if w in adj[u] and w in adj[v]:
                    triangle_count += 1

    deck: list[Polynomial] = []
    for vertex in nodes:
        kept_nodes, kept_edges = _deleted(nodes, ordered_edges, vertex)
        deck.append(_charpoly(_laplacian(kept_nodes, kept_edges)))

    return LocalizedSpectralDeckReceipt(
        degree_sequence=degrees,
        laplacian_characteristic_polynomial=charpoly,
        articulation_count=articulation_count,
        bridge_count=bridge_count,
        diameter=diameter,
        distance_histogram=distance_histogram,
        triangle_count=triangle_count,
        vertex_deleted_laplacian_deck=tuple(sorted(deck)),
    )
