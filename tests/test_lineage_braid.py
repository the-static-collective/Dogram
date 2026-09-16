import copy
import unittest

from dogram.lineage_braid import (
    make_braid_capsule,
    make_braid_ledger,
    make_parent_set,
    make_sum_merge,
    root_set_digest,
    store_braid_capsule,
    store_merge_receipt,
    store_parent_set,
    verify_braid,
)
from dogram.lineage_spine import (
    append_from_crossing,
    canonical_digest,
    make_ledger as make_spine_ledger,
    make_root,
    store_capsule as store_spine_capsule,
    store_receipt as store_spine_receipt,
)
from dogram.triangulator import compare_order, square, triangular, triangulator_001_receipt


def sample_parent_set() -> dict[str, object]:
    return make_parent_set(
        [
            {"head_digest": "head-b", "root_digest": "root-b", "carrier": 9},
            {"head_digest": "head-a", "root_digest": "root-a", "carrier": 100},
        ]
    )


def crossing_at(carrier: int) -> dict[str, object]:
    receipt = compare_order(
        carrier,
        square,
        triangular,
        structure_test=lambda n, delta: delta == triangular(n - 1) ** 2,
        structure_label="delta == triangular(carrier - 1)^2",
    )
    receipt["specimen"] = "TRIANGULATOR-001"
    return receipt


def build_spine_parents() -> tuple[dict[str, object], list[dict[str, object]]]:
    ledger = make_spine_ledger()

    root5 = make_root(5)
    store_spine_capsule(ledger, root5)
    crossing5 = triangulator_001_receipt()
    store_spine_receipt(ledger, crossing5)
    child5 = append_from_crossing(root5, crossing5)
    head5 = store_spine_capsule(ledger, child5)

    root3 = make_root(3)
    store_spine_capsule(ledger, root3)
    crossing3 = crossing_at(3)
    store_spine_receipt(ledger, crossing3)
    child3 = append_from_crossing(root3, crossing3)
    head3 = store_spine_capsule(ledger, child3)

    parents = [
        {
            "head_digest": head5,
            "root_digest": child5["root_digest"],
            "carrier": child5["carrier"],
        },
        {
            "head_digest": head3,
            "root_digest": child3["root_digest"],
            "carrier": child3["carrier"],
        },
    ]
    return ledger, parents


def build_complete_braid() -> tuple[
    dict[str, object],
    dict[str, object],
    str,
    dict[str, object],
]:
    spine_ledger, parents = build_spine_parents()
    parent_set = make_parent_set(parents)
    merge_receipt = make_sum_merge(parent_set)
    capsule = make_braid_capsule(parent_set, merge_receipt)

    braid_ledger = make_braid_ledger()
    store_parent_set(braid_ledger, parent_set)
    store_merge_receipt(braid_ledger, merge_receipt)
    head_digest = store_braid_capsule(braid_ledger, capsule)
    return spine_ledger, braid_ledger, head_digest, parent_set


class LineageBraidParentSetTests(unittest.TestCase):
    def test_parent_order_canonicalizes_to_same_identity(self):
        a = {"head_digest": "head-a", "root_digest": "root-a", "carrier": 100}
        b = {"head_digest": "head-b", "root_digest": "root-b", "carrier": 9}

        left = make_parent_set([a, b])
        right = make_parent_set([b, a])

        self.assertEqual(left, right)
        self.assertEqual(canonical_digest(left), canonical_digest(right))
        self.assertEqual([p["head_digest"] for p in left["parents"]], ["head-a", "head-b"])

    def test_parent_set_requires_at_least_two_distinct_heads(self):
        a = {"head_digest": "head-a", "root_digest": "root-a", "carrier": 100}

        with self.assertRaisesRegex(ValueError, "at least two"):
            make_parent_set([a])

        with self.assertRaisesRegex(ValueError, "unique"):
            make_parent_set([a, dict(a)])

    def test_parent_descriptor_shape_is_exact(self):
        polluted = {
            "head_digest": "head-a",
            "root_digest": "root-a",
            "carrier": 100,
            "ancestry": {"recursive": True},
        }
        b = {"head_digest": "head-b", "root_digest": "root-b", "carrier": 9}

        with self.assertRaisesRegex(ValueError, "descriptor shape"):
            make_parent_set([polluted, b])

    def test_root_set_digest_deduplicates_shared_roots(self):
        a = {"head_digest": "head-a", "root_digest": "root-shared", "carrier": 100}
        b = {"head_digest": "head-b", "root_digest": "root-shared", "carrier": 9}
        parent_set = make_parent_set([a, b])

        expected = canonical_digest({"roots": ["root-shared"]})
        self.assertEqual(root_set_digest(parent_set), expected)


