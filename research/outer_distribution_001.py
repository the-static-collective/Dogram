"""OUTER-DISTRIBUTION-001: exact finite Hamming-space receipt."""
from collections import Counter
from itertools import product, combinations

A = ("0000", "0001", "0010", "0101")
B = ("0000", "0001", "0010", "0111")


def hamming(a, b):
    if len(a) != len(b):
        raise ValueError("equal lengths required")
    return sum(x != y for x, y in zip(a, b))


def outer_row(code, y):
    n = len(y)
    return tuple(sum(hamming(c, y) == d for c in code) for d in range(n + 1))


def receipt(code, radius=1):
    if not code or len({len(c) for c in code}) != 1:
        raise ValueError("nonempty equal-length code required")
    n = len(code[0])
    ambient = tuple("".join(bits) for bits in product("01", repeat=n))
    rows = {y: outer_row(code, y) for y in ambient}
    list_sizes = {y: sum(rows[y][: radius + 1]) for y in ambient}
    return {
        "code": tuple(code),
        "minimum_distance": min(hamming(x, y) for x, y in combinations(code, 2)),
        "covering_radius": max(min(hamming(c, y) for c in code) for y in ambient),
        "radius": radius,
        "list_size_histogram": dict(sorted(Counter(list_sizes.values()).items())),
        "outer_row_histogram": dict(sorted(Counter(rows.values()).items())),
        "outer_rows": rows,
    }


def compare():
    a, b = receipt(A), receipt(B)
    return {
        "same_coarse": (
            a["minimum_distance"], a["covering_radius"], a["list_size_histogram"]
        ) == (
            b["minimum_distance"], b["covering_radius"], b["list_size_histogram"]
        ),
        "same_outer_distribution": a["outer_row_histogram"] == b["outer_row_histogram"],
        "witness": "0000",
        "A_outer_at_witness": a["outer_rows"]["0000"],
        "B_outer_at_witness": b["outer_rows"]["0000"],
        "A": a,
        "B": b,
    }

if __name__ == "__main__":
    import pprint
    pprint.pp(compare())
