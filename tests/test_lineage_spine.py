import copy
import unittest

from dogram.lineage_spine import (
    append_from_crossing,
    canonical_digest,
    make_ledger,
    make_root,
    store_capsule,
    store_receipt,
    verify_lineage,
)
from dogram.triangulator import compare_order, square, triangular, triangulator_001_receipt


def crossing_at(carrier: int) -> dict[str, object]:
    return compare_order(
        carrier,
        square,
        triangular,
        structure_test=lambda n, delta: delta == triangular(n - 1) ** 2,
        structure_label="delta == triangular(carrier - 1)^2",
    )


class LineageSpineTests(unittest.TestCase):
    def test_canonical_digest_is_order_independent_for_mappings(self):
        left = {"b": 2, "a": {"y": 4, "x": 3}}
        right = {"a": {"x": 3, "y": 4}, "b": 2}
        self.assertEqual(canonical_digest(left), canonical_digest(right))

    def test_two_generations_keep_bounded_capsule_shape(self):
        root = make_root(5)
        crossing0 = triangulator_001_receipt()
        child1 = append_from_crossing(root, crossing0)
        crossing1 = crossing_at(child1["carrier"])
        child2 = append_from_crossing(child1, crossing1)

        self.assertEqual(child1["carrier"], 100)
        self.assertEqual(child2["carrier"], 24_502_500)
        self.assertEqual(child1["generation"], 1)
        self.assertEqual(child2["generation"], 2)
        self.assertEqual(set(child1), set(child2))
        self.assertNotIn("ancestry", child1)
        self.assertNotIn("ancestry", child2)
        self.assertEqual(child1["root_digest"], child2["root_digest"])
        self.assertEqual(child2["parent_digest"], canonical_digest(child1))

    def test_complete_three_generation_line_is_reconstructible(self):
        ledger = make_ledger()
        root = make_root(5)
        root_digest = store_capsule(ledger, root)

        crossing0 = triangulator_001_receipt()
        store_receipt(ledger, crossing0)
        child1 = append_from_crossing(root, crossing0)
        child1_digest = store_capsule(ledger, child1)

        crossing1 = crossing_at(child1["carrier"])
        store_receipt(ledger, crossing1)
        child2 = append_from_crossing(child1, crossing1)
        child2_digest = store_capsule(ledger, child2)

        verified = verify_lineage(child2_digest, ledger)

        self.assertEqual(verified["status"], "complete")
        self.assertEqual(verified["generations"], [0, 1, 2])
        self.assertEqual(verified["carriers"], [5, 100, 24_502_500])
        self.assertEqual(verified["capsule_digests"], [root_digest, child1_digest, child2_digest])

    def test_missing_receipt_is_incomplete_not_invalid(self):
        ledger = make_ledger()
        root = make_root(5)
        store_capsule(ledger, root)
        crossing0 = triangulator_001_receipt()
        child1 = append_from_crossing(root, crossing0)
        child1_digest = store_capsule(ledger, child1)

        verified = verify_lineage(child1_digest, ledger)

        self.assertEqual(verified["status"], "incomplete")
        self.assertEqual(verified["reason"], "missing_crossing_receipt")

    def test_tampered_capsule_is_invalid(self):
        ledger = make_ledger()
        root = make_root(5)
        root_digest = store_capsule(ledger, root)
        crossing0 = triangulator_001_receipt()
        store_receipt(ledger, crossing0)
        child1 = append_from_crossing(root, crossing0)
        child1_digest = store_capsule(ledger, child1)

        ledger["capsules"][child1_digest] = copy.deepcopy(child1)
        ledger["capsules"][child1_digest]["generation"] = 99

        verified = verify_lineage(child1_digest, ledger)

        self.assertEqual(verified["status"], "invalid")
        self.assertEqual(verified["reason"], "capsule_digest_mismatch")
        self.assertIn(root_digest, ledger["capsules"])


if __name__ == "__main__":
    unittest.main()
