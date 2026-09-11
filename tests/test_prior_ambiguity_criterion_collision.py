from fractions import Fraction
import unittest

from dogram.prior_ambiguity_criterion_collision import (
    bayes_costs,
    expected_cost,
    max_expected_costs,
    max_regrets,
    minimax_regret_winner,
    robust_minimax_winner,
    unique_bayes_winner,
)


POLICIES = {
    "A": (2, 2, 7),
    "B": (1, 7, 1),
    "C": (5, 5, 1),
}

BAYES_PRIOR = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))

AMBIGUITY_PRIORS = (
    (Fraction(3, 5), Fraction(1, 5), Fraction(1, 5)),
    (Fraction(1, 5), Fraction(3, 5), Fraction(1, 5)),
    (Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)),
)


class PriorAmbiguityCriterionCollisionTests(unittest.TestCase):
    def test_expected_cost_is_exact_and_requires_normalized_prior(self):
        self.assertEqual(expected_cost(POLICIES["A"], BAYES_PRIOR), Fraction(17, 6))
        with self.assertRaises(ValueError):
            expected_cost(POLICIES["A"], (Fraction(1, 2), Fraction(1, 2)))
        with self.assertRaises(ValueError):
            expected_cost(POLICIES["A"], (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)))

    def test_declared_bayes_prior_selects_A(self):
        costs = bayes_costs(POLICIES, BAYES_PRIOR)
        self.assertEqual(
            costs,
            {"A": Fraction(17, 6), "B": Fraction(3, 1), "C": Fraction(13, 3)},
        )
        self.assertEqual(unique_bayes_winner(POLICIES, BAYES_PRIOR), "A")

    def test_robust_minimax_expected_cost_over_declared_prior_set_selects_C(self):
        costs = max_expected_costs(POLICIES, AMBIGUITY_PRIORS)
        self.assertEqual(
            costs,
            {"A": Fraction(5, 1), "B": Fraction(23, 5), "C": Fraction(21, 5)},
        )
        self.assertEqual(robust_minimax_winner(POLICIES, AMBIGUITY_PRIORS), "C")

    def test_minimax_regret_over_same_declared_prior_set_selects_B(self):
        regrets = max_regrets(POLICIES, AMBIGUITY_PRIORS)
        self.assertEqual(
            regrets,
            {"A": Fraction(14, 5), "B": Fraction(8, 5), "C": Fraction(2, 1)},
        )
        self.assertEqual(minimax_regret_winner(POLICIES, AMBIGUITY_PRIORS), "B")

    def test_same_policy_table_supports_three_distinct_criterion_winners(self):
        self.assertEqual(unique_bayes_winner(POLICIES, BAYES_PRIOR), "A")
        self.assertEqual(robust_minimax_winner(POLICIES, AMBIGUITY_PRIORS), "C")
        self.assertEqual(minimax_regret_winner(POLICIES, AMBIGUITY_PRIORS), "B")


if __name__ == "__main__":
    unittest.main()
