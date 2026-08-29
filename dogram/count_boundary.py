"""COUNT-BOUNDARY-001: a deliberately small arithmetic traversal floor.

Traversal is restricted to a frozen family of independently named arithmetic
operators. Representation diagnostics (digit patterns, base changes, modular
coincidences, ad-hoc affine formulas) do not become traversal edges unless a
future version explicitly promotes them through review.
"""

from __future__ import annotations

from math import isqrt

FROZEN_OPERATOR_NAMES = (
    "pred",
    "succ",
    "prime_pi",
    "nth_prime",
    "divisor_count",
    "totient",
    "pair_count",
)


def _require_positive_int(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("COUNT-BOUNDARY operators require a positive integer")


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = isqrt(n)
    candidate = 3
    while candidate <= limit:
        if n % candidate == 0:
            return False
        candidate += 2
    return True


def _prime_pi(n: int) -> int:
    return sum(1 for value in range(2, n + 1) if _is_prime(value))


def _nth_prime(n: int) -> int:
    found = 0
    candidate = 1
    while found < n:
        candidate += 1
        if _is_prime(candidate):
            found += 1
    return candidate


def _divisor_count(n: int) -> int:
    remaining = n
    count = 1
    factor = 2
    while factor * factor <= remaining:
        exponent = 0
        while remaining % factor == 0:
            remaining //= factor
            exponent += 1
        if exponent:
            count *= exponent + 1
        factor = 3 if factor == 2 else factor + 2
    if remaining > 1:
        count *= 2
    return count


def _totient(n: int) -> int:
    if n == 1:
        return 1
    result = n
    remaining = n
    factor = 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            while remaining % factor == 0:
                remaining //= factor
            result -= result // factor
        factor = 3 if factor == 2 else factor + 2
    if remaining > 1:
        result -= result // remaining
    return result


def _pair_count(n: int) -> int:
    return n * (n - 1) // 2


def apply_operator(name: str, n: int) -> int:
    """Apply one frozen traversal operator to one positive integer."""

    _require_positive_int(n)
    if name not in FROZEN_OPERATOR_NAMES:
        raise KeyError(name)

    if name == "pred":
        if n == 1:
            raise ValueError("pred is undefined at 1 in COUNT-BOUNDARY-001")
        return n - 1
    if name == "succ":
        return n + 1
    if name == "prime_pi":
        return _prime_pi(n)
    if name == "nth_prime":
        return _nth_prime(n)
    if name == "divisor_count":
        return _divisor_count(n)
    if name == "totient":
        return _totient(n)
    if name == "pair_count":
        return _pair_count(n)

    raise AssertionError("frozen operator registry and dispatcher diverged")


def audit_edge(source: int, target: int, operator: str) -> dict[str, object]:
    """Return an inert receipt for a proposed labeled arithmetic edge."""

    _require_positive_int(source)
    _require_positive_int(target)

    if operator not in FROZEN_OPERATOR_NAMES:
        return {
            "source": source,
            "target": target,
            "operator": operator,
            "status": "REFUSE_UNKNOWN_OPERATOR",
            "calculated": None,
            "exact": False,
        }

    calculated = apply_operator(operator, source)
    exact = calculated == target
    return {
        "source": source,
        "target": target,
        "operator": operator,
        "status": "MATCH" if exact else "NO_MATCH",
        "calculated": calculated,
        "exact": exact,
    }


def induced_edges(values: tuple[int, ...] | list[int]) -> tuple[dict[str, object], ...]:
    """Return every frozen exact edge whose source and target are both in values.

    The input corpus defines the visible node set. This function does not add
    intermediary values, rank edges, infer meaning, or widen the operator family.
    """

    ordered_values = tuple(values)
    for value in ordered_values:
        _require_positive_int(value)
    visible = set(ordered_values)
    edges: list[dict[str, object]] = []

    for source in ordered_values:
        for operator in FROZEN_OPERATOR_NAMES:
            try:
                target = apply_operator(operator, source)
            except ValueError:
                continue
            if target in visible:
                edges.append(audit_edge(source, target, operator))

    return tuple(edges)


def trace_path(seed: int, operators: tuple[str, ...] | list[str]) -> dict[str, object]:
    """Replay a declared operator sequence without inventing repair edges."""

    _require_positive_int(seed)
    current = seed
    nodes = [seed]
    edges = []

    for operator in operators:
        if operator not in FROZEN_OPERATOR_NAMES:
            return {
                "seed": seed,
                "operators": tuple(operators),
                "nodes": tuple(nodes),
                "edges": tuple(edges),
                "status": "REFUSE_UNKNOWN_OPERATOR",
                "refused_operator": operator,
                "exact": False,
            }
        target = apply_operator(operator, current)
        edge = audit_edge(current, target, operator)
        edges.append(edge)
        nodes.append(target)
        current = target

    return {
        "seed": seed,
        "operators": tuple(operators),
        "nodes": tuple(nodes),
        "edges": tuple(edges),
        "status": "EXACT_REPLAY",
        "exact": True,
    }
