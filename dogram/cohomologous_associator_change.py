"""Exact finite research kernel for cohomologous associator presentations over Z/3.

This module is intentionally not wired into Dogram's public operator floor.
It freezes one normalized 2-cochain beta on G=Z/3 with trivial coefficients
H=Z/3, computes the 3-coboundary delta beta, and checks that the zero
associator and delta beta are pointwise different but cohomologous.

No occurrence, evidence, causal, semantic, or authority meaning is assigned.
"""

from itertools import product


Z3 = (0, 1, 2)


def z3_add(*values: int) -> int:
    return sum(values) % 3


def beta(g: int, h: int) -> int:
    """Normalized 2-cochain: beta(1,1)=1 and zero elsewhere."""
    if g not in Z3 or h not in Z3:
        raise ValueError("beta inputs must lie in Z/3")
    return 1 if (g, h) == (1, 1) else 0


def delta2(g: int, h: int, k: int) -> int:
    """Inhomogeneous group-cohomology coboundary for trivial action."""
    if g not in Z3 or h not in Z3 or k not in Z3:
        raise ValueError("delta2 inputs must lie in Z/3")
    return (
        beta(h, k)
        - beta(z3_add(g, h), k)
        + beta(g, z3_add(h, k))
        - beta(g, h)
    ) % 3


def zero_associator(g: int, h: int, k: int) -> int:
    if g not in Z3 or h not in Z3 or k not in Z3:
        raise ValueError("associator inputs must lie in Z/3")
    return 0


def shifted_associator(g: int, h: int, k: int) -> int:
    """Pointwise presentation obtained from zero by the coboundary delta beta."""
    return delta2(g, h, k)


def delta3_of_shifted(g: int, h: int, k: int, ell: int) -> int:
    """Pentagon / 3-cocycle residual for the shifted associator."""
    if any(value not in Z3 for value in (g, h, k, ell)):
        raise ValueError("delta3 inputs must lie in Z/3")
    a = shifted_associator
    return (
        a(h, k, ell)
        - a(z3_add(g, h), k, ell)
        + a(g, z3_add(h, k), ell)
        - a(g, h, z3_add(k, ell))
        + a(g, h, k)
    ) % 3


def coboundary_table() -> dict[tuple[int, int, int], int]:
    return {
        triple: shifted_associator(*triple)
        for triple in product(Z3, repeat=3)
    }


def nonzero_coboundary_entries() -> dict[tuple[int, int, int], int]:
    return {triple: value for triple, value in coboundary_table().items() if value}


def pentagon_residuals() -> dict[tuple[int, int, int, int], int]:
    return {
        quadruple: delta3_of_shifted(*quadruple)
        for quadruple in product(Z3, repeat=4)
    }


def normalized_shifted_associator() -> bool:
    for triple, value in coboundary_table().items():
        if 0 in triple and value != 0:
            return False
    return True


def specimen_receipt() -> dict[str, object]:
    nonzero = nonzero_coboundary_entries()
    residuals = pentagon_residuals()
    raw_delta_count = sum(
        zero_associator(*triple) != shifted_associator(*triple)
        for triple in product(Z3, repeat=3)
    )
    return {
        "group": "Z/3Z",
        "coefficients": "Z/3Z",
        "action": "trivial",
        "beta_support": [[1, 1, 1]],
        "nonzero_shifted_entries": [
            [*triple, value] for triple, value in sorted(nonzero.items())
        ],
        "raw_associator_delta_count": raw_delta_count,
        "normalized": normalized_shifted_associator(),
        "pentagon_residual_nonzero_count": sum(value != 0 for value in residuals.values()),
        "cohomology_relation": "shifted = zero + delta(beta)",
        "same_cohomology_class": True,
    }
