import unittest

from dogram.weak2_associator_cohomology import (
    associator,
    associator_receipt,
    normalized_2cochains,
    normalized_3cocycle,
    pentagon_residuals,
)


class Weak2AssociatorCohomologyTests(unittest.TestCase):
    def test_nontrivial_associator_is_normalized_and_pentagon_coherent(self):
        self.assertEqual(associator(1, 1, 1), 1)
        self.assertTrue(normalized_3cocycle())
        self.assertEqual(set(pentagon_residuals().values()), {0})

    def test_same_object_product_can_retain_nonzero_associator_witness(self):
        receipt = associator_receipt(1, 1, 1)
        self.assertEqual(receipt["left_object"], 1)
        self.assertEqual(receipt["right_object"], 1)
        self.assertEqual(receipt["associator_witness"], 1)
        self.assertFalse(receipt["strict_on_this_triple"])

    def test_associator_is_not_a_normalized_2_cochain_coboundary(self):
        cochains = normalized_2cochains()
        self.assertEqual(len(cochains), 2)
        self.assertTrue(all(not item["matches_associator"] for item in cochains))


if __name__ == "__main__":
    unittest.main()
