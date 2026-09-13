from __future__ import annotations

import unittest

from dogram.tree_treewidth2_test_language import analyze_treewidth_language_gap


class TreeTreewidth2TestLanguageTests(unittest.TestCase):
    def test_all_tree_counts_collide_by_regular_target_recurrence(self) -> None:
        result = analyze_treewidth_language_gap()

        self.assertEqual(result.left_vertex_count, 6)
        self.assertEqual(result.right_vertex_count, 6)
        self.assertEqual(result.left_degree, 2)
        self.assertEqual(result.right_degree, 2)
        self.assertTrue(result.all_tree_counts_agree)

        for source_vertex_count in (1, 2, 3, 4, 7):
            expected = 6 * (2 ** (source_vertex_count - 1))
            self.assertEqual(result.tree_hom_count(source_vertex_count), expected)

    def test_triangle_is_a_treewidth2_source_that_separates_the_targets(self) -> None:
        result = analyze_treewidth_language_gap()

        self.assertEqual(result.k3_treewidth, 2)
        self.assertEqual(result.k3_hom_left, 0)
        self.assertEqual(result.k3_hom_right, 12)
        self.assertEqual(result.k3_hom_delta, 12)
        self.assertNotEqual(result.left_component_count, result.right_component_count)

    def test_receipt_does_not_promote_test_language_to_carrier_identity(self) -> None:
        result = analyze_treewidth_language_gap()

        self.assertTrue(result.all_tree_counts_agree)
        self.assertFalse(result.graphs_are_isomorphic)
        self.assertEqual(
            result.refusals,
            (
                "TREE-HOM COLLISION != GRAPH IDENTITY",
                "TREEWIDTH-2 DELTA != OCCURRENCE DELTA",
                "STRONGER TEST LANGUAGE != MORE TRUE",
                "HOMOMORPHISM COUNT != EVIDENCE COUNT",
            ),
        )


if __name__ == "__main__":
    unittest.main()
