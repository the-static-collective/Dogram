from __future__ import annotations

import unittest

from dogram.ingleton import IngletonInputError, evaluate_ingleton


class IngletonRepresentabilityTests(unittest.TestCase):
    def test_vamos_witness_violates_ingleton_by_one(self) -> None:
        y1 = frozenset({3, 4})
        y2 = frozenset({5, 6})
        y3 = frozenset({1, 2})
        y4 = frozenset({7, 8})
        ranks = {
            y1: 2,
            y2: 2,
            y1 | y2: 3,
            y1 | y3: 3,
            y1 | y4: 3,
            y2 | y3: 3,
            y2 | y4: 3,
            y1 | y2 | y3: 4,
            y1 | y2 | y4: 4,
            y3 | y4: 4,
        }
        result = evaluate_ingleton(ranks, y1, y2, y3, y4)
        self.assertEqual(result.left, 16)
        self.assertEqual(result.right, 15)
        self.assertEqual(result.slack, -1)
        self.assertTrue(result.violates)

    def test_uniform_rank_four_control_satisfies_ingleton(self) -> None:
        y1 = frozenset({3, 4})
        y2 = frozenset({5, 6})
        y3 = frozenset({1, 2})
        y4 = frozenset({7, 8})
        needed = {
            y1,
            y2,
            y1 | y2,
            y1 | y3,
            y1 | y4,
            y2 | y3,
            y2 | y4,
            y1 | y2 | y3,
            y1 | y2 | y4,
            y3 | y4,
        }
        ranks = {subset: min(4, len(subset)) for subset in needed}
        result = evaluate_ingleton(ranks, y1, y2, y3, y4)
        self.assertEqual(result.left, 16)
        self.assertEqual(result.right, 20)
        self.assertEqual(result.slack, 4)
        self.assertFalse(result.violates)

    def test_missing_consumed_rank_is_refused(self) -> None:
        with self.assertRaises(IngletonInputError) as caught:
            evaluate_ingleton({}, frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}))
        self.assertEqual(caught.exception.reason_code, "MISSING_RANK")


if __name__ == "__main__":
    unittest.main()
