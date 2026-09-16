import unittest

from dogram.lineage_braid import (
    make_braid_capsule,
    make_parent_set,
    make_sum_merge,
    root_set_digest,
)
from dogram.lineage_spine import canonical_digest


def sample_parent_set() -> dict[str, object]:
    return make_parent_set(
        [
            {"head_digest": "head-b", "root_digest": "root-b", "carrier": 9},
            {"head_digest": "head-a", "root_digest": "root-a", "carrier": 100},
        ]
    )


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


if __name__ == "__main__":
    unittest.main()
