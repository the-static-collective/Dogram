"""DESCEND-001: finite, declared state-transition descent through a quotient.

Research-only and pure: no public Dogram dispatch, execution authority, or
claims about historical occurrences or evidence.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
import json


def _typed(value: object) -> tuple[object, ...]:
    """Type-sensitive finite projection key (bool and int stay distinct)."""
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
    raise ValueError("projection values must be None, bool, int, str, or tuples thereof")


@dataclass(frozen=True)
class DescentCounterexample:
    states: tuple[str, str]
    shared_projection: object
    successors: tuple[str, str]
    projected_successors: tuple[object, object]


@dataclass(frozen=True)
class DescentMode:
    status: str  # preserved | counterexample | inconclusive
    checked_pairs: int
    possible_pairs: int
    counterexample: DescentCounterexample | None


@dataclass(frozen=True)
class DescentProbe:
    operation: str
    raw: DescentMode
    projected: DescentMode
    induced_table: tuple[tuple[object, object], ...] | None


@dataclass(frozen=True)
class DescentReceipt:
    input_sha256: str
    states: tuple[str, ...]
    projection: tuple[object, ...]
    collapse_classes: tuple[tuple[str, ...], ...]
    possible_pairs: int
    max_pair_checks_per_mode: int
    probes: tuple[DescentProbe, ...]


def analyze_descent(
    states: tuple[str, ...],
    projection: tuple[object, ...],
    operations: Mapping[str, tuple[str, ...]],
    *,
    max_pair_checks: int = 4096,
) -> DescentReceipt:
    """Check q(x)=q(y) => f(x)=f(y) and q(f(x))=q(f(y)) separately.

    Operations are declared total state-to-state tables (not callbacks).
    A preserved projected mode determines an induced operation on q(X).
    An unfinished check without a counterexample is inconclusive.
    """
    if type(states) is not tuple or not 1 <= len(states) <= 64:
        raise ValueError("states must be a nonempty tuple of at most 64 labels")
    if any(type(s) is not str or not s for s in states) or len(set(states)) != len(states):
        raise ValueError("states must be distinct nonempty strings")
    if type(projection) is not tuple or len(projection) != len(states):
        raise ValueError("projection must provide exactly one entry per state")
    if type(max_pair_checks) is not int or max_pair_checks < 0:
        raise ValueError("max_pair_checks must be a nonnegative integer")
    if not isinstance(operations, Mapping) or not 1 <= len(operations) <= 16:
        raise ValueError("operations must contain 1..16 declared transition tables")

    keys = tuple(_typed(v) for v in projection)
    state_index = {state: index for index, state in enumerate(states)}
    if any(type(name) is not str or not name for name in operations):
        raise ValueError("operation names must be nonempty strings")
    op_items = tuple(sorted(operations.items()))
    for name, targets in op_items:
        if type(targets) is not tuple or len(targets) != len(states):
            raise ValueError("each transition table must have exactly one successor per state")
        if any(type(target) is not str or target not in state_index for target in targets):
            raise ValueError("each transition target must name a declared state")

    payload = {
        "schema": "dogram/descend-001/v0",
        "states": states,
        "projection": keys,
        "operations": op_items,
        "max_pair_checks": max_pair_checks,
    }
    digest = sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    fiber_map: dict[tuple[object, ...], list[int]] = {}
    for index, key in enumerate(keys):
        fiber_map.setdefault(key, []).append(index)
    fibers = tuple(tuple(members) for members in fiber_map.values())
    collapse_classes = tuple(tuple(states[i] for i in fiber) for fiber in fibers)
    possible_pairs = sum(len(fiber) * (len(fiber) - 1) // 2 for fiber in fibers)

    probes: list[DescentProbe] = []
    for name, targets in op_items:
        successors = tuple(state_index[target] for target in targets)
        projected_successors = tuple(keys[j] for j in successors)
        modes: list[DescentMode] = []
        for outputs in (successors, projected_successors):
            checked = 0
            witness: DescentCounterexample | None = None
            for fiber in fibers:
                for left_pos, left in enumerate(fiber):
                    for right in fiber[left_pos + 1 :]:
                        if checked >= max_pair_checks or witness is not None:
                            break
                        checked += 1
                        if outputs[left] != outputs[right]:
                            witness = DescentCounterexample(
                                states=(states[left], states[right]),
                                shared_projection=projection[left],
                                successors=(targets[left], targets[right]),
                                projected_successors=(projection[successors[left]], projection[successors[right]]),
                            )
                            break
                    if checked >= max_pair_checks or witness is not None:
                        break
                if checked >= max_pair_checks or witness is not None:
                    break
            status = ("counterexample" if witness is not None else
                      "preserved" if checked == possible_pairs else "inconclusive")
            modes.append(DescentMode(status, checked, possible_pairs, witness))
        induced = None
        if modes[1].status == "preserved":
            induced = tuple((projection[fiber[0]], projection[successors[fiber[0]]]) for fiber in fibers)
        probes.append(DescentProbe(name, modes[0], modes[1], induced))

    return DescentReceipt(digest, states, projection, collapse_classes,
                          possible_pairs, max_pair_checks, tuple(probes))


__all__ = ["DescentCounterexample", "DescentMode", "DescentProbe", "DescentReceipt", "analyze_descent"]
