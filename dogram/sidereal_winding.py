from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TypeAlias

ExactTurn: TypeAlias = int | Fraction


@dataclass
class DualClockInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class DualClockProjection:
    rotation_turns: Fraction
    orbit_turns: Fraction
    sidereal_turns: Fraction
    solar_turns: Fraction
    winding_receipt: Fraction

    def to_data(self) -> dict[str, tuple[int, int]]:
        def pair(value: Fraction) -> tuple[int, int]:
            return (value.numerator, value.denominator)

        return {
            "rotation_turns": pair(self.rotation_turns),
            "orbit_turns": pair(self.orbit_turns),
            "sidereal_turns": pair(self.sidereal_turns),
            "solar_turns": pair(self.solar_turns),
            "winding_receipt": pair(self.winding_receipt),
        }


def _exact_fraction(value: ExactTurn, label: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise DualClockInputError(
            "NON_EXACT_INPUT",
            f"{label} must be an int or fractions.Fraction; floats are refused",
        )
    return Fraction(value)


def project_dual_clock(
    rotation_turns: ExactTurn,
    orbit_turns: ExactTurn,
) -> DualClockProjection:
    """Project one underlying rotation/orbit state into sidereal and solar counts.

    The model is purely kinematic:

        sidereal = rotation
        solar    = rotation - orbit

    so the projection delta preserves orbital winding exactly:

        sidereal - solar = orbit
    """

    rotation = _exact_fraction(rotation_turns, "rotation_turns")
    orbit = _exact_fraction(orbit_turns, "orbit_turns")
    sidereal = rotation
    solar = rotation - orbit

    return DualClockProjection(
        rotation_turns=rotation,
        orbit_turns=orbit,
        sidereal_turns=sidereal,
        solar_turns=solar,
        winding_receipt=sidereal - solar,
    )


__all__ = [
    "DualClockInputError",
    "DualClockProjection",
    "ExactTurn",
    "project_dual_clock",
]
