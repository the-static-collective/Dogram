from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


ProbeStatus = Literal["PRESERVED", "CHANGED", "BROKEN", "UNMAPPED", "RESIDUAL"]
ComparisonKind = Literal["exact", "numeric"]
Exactness = Literal["exact", "approximate", "refused"]


@dataclass(frozen=True)
class ProbeObservation:
    name: str
    left: object | None
    right: object | None
    comparison: ComparisonKind = "exact"
    tolerance: float = 0.0
    must_preserve: bool = True
    decisive: bool = False
    left_defined: bool = True
    right_defined: bool = True


@dataclass(frozen=True)
class ProbeOutcome:
    name: str
    status: ProbeStatus
    left: object | None
    right: object | None
    delta: tuple[object | None, object | None] | None
    residual: float | None
    decisive: bool


@dataclass(frozen=True)
class MathBandReceipt:
    bridge_ref: str
    voice_a_ref: str
    voice_b_ref: str
    declared_assumptions: tuple[str, ...]
    declared_transforms: tuple[str, ...]
    outcomes: tuple[ProbeOutcome, ...]
    extra_a: tuple[str, ...]
    extra_b: tuple[str, ...]
    lossy_steps: tuple[str, ...]
    exactness: Exactness
    first_decisive_probe: str | None
    refusals: tuple[str, ...]


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _validate_probe(probe: ProbeObservation) -> None:
    if not _nonempty_text(probe.name):
        raise ValueError("probe names must be non-empty strings")
    if probe.comparison not in ("exact", "numeric"):
        raise ValueError("unsupported comparison kind")
    if not isinstance(probe.tolerance, (int, float)) or isinstance(probe.tolerance, bool):
        raise ValueError("probe tolerance must be numeric")
    if not isfinite(float(probe.tolerance)) or float(probe.tolerance) < 0.0:
        raise ValueError("probe tolerance must be finite and non-negative")


def evaluate_bridge(
    *,
    bridge_ref: str,
    voice_a_ref: str,
    voice_b_ref: str,
    required_assumptions: tuple[str, ...],
    provided_assumptions: tuple[str, ...],
    probes: tuple[ProbeObservation, ...],
    declared_transforms: tuple[str, ...] = (),
    extra_a: tuple[str, ...] = (),
    extra_b: tuple[str, ...] = (),
    lossy_steps: tuple[str, ...] = (),
) -> MathBandReceipt:
    """Evaluate already-constituted finite bridge probes without semantic promotion."""

    if not all(_nonempty_text(value) for value in (bridge_ref, voice_a_ref, voice_b_ref)):
        raise ValueError("bridge and voice refs must be non-empty strings")
    if not probes:
        raise ValueError("at least one probe is required")

    names: list[str] = []
    for probe in probes:
        if not isinstance(probe, ProbeObservation):
            raise ValueError("probes must be ProbeObservation values")
        _validate_probe(probe)
        names.append(probe.name)
    if len(set(names)) != len(names):
        raise ValueError("probe names must be unique")

    outcomes: list[ProbeOutcome] = []
    first_decisive_probe: str | None = None

    for probe in probes:
        if probe.comparison != "exact":
            raise ValueError("numeric comparison is not implemented in the exact floor")

        if probe.left == probe.right:
            status: ProbeStatus = "PRESERVED"
            delta = None
        else:
            status = "BROKEN" if probe.must_preserve else "CHANGED"
            delta = (probe.left, probe.right)
            if probe.decisive and status == "BROKEN" and first_decisive_probe is None:
                first_decisive_probe = probe.name

        outcomes.append(
            ProbeOutcome(
                name=probe.name,
                status=status,
                left=probe.left,
                right=probe.right,
                delta=delta,
                residual=None,
                decisive=probe.decisive,
            )
        )

    return MathBandReceipt(
        bridge_ref=bridge_ref,
        voice_a_ref=voice_a_ref,
        voice_b_ref=voice_b_ref,
        declared_assumptions=provided_assumptions,
        declared_transforms=declared_transforms,
        outcomes=tuple(outcomes),
        extra_a=extra_a,
        extra_b=extra_b,
        lossy_steps=lossy_steps,
        exactness="exact",
        first_decisive_probe=first_decisive_probe,
        refusals=(),
    )


__all__ = [
    "MathBandReceipt",
    "ProbeObservation",
    "ProbeOutcome",
    "evaluate_bridge",
]
