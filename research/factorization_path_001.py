"""FACTORIZATION-PATH-001: exact finite transport-factorization receipt.

Research only. Structural arrows are not occurrence, evidence, causation, or authority.
"""
from itertools import permutations

Perm = tuple[int, int, int]
ID: Perm = (0, 1, 2)


def compose(left: Perm, right: Perm) -> Perm:
    """Return left after right."""
    return tuple(left[right[i]] for i in range(3))  # type: ignore[return-value]


def inverse(p: Perm) -> Perm:
    out = [0, 0, 0]
    for i, image in enumerate(p):
        out[image] = i
    return tuple(out)  # type: ignore[return-value]


def conjugate(g: Perm, h: Perm) -> Perm:
    return compose(compose(g, h), inverse(g))


def subgroup_generated_by_transposition(t: Perm) -> frozenset[Perm]:
    assert compose(t, t) == ID and t != ID
    return frozenset((ID, t))


def s3() -> tuple[Perm, ...]:
    return tuple(permutations(range(3)))


def transport_subgroup(g: Perm, h: frozenset[Perm]) -> frozenset[Perm]:
    return frozenset(conjugate(g, x) for x in h)


def cycle012() -> Perm:
    return (1, 2, 0)


def cycle021() -> Perm:
    return (2, 0, 1)


def transposition01() -> Perm:
    return (1, 0, 2)


def receipt() -> dict:
    h01 = subgroup_generated_by_transposition(transposition01())
    g = cycle012()
    k = cycle021()

    mid_g = transport_subgroup(g, h01)
    mid_k = transport_subgroup(k, h01)

    path_g = (g, inverse(g))
    path_k = (k, inverse(k))

    # Arrows are applied left-to-right; net action is second after first.
    composite_g = compose(path_g[1], path_g[0])
    composite_k = compose(path_k[1], path_k[0])

    assert mid_g != mid_k
    assert transport_subgroup(path_g[1], mid_g) == h01
    assert transport_subgroup(path_k[1], mid_k) == h01
    assert composite_g == composite_k == ID
    assert path_g != path_k

    return {
        "group_order": len(s3()),
        "source_equals_target": True,
        "composites_equal": composite_g == composite_k,
        "composite": list(composite_g),
        "paths_distinct": path_g != path_k,
        "intermediate_constitutions_distinct": mid_g != mid_k,
        "path_a": [list(x) for x in path_g],
        "path_b": [list(x) for x in path_k],
        "intermediate_a": sorted([list(x) for x in mid_g]),
        "intermediate_b": sorted([list(x) for x in mid_k]),
        "seal": "SAME COMPOSITE TRANSPORT != SAME FACTORIZATION HISTORY.",
        "nonclaims": [
            "transport arrow != occurrence",
            "factorization path != historical path",
            "same composite != same provenance",
            "intermediate constitution != observed intermediate state",
            "groupoid composition != causal composition",
        ],
    }
