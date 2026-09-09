from fractions import Fraction
import unittest

from dogram.coordinate_covariance import (
    coordinate_change_receipt,
    stationarity_residual,
)


BASE_CONSTRAINTS = (
    ((-1, 0), 0),
    ((0, -1), 0),
    ((1, 1), 2),
)
BASE_OBJECTIVE = (1, 0)
T = (
    (1, 1),
    (1, 2),
)
T_INV = (
    (2, -1),
    (-1, 1),
)
BASE_OPTIMUM = (2, 0)
BASE_DUAL = (Fraction(0), Fraction(1), Fraction(1))


class CoordinateCovarianceTests(unittest.TestCase):
    def test_coordinate_change_transforms_declared_coefficients_exactly(self):
        receipt = coordinate_change_receipt(
            BASE_CONSTRAINTS,
            BASE_OBJECTIVE,
            T,
            T_INV,
            BASE_OPTIMUM,
        )
        self.assertEqual(receipt["transformed_objective"], (Fraction(1), Fraction(1)))
        self.assertEqual(
            receipt["transformed_constraints"],
            (
                ((Fraction(-1), Fraction(-1)), Fraction(0)),
                ((Fraction(-1), Fraction(-2)), Fraction(0)),
                ((Fraction(2), Fraction(3)), Fraction(2)),
            ),
        )
        self.assertEqual(receipt["transformed_optimum"], (Fraction(4), Fraction(-2)))

    def test_coordinate_map_and_inverse_replay_the_same_point(self):
        receipt = coordinate_change_receipt(
            BASE_CONSTRAINTS,
            BASE_OBJECTIVE,
            T,
            T_INV,
            BASE_OPTIMUM,
        )
        self.assertEqual(receipt["replayed_base_optimum"], (Fraction(2), Fraction(0)))
        self.assertTrue(receipt["inverse_witness"])

    def test_objective_value_is_invariant_under_declared_coordinate_change(self):
        receipt = coordinate_change_receipt(
            BASE_CONSTRAINTS,
            BASE_OBJECTIVE,
            T,
            T_INV,
            BASE_OPTIMUM,
        )
        self.assertEqual(receipt["base_objective_value"], Fraction(2))
        self.assertEqual(receipt["transformed_objective_value"], Fraction(2))

    def test_same_dual_certificate_satisfies_transformed_stationarity(self):
        receipt = coordinate_change_receipt(
            BASE_CONSTRAINTS,
            BASE_OBJECTIVE,
            T,
            T_INV,
            BASE_OPTIMUM,
        )
        self.assertEqual(
            stationarity_residual(BASE_CONSTRAINTS, BASE_OBJECTIVE, BASE_DUAL),
            (Fraction(0), Fraction(0)),
        )
        self.assertEqual(
            stationarity_residual(
                receipt["transformed_constraints"],
                receipt["transformed_objective"],
                BASE_DUAL,
            ),
            (Fraction(0), Fraction(0)),
        )


if __name__ == "__main__":
    unittest.main()
