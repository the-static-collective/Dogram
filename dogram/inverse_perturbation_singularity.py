"""Bounded exact kernel for INVERSE-PERTURBATION-SINGULARITY-001.

For n>=2 freeze two invertible diagonal operators on R^2:
    A_n = diag(1, 1/n)
    B_n = diag(1, 2/n)
with Euclidean operator norm.

The family records perturbation sensitivity near the rank-deficient boundary.
It does not infer occurrence, evidence, causation, authority, or semantics.
"""

from fractions import Fraction
from typing import Dict, Tuple

Diagonal2 = Tuple[Fraction, Fraction]


def _parameter(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be an integer >= 2")
    return n


def forward_pair(n: int) -> Tuple[Diagonal2, Diagonal2]:
    n = _parameter(n)
    return ((Fraction(1), Fraction(1, n)), (Fraction(1), Fraction(2, n)))


def inverse_pair(n: int) -> Tuple[Diagonal2, Diagonal2]:
    n = _parameter(n)
    return ((Fraction(1), Fraction(n)), (Fraction(1), Fraction(n, 2)))


def _diagonal_operator_norm(diagonal: Diagonal2) -> Fraction:
    return max(abs(diagonal[0]), abs(diagonal[1]))


def _subtract(left: Diagonal2, right: Diagonal2) -> Diagonal2:
    return (left[0] - right[0], left[1] - right[1])


def _multiply(left: Diagonal2, right: Diagonal2) -> Diagonal2:
    return (left[0] * right[0], left[1] * right[1])


def forward_delta(n: int) -> Fraction:
    """Return ||A_n-B_n||_2 = 1/n exactly."""
    A, B = forward_pair(n)
    return _diagonal_operator_norm(_subtract(A, B))


def inverse_delta(n: int) -> Fraction:
    """Return ||A_n^-1-B_n^-1||_2 = n/2 exactly."""
    A_inv, B_inv = inverse_pair(n)
    return _diagonal_operator_norm(_subtract(A_inv, B_inv))


def inverse_delta_ratio(n: int) -> Fraction:
    """Return inverse-delta / forward-delta = n^2/2."""
    return inverse_delta(n) / forward_delta(n)


def distance_to_singularity(n: int) -> Tuple[Fraction, Fraction]:
    """Return spectral-norm distances of A_n and B_n to singular matrices.

    For an invertible matrix this distance equals sigma_min.  Here the
    singular values are visible directly from the positive diagonal entries.
    """
    A, B = forward_pair(n)
    return (min(A), min(B))


def resolvent_identity_holds(n: int) -> bool:
    """Check B^-1-A^-1 = B^-1 (A-B) A^-1 exactly."""
    A, B = forward_pair(n)
    A_inv, B_inv = inverse_pair(n)
    left = _subtract(B_inv, A_inv)
    right = _multiply(_multiply(B_inv, _subtract(A, B)), A_inv)
    return left == right


def family_receipt(n: int) -> Dict[str, object]:
    n = _parameter(n)
    A, B = forward_pair(n)
    distance_A, distance_B = distance_to_singularity(n)
    return {
        "parameter": n,
        "A": A,
        "B": B,
        "operator_norm_A": _diagonal_operator_norm(A),
        "operator_norm_B": _diagonal_operator_norm(B),
        "forward_delta": forward_delta(n),
        "inverse_delta": inverse_delta(n),
        "inverse_delta_ratio": inverse_delta_ratio(n),
        "distance_to_singularity_A": distance_A,
        "distance_to_singularity_B": distance_B,
        "inverse_norm_A": Fraction(n),
        "inverse_norm_B": Fraction(n, 2),
        "resolvent_identity_holds": resolvent_identity_holds(n),
        "seal": "SMALL FORWARD-OPERATOR DELTA != SMALL INVERSE DELTA NEAR RANK LOSS. KEEP THE DISTANCE TO SINGULARITY IN THE RECEIPT.",
    }
