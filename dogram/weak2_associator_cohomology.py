"""Exact finite research kernel for a weak 2-group associator over Z/2.

This module is intentionally not wired into Dogram's public operator floor.
It computes one declared skeletal coherent-2-group specimen and preserves the
coherence witness without attaching semantic, causal, evidentiary, or
historical meaning to it.
"""

from itertools import product


Z2 = (0, 1)


def z2_add(*values: int) -> int:
    return sum(values) % 2


def associator(g: int, h: int, k: int) -> int:
    """Normalized Z/2-valued 3-cochain a(g,h,k)=g*h*k mod 2."""
    if g not in Z2 or h not in Z2 or k not in Z2:
        raise ValueError("associator inputs must lie in Z/2")
    return (g * h * k) % 2


def delta3(g: int, h: int, k: int, ell: int) -> int:
    """Additive group-cohomology coboundary for trivial Z/2 action."""
    terms = (
        associator(h, k, ell)
        - associator(z2_add(g, h), k, ell)
        + associator(g, z2_add(h, k), ell)
        - associator(g, h, z2_add(k, ell))
        + associator(g, h, k)
    )
    return terms % 2


def pentagon_residuals() -> dict[tuple[int, int, int, int], int]:
    return {
        quadruple: delta3(*quadruple)
        for quadruple in product(Z2, repeat=4)
    }


def normalized_3cocycle() -> bool:
    for g, h, k in product(Z2, repeat=3):
        if 0 in (g, h, k) and associator(g, h, k) != 0:
            return False
    return all(value == 0 for value in pentagon_residuals().values())


def _normalized_2cochain(beta_11: int, g: int, h: int) -> int:
    if beta_11 not in Z2:
        raise ValueError("beta_11 must lie in Z/2")
    return beta_11 if (g, h) == (1, 1) else 0


def delta2(beta_11: int, g: int, h: int, k: int) -> int:
    """Coboundary of a normalized 2-cochain, with trivial Z/2 action."""
    beta = lambda x, y: _normalized_2cochain(beta_11, x, y)
    terms = (
        beta(h, k)
        - beta(z2_add(g, h), k)
        + beta(g, z2_add(h, k))
        - beta(g, h)
    )
    return terms % 2


def normalized_2cochains() -> list[dict[str, object]]:
    receipts = []
    target = {
        triple: associator(*triple)
        for triple in product(Z2, repeat=3)
    }
    for beta_11 in Z2:
        coboundary = {
            triple: delta2(beta_11, *triple)
            for triple in product(Z2, repeat=3)
        }
        receipts.append(
            {
                "beta_11": beta_11,
                "coboundary": coboundary,
                "matches_associator": coboundary == target,
            }
        )
    return receipts


def associator_receipt(g: int, h: int, k: int) -> dict[str, object]:
    """Receipt the two object-level bracketings and their coherence witness."""
    left_object = z2_add(z2_add(g, h), k)
    right_object = z2_add(g, z2_add(h, k))
    witness = associator(g, h, k)
    return {
        "inputs": [g, h, k],
        "left_object": left_object,
        "right_object": right_object,
        "object_level_equal": left_object == right_object,
        "associator_witness": witness,
        "strict_on_this_triple": witness == 0,
    }
