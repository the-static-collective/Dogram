"""Exact finite specimen for blocker-summary collisions.

Research-only. This module computes finite clutter blockers and coarse receipts;
it does not attach causal, evidential, semantic, or authority meaning.
"""

from itertools import combinations


def _norm(family):
    return tuple(sorted((tuple(sorted(edge)) for edge in family), key=lambda e: (len(e), e)))


def blocker(vertices, family):
    """Return all inclusion-minimal transversals of a finite clutter."""
    vertices = tuple(sorted(vertices))
    edges = tuple(frozenset(edge) for edge in family)
    found = []
    for size in range(len(vertices) + 1):
        for candidate in combinations(vertices, size):
            c = frozenset(candidate)
            if all(c & edge for edge in edges) and not any(prev <= c for prev in found):
                found.append(c)
    return _norm(found)


def degree_sequence(vertices, family):
    """Vertex degrees, sorted descending, retaining isolated vertices."""
    edges = tuple(frozenset(edge) for edge in family)
    return tuple(sorted((sum(v in edge for edge in edges) for v in vertices), reverse=True))


def receipt(vertices, family):
    family = _norm(family)
    dual = blocker(vertices, family)
    return {
        "family": family,
        "edge_size_multiset": tuple(sorted(map(len, family))),
        "transversal_number": min(map(len, dual)),
        "blocker": dual,
        "blocker_size_multiset": tuple(sorted(map(len, dual))),
        "degree_sequence": degree_sequence(vertices, family),
        "blocker_degree_sequence": degree_sequence(vertices, dual),
        "double_blocker": blocker(vertices, dual),
    }


def specimen():
    """Triangle+isolated-vertex versus P4: same coarse blocker summaries, different geometry."""
    vertices = (0, 1, 2, 3)
    triangle = ((0, 1), (0, 2), (1, 2))
    path = ((0, 1), (0, 3), (1, 2))
    left = receipt(vertices, triangle)
    right = receipt(vertices, path)
    return {
        "vertices": vertices,
        "left": left,
        "right": right,
        "same_edge_size_multiset": left["edge_size_multiset"] == right["edge_size_multiset"],
        "same_transversal_number": left["transversal_number"] == right["transversal_number"],
        "same_blocker_size_multiset": left["blocker_size_multiset"] == right["blocker_size_multiset"],
        "different_degree_sequence": left["degree_sequence"] != right["degree_sequence"],
        "different_blocker_degree_sequence": left["blocker_degree_sequence"] != right["blocker_degree_sequence"],
        "both_round_trip": left["double_blocker"] == left["family"] and right["double_blocker"] == right["family"],
    }
