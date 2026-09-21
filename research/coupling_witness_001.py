"""COUPLING-WITNESS-001: exact finite coupling receipts.

Research only. A coupling is a joint probability law with declared marginals.
Nothing here promotes probability, disagreement, or coupling to occurrence,
evidence, causality, or semantic equivalence.
"""
from fractions import Fraction


def _F(x):
    return x if isinstance(x, Fraction) else Fraction(x)


def coupling_receipt(matrix):
    """Return exact marginals, disagreement mass, and support for a square coupling."""
    rows = tuple(tuple(_F(x) for x in row) for row in matrix)
    n = len(rows)
    if n == 0 or any(len(row) != n for row in rows):
        raise ValueError("coupling must be a nonempty square matrix")
    if any(x < 0 for row in rows for x in row):
        raise ValueError("coupling masses must be nonnegative")
    total = sum((x for row in rows for x in row), Fraction(0))
    if total != 1:
        raise ValueError("coupling masses must sum exactly to 1")
    left = tuple(sum((rows[i][j] for j in range(n)), Fraction(0)) for i in range(n))
    right = tuple(sum((rows[i][j] for i in range(n)), Fraction(0)) for j in range(n))
    diagonal = sum((rows[i][i] for i in range(n)), Fraction(0))
    support = tuple((i, j) for i in range(n) for j in range(n) if rows[i][j] > 0)
    tv = sum((abs(left[i] - right[i]) for i in range(n)), Fraction(0)) / 2
    return {
        "left_marginal": left,
        "right_marginal": right,
        "total_variation": tv,
        "disagreement": 1 - diagonal,
        "support": support,
        "matrix": rows,
        "coupling_inequality_holds": 1 - diagonal >= tv,
        "maximal": 1 - diagonal == tv,
    }


def frozen_specimen():
    """Three couplings with identical uniform marginals; two collide scalarly."""
    z = Fraction(0); t = Fraction(1, 3)
    identity = ((t,z,z),(z,t,z),(z,z,t))
    swap01 = ((z,t,z),(t,z,z),(z,z,t))
    swap12 = ((t,z,z),(z,z,t),(z,t,z))
    return tuple(coupling_receipt(m) for m in (identity, swap01, swap12))


if __name__ == "__main__":
    for receipt in frozen_specimen():
        print(receipt)
