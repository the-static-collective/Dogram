import unittest

from dogram.productive_desync import assess_productive_desync


class ProductiveDesyncTests(unittest.TestCase):
    def assess(self, **overrides):
        values = {
            "target_preserved": True,
            "execution_residual": {"step_trace": {"changed": True}},
            "baseline_reach_count": 18,
            "historical_reach_count": 36,
            "closure_reach_count": 54,
            "cut_declared": True,
            "cut_budget": 1,
            "cuts_used": 1,
            "returned_to_coherence": True,
        }
        values.update(overrides)
        return assess_productive_desync(**values)

    def test_historical_expansion_inside_budget_is_witness(self):
        result = self.assess()
        self.assertEqual((result.status, result.reason_code), ("WITNESS", None))
        self.assertTrue(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_closure_only_expansion_is_potential(self):
        result = self.assess(historical_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("POTENTIAL", "CLOSURE_ONLY"))
        self.assertFalse(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_target_failure_refuses_even_when_reach_expands(self):
        result = self.assess(target_preserved=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "TARGET_NOT_PRESERVED"))

    def test_missing_execution_residual_refuses(self):
        result = self.assess(execution_residual={})
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_EXECUTION_RESIDUAL"))

    def test_untyped_cut_refuses(self):
        result = self.assess(cut_declared=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "UNTYPED_CUT"))

    def test_budget_exceeded_refuses(self):
        result = self.assess(cut_budget=1, cuts_used=2)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "CUT_BUDGET_EXCEEDED"))

    def test_no_coherence_return_refuses_bounded_desync_label(self):
        result = self.assess(returned_to_coherence=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_COHERENCE_RETURN"))

    def test_no_reachability_gain_refuses(self):
        result = self.assess(historical_reach_count=18, closure_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_REACHABILITY_EXPANSION"))

    def test_history_cannot_exceed_declared_closure(self):
        with self.assertRaises(ValueError):
            self.assess(historical_reach_count=55, closure_reach_count=54)

    def test_negative_cut_budget_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(cut_budget=-1)

    def test_non_dictionary_residual_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(execution_residual=True)


if __name__ == "__main__":
    unittest.main()
