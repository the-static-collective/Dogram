"""Exact finite research kernel for cohomologous associator tables over Z/3.

This module is intentionally not wired into Dogram's public operator floor.
It receipts one declared change of normalized associator by an explicit
2-cochain coboundary without attaching semantic, causal, evidentiary, or
historical meaning to the resulting cohomology equivalence.
"""

from itertools import product
from typing import Callable


Z3 = (0, 1, 2)
_NONZERO_PAIRS = ((1, 1), (1, 2), (2, 1), (2, 2))


def _check_z3(*values: int) -> None:
    if any(value not in Z3 for value in values):
        raise ValueError("inputs must lie in Z/3")


def z3_add(*values: int) -> int:
    _check_z3(*values)
    return sum(values) % 3


def associator(g: int, h: int, k: int) -> int:
    """Frozen normalized 3-cocycle g*floor((h+k)/3) mod 3."""
    _check_z3(g, h, k)
    carry = (h + k) // 3
    return (g * carry) % 3


def _declared_beta(g: int, h: int) -> int:
    """Normalized 2-cochain supported only at beta(1,1)=1."""
    _check_z3(g, h)
    return 1 if (g, h) == (1, 1) else 0


def delta2(beta: Callable[[int, int], int], g: int, h: int, k: int) -> int:
    """Additive group-cohomology coboundary for trivial Z/3 action."""
    _check_z3(g, h, k)
    return (
        beta(h, k)
        - beta(z3_add(g, h), k)
        + beta(g, z3_add(h, k))
        - beta(g, h)
    ) % 3


def coboundary(g: int, h: int, k: int) -> int:
    return delta2(_declared_beta, g, h, k)


def shifted_associator(g: int, h: int, k: int) -> int:
    _check_z3(g, h, k)
    return (associator(g, h, k) + coboundary(g, h, k)) % 3


def delta3(
    cochain: Callable[[int, int, int], int],
    g: int,
    h: int,
    k: int,
    ell: int,
) -> int:
    """Additive normalized 3-cochain coboundary for trivial Z/3 action."""
    _check_z3(g, h, k, ell)
    return (
        cochain(h, k, ell)
        - cochain(z3_add(g, h), k, ell)
        + cochain(g, z3_add(h, k), ell)
        - cochain(g, h, z3_add(k, ell))
        + cochain(g, h, k)
    ) % 3


def cocycle_residuals(
    cochain: Callable[[int, int, int], int],
) -> dict[tuple[int, int, int, int], int]:
    return {
        quadruple: delta3(cochain, *quadruple)
        for quadruple in product(Z3, repeat=4)
    }


def table_delta() -> dict[tuple[int, int, int], int]:
    """Return only triples where the shifted table differs from the base table."""
    result: dict[tuple[int, int, int], int] = {}
    for triple in product(Z3, repeat=3):
        delta = (shifted_associator(*triple) - associator(*triple)) % 3
        if delta:
            result[triple] = delta
    return result


def _normalized_2cochain(values: tuple[int, int, int, int]) -> Callable[[int, int], int]:
    if len(values) != len(_NONZERO_PAIRS) or any(value not in Z3 for value in values):
        raise ValueError("normalized 2-cochain values must be four Z/3 entries")
    table = dict(zip(_NONZERO_PAIRS, values, strict=True))

    def beta(g: int, h: int) -> int:
        _check_z3(g, h)
        if g == 0 or h == 0:
            return 0
        return table[(g, h)]

    return beta


def normalized_2cochains_matching(
    target: Callable[[int, int, int], int],
) -> list[tuple[int, int, int, int]]:
    """Enumerate normalized 2-cochains whose coboundary equals target exactly."""
    target_table = {
        triple: target(*triple)
        for triple in product(Z3, repeat=3)
    }
    matches: list[tuple[int, int, int, int]] = []
    for values in product(Z3, repeat=len(_NONZERO_PAIRS)):
        beta = _normalized_2cochain(values)
        candidate = {
            triple: delta2(beta, *triple)
            for triple in product(Z3, repeat=3)
        }
        if candidate == target_table:
            matches.append(values)
    return matches
