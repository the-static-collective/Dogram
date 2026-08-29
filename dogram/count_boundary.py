from __future__ import annotations

from collections import deque
from functools import lru_cache
from math import comb, isqrt

FROZEN_OPERATOR_IDS = (
    "prime_count@1",
    "divisor_count_record@1",
    "pair_count@1",
)


def _validate_pair(pair: tuple[int, int]) -> tuple[int, int]:
    if len(pair) != 2:
        raise ValueError("pair must contain exactly two integers")
    left, right = pair
    if not isinstance(left, int) or not isinstance(right, int):
        raise TypeError("pair values must be integers")
    if left < 1 or right < 1 or left >= right:
        raise ValueError("pair must satisfy 1 <= left < right")
    return left, right


@lru_cache(maxsize=None)
def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for p in range(3, isqrt(n) + 1, 2):
        if n % p == 0:
            return False
    return True


@lru_cache(maxsize=None)
def prime_count(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return sum(1 for k in range(2, n + 1) if _is_prime(k))


@lru_cache(maxsize=None)
def nth_prime(index: int) -> int:
    if index < 1:
        raise ValueError("prime index must be positive")
    seen = 0
    candidate = 1
    while seen < index:
        candidate += 1
        if _is_prime(candidate):
            seen += 1
    return candidate


def _prime_count_fiber_width(count_value: int) -> int:
    if count_value == 0:
        return 1
    return nth_prime(count_value + 1) - nth_prime(count_value)


def prime_count_pair_fiber_size(pair: tuple[int, int]) -> int:
    left, right = _validate_pair(pair)
    a = prime_count(left)
    b = prime_count(right)
    width_a = _prime_count_fiber_width(a)
    width_b = _prime_count_fiber_width(b)
    if a < b:
        return width_a * width_b
    if a == b:
        return comb(width_a, 2)
    raise AssertionError("prime count cannot decrease across an ordered pair")


@lru_cache(maxsize=None)
def divisor_count(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    x = n
    result = 1
    p = 2
    while p * p <= x:
        if x % p == 0:
            exponent = 0
            while x % p == 0:
                x //= p
                exponent += 1
            result *= exponent + 1
        p = 3 if p == 2 else p + 2
    if x > 1:
        result *= 2
    return result


@lru_cache(maxsize=None)
def is_strict_divisor_record(n: int) -> bool:
    if n < 1:
        raise ValueError("n must be positive")
    value = divisor_count(n)
    return all(divisor_count(k) < value for k in range(1, n))


def pair_count(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return comb(n, 2)


def _boundary_receipts(
    *,
    source_pair: tuple[int, int],
    operator: str,
    source_side: str,
    source_value: int,
    derived_value: int,
) -> list[dict]:
    receipts: list[dict] = []
    if derived_value > 1:
        receipts.append(
            {
                "operator": operator,
                "mode": f"{source_side}_predecessor",
                "source_pair": list(source_pair),
                "source_side": source_side,
                "source_value": source_value,
                "derived_value": derived_value,
                "derived_pair": [derived_value - 1, derived_value],
                "fiber_size": None,
                "support_arity": 1,
                "support_values": [source_value],
            }
        )
    receipts.append(
        {
            "operator": operator,
            "mode": f"{source_side}_successor",
            "source_pair": list(source_pair),
            "source_side": source_side,
            "source_value": source_value,
            "derived_value": derived_value,
            "derived_pair": [derived_value, derived_value + 1],
            "fiber_size": None,
            "support_arity": 1,
            "support_values": [source_value],
        }
    )
    return receipts


def expand_pair(pair: tuple[int, int]) -> list[dict]:
    left, right = _validate_pair(pair)
    pair = (left, right)
    receipts: list[dict] = []

    receipts.append(
        {
            "operator": "prime_count@1",
            "mode": "pair_image",
            "source_pair": [left, right],
            "source_side": None,
            "source_value": None,
            "derived_value": None,
            "derived_pair": [prime_count(left), prime_count(right)],
            "fiber_size": prime_count_pair_fiber_size(pair),
            "support_arity": 2,
            "support_values": [left, right],
        }
    )

    for side, value in (("left", left), ("right", right)):
        if is_strict_divisor_record(value):
            receipts.extend(
                _boundary_receipts(
                    source_pair=pair,
                    operator="divisor_count_record@1",
                    source_side=side,
                    source_value=value,
                    derived_value=divisor_count(value),
                )
            )

    for side, value in (("left", left), ("right", right)):
        receipts.extend(
            _boundary_receipts(
                source_pair=pair,
                operator="pair_count@1",
                source_side=side,
                source_value=value,
                derived_value=pair_count(value),
            )
        )

    return receipts


def walk_registry(
    seed_pair: tuple[int, int],
    registry: set[tuple[int, int]],
    *,
    max_depth: int = 4,
) -> dict:
    seed_pair = _validate_pair(seed_pair)
    frozen_registry = {_validate_pair(pair) for pair in registry}
    queue = deque([(seed_pair, 0)])
    visited = {seed_pair}
    visit_order = [seed_pair]
    edges: list[dict] = []
    edge_keys: set[tuple] = set()

    while queue:
        source, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for receipt in expand_pair(source):
            derived = tuple(receipt["derived_pair"])
            if derived == source or derived not in frozen_registry:
                continue
            edge_key = (
                tuple(receipt["source_pair"]),
                receipt["operator"],
                receipt["mode"],
                derived,
            )
            if edge_key not in edge_keys:
                edge_keys.add(edge_key)
                edges.append(receipt)
            if derived not in visited:
                visited.add(derived)
                visit_order.append(derived)
                queue.append((derived, depth + 1))

    return {
        "method": "count-boundary-recursion/v0",
        "operators": list(FROZEN_OPERATOR_IDS),
        "seed_pair": list(seed_pair),
        "visited_pairs": [list(pair) for pair in visit_order],
        "edges": edges,
    }
