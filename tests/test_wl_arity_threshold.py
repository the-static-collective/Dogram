from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.wl_arity_threshold import compare_graphs_wl


FIXTURE = Path(__file__).parent / "fixtures" / "wl_arity_threshold_001.json"


class WLArityThresholdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.rook_edges = tuple(tuple(edge) for edge in cls.fixture["rook_edges"])
        cls.shrikhande_edges = tuple(tuple(edge) for edge in cls.fixture["shrikhande_edges"])

    def test_three_wl_reaches_same_stable_color_histogram(self) -> None:
        result = compare_graphs_wl(self.rook_edges, self.shrikhande_edges, dimension=3)
        expected = self.fixture["k3"]

        self.assertFalse(result.distinguished)
        self.assertEqual(result.stable_round, expected["stable_round"])
        self.assertEqual(list(result.left_color_class_sizes), expected["color_class_sizes"])
        self.assertEqual(result.left_color_class_sizes, result.right_color_class_sizes)

    def test_four_point_atomic_type_distinguishes_before_refinement(self) -> None:
        result = compare_graphs_wl(self.rook_edges, self.shrikhande_edges, dimension=4)
        expected = self.fixture["k4"]

        self.assertTrue(result.distinguished)
        self.assertEqual(result.first_distinguishing_round, expected["first_distinguishing_round"])
        self.assertEqual(result.rounds_run, 0)
        self.assertNotEqual(result.left_color_class_sizes, result.right_color_class_sizes)

    def test_dimension_is_bounded_to_declared_specimen(self) -> None:
        with self.assertRaises(ValueError):
            compare_graphs_wl(self.rook_edges, self.shrikhande_edges, dimension=2)
        with self.assertRaises(ValueError):
            compare_graphs_wl(self.rook_edges, self.shrikhande_edges, dimension=5)


if __name__ == "__main__":
    unittest.main()
