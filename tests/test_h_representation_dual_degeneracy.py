from fractions import Fraction
import unittest

from dogram.h_representation_dual_degeneracy import (
    dual_objective,
    dual_residual,
    redundant_dual_family,
    verify_redundant_constraint,
)


MINIMAL = (
    ((-1, 0), 0),
    ((0, -1), 0),
    ((1, 1), 2),
)
REDUNDANT = MINIMAL + (((1, 0), 2),)
OBJECTIVE = (1, 0)


class HRepresentationDualDegeneracyTests(unittest.TestCase):
    def test_extra_inequality_is_redundant_for_frozen_triangle(self):
        receipt = verify_redundant_constraint(MINIMAL, ((1, 0), 2))
        self.assertTrue(receipt["same_feasible_triangle"])
        self.assertEqual(receipt["witness"], "x<=x+y<=2 because y>=0")

    def test_minimal_presentation_has_unique_declared_dual_certificate(self):
        lam = (Fraction(0), Fraction(1), Fraction(1))
        self.assertEqual(dual_residual(MINIMAL, OBJECTIVE, lam), (Fraction(0), Fraction(0)))
        self.assertEqual(dual_objective(MINIMAL, lam), Fraction(2))

    def test_redundant_presentation_has_continuum_of_optimal_certificates(self):
        for t in (Fraction(0), Fraction(1, 3), Fraction(1)):
            lam = redundant_dual_family(t)
            self.assertEqual(dual_residual(REDUNDANT, OBJECTIVE, lam), (Fraction(0), Fraction(0)))
            self.assertEqual(dual_objective(REDUNDANT, lam), Fraction(2))
        self.assertNotEqual(redundant_dual_family(Fraction(0)), redundant_dual_family(Fraction(1)))

    def test_same_primal_optimum_does_not_force_same_dual_certificate_set(self):
        minimal = (Fraction(0), Fraction(1), Fraction(1))
        redundant_a = redundant_dual_family(Fraction(0))
        redundant_b = redundant_dual_family(Fraction(1))
        self.assertEqual(dual_objective(MINIMAL, minimal), dual_objective(REDUNDANT, redundant_a))
        self.assertEqual(dual_objective(REDUNDANT, redundant_a), dual_objective(REDUNDANT, redundant_b))
        self.assertNotEqual(redundant_a, redundant_b)


if __name__ == "__main__":
    unittest.main()
