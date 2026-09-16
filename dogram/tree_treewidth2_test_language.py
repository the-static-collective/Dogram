from __future__ import annotations

from dataclasses import dataclass
from itertools import product


Edge = tuple[int, int]


CYCLE_6_EDGES: tuple[Edge, ...] = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 0),
)

TWO_TRIANGLES_EDGES: tuple[Edge, ...] = (
    (0, 1),
    (1, 2),
    (2, 0),
    (3, 4),
    (4, 5),
    (5, 3),
)


@dataclass(frozen=True)
class TreeTreewidth2Receipt:
    left_vertex_count: int
    right_vertex_count: int
    left_degree: int
    right_degree: int
    left_component_count: int
    right_component_count: int
    all_tree_counts_agree: bool
    k3_treewidth: int
    k3_hom_left: int
    k3_hom_right: int
    k3_hom_delta: int
    graphs_are_isomorphic: bool
    refusals: tuple[str, ...]

    def tree_hom_count(self, source_vertex_count: int) -> int:
        if not isinstance(source_vertex_count, int) or source_vertex_count < 1:
            raise ValueError("source tree must have a positive integer vertex count")
        # For any tree T on m vertices and any d-regular target Q on n vertices,
        # root T arbitrarily: n choices for the root image and d independent
        # choices for each of the remaining m-1 vertices along its parent edge.
        return self.left_vertex_count * (self.left_degree ** (source_vertex_count - 1))


def _adjacency(vertex_count: int, edges: tuple[Edge, ...]) -> tuple[frozenset[int], ...]:
    neighbors = [set() for _ in range(vertex_count)]
    for u, v in edges:
        if u == v or not (0 <= u < vertex_count and 0 <= v < vertex_count):
            raise ValueError("edges must define a simple loopless graph on the declared vertices")
        neighbors[u].add(v)
        neighbors[v].add(u)
    return tuple(frozenset(row) for row in neighbors)


def _component_count(adjacency: tuple[frozenset[int], ...]) -> int:
    unseen = set(range(len(adjacency)))
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            fresh = set(adjacency[vertex]) & unseen
            unseen.difference_update(fresh)
            stack.extend(fresh)
    return count


def _k3_hom_count(adjacency: tuple[frozenset[int], ...]) -> int:
    count = 0
    for a, b, c in product(range(len(adjacency)), repeat=3):
        if b in adjacency[a] and c in adjacency[b] and a in adjacency[c]:
            count += 1
    return count


def analyze_treewidth_language_gap() -> TreeTreewidth2Receipt:
    left = _adjacency(6, CYCLE_6_EDGES)
    right = _adjacency(6, TWO_TRIANGLES_EDGES)

    left_degrees = tuple(len(row) for row in left)
    right_degrees = tuple(len(row) for row in right)
    if len(set(left_degrees)) != 1 or len(set(right_degrees)) != 1:
        raise AssertionError("frozen targets must remain regular")

    left_degree = left_degrees[0]
    right_degree = right_degrees[0]
    same_tree_formula = len(left) == len(right) and left_degree == right_degree

    k3_left = _k3_hom_count(left)
    k3_right = _k3_hom_count(right)
    left_components = _component_count(left)
    right_components = _component_count(right)

    return TreeTreewidth2Receipt(
        left_vertex_count=len(left),
        right_vertex_count=len(right),
        left_degree=left_degree,
        right_degree=right_degree,
        left_component_count=left_components,
        right_component_count=right_components,
        all_tree_counts_agree=same_tree_formula,
        k3_treewidth=2,
        k3_hom_left=k3_left,
        k3_hom_right=k3_right,
        k3_hom_delta=k3_right - k3_left,
        graphs_are_isomorphic=left_components == right_components,
        refusals=(
            "TREE-HOM COLLISION != GRAPH IDENTITY",
            "TREEWIDTH-2 DELTA != OCCURRENCE DELTA",
            "STRONGER TEST LANGUAGE != MORE TRUE",
            "HOMOMORPHISM COUNT != EVIDENCE COUNT",
        ),
    )
