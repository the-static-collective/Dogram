"""SUCCESSOR-DESCENT-001: finite nondeterministic one-step quotient pressure.

Research only. Successor possibility is not event occurrence or execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json


def _typed(value: object) -> tuple[object, ...]:
    if value is None:
        return ('none',)
    if type(value) is bool:
        return ('bool', value)
    if type(value) is int:
        return ('int', value)
    if type(value) is str:
        return ('str', value)
    if type(value) is tuple:
        return ('tuple', tuple(_typed(v) for v in value))
    raise ValueError('projection values must be None, bool, int, str or tuples thereof')


@dataclass(frozen=True)
class SuccessorWitness:
    states: tuple[str, str]
    shared_projection: object
    raw_successors: tuple[tuple[str, ...], tuple[str, ...]]
    projected_successors: tuple[tuple[object, ...], tuple[object, ...]]
    left_only: tuple[object, ...]
    right_only: tuple[object, ...]


@dataclass(frozen=True)
class SuccessorMode:
    status: str  # preserved | counterexample | inconclusive
    checked_pairs: int
    possible_pairs: int
    witness: SuccessorWitness | None
    induced: tuple[tuple[object, tuple[object, ...]], ...] | None


@dataclass(frozen=True)
class SuccessorDescentReceipt:
    input_sha256: str
    states: tuple[str, ...]
    projection: tuple[object, ...]
    collapse_classes: tuple[tuple[str, ...], ...]
    possible_pairs: int
    max_pair_checks_per_mode: int
    raw: SuccessorMode
    projected: SuccessorMode


def analyze_successor_descent(
    states: tuple[str, ...],
    projection: tuple[object, ...],
    successors: tuple[tuple[str, ...], ...],
    *,
    max_pair_checks: int = 4096,
) -> SuccessorDescentReceipt:
    """Check whether identical quotient inputs have identical successor sets.

    Raw and projected successor sets are checked independently. The projected
    induced relation exists only if every within-fiber pair is checked.
    """
    if type(states) is not tuple or not 1 <= len(states) <= 64:
        raise ValueError('states must be a nonempty tuple of at most 64 labels')
    if any(type(s) is not str or not s for s in states) or len(set(states)) != len(states):
        raise ValueError('states must be unique nonempty strings')
    if type(projection) is not tuple or len(projection) != len(states):
        raise ValueError('projection must give exactly one value per state')
    if type(successors) is not tuple or len(successors) != len(states):
        raise ValueError('successors must give exactly one tuple per state')
    if type(max_pair_checks) is not int or max_pair_checks < 0:
        raise ValueError('max_pair_checks must be a nonnegative integer')
    keys = tuple(_typed(v) for v in projection)
    index = {s: i for i, s in enumerate(states)}
    raw_rows: list[tuple[int, ...]] = []
    for row in successors:
        if type(row) is not tuple:
            raise ValueError('each successor row must be a tuple')
        if any(type(s) is not str or s not in index for s in row) or len(set(row)) != len(row):
            raise ValueError('successors must name distinct declared states')
        raw_rows.append(tuple(sorted(index[s] for s in row)))
    raw = tuple(raw_rows)

    projection_order: list[tuple[object, ...]] = []
    representative: dict[tuple[object, ...], object] = {}
    for value, key in zip(projection, keys):
        if key not in representative:
            projection_order.append(key)
            representative[key] = value
    projection_index = {key: i for i, key in enumerate(projection_order)}
    projected = tuple(tuple(sorted({keys[target] for target in row}, key=projection_index.__getitem__)) for row in raw)
    fiber_map: dict[tuple[object, ...], list[int]] = {}
    for i, key in enumerate(keys):
        fiber_map.setdefault(key, []).append(i)
    fibers = tuple(tuple(fiber) for fiber in fiber_map.values())
    pairs = tuple((left, right) for fiber in fibers for n, left in enumerate(fiber) for right in fiber[n + 1:])

    payload = {
        'schema': 'dogram/successor-descent-001/v0',
        'states': states,
        'projection': keys,
        'successors': raw,
        'max_pair_checks': max_pair_checks,
    }
    digest = sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()

    def check(projected_mode: bool) -> SuccessorMode:
        outputs = projected if projected_mode else raw
        checked = 0
        for left, right in pairs:
            if checked >= max_pair_checks:
                break
            checked += 1
            if outputs[left] == outputs[right]:
                continue
            raw_left = tuple(states[i] for i in raw[left])
            raw_right = tuple(states[i] for i in raw[right])
            proj_left = tuple(representative[k] for k in projected[left])
            proj_right = tuple(representative[k] for k in projected[right])
            if projected_mode:
                left_only = tuple(representative[k] for k in projected[left] if k not in projected[right])
                right_only = tuple(representative[k] for k in projected[right] if k not in projected[left])
            else:
                left_only = tuple(states[i] for i in raw[left] if i not in raw[right])
                right_only = tuple(states[i] for i in raw[right] if i not in raw[left])
            witness = SuccessorWitness(
                states=(states[left], states[right]),
                shared_projection=projection[left],
                raw_successors=(raw_left, raw_right),
                projected_successors=(proj_left, proj_right),
                left_only=left_only,
                right_only=right_only,
            )
            return SuccessorMode('counterexample', checked, len(pairs), witness, None)
        if checked < len(pairs):
            return SuccessorMode('inconclusive', checked, len(pairs), None, None)
        induced = None
        if projected_mode:
            induced = tuple(
                (projection[fiber[0]], tuple(representative[k] for k in projected[fiber[0]]))
                for fiber in fibers
            )
        return SuccessorMode('preserved', checked, len(pairs), None, induced)

    return SuccessorDescentReceipt(
        digest, states, projection, tuple(tuple(states[i] for i in fiber) for fiber in fibers),
        len(pairs), max_pair_checks, check(False), check(True),
    )


__all__ = ['SuccessorWitness', 'SuccessorMode', 'SuccessorDescentReceipt', 'analyze_successor_descent']
