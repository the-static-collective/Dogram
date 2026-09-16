import unittest

from dogram.declared_failure_family import collapsed_pairs, hamming, minimum_distance, specimen, survives_erasure


class DeclaredFailureFamilyTests(unittest.TestCase):
    def test_same_minimum_distance_different_declared_failure_resilience(self):
        receipt = specimen()
        self.assertEqual(receipt["minimum_distance"], {"resilient": 2, "fragile": 2})
        self.assertEqual(receipt["declared_failure"], [0, 1])
        self.assertEqual(
            receipt["survives_declared_failure"],
            {"resilient": True, "fragile": False},
        )
        self.assertEqual(receipt["fragile_collisions"], ((0, 3),))

    def test_pairwise_distance_receipt_is_exact(self):
        receipt = specimen()
        for family in (receipt["resilient"], receipt["fragile"]):
            self.assertEqual(minimum_distance(family), 2)
            self.assertTrue(all(hamming(a, b) >= 2 for i, a in enumerate(family) for b in family[i + 1 :]))

    def test_declared_failure_is_about_coordinates_not_only_cardinality(self):
        fragile = specimen()["fragile"]
        self.assertFalse(survives_erasure(fragile, frozenset({0, 1})))
        self.assertTrue(survives_erasure(fragile, frozenset({2, 3})))
        self.assertEqual(collapsed_pairs(fragile, frozenset({0, 1})), ((0, 3),))


if __name__ == "__main__":
    unittest.main()
