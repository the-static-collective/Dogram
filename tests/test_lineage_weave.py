import unittest

from dogram.lineage_spine import canonical_digest
from dogram.lineage_weave import (
    make_parent_set,
    make_root_set,
    make_sum_merge,
    make_typed_parent,
    make_weave_capsule,
    make_weave_ledger,
    store_merge_receipt,
    store_parent_set,
    store_root_set,
    store_weave_capsule,
)


def sample_parent_set() -> dict[str, object]:
    braid = make_typed_parent("braid", "head-b", 109, ["root-a", "root-b"])
    spine = make_typed_parent("spine", "head-s", 36, ["root-c"])
    return make_parent_set([spine, braid])


class LineageWeaveParentTests(unittest.TestCase):
    def test_root_set_canonicalizes_sorted_unique_roots(self):
        left = make_root_set(["root-b", "root-a", "root-b"])
        right = make_root_set(["root-a", "root-b"])

        self.assertEqual(left, right)
        self.assertEqual(left["roots"], ["root-a", "root-b"])
        self.assertEqual(canonical_digest(left), canonical_digest(right))

    def test_typed_parent_has_exact_shape_and_root_set_digest(self):
        parent = make_typed_parent("braid", "head-braid", 109, ["root-b", "root-a"])

        self.assertEqual(
            set(parent),
            {"kind", "head_digest", "carrier", "root_set_digest"},
        )
        self.assertEqual(parent["kind"], "braid")
        self.assertEqual(parent["carrier"], 109)
        self.assertEqual(
            parent["root_set_digest"],
            canonical_digest(make_root_set(["root-a", "root-b"])),
        )

    def test_typed_parent_rejects_unknown_kind(self):
        with self.assertRaisesRegex(ValueError, "kind"):
            make_typed_parent("unknown", "head", 1, ["root"])

    def test_typed_parent_rejects_bool_carrier_and_empty_digests(self):
        with self.assertRaisesRegex(ValueError, "carrier"):
            make_typed_parent("spine", "head", True, ["root"])
        with self.assertRaisesRegex(ValueError, "head"):
            make_typed_parent("spine", "", 1, ["root"])
        with self.assertRaisesRegex(ValueError, "root"):
            make_typed_parent("spine", "head", 1, [])

    def test_parent_order_canonicalizes_to_same_identity(self):
        braid = make_typed_parent("braid", "head-b", 109, ["root-a", "root-b"])
        spine = make_typed_parent("spine", "head-s", 36, ["root-c"])

        left = make_parent_set([spine, braid])
        right = make_parent_set([braid, spine])

        self.assertEqual(left, right)
        self.assertEqual(canonical_digest(left), canonical_digest(right))
        self.assertEqual(
            [(p["kind"], p["head_digest"]) for p in left["parents"]],
            [("braid", "head-b"), ("spine", "head-s")],
        )

    def test_parent_set_requires_two_unique_typed_heads(self):
        braid = make_typed_parent("braid", "same", 109, ["root-a"])

        with self.assertRaisesRegex(ValueError, "at least two"):
            make_parent_set([braid])

        with self.assertRaisesRegex(ValueError, "unique"):
            make_parent_set([braid, dict(braid)])

    def test_parent_descriptor_shape_is_exact(self):
        polluted = {
            "kind": "spine",
            "head_digest": "head-s",
            "carrier": 36,
            "root_set_digest": "roots",
            "ancestry": {"recursive": True},
        }
        braid = make_typed_parent("braid", "head-b", 109, ["root-a"])

        with self.assertRaisesRegex(ValueError, "shape"):
            make_parent_set([polluted, braid])


class LineageWeaveMergeTests(unittest.TestCase):
    def test_sum_merge_uses_canonical_parent_order_and_outputs_145(self):
        parent_set = sample_parent_set()

        receipt = make_sum_merge(parent_set)

        self.assertEqual(receipt["operator"], "sum")
        self.assertEqual(receipt["inputs"], [109, 36])
        self.assertEqual(receipt["output"], 145)
        self.assertEqual(receipt["parent_set_digest"], canonical_digest(parent_set))

    def test_weave_capsule_is_fixed_shape_and_externalizes_plurality(self):
        parent_set = sample_parent_set()
        root_set = make_root_set(["root-a", "root-b", "root-c"])
        receipt = make_sum_merge(parent_set)

        capsule = make_weave_capsule(parent_set, root_set, receipt)

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
        self.assertEqual(capsule["carrier"], 145)
        self.assertEqual(capsule["carrier_origin"], "typed_parent_set_merge")
        self.assertEqual(capsule["parent_set_digest"], canonical_digest(parent_set))
        self.assertEqual(capsule["merge_receipt_digest"], canonical_digest(receipt))
        self.assertEqual(capsule["root_set_digest"], canonical_digest(root_set))
        self.assertNotIn("parents", capsule)
        self.assertNotIn("ancestry", capsule)

    def test_weave_ledger_stores_objects_by_content_digest(self):
        parent_set = sample_parent_set()
        root_set = make_root_set(["root-a", "root-b", "root-c"])
        receipt = make_sum_merge(parent_set)
        capsule = make_weave_capsule(parent_set, root_set, receipt)
        ledger = make_weave_ledger()

        parent_digest = store_parent_set(ledger, parent_set)
        root_digest = store_root_set(ledger, root_set)
        receipt_digest = store_merge_receipt(ledger, receipt)
        head_digest = store_weave_capsule(ledger, capsule)

        self.assertEqual(ledger["parent_sets"][parent_digest], parent_set)
        self.assertEqual(ledger["root_sets"][root_digest], root_set)
        self.assertEqual(ledger["merge_receipts"][receipt_digest], receipt)
        self.assertEqual(ledger["capsules"][head_digest], capsule)


if __name__ == "__main__":
    unittest.main()
