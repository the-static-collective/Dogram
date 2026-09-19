"""Bounded exact specimen for ACTION-GROUPOID-TRANSPORT-001.

Research only. Group-action arrows are structural transports, not occurrences.
"""
from itertools import permutations

Perm = tuple[int, ...]


def compose(p: Perm, q: Perm) -> Perm:
    """Return p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def conjugate(g: Perm, h: Perm) -> Perm:
    return compose(compose(g, h), inverse(g))


def subgroup_generated_by_transposition() -> frozenset[Perm]:
    e = (0, 1, 2)
    t01 = (1, 0, 2)
    return frozenset((e, t01))


def conjugate_subgroup(g: Perm, H: frozenset[Perm]) -> frozenset[Perm]:
    return frozenset(conjugate(g, h) for h in H)


def transporter(source: frozenset[Perm], target: frozenset[Perm]) -> tuple[Perm, ...]:
    G = tuple(permutations(range(3)))
    return tuple(g for g in G if conjugate_subgroup(g, source) == target)


def receipt() -> dict:
    H = subgroup_generated_by_transposition()
    arrows = transporter(H, H)
    e = (0, 1, 2)
    t01 = (1, 0, 2)
    assert set(arrows) == {e, t01}
    assert e != t01
    assert conjugate_subgroup(e, H) == H
    assert conjugate_subgroup(t01, H) == H
    return {
        "group": "S3",
        "object": "H=< (01) >",
        "source": "H",
        "target": "H",
        "transporter_size": len(arrows),
        "distinct_arrow_labels": [list(g) for g in arrows],
        "endpoint_pair": ["H", "H"],
        "endpoint_pair_determines_arrow": False,
        "normalizer_size": len(arrows),
        "seal": "SAME SOURCE + SAME TARGET != SAME TRANSPORT ARROW.",
        "refusals": [
            "GROUP ACTION ARROW != OCCURRENCE",
            "SAME ENDPOINT != SAME HISTORY",
            "TRANSPORTER ELEMENT != EVIDENCE",
            "GROUPoid COMPOSITION != CAUSAL COMPOSITION",
        ],
    }
