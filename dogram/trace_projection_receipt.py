"""Bounded Mazurkiewicz-trace projection receipt research kernel.

Research-only: no public operator or semantic interpretation.
"""

from collections import deque


def projection(word: str, letters: frozenset[str]) -> str:
    return "".join(ch for ch in word if ch in letters)


def dependent_pairs(alphabet: tuple[str, ...], independence: frozenset[tuple[str, str]]):
    """Canonical unordered dependency pairs, including reflexive pairs."""
    out = []
    for i, a in enumerate(alphabet):
        for b in alphabet[i:]:
            if (a, b) not in independence:
                out.append((a, b))
    return tuple(out)


def projection_receipt(word: str, alphabet: tuple[str, ...], independence: frozenset[tuple[str, str]]):
    return {
        "".join(pair): projection(word, frozenset(pair))
        for pair in dependent_pairs(alphabet, independence)
    }


def trace_class(word: str, independence: frozenset[tuple[str, str]]):
    """Exact finite closure under adjacent independent swaps."""
    seen = {word}
    queue = deque([word])
    while queue:
        current = queue.popleft()
        for i in range(len(current) - 1):
            if (current[i], current[i + 1]) in independence:
                nxt = current[:i] + current[i + 1] + current[i] + current[i + 2:]
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return tuple(sorted(seen))


def specimen():
    alphabet = ("a", "b", "c")
    independence = frozenset({("a", "c"), ("c", "a")})
    left = "abac"
    right = "baac"
    left_receipt = projection_receipt(left, alphabet, independence)
    right_receipt = projection_receipt(right, alphabet, independence)
    differing = tuple(k for k in left_receipt if left_receipt[k] != right_receipt[k])
    omitted = "ab"
    reduced_left = {k: v for k, v in left_receipt.items() if k != omitted}
    reduced_right = {k: v for k, v in right_receipt.items() if k != omitted}
    return {
        "alphabet": alphabet,
        "independence": tuple(sorted(independence)),
        "left": left,
        "right": right,
        "left_trace_class": trace_class(left, independence),
        "right_trace_class": trace_class(right, independence),
        "left_projection_receipt": left_receipt,
        "right_projection_receipt": right_receipt,
        "differing_dependent_projections": differing,
        "omitted_projection": omitted,
        "reduced_receipts_equal": reduced_left == reduced_right,
        "trace_classes_disjoint": set(trace_class(left, independence)).isdisjoint(trace_class(right, independence)),
    }
