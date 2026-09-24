"""AMBIGUITY-PROFILE-001: exact finite list-size profiles.

Research-only kernel. It computes declared Hamming-radius compatibility counts;
it does not infer occurrence, evidence, source identity, or authority.
"""
from collections import Counter
from itertools import product, combinations


def hamming(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError("words must have equal length")
    return sum(x != y for x, y in zip(a, b))


def receipt(code, radius=1):
    code = tuple(code)
    if not code:
        raise ValueError("code must be nonempty")
    n = len(code[0])
    if any(len(c) != n or set(c) - {"0", "1"} for c in code):
        raise ValueError("code must contain equal-length binary words")
    ambient = tuple("".join(bits) for bits in product("01", repeat=n))
    lists = {y: tuple(c for c in code if hamming(y, c) <= radius) for y in ambient}
    sizes = {y: len(xs) for y, xs in lists.items()}
    minimum_distance = min(hamming(a, b) for a, b in combinations(code, 2)) if len(code) > 1 else None
    covering_radius = max(min(hamming(y, c) for c in code) for y in ambient)
    profile = dict(sorted(Counter(sizes.values()).items()))
    return {
        "length": n,
        "cardinality": len(code),
        "radius": radius,
        "minimum_distance": minimum_distance,
        "covering_radius": covering_radius,
        "maximum_list_size": max(sizes.values()),
        "list_size_profile": profile,
        "lists": lists,
        "authority": "none",
    }


CODE_A = ("0000", "0011", "0101", "0110")
CODE_B = ("0000", "0011", "0101", "1010")
