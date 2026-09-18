"""Bounded exact kernel for HYPERGRAPH-BLOCKER-DUALITY-001.

Pure finite-set mathematics. No occurrence, evidence, causal, semantic, or
authority interpretation is promoted by this module.
"""

from itertools import combinations


def normalize(edges):
    """Return the clutter of inclusion-minimal nonempty edges."""
    unique = {frozenset(edge) for edge in edges if edge}
    return tuple(sorted((e for e in unique if not any(f < e for f in unique)), key=lambda e: (len(e), tuple(sorted(e)))))


def blocker(vertices, edges):
    """Enumerate all inclusion-minimal transversals of a finite hypergraph."""
    clutter = normalize(edges)
    vertices = tuple(sorted(vertices))
    hits = []
    for size in range(len(vertices) + 1):
        for choice in combinations(vertices, size):
            candidate = frozenset(choice)
            if all(candidate & edge for edge in clutter):
                if not any(prev <= candidate for prev in hits):
                    hits.append(candidate)
    return normalize(hits)


def receipt():
    """Frozen specimen: path-shaped distinction-support clutter on four views."""
    vertices = (0, 1, 2, 3)
    supports = normalize(({0, 1}, {1, 2}, {2, 3}))
    minimal_retained = blocker(vertices, supports)
    reconstructed = blocker(vertices, minimal_retained)
    return {
        "vertices": vertices,
        "distinction_supports": supports,
        "minimal_retained_view_sets": minimal_retained,
        "double_blocker": reconstructed,
        "involution_holds": reconstructed == supports,
    }
