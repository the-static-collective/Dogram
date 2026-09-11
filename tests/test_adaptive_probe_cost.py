from fractions import Fraction
import unittest

from dogram.adaptive_probe_cost import (
    adaptive_receipt,
    expected_cost,
    fixed_receipt,
    worst_case_cost,
)


class AdaptiveProbeCostTests(unittest.TestCase):
    def test_adaptive_policy_uses_second_probe_only_after_non_a_root_outcome(self):
        receipt = adaptive_receipt()
        self.assertEqual(receipt["target_labels"], {"a": 1, "b": 1, "c": 0, "d": 0})
        self.assertEqual(receipt["paths"]["a"], ("root",))
        self.assertEqual(receipt["paths"]["b"], ("root", "branch"))
        self.assertEqual(receipt["paths"]["c"], ("root", "branch"))
        self.assertEqual(receipt["paths"]["d"], ("root", "branch"))
        self.assertEqual(receipt["state_costs"], {"a": 1, "b": 3, "c": 3, "d": 3})

    def test_fixed_probe_computes_same_target_with_uniform_state_cost(self):
        receipt = fixed_receipt()
        self.assertEqual(receipt["target_labels"], {"a": 1, "b": 1, "c": 0, "d": 0})
        self.assertEqual(receipt["state_costs"], {"a": 2, "b": 2, "c": 2, "d": 2})

    def test_worst_case_order_is_prior_independent(self):
        self.assertEqual(worst_case_cost(adaptive_receipt()), 3)
        self.assertEqual(worst_case_cost(fixed_receipt()), 2)

    def test_expected_cost_order_flips_when_only_prior_changes(self):
        heavy_a = {
            "a": Fraction(3, 4),
            "b": Fraction(1, 12),
            "c": Fraction(1, 12),
            "d": Fraction(1, 12),
        }
        uniform = {state: Fraction(1, 4) for state in "abcd"}

        self.assertEqual(expected_cost(adaptive_receipt(), heavy_a), Fraction(3, 2))
        self.assertEqual(expected_cost(fixed_receipt(), heavy_a), Fraction(2, 1))
        self.assertLess(
            expected_cost(adaptive_receipt(), heavy_a),
            expected_cost(fixed_receipt(), heavy_a),
        )

        self.assertEqual(expected_cost(adaptive_receipt(), uniform), Fraction(5, 2))
        self.assertEqual(expected_cost(fixed_receipt(), uniform), Fraction(2, 1))
        self.assertGreater(
            expected_cost(adaptive_receipt(), uniform),
            expected_cost(fixed_receipt(), uniform),
        )

    def test_expected_cost_requires_declared_normalized_prior(self):
        with self.assertRaises(ValueError):
            expected_cost(adaptive_receipt(), None)
        with self.assertRaises(ValueError):
            expected_cost(adaptive_receipt(), {"a": Fraction(1, 1)})


if __name__ == "__main__":
    unittest.main()
