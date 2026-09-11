import json
from pathlib import Path
import unittest

from dogram.critical_hessian_inertia import critical_hessian_receipt


FIXTURE = Path(__file__).resolve().parents[1] / "research" / "fixtures" / "critical_hessian_inertia_001.json"


class CriticalHessianInertiaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())

    def test_nonlinear_terms_contribute_zero_at_declared_critical_point(self):
        data = self.fixture
        receipt = critical_hessian_receipt(
            data["base"]["hessian"],
            data["base"]["gradient"],
            data["coordinate_map"]["jacobian"],
            data["coordinate_map"]["component_hessians"],
        )
        self.assertEqual(receipt["second_order_correction"], ((0, 0), (0, 0)))
        self.assertEqual(receipt["transformed_hessian"], ((0, -4), (-4, -16)))

    def test_raw_hessian_characteristic_data_changes_under_congruence(self):
        data = self.fixture
        receipt = critical_hessian_receipt(
            data["base"]["hessian"],
            data["base"]["gradient"],
            data["coordinate_map"]["jacobian"],
            data["coordinate_map"]["component_hessians"],
        )
        self.assertEqual(receipt["base_characteristic_coefficients"], (1, 0, -4))
        self.assertEqual(receipt["transformed_characteristic_coefficients"], (1, 16, -16))
        self.assertNotEqual(
            receipt["base_characteristic_coefficients"],
            receipt["transformed_characteristic_coefficients"],
        )

    def test_determinant_scales_by_square_of_jacobian_determinant(self):
        data = self.fixture
        receipt = critical_hessian_receipt(
            data["base"]["hessian"],
            data["base"]["gradient"],
            data["coordinate_map"]["jacobian"],
            data["coordinate_map"]["component_hessians"],
        )
        self.assertEqual(receipt["base_determinant"], -4)
        self.assertEqual(receipt["jacobian_determinant"], 2)
        self.assertEqual(receipt["transformed_determinant"], -16)
        self.assertEqual(
            receipt["transformed_determinant"],
            receipt["base_determinant"] * receipt["jacobian_determinant"] ** 2,
        )

    def test_inertia_and_morse_index_survive_invertible_reparameterization(self):
        data = self.fixture
        receipt = critical_hessian_receipt(
            data["base"]["hessian"],
            data["base"]["gradient"],
            data["coordinate_map"]["jacobian"],
            data["coordinate_map"]["component_hessians"],
        )
        self.assertEqual(receipt["base_inertia"], (1, 1, 0))
        self.assertEqual(receipt["transformed_inertia"], (1, 1, 0))
        self.assertEqual(receipt["base_morse_index"], 1)
        self.assertEqual(receipt["transformed_morse_index"], 1)


if __name__ == "__main__":
    unittest.main()
