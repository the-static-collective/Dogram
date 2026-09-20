"""COMMUTE-001: bounded finite operation-order comparison.

Research-only; equality of resulting states or projections does not establish
identity of supplied paths, independence, historical occurrence or authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json


def _typed(value: object) -> tuple[object, ...]:
    """Encode finite projection values with type-sensitive equality keys."""
    if value is None:
        return ("none",)
    if type(value) is bool:
        return ("bool", value)
    if type(value) is int:
        return ("int", value)
    if type(value) is str:
        return ("str", value)
    if type(value) is tuple:
        return ("tuple", tuple(_typed(item) for item in value))
    raise ValueError("projection values must be None, bool, int, str or tuples thereof")


@dataclass(frozen=True)
class OrderedPaths:
    origin: str
    first_then_second: tuple[str, str, str]
    second_then_first: tuple[str, str, str]


@dataclass(frozen=True)
class CommutationWitness:
    origin: str
    first_then_second: tuple[str, str, str]
    second_then_first: tuple[str, str, str]
    projected_endpoints: tuple[object, object]


@dataclass(frozen=True)
class CommutationMode:
    status: str  # preserved | counterexample | inconclusive
    checked_states: int
    total_states: int
    witness: CommutationWitness | None


@dataclass(frozen=True)
class CommutationReceipt:
    input_sha256: str
    states: tuple[str, ...]
    projection: tuple[object, ...]
    operation_names: tuple[str, str]
    max_state_checks_per_mode: int
    paths: tuple[OrderedPaths, ...]
    raw: CommutationMode
    projected: CommutationMode


def analyze_commutation(
    states: tuple[str, ...],
    projection: tuple[object, ...],
    first: tuple[str, tuple[str, ...]],
    second: tuple[str, tuple[str, ...]],
    *,
    max_state_checks: int = 64,
) -> CommutationReceipt:
    """Check g(f(x)) == f(g(x)), in raw and declared projected endpoints.

    Every declared operation is a total, inert state-to-state lookup table.
    Comparison is pointwise on the declared finite carrier, independently
    budgeted per mode. No assumption that either map descends to the quotient.
    """
    if type(states) is not tuple or not 1 <= len(states) <= 64:
        raise ValueError("states must be a nonempty tuple of at most 64 labels")
    if any(type(s) is not str or not s for s in states) or len(set(states)) != len(states):
        raise ValueError("states must be distinct nonempty strings")
    if type(projection) is not tuple or len(projection) != len(states):
        raise ValueError("projection must provide one value per state")
    keys = tuple(_typed(v) for v in projection)
    if type(max_state_checks) is not int or max_state_checks < 0:
        raise ValueError("max_state_checks must be a nonnegative integer")

    index = {name: i for i, name in enumerate(states)}
    for op in (first, second):
        if type(op) is not tuple or len(op) != 2:
            raise ValueError("each operation must be a (name, targets) tuple")
        name, targets = op
        if type(name) is not str or not name:
            raise ValueError("operation names must be nonempty strings")
        if type(targets) is not tuple or len(targets) != len(states):
            raise ValueError("operation targets must be a tuple with one target per state")
        if any(type(target) is not str or target not in index for target in targets):
            raise ValueError("all operation targets must be declared state labels")
    if first[0] == second[0]:
        raise ValueError("operation names must be distinct")

    payload = {
        "schema": "dogram/commute-001/v0",
        "states": states,
        "projection": keys,
        "first": first,
        "second": second,
        "max_state_checks": max_state_checks,
    }
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
    first_map, second_map = first[1], second[1]
    paths = tuple(
        OrderedPaths(
            origin=s,
            first_then_second=(s, first_map[i], second_map[index[first_map[i]]]),
            second_then_first=(s, second_map[i], first_map[index[second_map[i]]]),
        )
        for i, s in enumerate(states)
    )

    def check(projected_mode: bool) -> CommutationMode:
        checked = 0
        for path in paths:
            if checked >= max_state_checks:
                break
            checked += 1
            left = path.first_then_second[-1]
            right = path.second_then_first[-1]
            left_key, right_key = keys[index[left]], keys[index[right]]
            different = (left_key != right_key) if projected_mode else (left != right)
            if different:
                witness = CommutationWitness(
                    path.origin, path.first_then_second, path.second_then_first,
                    (projection[index[left]], projection[index[right]]),
                )
                return CommutationMode("counterexample", checked, len(states), witness)
        if checked < len(states):
            return CommutationMode("inconclusive", checked, len(states), None)
        return CommutationMode("preserved", checked, len(states), None)

    return CommutationReceipt(
        digest, states, projection, (first[0], second[0]), max_state_checks,
        paths, check(False), check(True),
    )


__all__ = [
    "OrderedPaths", "CommutationWitness", "CommutationMode", "CommutationReceipt",
    "analyze_commutation",
]
