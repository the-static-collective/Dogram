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
        self.assertEqual(receipt["fragile_collisions"], ((2, 3),))

    def test_pairwise_distance_receipt_is_exact(self):
        receipt = specimen()
        for family in (receipt["resilient"], receipt["fragile"]):
            self.assertEqual(minimum_distance(family), 2)
            self.assertTrue(all(hamming(a, b) >= 2 for i, a in enumerate(family) for b in family[i + 1 :]))

    def test_same_failure_cardinality_can_change_resilience_by_support(self):
        receipt = specimen()
        resilient = receipt["resilient"]
        declared = frozenset(receipt["declared_failure"])
        alternate = frozenset(receipt["alternate_same_cardinality_failure"])

        self.assertEqual(len(declared), len(alternate))
        self.assertTrue(survives_erasure(resilient, declared))
        self.assertFalse(survives_erasure(resilient, alternate))
        self.assertEqual(receipt["resilient_collisions_after_alternate_failure"], ((0, 1), (2, 3)))


if __name__ == "__main__":
    unittest.main()
