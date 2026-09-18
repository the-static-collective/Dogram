"""TYPE-ACTION-SUBGROUP-001: exact finite group-action research specimen.

Research-only. Structural symmetry is not authority.
"""
from itertools import permutations

TYPES = ("R", "S", "W")
EDGES = frozenset({frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))})


def parity(p):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return inversions % 2


def is_automorphism(p):
    moved = {frozenset((p[u], p[v])) for u, v in ((0, 1), (1, 2), (0, 2))}
    return moved == EDGES


def induced_type_permutation(p):
    # Vertex i initially carries TYPES[i]. Return images as type indices.
    return tuple(p[i] for i in range(3))


def receipt():
    aut = tuple(p for p in permutations(range(3)) if is_automorphism(p))
    even = tuple(p for p in aut if parity(p) == 0)
    odd = tuple(p for p in aut if parity(p) == 1)
    return {
        "carrier": "K3 with three declared singleton role-types R,S,W",
        "automorphism_count": len(aut),
        "induced_type_actions": [list(induced_type_permutation(p)) for p in aut],
        "declared_admissible_subgroup": "A3 (even type permutations)",
        "admissible_count": len(even),
        "refused_structural_symmetry_count": len(odd),
        "admissible_actions": [list(p) for p in even],
        "refused_actions": [list(p) for p in odd],
        "coset_index": len(aut) // len(even),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(receipt(), indent=2, sort_keys=True))
