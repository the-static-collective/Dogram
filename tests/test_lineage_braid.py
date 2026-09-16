import unittest

from dogram.lineage_braid import make_parent_set, root_set_digest
from dogram.lineage_spine import canonical_digest


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


if __name__ == "__main__":
    unittest.main()
