from fractions import Fraction
import unittest

from dogram.convex_presentation_invariance import (
    convex_combination,
    support_value,
    uniform_generator_mean,
    verify_same_triangle_hull,
)


MINIMAL = ((0, 0), (2, 0), (0, 2))
REDUNDANT = ((0, 0), (2, 0), (0, 2), (1, 1))
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (-1, 0), (0, -1))


class ConvexPresentationInvarianceTests(unittest.TestCase):
    def test_redundant_point_has_exact_convex_combination_witness(self):
        point = convex_combination(((2, 0), (0, 2)), (Fraction(1, 2), Fraction(1, 2)))
        self.assertEqual(point, (Fraction(1, 1), Fraction(1, 1)))

    def test_declared_presentations_generate_same_triangle(self):
        receipt = verify_same_triangle_hull(MINIMAL, REDUNDANT)
        self.assertTrue(receipt["same_hull"])
        self.assertEqual(receipt["extreme_points"], ((0, 0), (0, 2), (2, 0)))
        self.assertEqual(receipt["redundant_points"], ((1, 1),))

    def test_linear_support_receipts_are_presentation_invariant(self):
        for direction in DIRECTIONS:
            self.assertEqual(
                support_value(MINIMAL, direction),
                support_value(REDUNDANT, direction),
            )

    def test_uniform_over_listed_generators_is_not_hull_invariant(self):
        self.assertEqual(uniform_generator_mean(MINIMAL), (Fraction(2, 3), Fraction(2, 3)))
        self.assertEqual(uniform_generator_mean(REDUNDANT), (Fraction(3, 4), Fraction(3, 4)))
        self.assertNotEqual(uniform_generator_mean(MINIMAL), uniform_generator_mean(REDUNDANT))


if __name__ == "__main__":
    unittest.main()
