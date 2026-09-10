"""Bounded research kernel for TAYLOR-MAP-FIBER-001.

This module separates two theorem-level facts from finite computation:

1. Borel's theorem supplies existence of a smooth germ realizing arbitrary
   formal Taylor data.
2. A nonzero flat smooth germ lies in the kernel of the Taylor map.

The module does not construct a general Borel realization and does not select
any canonical representative from a Taylor fiber.
"""

from __future__ import annotations

import math
from typing import Iterable


def polynomial_value(taylor_coefficients: Iterable[float], x: float) -> float:
    """Evaluate a polynomial whose entries are Taylor coefficients."""
    return sum(coefficient * (x ** degree) for degree, coefficient in enumerate(taylor_coefficients))


def flat_value(x: float) -> float:
    """Evaluate h(x)=exp(-1/x^2), extended by h(0)=0."""
    if x == 0.0:
        return 0.0
    return math.exp(-1.0 / (x * x))


def fiber_value(taylor_coefficients: Iterable[float], flat_scale: float, x: float) -> float:
    """Evaluate p(x) + c h(x) for the frozen Taylor-fiber family."""
    return polynomial_value(taylor_coefficients, x) + flat_scale * flat_value(x)


def fiber_collision_receipt(
    taylor_coefficients: Iterable[float],
    flat_scales: Iterable[float],
    *,
    flat_kernel_fact_declared: bool,
) -> dict[str, object]:
    """Receipt a finite family inside one complete Taylor fiber.

    Equality of complete Taylor series is theorem-gated: it uses the declared
    fact that every derivative of the frozen flat germ vanishes at zero.
    Distinctness is witnessed at x=1/2, where h(x)>0.
    """
    if not flat_kernel_fact_declared:
        raise ValueError("complete Taylor-fiber claim requires the declared flat-kernel theorem")

    coeffs = tuple(taylor_coefficients)
    scales = tuple(flat_scales)
    if not scales:
        raise ValueError("at least one flat scale is required")
    if len(set(scales)) != len(scales):
        raise ValueError("flat scales must be distinct for a distinctness receipt")

    witness_x = 0.5
    values = tuple(fiber_value(coeffs, scale, witness_x) for scale in scales)
    distinct = len(set(values)) == len(values)

    return {
        "base_taylor_coefficients": coeffs,
        "same_complete_taylor_series": True,
        "distinct_germs_witnessed": distinct,
        "distinctness_witness_x": witness_x,
        "fiber_cardinality_lower_bound": len(scales) if distinct else 1,
        "canonical_representative_selected": False,
    }


def formal_series_realization_receipt(
    finite_prefix: Iterable[float],
    *,
    borel_theorem_declared: bool,
) -> dict[str, object]:
    """Record theorem-level smooth realizability without constructing it.

    A finite prefix is retained only as a bounded specimen of supplied formal
    data. The existential statement for an arbitrary complete formal series is
    not inferred from that prefix; it is accepted only when Borel's theorem is
    explicitly declared as the proof basis.
    """
    if not borel_theorem_declared:
        raise ValueError("smooth realization claim requires the declared Borel theorem")

    return {
        "supplied_prefix": tuple(finite_prefix),
        "smooth_realization_exists": True,
        "proof_basis": "declared Borel theorem",
        "constructed_by_kernel": False,
        "canonical_representative_selected": False,
    }
