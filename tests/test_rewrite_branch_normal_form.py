from __future__ import annotations

import unittest

from dogram.rewrite_branch import RewriteInputError, analyze_rewrite_branch


class RewriteBranchNormalFormTests(unittest.TestCase):
    def test_declared_branches_can_reconcile_to_one_normal_form(self) -> None:
        result = analyze_rewrite_branch(
            "abc",
            (("abc", "ab"), ("abc", "ac"), ("ab", "a"), ("ac", "a")),
        )
        self.assertEqual(result.immediate_successors, ("ab", "ac"))
        self.assertEqual(result.normal_forms, ("a",))
        self.assertTrue(result.unique_normal_form)
        self.assertEqual(result.reachable_state_count, 4)

    def test_same_initial_branching_can_terminate_in_distinct_normal_forms(self) -> None:
        result = analyze_rewrite_branch(
            "abc",
            (("abc", "ab"), ("abc", "ac"), ("ab", "a"), ("ac", "c")),
        )
        self.assertEqual(result.immediate_successors, ("ab", "ac"))
        self.assertEqual(result.normal_forms, ("a", "c"))
        self.assertFalse(result.unique_normal_form)
        self.assertEqual(result.reachable_state_count, 5)

    def test_non_length_decreasing_rules_are_refused(self) -> None:
        with self.assertRaises(RewriteInputError) as caught:
            analyze_rewrite_branch("ab", (("ab", "ba"),))
        self.assertEqual(caught.exception.reason_code, "NON_DECREASING_RULE")


if __name__ == "__main__":
    unittest.main()
