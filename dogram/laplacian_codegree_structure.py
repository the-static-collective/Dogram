from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class LaplacianCodegreeStructureReceipt:
    vertices: int
    edges: tuple[tuple[int, int], ...]
    degree_sequence: tuple[int, ...]
    characteristic_polynomial: tuple[int, ...]
    articulation_vertices: tuple[int, ...]
    diameter: int


def _adjacency(vertices: int, edges: tuple[tuple[int, int], ...]) -> tuple[frozenset[int], ...]:
    if not isinstance(vertices, int) or isinstance(vertices, bool) or vertices <= 0:
        raise ValueError("vertices must be a positive integer")
    neighbors = [set() for _ in range(vertices)]
    seen: set[tuple[int, int]] = set()
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("each edge must contain exactly two endpoints")
        u, v = edge
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in edge):
            raise ValueError("edge endpoints must be integers")
        if not (0 <= u < vertices and 0 <= v < vertices) or u == v:
            raise ValueError("edges must be loopless and within the declared vertex set")
        key = (min(u, v), max(u, v))
        if key in seen:
            raise ValueError("duplicate undirected edge")
        seen.add(key)
        neighbors[u].add(v)
        neighbors[v].add(u)
    return tuple(frozenset(row) for row in neighbors)


def _matrix_multiply(a: tuple[tuple[int, ...], ...], b: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def _characteristic_polynomial(matrix: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    """Exact Faddeev-LeVerrier coefficients of det(lambda I - matrix)."""
    n = len(matrix)
    power = matrix
    traces = [0]
    for exponent in range(1, n + 1):
        traces.append(sum(power[i][i] for i in range(n)))
        if exponent < n:
            power = _matrix_multiply(power, matrix)

    coefficients = [1]
    for k in range(1, n + 1):
        numerator = sum(coefficients[k - i] * traces[i] for i in range(1, k + 1))
        quotient, remainder = divmod(-numerator, k)
        if remainder:
            raise ArithmeticError("non-integral characteristic coefficient")
        coefficients.append(quotient)
    return tuple(coefficients)


def _connected(adjacency: tuple[frozenset[int], ...], removed: int | None = None) -> bool:
    remaining = [vertex for vertex in range(len(adjacency)) if vertex != removed]
    if not remaining:
        return True
    seen = {remaining[0]}
    queue = deque([remaining[0]])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor == removed or neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append(neighbor)
    return len(seen) == len(remaining)


def _diameter(adjacency: tuple[frozenset[int], ...]) -> int:
    if not _connected(adjacency):
        raise ValueError("graph must be connected")
    maximum = 0
    for source in range(len(adjacency)):
        distance = {source: 0}
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in distance:
                    continue
                distance[neighbor] = distance[vertex] + 1
                queue.append(neighbor)
        maximum = max(maximum, max(distance.values()))
    return maximum


def analyze_graph(vertices: int, edges: tuple[tuple[int, int], ...]) -> LaplacianCodegreeStructureReceipt:
    """Receipt exact finite Laplacian and cut geometry for one simple connected graph.

    This bounded research kernel compares mathematical projections only. It does not
    infer occurrence, evidence, causal structure, semantic identity, or truth.
    """
    adjacency = _adjacency(vertices, edges)
    if not _connected(adjacency):
        raise ValueError("graph must be connected")

    degree_sequence = tuple(sorted((len(row) for row in adjacency), reverse=True))
    laplacian = tuple(
        tuple(
            len(adjacency[i]) if i == j else (-1 if j in adjacency[i] else 0)
            for j in range(vertices)
        )
        for i in range(vertices)
    )
    articulation_vertices = tuple(
        vertex for vertex in range(vertices) if not _connected(adjacency, vertex)
    )

    return LaplacianCodegreeStructureReceipt(
        vertices=vertices,
        edges=edges,
        degree_sequence=degree_sequence,
        characteristic_polynomial=_characteristic_polynomial(laplacian),
        articulation_vertices=articulation_vertices,
        diameter=_diameter(adjacency),
    )


__all__ = ["LaplacianCodegreeStructureReceipt", "analyze_graph"]
