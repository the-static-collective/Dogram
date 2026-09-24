"""LIST-DECODING-AMBIGUITY-001: finite Hamming compatibility receipts.

Research only. A compatibility list is not an identified source or occurrence.
"""
from itertools import product


def hamming(a, b):
    if len(a) != len(b):
        raise ValueError("equal lengths required")
    return sum(x != y for x, y in zip(a, b))


def analyze(codewords, radius=1):
    code = tuple(tuple(int(x) for x in c) for c in codewords)
    if not code or radius < 0:
        raise ValueError("nonempty code and nonnegative radius required")
    n = len(code[0])
    if any(len(c) != n or any(x not in (0, 1) for x in c) for c in code):
        raise ValueError("binary equal-length codewords required")
    if len(set(code)) != len(code):
        raise ValueError("duplicate codewords")
    universe = tuple(product((0, 1), repeat=n))
    rows = []
    for received in universe:
        candidates = tuple(c for c in code if hamming(c, received) <= radius)
        nearest_distance = min(hamming(c, received) for c in code)
        rows.append({
            "received": received,
            "candidates": candidates,
            "list_size": len(candidates),
            "nearest_distance": nearest_distance,
            "status": "unique" if len(candidates) == 1 else ("ambiguous" if len(candidates) > 1 else "empty"),
        })
    pairwise = [hamming(a, b) for i, a in enumerate(code) for b in code[i + 1:]]
    return {
        "length": n,
        "radius": radius,
        "minimum_distance": min(pairwise) if pairwise else None,
        "covering_radius": max(r["nearest_distance"] for r in rows),
        "maximum_list_size": max(r["list_size"] for r in rows),
        "list_size_distribution": {k: sum(r["list_size"] == k for r in rows) for k in sorted({r["list_size"] for r in rows})},
        "rows": rows,
        "authority": "none",
    }
