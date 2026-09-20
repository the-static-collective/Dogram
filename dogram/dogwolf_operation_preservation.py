"""DOGWOLF-001: finite, budgeted operation-preservation counterexample hunt.

Research only. This module accepts predeclared tables, not executable user code,
and does not add a public Dogram operator or an external dependency.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
import json


def _typed(value: object) -> tuple[object, ...]:
    """Give supported finite values type-sensitive, immutable equality keys."""
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
    raise ValueError("values must be None, bool, int, str, or tuples thereof")


@dataclass(frozen=True)
class Counterexample:
    left_state: str
    right_state: str
    shared_projection: object
    left_result: object
    right_result: object


@dataclass(frozen=True)
class OperationProbe:
    operation: str
    status: str  # preserved | counterexample | inconclusive
    checked_pairs: int
    possible_pairs: int
    counterexample: Counterexample | None


@dataclass(frozen=True)
class DogwolfReceipt:
    input_sha256: str
    states: tuple[str, ...]
    projection: tuple[object, ...]
    collapse_classes: tuple[tuple[str, ...], ...]
    max_pair_checks_per_operation: int
    probes: tuple[OperationProbe, ...]


def probe_operation_preservation(
    states: tuple[str, ...],
    projection: tuple[object, ...],
    operations: Mapping[str, tuple[object, ...]],
    *,
    max_pair_checks: int = 4096,
) -> DogwolfReceipt:
    """Test if each declared result table factors through a finite projection.

    A counterexample proves non-factorization for that operation. A preserved
    status means all pairs within every declared fiber were checked. An
    uncompleted search without a counterexample is inconclusive, never proof.
    The bound applies separately to each operation; no evaluation is delegated
    to Python callables or to the optional Wolfram oracle.
    """
    if type(states) is not tuple or not states or len(states) > 64:
        raise ValueError("states must be a nonempty tuple of at most 64 labels")
    if any(type(state) is not str or not state for state in states) or len(set(states)) != len(states):
        raise ValueError("state labels must be distinct nonempty strings")
    if type(projection) is not tuple or len(projection) != len(states):
        raise ValueError("projection must have exactly one entry per state")
    if type(max_pair_checks) is not int or max_pair_checks < 0:
        raise ValueError("max_pair_checks must be a nonnegative integer")
    if not isinstance(operations, Mapping) or not 1 <= len(operations) <= 16:
        raise ValueError("operations must contain between 1 and 16 named result tables")

    projection_keys = tuple(_typed(value) for value in projection)
    operation_items = tuple(operations.items())
    for name, outputs in operation_items:
        if type(name) is not str or not name:
            raise ValueError("operation names must be nonempty strings")
        if type(outputs) is not tuple or len(outputs) != len(states):
            raise ValueError("each operation needs one result per state")
        for value in outputs:
            _typed(value)

    payload = {
        "schema": "dogram/dogwolf-operation-preservation/v0",
        "states": states,
        "projection": projection_keys,
        "operations": [(name, tuple(_typed(value) for value in outputs)) for name, outputs in operation_items],
        "max_pair_checks": max_pair_checks,
    }
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

    fiber_map: dict[tuple[object, ...], list[int]] = {}
    for index, key in enumerate(projection_keys):
        fiber_map.setdefault(key, []).append(index)
    indices = tuple(tuple(fiber) for fiber in fiber_map.values())
    possible_pairs = sum(len(fiber) * (len(fiber) - 1) // 2 for fiber in indices)

    probes: list[OperationProbe] = []
    for name, outputs in operation_items:
        output_keys = tuple(_typed(value) for value in outputs)
        checked = 0
        witness: Counterexample | None = None
        for fiber in indices:
            for left_position, left in enumerate(fiber):
                for right in fiber[left_position + 1 :]:
                    if checked >= max_pair_checks:
                        break
                    checked += 1
                    if output_keys[left] != output_keys[right]:
                        witness = Counterexample(
                            left_state=states[left],
                            right_state=states[right],
                            shared_projection=projection[left],
                            left_result=outputs[left],
                            right_result=outputs[right],
                        )
                        break
                if witness is not None or checked >= max_pair_checks:
                    break
            if witness is not None or checked >= max_pair_checks:
                break
        status = (
            "counterexample" if witness is not None else
            "preserved" if checked == possible_pairs else
            "inconclusive"
        )
        probes.append(OperationProbe(name, status, checked, possible_pairs, witness))

    return DogwolfReceipt(
        input_sha256=digest,
        states=states,
        projection=projection,
        collapse_classes=tuple(tuple(states[index] for index in fiber) for fiber in indices),
        max_pair_checks_per_operation=max_pair_checks,
        probes=tuple(probes),
    )


__all__ = ["Counterexample", "OperationProbe", "DogwolfReceipt", "probe_operation_preservation"]
