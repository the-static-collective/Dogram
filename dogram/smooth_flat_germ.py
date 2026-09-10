"""Bounded research kernel for SMOOTH-FLAT-GERM-001.

This module does not attempt to establish an infinite theorem by finite testing.
It exposes the exact polynomial recurrence for derivatives of

    h(x) = exp(-1/x^2), x != 0,
    h(0) = 0,

and records the zero Taylor jet only under the standard declared limit fact
that every polynomial in 1/x multiplied by exp(-1/x^2) tends to zero as
x -> 0.
"""

from __future__ import annotations

import math
from typing import Iterable


def flat_value(x: float) -> float:
    """Evaluate the frozen flat-function specimen."""
    if x == 0.0:
        return 0.0
    return math.exp(-1.0 / (x * x))


def _trim(coeffs: list[int]) -> tuple[int, ...]:
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def _next_derivative_polynomial(coeffs: Iterable[int]) -> tuple[int, ...]:
    """Apply P -> -y^2 P'(y) + 2 y^3 P(y) exactly over integers."""
    p = tuple(coeffs)
    out = [0] * (len(p) + 3)
    for degree, coefficient in enumerate(p):
        if degree:
            out[degree + 1] -= degree * coefficient
        out[degree + 3] += 2 * coefficient
    return _trim(out)


def derivative_polynomials(max_order: int) -> list[tuple[int, ...]]:
    """Return P_0,...,P_n where h^(n)(x)=P_n(1/x) exp(-1/x^2), x!=0."""
    if max_order < 0:
        raise ValueError("max_order must be nonnegative")
    polys = [(1,)]
    for _ in range(max_order):
        polys.append(_next_derivative_polynomial(polys[-1]))
    return polys


def zero_taylor_jet(max_order: int, *, limit_fact_declared: bool = True) -> list[int]:
    """Return the zero Taylor jet under the explicit flatness proof obligation.

    The infinite mathematical step is not inferred from this program.  It is
    supplied by the standard limit theorem that exp(-1/x^2) dominates every
    polynomial in 1/x as x approaches zero.  The recurrence above shows every
    punctured derivative has exactly that form.
    """
    if max_order < 0:
        raise ValueError("max_order must be nonnegative")
    if not limit_fact_declared:
        raise ValueError("zero-jet claim requires the declared flatness limit theorem")
    derivative_polynomials(max_order)
    return [0] * (max_order + 1)
