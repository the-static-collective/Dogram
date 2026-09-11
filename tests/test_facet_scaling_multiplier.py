from fractions import Fraction
import unittest

from dogram.facet_scaling_multiplier import (
    dual_objective,
    dual_residual,
    facet_contribution,
    positive_row_scaling_witness,
)


BASE = (
    ((-1, 0), 0),
    ((0, -1), 0),
    ((1, 1), 2),
)
SCALED = (
    ((-1, 0), 0),
    ((0, -1), 0),
    ((7, 7), 14),
)
OBJECTIVE = (1, 0)
BASE_DUAL = (Fraction(0), Fraction(1), Fraction(1))
SCALED_DUAL = (Fraction(0), Fraction(1), Fraction(1, 7))


class FacetScalingMultiplierTests(unittest.TestCase):
    def test_positive_row_scaling_preserves_declared_halfspace(self):
        receipt = positive_row_scaling_witness(BASE[2], SCALED[2])
        self.assertEqual(receipt["scale"], Fraction(7))
        self.assertTrue(receipt["same_halfspace"])

    def test_primal_geometry_and_dual_value_are_unchanged(self):
        self.assertEqual(dual_residual(BASE, OBJECTIVE, BASE_DUAL), (Fraction(0), Fraction(0)))
        self.assertEqual(dual_residual(SCALED, OBJECTIVE, SCALED_DUAL), (Fraction(0), Fraction(0)))
        self.assertEqual(dual_objective(BASE, BASE_DUAL), Fraction(2))
        self.assertEqual(dual_objective(SCALED, SCALED_DUAL), Fraction(2))

    def test_raw_multiplier_rescales_inversely(self):
        self.assertEqual(BASE_DUAL[2], Fraction(1))
        self.assertEqual(SCALED_DUAL[2], Fraction(1, 7))
        self.assertEqual(BASE_DUAL[2], Fraction(7) * SCALED_DUAL[2])

    def test_multiplier_weighted_facet_normal_is_invariant(self):
        base = facet_contribution(BASE[2], BASE_DUAL[2])
        scaled = facet_contribution(SCALED[2], SCALED_DUAL[2])
        self.assertEqual(base["weighted_normal"], (Fraction(1), Fraction(1)))
        self.assertEqual(scaled["weighted_normal"], base["weighted_normal"])
        self.assertEqual(base["weighted_bound"], Fraction(2))
        self.assertEqual(scaled["weighted_bound"], base["weighted_bound"])


if __name__ == "__main__":
    unittest.main()