class LineageBraidMergeTests(unittest.TestCase):
    def test_sum_merge_uses_canonical_parent_order_and_outputs_109(self):
        parent_set = sample_parent_set()

        receipt = make_sum_merge(parent_set)

        self.assertEqual(receipt["operator"], "sum")
        self.assertEqual(receipt["inputs"], [100, 9])
        self.assertEqual(receipt["output"], 109)
        self.assertEqual(receipt["parent_set_digest"], canonical_digest(parent_set))

    def test_braid_capsule_is_fixed_shape_and_points_to_external_objects(self):
        parent_set = sample_parent_set()
        receipt = make_sum_merge(parent_set)

        capsule = make_braid_capsule(parent_set, receipt)

        self.assertEqual(
            set(capsule),
            {
                "schema",
                "specimen",
                "carrier",
                "carrier_origin",
                "parent_set_digest",
                "merge_receipt_digest",
                "root_set_digest",
            },
        )
        self.assertEqual(capsule["carrier"], 109)
        self.assertEqual(capsule["carrier_origin"], "parent_set_merge")
        self.assertEqual(capsule["parent_set_digest"], canonical_digest(parent_set))
        self.assertEqual(capsule["merge_receipt_digest"], canonical_digest(receipt))
        self.assertEqual(capsule["root_set_digest"], root_set_digest(parent_set))
        self.assertNotIn("parents", capsule)
        self.assertNotIn("ancestry", capsule)


class LineageBraidVerificationTests(unittest.TestCase):
    def test_complete_braid_reconstructs_both_parent_lines(self):
        spine_ledger, braid_ledger, head_digest, _ = build_complete_braid()

        result = verify_braid(head_digest, braid_ledger, spine_ledger)

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["carrier"], 109)
        self.assertEqual(result["parent_count"], 2)
        self.assertEqual(len(result["parent_heads"]), 2)

    def test_missing_parent_witness_is_incomplete_not_invalid(self):
        spine_ledger, braid_ledger, head_digest, parent_set = build_complete_braid()
        missing_head = parent_set["parents"][0]["head_digest"]
        del spine_ledger["capsules"][missing_head]

        result = verify_braid(head_digest, braid_ledger, spine_ledger)

        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["reason"], "parent_line_incomplete")
        self.assertEqual(result["parent_head"], missing_head)

    def test_contradictory_parent_carrier_is_invalid(self):
        spine_ledger, parents = build_spine_parents()
        polluted = copy.deepcopy(parents)
        polluted[0]["carrier"] += 1
        parent_set = make_parent_set(polluted)
        merge_receipt = make_sum_merge(parent_set)
        capsule = make_braid_capsule(parent_set, merge_receipt)
        braid_ledger = make_braid_ledger()
        store_parent_set(braid_ledger, parent_set)
        store_merge_receipt(braid_ledger, merge_receipt)
        head_digest = store_braid_capsule(braid_ledger, capsule)

        result = verify_braid(head_digest, braid_ledger, spine_ledger)

        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_carrier_mismatch")

    def test_invalid_parent_spine_propagates_invalid(self):
        spine_ledger, braid_ledger, head_digest, parent_set = build_complete_braid()
        parent_head = parent_set["parents"][0]["head_digest"]
        spine_ledger["capsules"][parent_head] = copy.deepcopy(spine_ledger["capsules"][parent_head])
        spine_ledger["capsules"][parent_head]["carrier"] += 1

        result = verify_braid(head_digest, braid_ledger, spine_ledger)

        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_line_invalid")
        self.assertEqual(result["parent_head"], parent_head)

    def test_missing_merge_receipt_is_incomplete(self):
        spine_ledger, parents = build_spine_parents()
        parent_set = make_parent_set(parents)
        merge_receipt = make_sum_merge(parent_set)
        capsule = make_braid_capsule(parent_set, merge_receipt)
        braid_ledger = make_braid_ledger()
        store_parent_set(braid_ledger, parent_set)
        head_digest = store_braid_capsule(braid_ledger, capsule)

        result = verify_braid(head_digest, braid_ledger, spine_ledger)

        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["reason"], "missing_merge_receipt")


if __name__ == "__main__":
    unittest.main()
