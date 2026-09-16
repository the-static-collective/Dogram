import unittest

from dogram.triangulator import (
    add,
    compare_order,
    square,
    triangular,
    triangulator_001_receipt,
)


class TriangulatorTests(unittest.TestCase):
    def test_triangular_and_square_order_has_structured_delta_at_five(self):
        receipt = triangulator_001_receipt()

        self.assertEqual(receipt["carrier"], 5)
        self.assertEqual(receipt["paths"]["triangular_after_square"], 325)
        self.assertEqual(receipt["paths"]["square_after_triangular"], 225)
        self.assertEqual(receipt["delta"], 100)
        self.assertEqual(receipt["structure"]["expected_delta"], 100)
        self.assertTrue(receipt["structure"]["passed"])
        self.assertEqual(receipt["classification"], "nonzero_structured")

    def test_commuting_additions_produce_zero_delta(self):
        receipt = compare_order(5, add(2), add(3))

        self.assertEqual(receipt["paths"]["second_after_first"], 10)
        self.assertEqual(receipt["paths"]["first_after_second"], 10)
        self.assertEqual(receipt["delta"], 0)
        self.assertEqual(receipt["classification"], "zero")

    def test_failed_declared_structure_does_not_claim_global_unstructure(self):
        receipt = compare_order(
            5,
            square,
            triangular,
            structure_test=lambda carrier, delta: delta == carrier,
            structure_label="delta == carrier",
        )

        self.assertEqual(receipt["delta"], 100)
        self.assertFalse(receipt["structure"]["passed"])
        self.assertEqual(receipt["classification"], "nonzero_not_structured_under_declared_test")

    def test_triangular_rejects_negative_input(self):
        with self.assertRaises(ValueError):
            triangular(-1)


if __name__ == "__main__":
    unittest.main()
