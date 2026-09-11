"""Theorem-gated research kernel for algebraic vs bounded splitting.

This module does not attempt to prove Phillips' theorem computationally. It only
replays the exact categorical implication that a bounded linear right inverse of
a Banach quotient would induce a bounded projection onto its kernel, and gates
the infinite-dimensional conclusions on explicitly declared theorem bases.
"""

from dataclasses import dataclass


class ProofBasisMissing(ValueError):
    """Raised when an infinite-dimensional conclusion lacks its theorem basis."""


@dataclass(frozen=True)
class ProjectionIdentityReceipt:
    projection_formula: str
    on_kernel_formula: str
    idempotence_formula: str
    section_implies_complemented_kernel: bool


@dataclass(frozen=True)
class BanachSectionReceipt:
    sequence: str
    kernel: str
    quotient_surjective: bool
    algebraic_section_exists: bool
    bounded_linear_section_exists: bool
    category_delta: bool
    algebraic_basis: str
    bounded_obstruction_basis: str


def bounded_section_projection_identity() -> ProjectionIdentityReceipt:
    """Receipt the exact implication q∘s=id => P=I-sq projects onto ker(q).

    If k lies in ker(q), then P(k)=k-s(q(k))=k. Also q(P(x))=0, so the
    range lies in ker(q). Because P fixes its range, P∘P=P. If q and s are
    bounded linear maps then P is bounded linear as well.
    """
    return ProjectionIdentityReceipt(
        projection_formula="P = I - s o q",
        on_kernel_formula="P(k) = k",
        idempotence_formula="P o P = P",
        section_implies_complemented_kernel=True,
    )


def analyze_linf_c0_sequence(
    *,
    declare_vector_space_splitting: bool,
    declare_phillips_noncomplementation: bool,
) -> BanachSectionReceipt:
    """Analyze 0 -> c0 -> l_infinity -> l_infinity/c0 -> 0 under two categories.

    The algebraic conclusion uses the standard theorem that short exact
    sequences of vector spaces split. The Banach-space conclusion uses the
    Phillips non-complementation theorem for c0 in l_infinity together with
    ``bounded_section_projection_identity``.
    """
    if not declare_vector_space_splitting:
        raise ProofBasisMissing(
            "algebraic splitting requires the declared vector-space splitting theorem"
        )
    if not declare_phillips_noncomplementation:
        raise ProofBasisMissing(
            "bounded nonsplitting requires the declared Phillips non-complementation theorem"
        )

    bounded_section_projection_identity()

    return BanachSectionReceipt(
        sequence="0 -> c0 -> l_infinity -> l_infinity/c0 -> 0",
        kernel="c0",
        quotient_surjective=True,
        algebraic_section_exists=True,
        bounded_linear_section_exists=False,
        category_delta=True,
        algebraic_basis="short exact sequences of vector spaces split",
        bounded_obstruction_basis="Phillips: c0 is not complemented in l_infinity",
    )
