from __future__ import annotations

from fractions import Fraction
from typing import Mapping


_STATES = ("a", "b", "c", "d")
_TARGET = {"a": 1, "b": 1, "c": 0, "d": 0}


def adaptive_receipt() -> dict[str, object]:
    """Return the frozen two-stage adaptive policy receipt."""
    return {
        "policy": "adaptive",
        "target_labels": dict(_TARGET),
        "paths": {
            "a": ("root",),
            "b": ("root", "branch"),
            "c": ("root", "branch"),
            "d": ("root", "branch"),
        },
        "probe_costs": {"root": 1, "branch": 2},
        "state_costs": {"a": 1, "b": 3, "c": 3, "d": 3},
    }


def fixed_receipt() -> dict[str, object]:
    """Return the frozen one-shot policy receipt computing the same target."""
    return {
        "policy": "fixed",
        "target_labels": dict(_TARGET),
        "paths": {state: ("fixed",) for state in _STATES},
        "probe_costs": {"fixed": 2},
        "state_costs": {state: 2 for state in _STATES},
    }


def worst_case_cost(receipt: Mapping[str, object]) -> int:
    """Compute worst-case policy cost from the frozen state-cost vector."""
    state_costs = receipt.get("state_costs")
    if not isinstance(state_costs, Mapping) or set(state_costs) != set(_STATES):
        raise ValueError("receipt must contain state_costs for exactly a,b,c,d")
    values = list(state_costs.values())
    if not all(isinstance(value, int) and value >= 0 for value in values):
        raise ValueError("state costs must be nonnegative integers")
    return max(values)


def expected_cost(
    receipt: Mapping[str, object],
    prior: Mapping[str, Fraction] | None,
) -> Fraction:
    """Compute exact expected cost only from an explicitly declared prior."""
    if prior is None or set(prior) != set(_STATES):
        raise ValueError("expected cost requires a declared prior on exactly a,b,c,d")
    if not all(isinstance(weight, Fraction) and weight >= 0 for weight in prior.values()):
        raise ValueError("prior weights must be nonnegative Fractions")
    if sum(prior.values(), Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("prior weights must sum exactly to one")

    state_costs = receipt.get("state_costs")
    if not isinstance(state_costs, Mapping) or set(state_costs) != set(_STATES):
        raise ValueError("receipt must contain state_costs for exactly a,b,c,d")

    return sum(
        (prior[state] * int(state_costs[state]) for state in _STATES),
        Fraction(0, 1),
    )
