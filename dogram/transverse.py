from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm


@dataclass
class TransverseInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class TransverseAnalysis:
    m: int
    n: int
    generators: tuple[int, ...]
    state_capacity: int
    sync_sheet_size: int
    sheet_count: int
    closure_lift_index: int
    closure_reach_count: int
    closure_sheets: tuple[int, ...]

    def to_data(self) -> dict[str, object]:
        return {
            "m": self.m,
            "n": self.n,
            "generators": list(self.generators),
            "state_capacity": self.state_capacity,
            "sync_sheet_size": self.sync_sheet_size,
            "sheet_count": self.sheet_count,
            "closure_lift_index": self.closure_lift_index,
            "closure_reach_count": self.closure_reach_count,
            "closure_sheets": list(self.closure_sheets),
        }


def _validate_dimensions(m: int, n: int) -> None:
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise TransverseInputError("INVALID_DIMENSION", "m must be a positive integer")
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise TransverseInputError("INVALID_DIMENSION", "n must be a positive integer")


def _validate_generators(generators: tuple[int, ...]) -> None:
    if not isinstance(generators, tuple) or not generators:
        raise TransverseInputError("EMPTY_GENERATOR_FAMILY", "generators must be a non-empty tuple")
    if any(not isinstance(r, int) or isinstance(r, bool) for r in generators):
        raise TransverseInputError("INVALID_GENERATOR", "every generator must be an integer")


def _validate_cut_history(cuts: tuple[int, ...]) -> None:
    if not isinstance(cuts, tuple):
        raise TransverseInputError("INVALID_CUT_HISTORY", "cuts must be a tuple")
    if any(not isinstance(r, int) or isinstance(r, bool) for r in cuts):
        raise TransverseInputError("INVALID_CUT_HISTORY", "every cut must be an integer")


def sheet_coordinate(m: int, n: int, a: int, b: int) -> int:
    _validate_dimensions(m, n)
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (a, b)):
        raise TransverseInputError("INVALID_STATE", "state coordinates must be integers")
    return (a - b) % gcd(m, n)


def _generated_sheets(d: int, generators: tuple[int, ...]) -> tuple[int, ...]:
    seen = {0}
    frontier = [0]
    normalized = tuple(r % d for r in generators)
    while frontier:
        current = frontier.pop()
        for step in normalized:
            nxt = (current + step) % d
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return tuple(sorted(seen))


def analyze_transverse(m: int, n: int, generators: tuple[int, ...]) -> TransverseAnalysis:
    _validate_dimensions(m, n)
    _validate_generators(generators)
    d = gcd(m, n)
    sheet_size = lcm(m, n)
    lift = d // gcd(d, *generators)
    sheets = _generated_sheets(d, generators)
    if len(sheets) != lift:
        raise AssertionError("quotient traversal disagrees with gcd lift formula")
    return TransverseAnalysis(
        m=m,
        n=n,
        generators=generators,
        state_capacity=m * n,
        sync_sheet_size=sheet_size,
        sheet_count=d,
        closure_lift_index=lift,
        closure_reach_count=sheet_size * lift,
        closure_sheets=sheets,
    )


def bounded_history_sheet_trace(m: int, n: int, cuts: tuple[int, ...]) -> tuple[int, ...]:
    """Return sheets reached by declared cut->complete-sync-orbit cycles."""
    _validate_dimensions(m, n)
    _validate_cut_history(cuts)
    d = gcd(m, n)
    current = 0
    trace = [current]
    for cut in cuts:
        current = (current + cut) % d
        trace.append(current)
    return tuple(trace)


def bounded_history_reach_count(m: int, n: int, cuts: tuple[int, ...]) -> int:
    """Count states covered when every recorded sheet receives a full sync orbit."""
    trace = bounded_history_sheet_trace(m, n, cuts)
    return lcm(m, n) * len(set(trace))


__all__ = [
    "TransverseAnalysis",
    "TransverseInputError",
    "analyze_transverse",
    "bounded_history_reach_count",
    "bounded_history_sheet_trace",
    "sheet_coordinate",
]
