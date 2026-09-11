import unittest

from dogram.banach_section_obstruction import (
    ProofBasisMissing,
    analyze_linf_c0_sequence,
    bounded_section_projection_identity,
)


class BanachSectionObstructionTests(unittest.TestCase):
    def test_exact_projection_identity_is_receipted(self):
        receipt = bounded_section_projection_identity()
        self.assertEqual(receipt.projection_formula, "P = I - s o q")
        self.assertEqual(receipt.on_kernel_formula, "P(k) = k")
        self.assertEqual(receipt.idempotence_formula, "P o P = P")
        self.assertTrue(receipt.section_implies_complemented_kernel)

    def test_infinite_dimensional_conclusions_require_declared_theorem_bases(self):
        with self.assertRaises(ProofBasisMissing):
            analyze_linf_c0_sequence(
                declare_vector_space_splitting=False,
                declare_phillips_noncomplementation=False,
            )

    def test_algebraic_split_and_bounded_nonsplit_can_coexist(self):
        receipt = analyze_linf_c0_sequence(
            declare_vector_space_splitting=True,
            declare_phillips_noncomplementation=True,
        )
        self.assertTrue(receipt.quotient_surjective)
        self.assertEqual(receipt.kernel, "c0")
        self.assertTrue(receipt.algebraic_section_exists)
        self.assertFalse(receipt.bounded_linear_section_exists)
        self.assertTrue(receipt.category_delta)

    def test_phillips_gate_cannot_be_replaced_by_algebraic_splitting(self):
        with self.assertRaises(ProofBasisMissing):
            analyze_linf_c0_sequence(
                declare_vector_space_splitting=True,
                declare_phillips_noncomplementation=False,
            )


if __name__ == "__main__":
    unittest.main()
