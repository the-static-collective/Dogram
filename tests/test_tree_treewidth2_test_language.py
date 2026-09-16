from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.tree_treewidth2_test_language import analyze_treewidth_language_gap


FIXTURE = Path(__file__).parent / "fixtures" / "tree_treewidth2_test_language_001.json"


class TreeTreewidth2TestLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.result = analyze_treewidth_language_gap()

    def test_all_tree_counts_collide_by_regular_target_recurrence(self) -> None:
        result = self.result
        fixture = self.fixture

        self.assertEqual(result.left_vertex_count, fixture["left"]["vertex_count"])
        self.assertEqual(result.right_vertex_count, fixture["right"]["vertex_count"])
        self.assertEqual(result.left_degree, fixture["left"]["degree"])
        self.assertEqual(result.right_degree, fixture["right"]["degree"])
        self.assertTrue(result.all_tree_counts_agree)

        for source_vertex_count, expected in zip(
            fixture["tree_formula"]["sample_vertex_counts"],
            fixture["tree_formula"]["sample_counts"],
            strict=True,
        ):
            self.assertEqual(result.tree_hom_count(source_vertex_count), expected)

    def test_triangle_is_a_treewidth2_source_that_separates_the_targets(self) -> None:
        result = self.result
        separator = self.fixture["separator"]

        self.assertEqual(result.k3_treewidth, separator["treewidth"])
        self.assertEqual(result.k3_hom_left, separator["hom_left"])
        self.assertEqual(result.k3_hom_right, separator["hom_right"])
        self.assertEqual(result.k3_hom_delta, separator["delta"])
        self.assertEqual(result.left_component_count, self.fixture["left"]["component_count"])
        self.assertEqual(result.right_component_count, self.fixture["right"]["component_count"])

    def test_receipt_does_not_promote_test_language_to_carrier_identity(self) -> None:
        result = self.result

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
