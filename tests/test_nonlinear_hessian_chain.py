from fractions import Fraction
import unittest

from dogram.nonlinear_hessian_chain import nonlinear_hessian_receipt


PHI = (0, 1, 1)  # z + z^2
Z0 = 1
NONCRITICAL_F = (0, 1, 1)  # x + x^2
CRITICAL_F = (4, -4, 1)  # (x - 2)^2


class NonlinearHessianChainTests(unittest.TestCase):
    def test_noncritical_chain_rule_has_nonzero_second_order_correction(self):
        receipt = nonlinear_hessian_receipt(NONCRITICAL_F, PHI, Z0)

        self.assertEqual(receipt["x"], Fraction(2))
        self.assertEqual(receipt["base_gradient"], Fraction(5))
        self.assertEqual(receipt["base_hessian"], Fraction(2))
        self.assertEqual(receipt["jacobian"], Fraction(3))
        self.assertEqual(receipt["map_second_derivative"], Fraction(2))
        self.assertEqual(receipt["transformed_gradient"], Fraction(15))
        self.assertEqual(receipt["naive_hessian_pullback"], Fraction(18))
        self.assertEqual(receipt["second_order_correction"], Fraction(10))
        self.assertEqual(receipt["transformed_hessian"], Fraction(28))
        self.assertEqual(receipt["direct_composite_hessian"], Fraction(28))
        self.assertFalse(receipt["critical_point"])

    def test_critical_control_kills_only_the_gradient_weighted_correction(self):
        receipt = nonlinear_hessian_receipt(CRITICAL_F, PHI, Z0)

        self.assertEqual(receipt["x"], Fraction(2))
        self.assertEqual(receipt["base_gradient"], Fraction(0))
        self.assertEqual(receipt["base_hessian"], Fraction(2))
        self.assertEqual(receipt["jacobian"], Fraction(3))
        self.assertEqual(receipt["map_second_derivative"], Fraction(2))
        self.assertEqual(receipt["transformed_gradient"], Fraction(0))
        self.assertEqual(receipt["naive_hessian_pullback"], Fraction(18))
        self.assertEqual(receipt["second_order_correction"], Fraction(0))
        self.assertEqual(receipt["transformed_hessian"], Fraction(18))
        self.assertEqual(receipt["direct_composite_hessian"], Fraction(18))
        self.assertTrue(receipt["critical_point"])

    def test_first_order_chain_rule_replays_in_both_controls(self):
        for objective in (NONCRITICAL_F, CRITICAL_F):
            receipt = nonlinear_hessian_receipt(objective, PHI, Z0)
            self.assertEqual(
                receipt["transformed_gradient"],
                receipt["base_gradient"] * receipt["jacobian"],
            )

    def test_second_order_receipt_sums_pullback_and_correction_exactly(self):
        for objective in (NONCRITICAL_F, CRITICAL_F):
            receipt = nonlinear_hessian_receipt(objective, PHI, Z0)
            self.assertEqual(
                receipt["transformed_hessian"],
                receipt["naive_hessian_pullback"]
                + receipt["second_order_correction"],
            )
            self.assertEqual(
                receipt["transformed_hessian"],
                receipt["direct_composite_hessian"],
            )


if __name__ == "__main__":
    unittest.main()
