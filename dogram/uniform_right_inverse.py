"""Bounded research kernel for UNIFORM-RIGHT-INVERSE-001.

The family is A_n : R^3 -> R^2, A_n(x,y,z)=(x,y/n), n>=1,
with Euclidean norms.  The module records only exact finite-dimensional
algebra.  It does not infer evidence, occurrence, authority, or a preferred
reconstruction policy.
"""

from fractions import Fraction
from typing import Dict, Tuple

Vector2 = Tuple[Fraction, Fraction]
Vector3 = Tuple[Fraction, Fraction, Fraction]


def _parameter(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be an integer >= 1")
    return n


def apply_map(n: int, vector: Vector3) -> Vector2:
    """Apply A_n(x,y,z)=(x,y/n) exactly."""
    n = _parameter(n)
    x, y, _z = map(Fraction, vector)
    return (x, y / n)


def canonical_section(n: int, quotient_vector: Vector2) -> Vector3:
    """Return S_n(u,v)=(u,nv,0), an exact right inverse of A_n."""
    n = _parameter(n)
    u, v = map(Fraction, quotient_vector)
    return (u, n * v, Fraction(0))


def operator_norm(n: int) -> Fraction:
    """Spectral/operator norm of A_n for n>=1.

    A_n has singular values 1 and 1/n, hence ||A_n||_2=1.
    """
    _parameter(n)
    return Fraction(1)


def smallest_positive_singular_value(n: int) -> Fraction:
    _parameter(n)
    return Fraction(1, n)


def optimal_section_norm(n: int) -> Fraction:
    """Minimum possible Euclidean operator norm of any linear right inverse.

    Lower bound: if S is any right inverse and e2=(0,1), then writing
    S(e2)=(a,b,c), A_n S(e2)=e2 forces b=n.  Therefore
    ||S|| >= ||S(e2)|| >= n.

    Attainment: the canonical S_n has singular values 1 and n, so ||S_n||=n.
    """
    _parameter(n)
    return Fraction(n)


def escape_uniform_bound(bound: Fraction) -> int:
    """Return explicit n>=1 with optimal_section_norm(n) > bound."""
    bound = Fraction(bound)
    if bound < 1:
        return 1
    return bound.numerator // bound.denominator + 1


def section_receipt(n: int) -> Dict[str, object]:
    """Return the exact quantitative receipt for one family member."""
    n = _parameter(n)
    section = canonical_section(n, (Fraction(0), Fraction(1)))
    return {
        "parameter": n,
        "operator_norm": operator_norm(n),
        "smallest_positive_singular_value": smallest_positive_singular_value(n),
        "right_inverse_basis_witness": section,
        "lower_bound_any_right_inverse": Fraction(n),
        "canonical_section_norm": optimal_section_norm(n),
        "lower_bound_attained": True,
        "condition_number_on_kernel_complement": Fraction(n),
        "seal": "POINTWISE BOUNDED SECTION EXISTS != UNIFORMLY BOUNDED FAMILY OF SECTIONS EXISTS.",
    }
