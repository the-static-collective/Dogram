"""Bounded exact specimen for quotient maps and noncanonical linear sections."""

from fractions import Fraction
from typing import Tuple

Vector = Tuple[Fraction, Fraction]


def project(v: Vector) -> Fraction:
    """Canonical quotient/projection T(a,b)=a for the frozen specimen."""
    return v[0]


def section(c: Fraction, q: Fraction) -> Vector:
    """Linear right inverse s_c(q)=(q,cq)."""
    return (q, c * q)


def difference_of_sections(c: Fraction, d: Fraction, q: Fraction) -> Vector:
    """Return s_c(q)-s_d(q), which must lie in ker(T)."""
    sc = section(c, q)
    sd = section(d, q)
    return (sc[0] - sd[0], sc[1] - sd[1])


def is_kernel_vector(v: Vector) -> bool:
    """Membership test for ker(T)={(0,k)}."""
    return project(v) == 0
