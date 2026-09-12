from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Hashable, Iterable

Vertex = Hashable
Edge = tuple[Vertex, Vertex]


def _normalize_graph(
    vertices: Iterable[Vertex], edges: Iterable[Edge]
) -> tuple[tuple[Vertex, ...], tuple[Edge, ...]]:
    ordered_vertices = tuple(vertices)
    if len(set(ordered_vertices)) != len(ordered_vertices):
        raise ValueError("vertices must be unique")
    vertex_set = set(ordered_vertices)
    normalized_edges = tuple(edges)
    if len(set(normalized_edges)) != len(normalized_edges):
        raise ValueError("edges must be unique")
    for source, target in normalized_edges:
        if source not in vertex_set or target not in vertex_set:
            raise ValueError("edge endpoint is not a declared vertex")
        if source == target:
            raise ValueError("path homology research kernel requires loopless digraphs")
    return ordered_vertices, normalized_edges


def _rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    column_count = len(matrix[0])
    if column_count == 0:
        return 0
    rows = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(rows)
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def reachability_closure(
    vertices: Iterable[Vertex], edges: Iterable[Edge]
) -> tuple[Edge, ...]:
    ordered_vertices, normalized_edges = _normalize_graph(vertices, edges)
    adjacency = {vertex: [] for vertex in ordered_vertices}
    for source, target in normalized_edges:
        adjacency[source].append(target)

    reachable_pairs: list[Edge] = []
    for source in ordered_vertices:
        seen = {source}
        frontier = [source]
        while frontier:
            current = frontier.pop()
            for target in adjacency[current]:
                if target not in seen:
                    seen.add(target)
                    frontier.append(target)
        reachable_pairs.extend(
            (source, target) for target in ordered_vertices if target in seen
        )
    return tuple(reachable_pairs)


def first_betti_number(
    vertices: Iterable[Vertex], edges: Iterable[Edge]
) -> int:
    """Return non-regular path-homology beta_1 over Q for a loopless digraph."""

    ordered_vertices, normalized_edges = _normalize_graph(vertices, edges)
    edge_set = set(normalized_edges)
    edge_index = {edge: index for index, edge in enumerate(normalized_edges)}
    vertex_index = {vertex: index for index, vertex in enumerate(ordered_vertices)}

    boundary_1 = [[0 for _ in normalized_edges] for _ in ordered_vertices]
    for column, (source, target) in enumerate(normalized_edges):
        boundary_1[vertex_index[source]][column] -= 1
        boundary_1[vertex_index[target]][column] += 1
    cycle_dimension = len(normalized_edges) - _rank(boundary_1)

    allowed_two_paths = tuple(
        (first, middle, last)
        for first, middle, last in product(ordered_vertices, repeat=3)
        if (first, middle) in edge_set and (middle, last) in edge_set
    )
    if not allowed_two_paths:
        return cycle_dimension

    nonallowed_pairs = tuple(
        pair for pair in product(ordered_vertices, repeat=2) if pair not in edge_set
    )
    nonallowed_index = {pair: index for index, pair in enumerate(nonallowed_pairs)}

    allowed_boundary = [[0 for _ in allowed_two_paths] for _ in normalized_edges]
    nonallowed_boundary = [[0 for _ in allowed_two_paths] for _ in nonallowed_pairs]

    for column, (first, middle, last) in enumerate(allowed_two_paths):
        terms = (
            (1, (middle, last)),
            (-1, (first, last)),
            (1, (first, middle)),
        )
        for coefficient, pair in terms:
            if pair in edge_index:
                allowed_boundary[edge_index[pair]][column] += coefficient
            else:
                nonallowed_boundary[nonallowed_index[pair]][column] += coefficient

    nonallowed_rank = _rank(nonallowed_boundary)
    full_boundary_rank = _rank(nonallowed_boundary + allowed_boundary)
    boundary_dimension = full_boundary_rank - nonallowed_rank
    return cycle_dimension - boundary_dimension


__all__ = ["first_betti_number", "reachability_closure"]
