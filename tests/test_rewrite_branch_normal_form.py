from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.rewrite_branch import RewriteInputError, analyze_rewrite_branch


FIXTURE = Path(__file__).parent / "fixtures" / "rewrite_branch_normal_form_001.json"


class RewriteBranchNormalFormTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def _analyze(self, key: str):
        case = self.fixture[key]
        rules = tuple(tuple(rule) for rule in case["rules"])
        return case, analyze_rewrite_branch(case["start"], rules)

    def test_declared_branches_can_reconcile_to_one_normal_form(self) -> None:
        case, result = self._analyze("convergent")
        self.assertEqual(result.immediate_successors, tuple(case["expected_immediate_successors"]))
        self.assertEqual(result.normal_forms, tuple(case["expected_normal_forms"]))
        self.assertTrue(result.unique_normal_form)
        self.assertEqual(result.reachable_state_count, case["expected_reachable_state_count"])

    def test_same_initial_branching_can_terminate_in_distinct_normal_forms(self) -> None:
        case, result = self._analyze("divergent")
        self.assertEqual(result.immediate_successors, tuple(case["expected_immediate_successors"]))
        self.assertEqual(result.normal_forms, tuple(case["expected_normal_forms"]))
        self.assertFalse(result.unique_normal_form)
        self.assertEqual(result.reachable_state_count, case["expected_reachable_state_count"])

    def test_non_length_decreasing_rules_are_refused(self) -> None:
        with self.assertRaises(RewriteInputError) as caught:
            analyze_rewrite_branch("ab", (("ab", "ba"),))
        self.assertEqual(caught.exception.reason_code, "NON_DECREASING_RULE")


if __name__ == "__main__":
    unittest.main()
