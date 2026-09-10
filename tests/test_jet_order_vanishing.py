import json
from pathlib import Path
import unittest

from dogram.jet_order_vanishing import jet_order_vanishing_receipt


FIXTURE = Path(__file__).resolve().parents[1] / "research" / "fixtures" / "jet_order_vanishing_001.json"


class JetOrderVanishingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())
        data = cls.fixture
        cls.receipt = jet_order_vanishing_receipt(
            data["left"]["coefficients_ascending"],
            data["right"]["coefficients_ascending"],
            data["declared_jet_order"],
            data["coordinate_map"]["coefficients_ascending"],
        )

    def test_same_two_jet_hides_different_first_nonzero_orders(self):
        expected = self.fixture["expected"]
        self.assertEqual(self.receipt["left_truncated_jet"], tuple(expected["shared_truncated_jet"]))
        self.assertEqual(self.receipt["right_truncated_jet"], tuple(expected["shared_truncated_jet"]))
        self.assertTrue(self.receipt["truncated_jets_equal"])
        self.assertEqual(self.receipt["left_first_nonzero_order"], expected["left_first_nonzero_order"])
        self.assertEqual(self.receipt["right_first_nonzero_order"], expected["right_first_nonzero_order"])

    def test_first_nonzero_derivative_magnitudes_are_exact(self):
        expected = self.fixture["expected"]
        self.assertEqual(self.receipt["left_first_nonzero_derivative"], expected["left_first_nonzero_derivative"])
        self.assertEqual(self.receipt["right_first_nonzero_derivative"], expected["right_first_nonzero_derivative"])

    def test_local_diffeomorphism_preserves_order_but_rescales_leading_derivative(self):
        expected = self.fixture["expected"]
        self.assertEqual(self.receipt["coordinate_linear_term"], expected["coordinate_linear_term"])
        self.assertEqual(
            self.receipt["left_transformed_coefficients"],
            tuple(expected["left_transformed_coefficients_ascending"]),
        )
        self.assertEqual(
            self.receipt["right_transformed_coefficients"],
            tuple(expected["right_transformed_coefficients_ascending"]),
        )
        self.assertEqual(
            self.receipt["left_transformed_first_nonzero_order"],
            expected["left_transformed_first_nonzero_order"],
        )
        self.assertEqual(
            self.receipt["right_transformed_first_nonzero_order"],
            expected["right_transformed_first_nonzero_order"],
        )
        self.assertEqual(
            self.receipt["left_transformed_first_nonzero_derivative"],
            expected["left_transformed_first_nonzero_derivative"],
        )
        self.assertEqual(
            self.receipt["right_transformed_first_nonzero_derivative"],
            expected["right_transformed_first_nonzero_derivative"],
        )
        self.assertTrue(self.receipt["left_order_preserved"])
        self.assertTrue(self.receipt["right_order_preserved"])

    def test_leading_derivative_scaling_law_is_receipted(self):
        m_left = self.receipt["left_first_nonzero_order"]
        m_right = self.receipt["right_first_nonzero_order"]
        a = self.receipt["coordinate_linear_term"]
        self.assertEqual(
            self.receipt["left_transformed_first_nonzero_derivative"],
            self.receipt["left_first_nonzero_derivative"] * a ** m_left,
        )
        self.assertEqual(
            self.receipt["right_transformed_first_nonzero_derivative"],
            self.receipt["right_first_nonzero_derivative"] * a ** m_right,
        )

    def test_noninvertible_coordinate_map_is_refused(self):
        with self.assertRaisesRegex(ValueError, "nonzero linear term"):
            jet_order_vanishing_receipt([0, 0, 0, 1], [0, 0, 0, 0, 1], 2, [0, 0, 1])


if __name__ == "__main__":
    unittest.main()
