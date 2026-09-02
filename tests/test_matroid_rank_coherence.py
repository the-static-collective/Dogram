from __future__ import annotations

import unittest

from dogram.matroid_rank_coherence import analyze_rank_table


class MatroidRankCoherenceTests(unittest.TestCase):
    def test_uniform_rank_one_control_is_coherent(self) -> None:
        ranks = {
            frozenset(): 0,
            frozenset({"a"}): 1,
            frozenset({"b"}): 1,
            frozenset({"c"}): 1,
            frozenset({"a", "b"}): 1,
            frozenset({"a", "c"}): 1,
            frozenset({"b", "c"}): 1,
            frozenset({"a", "b", "c"}): 1,
        }
        result = analyze_rank_table(("a", "b", "c"), ranks)
        self.assertTrue(result.is_matroid_rank)
        self.assertEqual(result.violations, ())

    def test_same_lower_order_surface_can_fail_only_at_the_triple(self) -> None:
        ranks = {
            frozenset(): 0,
            frozenset({"a"}): 1,
            frozenset({"b"}): 1,
            frozenset({"c"}): 1,
            frozenset({"a", "b"}): 1,
            frozenset({"a", "c"}): 1,
            frozenset({"b", "c"}): 1,
            frozenset({"a", "b", "c"}): 2,
        }
        result = analyze_rank_table(("a", "b", "c"), ranks)
        self.assertFalse(result.is_matroid_rank)
        submodular = [v for v in result.violations if v.kind == "SUBMODULARITY"]
        self.assertEqual(len(submodular), 3)
        self.assertEqual(submodular[0].residual, 1)
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
