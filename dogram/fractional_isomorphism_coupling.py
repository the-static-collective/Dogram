from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Iterable


Edge = tuple[int, int]
Matrix = tuple[tuple[Fraction, ...], ...]


@dataclass(frozen=True)
class GraphReceipt:
    vertex_count: int
    degree_sequence: tuple[int, ...]
    component_count: int
    triangle_count: int


@dataclass(frozen=True)
class FractionalIsomorphismReceipt:
    left: GraphReceipt
    right: GraphReceipt
    witness: Matrix
    witness_is_doubly_stochastic: bool
    intertwining_holds: bool
    same_degree_sequence: bool
    component_delta: int
    triangle_delta: int


def _normalize_edges(edges: Iterable[Edge]) -> tuple[tuple[int, ...], dict[int, set[int]]]:
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

    nodes = tuple(range(maximum + 1))
    if len(nodes) > 12:
        raise ValueError("bounded specimen supports at most 12 vertices")
    if {vertex for edge in normalized for vertex in edge} != set(nodes):
        raise ValueError("vertices must be consecutive and incident")

    adjacency = {node: set() for node in nodes}
    for u, v in normalized:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return nodes, adjacency


def _graph_receipt(nodes: tuple[int, ...], adjacency: dict[int, set[int]]) -> GraphReceipt:
    unseen = set(nodes)
    component_count = 0
    while unseen:
        component_count += 1
        start = next(iter(unseen))
        stack = [start]
        unseen.remove(start)
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)

    triangle_count = sum(
        1
        for a, b, c in combinations(nodes, 3)
        if b in adjacency[a] and c in adjacency[a] and c in adjacency[b]
    )
    return GraphReceipt(
        vertex_count=len(nodes),
        degree_sequence=tuple(sorted((len(adjacency[node]) for node in nodes), reverse=True)),
        component_count=component_count,
        triangle_count=triangle_count,
    )


def _adjacency_matrix(nodes: tuple[int, ...], adjacency: dict[int, set[int]]) -> Matrix:
    return tuple(
        tuple(Fraction(int(j in adjacency[i]), 1) for j in nodes)
        for i in nodes
    )


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    n = len(left)
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(n)), Fraction(0, 1)) for j in range(n))
        for i in range(n)
    )


def _uniform_witness(n: int) -> Matrix:
    entry = Fraction(1, n)
    return tuple(tuple(entry for _ in range(n)) for _ in range(n))


def _is_doubly_stochastic(matrix: Matrix) -> bool:
    n = len(matrix)
    one = Fraction(1, 1)
    zero = Fraction(0, 1)
    return (
        all(value >= zero for row in matrix for value in row)
        and all(sum(row, zero) == one for row in matrix)
        and all(sum((matrix[i][j] for i in range(n)), zero) == one for j in range(n))
    )


def analyze_pair(left_edges: Iterable[Edge], right_edges: Iterable[Edge]) -> FractionalIsomorphismReceipt:
    left_nodes, left_adjacency = _normalize_edges(left_edges)
    right_nodes, right_adjacency = _normalize_edges(right_edges)
    if len(left_nodes) != len(right_nodes):
        raise ValueError("fractional witness requires equal vertex counts")

    left_receipt = _graph_receipt(left_nodes, left_adjacency)
    right_receipt = _graph_receipt(right_nodes, right_adjacency)
    if len(set(left_receipt.degree_sequence)) != 1 or len(set(right_receipt.degree_sequence)) != 1:
        raise ValueError("bounded uniform witness specimen requires regular graphs")
    if left_receipt.degree_sequence[0] != right_receipt.degree_sequence[0]:
        raise ValueError("bounded uniform witness specimen requires equal regular degree")

    left_matrix = _adjacency_matrix(left_nodes, left_adjacency)
    right_matrix = _adjacency_matrix(right_nodes, right_adjacency)
    witness = _uniform_witness(len(left_nodes))

    return FractionalIsomorphismReceipt(
        left=left_receipt,
        right=right_receipt,
        witness=witness,
        witness_is_doubly_stochastic=_is_doubly_stochastic(witness),
        intertwining_holds=_matmul(left_matrix, witness) == _matmul(witness, right_matrix),
        same_degree_sequence=left_receipt.degree_sequence == right_receipt.degree_sequence,
        component_delta=right_receipt.component_count - left_receipt.component_count,
        triangle_delta=right_receipt.triangle_count - left_receipt.triangle_count,
    )
