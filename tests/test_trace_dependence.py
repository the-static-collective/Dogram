from __future__ import annotations

import unittest

from dogram.trace_dependence import TraceInputError, analyze_trace_pair, canonical_trace


class TraceDependenceTests(unittest.TestCase):
    def test_independent_interleavings_share_one_trace_class(self) -> None:
        independence = {("a", "b"), ("b", "a")}
        self.assertEqual(canonical_trace(("a", "b"), independence), ("a", "b"))
        self.assertEqual(canonical_trace(("b", "a"), independence), ("a", "b"))
        result = analyze_trace_pair(("a", "b"), ("b", "a"), independence)
        self.assertTrue(result.equivalent)
        self.assertEqual(result.left_canonical, result.right_canonical)

    def test_same_frozen_endpoint_does_not_erase_declared_dependence_order(self) -> None:
        independence = {("a", "b"), ("b", "a")}
        result = analyze_trace_pair(("a", "c"), ("c", "a"), independence)
        self.assertFalse(result.equivalent)
        self.assertEqual(result.left_canonical, ("a", "c"))
        self.assertEqual(result.right_canonical, ("c", "a"))

    def test_partial_commutation_uses_dependence_poset_not_naive_bubble_sort(self) -> None:
        independence = {
            ("a", "b"), ("b", "a"),
            ("b", "c"), ("c", "b"),
        }
        self.assertEqual(canonical_trace(("c", "b", "a"), independence), ("b", "c", "a"))
        self.assertEqual(canonical_trace(("c", "a", "b"), independence), ("b", "c", "a"))

    def test_independence_must_be_symmetric_irreflexive_and_declared_on_used_labels(self) -> None:
        with self.assertRaises(TraceInputError):
            canonical_trace(("a", "b"), {("a", "b")})
        with self.assertRaises(TraceInputError):
            canonical_trace(("a",), {("a", "a")})
        with self.assertRaises(TraceInputError):
            canonical_trace(("a",), {("a", "z"), ("z", "a")})


if __name__ == "__main__":
    unittest.main()
