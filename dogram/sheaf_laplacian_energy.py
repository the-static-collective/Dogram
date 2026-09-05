from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SheafLaplacianEnergyReceipt:
    edge_scales: tuple[int, int]
    coboundary: tuple[tuple[int, int, int], tuple[int, int, int]]
    laplacian: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    global_section_basis: tuple[int, int, int]
    nullity: int
    characteristic_polynomial: tuple[int, int, int, int]
    trace: int
    nonzero_eigenvalue_product: int
    probe: tuple[int, int, int]
    probe_energy: int


def analyze_weighted_path_sheaf(
    edge_scales: tuple[int, int], probe: tuple[int, int, int]
) -> SheafLaplacianEnergyReceipt:
    """Analyze a bounded scalar cellular-sheaf Laplacian on a 3-vertex path.

    For positive integer edge scales p and q, the coboundary is
    `delta(x) = (p(x1-x0), q(x2-x1))`. Scaling both restrictions incident
    to an edge leaves the exact global-section condition unchanged while
    changing the declared Euclidean energy `||delta(x)||^2` and the nonzero
    Laplacian spectrum.

    This kernel receipts only that finite algebra. It does not infer
    occurrence, evidence, causality, semantics, robustness, or truth.
    """

    if len(edge_scales) != 2:
        raise ValueError("edge_scales must contain exactly two entries")
    if any(
        not isinstance(scale, int) or isinstance(scale, bool) or scale <= 0
        for scale in edge_scales
    ):
        raise ValueError("edge scales must be positive integers")
    if len(probe) != 3 or any(
        not isinstance(value, int) or isinstance(value, bool) for value in probe
    ):
        raise ValueError("probe must contain exactly three integers")

    p, q = edge_scales
    p2 = p * p
    q2 = q * q

    coboundary = (
        (-p, p, 0),
        (0, -q, q),
    )
    laplacian = (
        (p2, -p2, 0),
        (-p2, p2 + q2, -q2),
        (0, -q2, q2),
    )

    # det(lambda I - L) = lambda *
    # (lambda^2 - 2(p^2+q^2) lambda + 3 p^2 q^2).
    characteristic_polynomial = (
        1,
        -2 * (p2 + q2),
        3 * p2 * q2,
        0,
    )

    x0, x1, x2 = probe
    probe_energy = p2 * (x1 - x0) ** 2 + q2 * (x2 - x1) ** 2

    return SheafLaplacianEnergyReceipt(
        edge_scales=edge_scales,
        coboundary=coboundary,
        laplacian=laplacian,
        global_section_basis=(1, 1, 1),
        nullity=1,
        characteristic_polynomial=characteristic_polynomial,
        trace=2 * (p2 + q2),
        nonzero_eigenvalue_product=3 * p2 * q2,
        probe=probe,
        probe_energy=probe_energy,
    )


__all__ = ["SheafLaplacianEnergyReceipt", "analyze_weighted_path_sheaf"]
