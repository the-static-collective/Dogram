"""Bounded exact kernel for PSEUDOINVERSE-RANK-STRATUM-001.

Two diagonal matrix families approach the same rank-one limit L=diag(1,0):

    A_n = diag(1, 1/n)        (rank 2 for every finite n)
    B_n = diag(1+1/n, 0)      (rank 1 for every finite n)

The Moore-Penrose pseudoinverse is computed exactly for diagonal matrices by
inverting nonzero diagonal entries and leaving zero entries zero.  This exposes
that A_n^+ diverges while B_n^+ converges to L^+, isolating rank-stratum
membership as a necessary receipt coordinate for this continuity claim.

No occurrence, evidence, causation, authority, or semantic meaning is inferred.
"""

from fractions import Fraction
from typing import Dict, Tuple

Diagonal2 = Tuple[Fraction, Fraction]


def _parameter(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be an integer >= 1")
    return n


def pseudoinverse(diagonal: Diagonal2) -> Diagonal2:
    """Exact Moore-Penrose pseudoinverse for a real diagonal 2x2 matrix."""
    return tuple(Fraction(0) if value == 0 else Fraction(1, 1) / value for value in diagonal)  # type: ignore[return-value]


def rank(diagonal: Diagonal2) -> int:
    return sum(value != 0 for value in diagonal)


def operator_norm(diagonal: Diagonal2) -> Fraction:
    return max(abs(diagonal[0]), abs(diagonal[1]))


def subtract(left: Diagonal2, right: Diagonal2) -> Diagonal2:
    return (left[0] - right[0], left[1] - right[1])


def limit_matrix() -> Diagonal2:
    return (Fraction(1), Fraction(0))


def rank_changing_matrix(n: int) -> Diagonal2:
    n = _parameter(n)
    return (Fraction(1), Fraction(1, n))


def rank_preserving_matrix(n: int) -> Diagonal2:
    n = _parameter(n)
    return (Fraction(n + 1, n), Fraction(0))


def family_receipt(n: int) -> Dict[str, object]:
    n = _parameter(n)
    limit = limit_matrix()
    changing = rank_changing_matrix(n)
    preserving = rank_preserving_matrix(n)
    limit_plus = pseudoinverse(limit)
    changing_plus = pseudoinverse(changing)
    preserving_plus = pseudoinverse(preserving)

    changing_forward_delta = operator_norm(subtract(changing, limit))
    preserving_forward_delta = operator_norm(subtract(preserving, limit))
    changing_plus_delta = operator_norm(subtract(changing_plus, limit_plus))
    preserving_plus_delta = operator_norm(subtract(preserving_plus, limit_plus))

    return {
        "parameter": n,
        "limit": limit,
        "limit_rank": rank(limit),
        "limit_pseudoinverse": limit_plus,
        "rank_changing": changing,
        "rank_changing_rank": rank(changing),
        "rank_changing_pseudoinverse": changing_plus,
        "rank_changing_forward_delta": changing_forward_delta,
        "rank_changing_pseudoinverse_delta": changing_plus_delta,
        "rank_changing_amplification_ratio": changing_plus_delta / changing_forward_delta,
        "rank_preserving": preserving,
        "rank_preserving_rank": rank(preserving),
        "rank_preserving_pseudoinverse": preserving_plus,
        "rank_preserving_forward_delta": preserving_forward_delta,
        "rank_preserving_pseudoinverse_delta": preserving_plus_delta,
        "same_forward_limit": changing_forward_delta == preserving_forward_delta == Fraction(1, n),
        "rank_stratum_delta_exposed": rank(changing) != rank(limit) and rank(preserving) == rank(limit),
        "seal": "PSEUDOINVERSE CONTINUITY REQUIRES A RANK-STRATUM RECEIPT.",
    }
