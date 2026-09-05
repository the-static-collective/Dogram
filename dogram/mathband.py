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
    declared_probe_family: tuple[str, ...]
    outcomes: tuple[ProbeOutcome, ...]
    extra_a: tuple[str, ...]
    extra_b: tuple[str, ...]
    lossy_steps: tuple[str, ...]
    exactness: Exactness
    first_decisive_probe: str | None
    refusals: tuple[str, ...]


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and isfinite(float(value))
    )


def _validate_probe(probe: ProbeObservation) -> None:
    if not _nonempty_text(probe.name):
        raise ValueError("probe names must be non-empty strings")
    if probe.comparison not in ("exact", "numeric"):
        raise ValueError("unsupported comparison kind")
    if not _finite_number(probe.tolerance) or float(probe.tolerance) < 0.0:
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
    declared_probe_family = tuple(names)

    provided = set(provided_assumptions)
    missing = tuple(
        assumption for assumption in required_assumptions if assumption not in provided
    )
    if missing:
        return MathBandReceipt(
            bridge_ref=bridge_ref,
            voice_a_ref=voice_a_ref,
            voice_b_ref=voice_b_ref,
            declared_assumptions=provided_assumptions,
            declared_transforms=declared_transforms,
            declared_probe_family=declared_probe_family,
            outcomes=(),
            extra_a=extra_a,
            extra_b=extra_b,
            lossy_steps=lossy_steps,
            exactness="refused",
            first_decisive_probe=None,
            refusals=tuple(f"missing assumption: {item}" for item in missing),
        )

    outcomes: list[ProbeOutcome] = []

    for probe in probes:
        if not probe.left_defined or not probe.right_defined:
            outcomes.append(
                ProbeOutcome(
                    name=probe.name,
                    status="UNMAPPED",
                    left=probe.left,
                    right=probe.right,
                    delta=None,
                    residual=None,
                    decisive=probe.decisive,
                )
            )
            continue

        residual: float | None = None
        if probe.comparison == "numeric":
            if not _finite_number(probe.left) or not _finite_number(probe.right):
                raise ValueError(
                    "numeric probes require finite numbers and nonnegative tolerance"
                )
            residual = abs(float(probe.left) - float(probe.right))
            if residual == 0.0:
                status: ProbeStatus = "PRESERVED"
                delta = None
            elif residual <= probe.tolerance:
                status = "RESIDUAL"
                delta = (probe.left, probe.right)
            elif probe.must_preserve:
                status = "BROKEN"
                delta = (probe.left, probe.right)
            else:
                status = "CHANGED"
                delta = (probe.left, probe.right)
        elif probe.left == probe.right:
            status = "PRESERVED"
            delta = None
        else:
            status = "BROKEN" if probe.must_preserve else "CHANGED"
            delta = (probe.left, probe.right)

        outcomes.append(
            ProbeOutcome(
                name=probe.name,
                status=status,
                left=probe.left,
                right=probe.right,
                delta=delta,
                residual=residual,
                decisive=probe.decisive,
            )
        )

    first_decisive_probe = next(
        (
            outcome.name
            for outcome in outcomes
            if outcome.decisive and outcome.status == "BROKEN"
        ),
        None,
    )
    exactness: Exactness = (
        "approximate"
        if any(outcome.status == "RESIDUAL" for outcome in outcomes) or lossy_steps
        else "exact"
    )

    return MathBandReceipt(
        bridge_ref=bridge_ref,
        voice_a_ref=voice_a_ref,
        voice_b_ref=voice_b_ref,
        declared_assumptions=provided_assumptions,
        declared_transforms=declared_transforms,
        declared_probe_family=declared_probe_family,
        outcomes=tuple(outcomes),
        extra_a=extra_a,
        extra_b=extra_b,
        lossy_steps=lossy_steps,
        exactness=exactness,
        first_decisive_probe=first_decisive_probe,
        refusals=(),
    )


__all__ = [
    "MathBandReceipt",
    "ProbeObservation",
    "ProbeOutcome",
    "evaluate_bridge",
]
