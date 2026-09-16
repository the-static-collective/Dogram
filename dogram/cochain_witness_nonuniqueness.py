"""Bounded exact group-cohomology witness-nonuniqueness specimen.

Research-only helper over G = Z/3Z and coefficients H = Z/3Z with trivial action.
It computes normalized 1/2-cochain coboundaries exactly and preserves witness deltas
without assigning semantic, evidentiary, causal, or authority meaning.
"""

from __future__ import annotations

from itertools import product

MODULUS = 3
ELEMENTS = tuple(range(MODULUS))


def beta_one(g: int, h: int) -> int:
    """Frozen #110-style 2-cochain: beta(1,1)=1 and zero elsewhere."""
    return 1 if (g, h) == (1, 1) else 0


def carry_cocycle(g: int, h: int) -> int:
    """Normalized carry cocycle for representatives 0,1,2 of Z/3Z."""
    if g == 0 or h == 0:
        return 0
    return 1 if g + h >= MODULUS else 0


def beta_two(g: int, h: int) -> int:
    """A second witness with the same 3-coboundary as beta_one."""
    return (beta_one(g, h) + carry_cocycle(g, h)) % MODULUS


def delta_1(values: tuple[int, int], g: int, h: int) -> int:
    """Coboundary of a normalized 1-cochain gamma with gamma(0)=0.

    ``values`` stores ``(gamma(1), gamma(2))``.
    """
    gamma = (0, values[0] % MODULUS, values[1] % MODULUS)
    return (gamma[h] - gamma[(g + h) % MODULUS] + gamma[g]) % MODULUS


def delta_2(cochain, g: int, h: int, k: int) -> int:
    """Inhomogeneous 3-coboundary for trivial action."""
    return (
        cochain(h, k)
        - cochain((g + h) % MODULUS, k)
        + cochain(g, (h + k) % MODULUS)
        - cochain(g, h)
    ) % MODULUS


def support_2(cochain) -> tuple[tuple[int, int, int], ...]:
    """Return nonzero 2-cochain entries as ``(g,h,value)`` tuples."""
    return tuple(
        (g, h, value)
        for g, h in product(ELEMENTS, repeat=2)
        if (value := cochain(g, h)) != 0
    )


def coboundary_support(cochain) -> tuple[tuple[int, int, int, int], ...]:
    """Return nonzero 3-coboundary entries as ``(g,h,k,value)`` tuples."""
    return tuple(
        (g, h, k, value)
        for g, h, k in product(ELEMENTS, repeat=3)
        if (value := delta_2(cochain, g, h, k)) != 0
    )


def carry_is_two_cocycle() -> bool:
    return all(
        delta_2(carry_cocycle, g, h, k) == 0
        for g, h, k in product(ELEMENTS, repeat=3)
    )


def carry_is_one_coboundary() -> bool:
    """Exhaust the 3^2 normalized 1-cochains and test whether any cobounds to carry."""
    for values in product(ELEMENTS, repeat=2):
        if all(
            delta_1(values, g, h) == carry_cocycle(g, h)
            for g, h in product(ELEMENTS, repeat=2)
        ):
            return True
    return False


def receipt() -> dict[str, object]:
    delta_one = coboundary_support(beta_one)
    delta_two = coboundary_support(beta_two)
    return {
        "group": "Z/3Z",
        "coefficients": "Z/3Z",
        "action": "trivial",
        "beta_one_support": support_2(beta_one),
        "beta_two_support": support_2(beta_two),
        "witness_difference_support": support_2(carry_cocycle),
        "delta_beta_one_support": delta_one,
        "delta_beta_two_support": delta_two,
        "same_endpoint_delta": delta_one == delta_two,
        "witnesses_distinct": support_2(beta_one) != support_2(beta_two),
        "difference_is_two_cocycle": carry_is_two_cocycle(),
        "difference_is_one_coboundary": carry_is_one_coboundary(),
        "normalized_one_cochains_exhausted": MODULUS ** 2,
    }
