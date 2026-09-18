from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.matroid_rank_coherence import analyze_rank_table


FIXTURE = Path(__file__).parent / "fixtures" / "matroid_rank_coherence_001.json"


def _load_case(name: str) -> tuple[tuple[str, ...], dict[frozenset[str], int], int]:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    ground_set = tuple(data["ground_set"])
    ranks = {
        frozenset(record["subset"]): record["rank"]
        for record in data[name]
    }
    return ground_set, ranks, data["expected_submodularity_residual"]


class MatroidRankCoherenceTests(unittest.TestCase):
    def test_uniform_rank_one_control_is_coherent(self) -> None:
        ground_set, ranks, _ = _load_case("valid_u1_3")
        result = analyze_rank_table(ground_set, ranks)
        self.assertTrue(result.is_matroid_rank)
        self.assertEqual(result.violations, ())

    def test_same_lower_order_surface_can_fail_only_at_the_triple(self) -> None:
        ground_set, ranks, expected_residual = _load_case("hostile_top_lift")
        result = analyze_rank_table(ground_set, ranks)
        self.assertFalse(result.is_matroid_rank)
        submodular = [v for v in result.violations if v.kind == "SUBMODULARITY"]
        self.assertEqual(len(submodular), 3)
        self.assertEqual(submodular[0].residual, expected_residual)
        self.assertEqual(submodular[0].left, ("a", "b"))
        self.assertEqual(submodular[0].right, ("a", "c"))
        self.assertEqual(submodular[0].intersection, ("a",))
        self.assertEqual(submodular[0].union, ("a", "b", "c"))

    def test_incomplete_rank_table_is_refused(self) -> None:
        ranks = {frozenset(): 0, frozenset({"a"}): 1}
        with self.assertRaises(ValueError):
            analyze_rank_table(("a", "b"), ranks)


if __name__ == "__main__":
    unittest.main()
