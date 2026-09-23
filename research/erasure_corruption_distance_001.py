"""ERASURE-CORRUPTION-DISTANCE-001: finite binary signature corruption receipt.

Research-only. A codeword/signature is a declared structural observation, not an
occurrence, evidence claim, semantic identity, sensor model, or authority.
"""
from itertools import combinations


def hamming(a, b):
    if len(a) != len(b):
        raise ValueError("equal lengths required")
    return sum(x != y for x, y in zip(a, b))


def analyze(codewords):
    words = tuple(tuple(int(bit) for bit in word) for word in codewords)
    if not words or len(set(words)) != len(words):
        raise ValueError("distinct nonempty codewords required")
    n = len(words[0])
    if n == 0 or any(len(w) != n for w in words):
        raise ValueError("equal positive lengths required")
    if any(bit not in (0, 1) for w in words for bit in w):
        raise ValueError("binary codewords required")

    distances = tuple((a, b, hamming(a, b)) for a, b in combinations(words, 2))
    dmin = min((d for _, _, d in distances), default=None)

    punctures = {}
    for i in range(n):
        projected = tuple(w[:i] + w[i + 1:] for w in words)
        punctures[i] = {
            "projected": projected,
            "unique": len(set(projected)) == len(words),
        }

    one_flip_receipts = []
    received_to_sources = {}
    for source in words:
        for i in range(n):
            received = source[:i] + (1 - source[i],) + source[i + 1:]
            received_to_sources.setdefault(received, set()).add(source)
    for received, sources in sorted(received_to_sources.items()):
        one_flip_receipts.append((received, tuple(sorted(sources))))

    ambiguous = tuple((r, s) for r, s in one_flip_receipts if len(s) > 1)
    undetected = tuple(r for r, _ in one_flip_receipts if r in set(words))

    return {
        "codewords": words,
        "pair_distances": distances,
        "minimum_distance": dmin,
        "single_known_erasure_recoverable": all(v["unique"] for v in punctures.values()),
        "punctures": punctures,
        "single_unknown_flip_detectable": not undetected,
        "single_unknown_flip_uniquely_correctable": not ambiguous,
        "ambiguous_one_flip_receipts": ambiguous,
        "undetected_one_flip_receipts": undetected,
    }


def frozen_specimen():
    # Even-parity [3,2,2] code: exactly the x,y,xor signatures from the prior seam.
    return analyze(((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)))


if __name__ == "__main__":
    receipt = frozen_specimen()
    for key in (
        "minimum_distance",
        "single_known_erasure_recoverable",
        "single_unknown_flip_detectable",
        "single_unknown_flip_uniquely_correctable",
        "ambiguous_one_flip_receipts",
    ):
        print(key, receipt[key])
