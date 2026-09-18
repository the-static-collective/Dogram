from itertools import permutations

VERTICES = (0, 1, 2, 3)
EDGES = frozenset({frozenset((0, 1)), frozenset((1, 2)), frozenset((2, 3)), frozenset((3, 0))})
TYPE = {0: "representative", 1: "successor", 2: "representative", 3: "successor"}


def image_edge(edge, p):
    return frozenset(p[v] for v in edge)


def is_automorphism(p):
    return frozenset(image_edge(e, p) for e in EDGES) == EDGES


def type_action(p):
    pairs = {(TYPE[v], TYPE[p[v]]) for v in VERTICES}
    preserve = {("representative", "representative"), ("successor", "successor")}
    swap = {("representative", "successor"), ("successor", "representative")}
    if pairs == preserve:
        return "preserve"
    if pairs == swap:
        return "swap"
    return "mixed"


def automorphisms():
    return tuple(p for p in permutations(VERTICES) if is_automorphism(p))


def admissible_automorphisms(allowed_type_actions=("preserve",)):
    allowed = frozenset(allowed_type_actions)
    if not allowed <= {"preserve", "swap"}:
        raise ValueError("allowed type actions must be declared from preserve/swap")
    return tuple(p for p in automorphisms() if type_action(p) in allowed)


def receipt():
    aut = automorphisms()
    preserve = admissible_automorphisms(("preserve",))
    licensed = admissible_automorphisms(("preserve", "swap"))
    return {
        "untyped_automorphism_count": len(aut),
        "type_preserving_count": len(preserve),
        "type_swapping_count": sum(type_action(p) == "swap" for p in aut),
        "admissible_without_swap_declaration": len(preserve),
        "admissible_with_swap_declaration": len(licensed),
        "all_automorphisms_have_uniform_type_action": all(type_action(p) in {"preserve", "swap"} for p in aut),
    }


if __name__ == "__main__":
    print(receipt())
