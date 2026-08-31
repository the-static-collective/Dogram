from __future__ import annotations

from dataclasses import dataclass
from math import gcd


@dataclass
class MappingTorusInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class MappingTorusAnalysis:
    fiber_count: int
    shift: int
    normalized_shift: int
    components: int
    orbit_length: int

    def to_data(self) -> dict[str, int]:
        return {
            "fiber_count": self.fiber_count,
            "shift": self.shift,
            "normalized_shift": self.normalized_shift,
            "components": self.components,
            "orbit_length": self.orbit_length,
        }


@dataclass(frozen=True)
class WindingDecomposition:
    fiber_count: int
    traversal_count: int
    winding: int
    residue: int

    def to_data(self) -> dict[str, int]:
        return {
            "fiber_count": self.fiber_count,
            "traversal_count": self.traversal_count,
            "winding": self.winding,
            "residue": self.residue,
        }


@dataclass(frozen=True)
class RelativeRealignment:
    fiber_count: int
    shift_a: int
    shift_b: int
    relative_delta: int
    realignment_period: int

    def to_data(self) -> dict[str, int]:
        return {
            "fiber_count": self.fiber_count,
            "shift_a": self.shift_a,
            "shift_b": self.shift_b,
            "relative_delta": self.relative_delta,
            "realignment_period": self.realignment_period,
        }


@dataclass(frozen=True)
class RationalValue:
    fiber_count: int
    shift: int
    longitudinal_index: int
    fiber_mode: int
    numerator: int
    denominator: int

    def to_data(self) -> dict[str, int]:
        return {
            "fiber_count": self.fiber_count,
            "shift": self.shift,
            "longitudinal_index": self.longitudinal_index,
            "fiber_mode": self.fiber_mode,
            "numerator": self.numerator,
            "denominator": self.denominator,
        }


def _validate_fiber_count(value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise MappingTorusInputError(
            "INVALID_FIBER_COUNT", "fiber_count must be a positive integer"
        )


def _validate_integer(value: int, label: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise MappingTorusInputError("INVALID_INTEGER", f"{label} must be an integer")


def analyze_mapping_torus(fiber_count: int, shift: int) -> MappingTorusAnalysis:
    """Analyze the finite-fiber return map j -> j + shift (mod fiber_count)."""

    _validate_fiber_count(fiber_count)
    _validate_integer(shift, "shift")
    components = gcd(fiber_count, shift)
    return MappingTorusAnalysis(
        fiber_count=fiber_count,
        shift=shift,
        normalized_shift=shift % fiber_count,
        components=components,
        orbit_length=fiber_count // components,
    )


def decompose_winding(
    fiber_count: int, traversal_count: int
) -> WindingDecomposition:
    """Return exact Euclidean winding + residue for a declared traversal count."""

    _validate_fiber_count(fiber_count)
    _validate_integer(traversal_count, "traversal_count")
    winding, residue = divmod(traversal_count, fiber_count)
    return WindingDecomposition(
        fiber_count=fiber_count,
        traversal_count=traversal_count,
        winding=winding,
        residue=residue,
    )


def relative_realignment(
    fiber_count: int, shift_a: int, shift_b: int
) -> RelativeRealignment:
    """Return the first positive round count at which two shifts re-align."""

    _validate_fiber_count(fiber_count)
    _validate_integer(shift_a, "shift_a")
    _validate_integer(shift_b, "shift_b")
    delta_raw = shift_a - shift_b
    return RelativeRealignment(
        fiber_count=fiber_count,
        shift_a=shift_a,
        shift_b=shift_b,
        relative_delta=delta_raw % fiber_count,
        realignment_period=fiber_count // gcd(fiber_count, delta_raw),
    )


def twisted_mode_fraction(
    fiber_count: int,
    shift: int,
    longitudinal_index: int,
    fiber_mode: int,
) -> RationalValue:
    """Return the exact reduced fraction n + k*shift/fiber_count."""

    _validate_fiber_count(fiber_count)
    _validate_integer(shift, "shift")
    _validate_integer(longitudinal_index, "longitudinal_index")
    _validate_integer(fiber_mode, "fiber_mode")
    numerator = longitudinal_index * fiber_count + fiber_mode * shift
    denominator = fiber_count
    divisor = gcd(abs(numerator), denominator)
    return RationalValue(
        fiber_count=fiber_count,
        shift=shift,
        longitudinal_index=longitudinal_index,
        fiber_mode=fiber_mode,
        numerator=numerator // divisor,
        denominator=denominator // divisor,
    )


__all__ = [
    "MappingTorusAnalysis",
    "MappingTorusInputError",
    "RationalValue",
    "RelativeRealignment",
    "WindingDecomposition",
    "analyze_mapping_torus",
    "decompose_winding",
    "relative_realignment",
    "twisted_mode_fraction",
]
