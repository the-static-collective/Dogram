from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.wl_arity_separation import analyze_pair


ROOT = Path(__file__).resolve().parents[1]


class WeisfeilerLemanAritySeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with (ROOT / "tests/fixtures/strongly_regular_clique_collision_001.json").open() as handle:
            cls.graphs = json.load(handle)
        with (ROOT / "tests/fixtures/wl_arity_separation_001.json").open() as handle:
            cls.expected = json.load(handle)

    def test_two_dimensional_refinement_stays_collided(self) -> None:
        receipt = analyze_pair(
            self.graphs["rook_4x4"]["edges"],
            self.graphs["shrikhande"]["edges"],
            dimension=2,
        )
        expected = self.expected["dimension_2"]
        self.assertEqual(list(receipt.left_initial_class_sizes), expected["initial_class_sizes"])
        self.assertEqual(list(receipt.right_initial_class_sizes), expected["initial_class_sizes"])
        self.assertEqual(list(receipt.left_one_round_class_sizes), expected["one_round_class_sizes"])
        self.assertEqual(list(receipt.right_one_round_class_sizes), expected["one_round_class_sizes"])
        self.assertEqual(receipt.left_stable_after_one_round, expected["stable_after_one_round"])
        self.assertEqual(receipt.right_stable_after_one_round, expected["stable_after_one_round"])
        self.assertEqual(receipt.distinguished_after_one_round, expected["distinguished"])

    def test_three_dimensional_refinement_separates_in_one_round(self) -> None:
        receipt = analyze_pair(
            self.graphs["rook_4x4"]["edges"],
            self.graphs["shrikhande"]["edges"],
            dimension=3,
        )
        expected = self.expected["dimension_3"]
        self.assertEqual(list(receipt.left_initial_class_sizes), expected["initial_class_sizes"])
        self.assertEqual(list(receipt.right_initial_class_sizes), expected["initial_class_sizes"])
        self.assertEqual(list(receipt.left_one_round_class_sizes), expected["rook_one_round_class_sizes"])
        self.assertEqual(list(receipt.right_one_round_class_sizes), expected["shrikhande_one_round_class_sizes"])
        self.assertTrue(receipt.distinguished_after_one_round)

    def test_dimension_guard_is_explicit(self) -> None:
        with self.assertRaisesRegex(ValueError, "dimension must be 2 or 3"):
            analyze_pair(
                self.graphs["rook_4x4"]["edges"],
                self.graphs["shrikhande"]["edges"],
                dimension=4,
            )


if __name__ == "__main__":
    unittest.main()
