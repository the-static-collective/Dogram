"""Bounded exact specimen for NON-NORMAL-TYPE-CONSTITUTION-001.

Research only.  Permutations are tuples of images of (0,1,2), and
compose(p, q) means p after q.  Nothing here promotes a public Dogram operator.
"""

from itertools import permutations

Permutation = tuple[int, int, int]
IDENTITY: Permutation = (0, 1, 2)
TRANSPOSE_01: Permutation = (1, 0, 2)
CYCLE_012: Permutation = (1, 2, 0)


def compose(p: Permutation, q: Permutation) -> Permutation:
    return tuple(p[q[i]] for i in range(3))  # type: ignore[return-value]


def inverse(p: Permutation) -> Permutation:
    return tuple(p.index(i) for i in range(3))  # type: ignore[return-value]


def left_coset(g: Permutation, subgroup: set[Permutation]) -> set[Permutation]:
    return {compose(g, h) for h in subgroup}


def right_coset(subgroup: set[Permutation], g: Permutation) -> set[Permutation]:
    return {compose(h, g) for h in subgroup}


def conjugate_subgroup(g: Permutation, subgroup: set[Permutation]) -> set[Permutation]:
    gi = inverse(g)
    return {compose(compose(g, h), gi) for h in subgroup}


def receipt() -> dict[str, object]:
    group = set(permutations(range(3)))
    h = {IDENTITY, TRANSPOSE_01}
    g = CYCLE_012
    conjugate = conjugate_subgroup(g, h)
    g_h = left_coset(g, h)
    h_g = right_coset(h, g)
    return {
        "group_order": len(group),
        "subgroup_order": len(h),
        "index": len(group) // len(h),
        "subgroup": sorted(h),
        "conjugate_subgroup": sorted(conjugate),
        "subgroup_is_normal": all(conjugate_subgroup(x, h) == h for x in group),
        "left_coset": sorted(g_h),
        "right_coset": sorted(h_g),
        "left_equals_right": g_h == h_g,
        "conjugate_equals_declared": conjugate == h,
        "seal": "CONJUGATE CONSTITUTION != DECLARED CONSTITUTION WHEN THE ADMISSIBLE SUBGROUP IS NON-NORMAL.",
        "refusals": [
            "CONJUGACY != IDENTITY",
            "CHANGE OF FRAME != CHANGE OF DECLARATION",
            "LEFT COSET != RIGHT COSET WITHOUT NORMALITY",
            "COSET != SEMANTIC CLASS",
            "GROUP ACTION != OCCURRENCE",
            "STRUCTURAL TRANSPORT != AUTHORITY",
        ],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(receipt(), indent=2))
