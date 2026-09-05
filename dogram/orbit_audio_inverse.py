from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from math import isfinite


@dataclass(frozen=True)
class OrbitAudioInverseReceipt:
    observed_frequencies_hz: tuple[float, ...]
    assignment: tuple[str, ...]
    assigned_period_days: tuple[float, ...]
    estimated_scale_hz_days: float
    scale_samples_hz_days: tuple[float, ...]
    max_relative_scale_residual: float


def _positive_finite(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and isfinite(float(value))
        and float(value) > 0.0
    )


def recover_period_days(
    frequencies_hz: tuple[float, ...], scale_hz_days: float
) -> tuple[float, ...]:
    """Invert the declared linear sonification f = K / T.

    This is a bounded decoder for a declared transform. It does not infer
    that any real audio carrier used this transform or that a recovered
    period identifies a physical planet without an additional witness.
    """

    if not _positive_finite(scale_hz_days):
        raise ValueError("scale_hz_days must be positive and finite")
    if not frequencies_hz or any(not _positive_finite(value) for value in frequencies_hz):
        raise ValueError("frequencies_hz must contain positive finite values")

    scale = float(scale_hz_days)
    return tuple(scale / float(frequency) for frequency in frequencies_hz)


def identify_orbits(
    observed_frequencies_hz: tuple[float, ...],
    candidate_periods: tuple[tuple[str, float], ...],
) -> OrbitAudioInverseReceipt:
    """Match unlabeled tones to declared candidate periods up to one global scale.

    For each candidate permutation, compute the implied scale samples
    `K_i = f_i * T_i`. The winning assignment minimizes the maximum relative
    disagreement of those samples around their arithmetic mean. A nonzero
    residual is retained rather than silently treated as exact equivalence.

    The search is deliberately finite and factorial, suitable only for small
    research specimens such as the five-planet Voyager/Kepler witness.
    """

    if len(observed_frequencies_hz) < 2:
        raise ValueError("at least two observed frequencies are required")
    if any(not _positive_finite(value) for value in observed_frequencies_hz):
        raise ValueError("observed frequencies must be positive and finite")
    if len(candidate_periods) != len(observed_frequencies_hz):
        raise ValueError("candidate and observed cardinalities must match")

    labels = tuple(label for label, _ in candidate_periods)
    if any(not isinstance(label, str) or not label for label in labels):
        raise ValueError("candidate labels must be non-empty strings")
    if len(set(labels)) != len(labels):
        raise ValueError("candidate labels must be unique")
    if any(not _positive_finite(period) for _, period in candidate_periods):
        raise ValueError("candidate periods must be positive and finite")

    observed = tuple(float(value) for value in observed_frequencies_hz)
    candidates = tuple((label, float(period)) for label, period in candidate_periods)

    best_key: tuple[float, tuple[str, ...]] | None = None
    best_payload: tuple[
        tuple[str, ...], tuple[float, ...], float, tuple[float, ...], float
    ] | None = None

    for candidate_order in permutations(candidates):
        assignment = tuple(label for label, _ in candidate_order)
        periods = tuple(period for _, period in candidate_order)
        scale_samples = tuple(
            frequency * period
            for frequency, period in zip(observed, periods, strict=True)
        )
        estimated_scale = sum(scale_samples) / len(scale_samples)
        residual = max(
            abs(sample - estimated_scale) / estimated_scale for sample in scale_samples
        )
        key = (residual, assignment)
        if best_key is None or key < best_key:
            best_key = key
            best_payload = (
                assignment,
                periods,
                estimated_scale,
                scale_samples,
                residual,
            )

    assert best_payload is not None
    assignment, periods, estimated_scale, scale_samples, residual = best_payload
    return OrbitAudioInverseReceipt(
        observed_frequencies_hz=observed,
        assignment=assignment,
        assigned_period_days=periods,
        estimated_scale_hz_days=estimated_scale,
        scale_samples_hz_days=scale_samples,
        max_relative_scale_residual=residual,
    )


__all__ = [
    "OrbitAudioInverseReceipt",
    "identify_orbits",
    "recover_period_days",
]
