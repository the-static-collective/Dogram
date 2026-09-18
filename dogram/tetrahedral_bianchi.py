"""Bounded exact non-Abelian tetrahedral closure research kernel.

This module is research-only. It computes finite permutation holonomies and
receipts the distinction between naive multiplication of face holonomies and
closure after transporting all compared loop data to a common basepoint.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

Permutation = tuple[int, ...]
EdgeKey = tuple[int, int]


def identity(size: int) -> Permutation:
    if size < 1:
        raise ValueError("permutation size must be positive")
    return tuple(range(1, size + 1))


def _validate_permutation(p: Permutation) -> None:
    if tuple(sorted(p)) != identity(len(p)):
        raise ValueError(f"not a permutation image tuple: {p!r}")


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left o right: apply ``right`` first, then ``left``."""
    _validate_permutation(left)
    _validate_permutation(right)
    if len(left) != len(right):
        raise ValueError("permutations must have equal size")
    return tuple(left[right[index] - 1] for index in range(len(left)))


def inverse(p: Permutation) -> Permutation:
    _validate_permutation(p)
    out = [0] * len(p)
    for source, target in enumerate(p, start=1):
        out[target - 1] = source
    return tuple(out)


def multiply_many(values: Sequence[Permutation]) -> Permutation:
    if not values:
        raise ValueError("at least one permutation is required")
    result = identity(len(values[0]))
    for value in values:
        result = compose(result, value)
    return result


def oriented_edge(edges: Mapping[EdgeKey, Permutation], source: int, target: int) -> Permutation:
    direct = edges.get((source, target))
    if direct is not None:
        return direct
    reverse = edges.get((target, source))
    if reverse is None:
        raise KeyError(f"missing edge transport for {source}<->{target}")
    return inverse(reverse)


def loop_holonomy(edges: Mapping[EdgeKey, Permutation], vertices: Sequence[int]) -> Permutation:
    if len(vertices) < 2 or vertices[0] != vertices[-1]:
        raise ValueError("loop must contain at least one edge and return to its start")
    values = [oriented_edge(edges, a, b) for a, b in zip(vertices, vertices[1:])]
    return multiply_many(values)


def conjugate(carrier: Permutation, value: Permutation) -> Permutation:
    return multiply_many((carrier, value, inverse(carrier)))


@dataclass(frozen=True)
class TetrahedralBianchiReceipt:
    face_012_at_0: Permutation
    face_023_at_0: Permutation
    face_031_at_0: Permutation
    face_123_at_1: Permutation
    three_face_product_at_0: Permutation
    transported_face_123_at_0: Permutation
    transported_closure_residual: Permutation
    naive_untransported_residual: Permutation


def tetrahedral_bianchi_receipt(edges: Mapping[EdgeKey, Permutation]) -> TetrahedralBianchiReceipt:
    """Receipt one oriented tetrahedron boundary identity.

    Conventions:
      F012 = g01 g12 g20
      F023 = g02 g23 g30
      F031 = g03 g31 g10
      F123 = g12 g23 g31, based at vertex 1

    Exact edge cancellation gives
      F012 F023 F031 = g01 F123 g10.

    The returned residuals compare the correctly transported closure against
    the tempting but generally invalid untransported multiplication.
    """
    f012 = loop_holonomy(edges, (0, 1, 2, 0))
    f023 = loop_holonomy(edges, (0, 2, 3, 0))
    f031 = loop_holonomy(edges, (0, 3, 1, 0))
    f123 = loop_holonomy(edges, (1, 2, 3, 1))
    three = multiply_many((f012, f023, f031))
    g01 = oriented_edge(edges, 0, 1)
    transported = conjugate(g01, f123)
    transported_residual = multiply_many((three, inverse(transported)))
    naive_residual = multiply_many((three, inverse(f123)))
    return TetrahedralBianchiReceipt(
        face_012_at_0=f012,
        face_023_at_0=f023,
        face_031_at_0=f031,
        face_123_at_1=f123,
        three_face_product_at_0=three,
        transported_face_123_at_0=transported,
        transported_closure_residual=transported_residual,
        naive_untransported_residual=naive_residual,
    )
