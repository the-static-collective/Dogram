from fractions import Fraction
import unittest

from dogram.randomized_minimax_saddle import (
    ambiguity_barycentric_weights,
    expected_cost,
    mixed_cost_vector,
    pure_minimax,
    verify_saddle,
)


POLICIES = {
    "A": (2, 2, 7),
    "B": (1, 7, 1),
    "C": (5, 5, 1),
}

AMBIGUITY_VERTICES = (
    (Fraction(3, 5), Fraction(1, 5), Fraction(1, 5)),
    (Fraction(1, 5), Fraction(3, 5), Fraction(1, 5)),
    (Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)),
)

MIXTURE = {
    "A": Fraction(4, 9),
    "B": Fraction(0, 1),
    "C": Fraction(5, 9),
}

LEAST_FAVORABLE = (Fraction(2, 9), Fraction(4, 9), Fraction(1, 3))


class RandomizedMinimaxSaddleTests(unittest.TestCase):
    def test_pure_minimax_over_ambiguity_vertices_is_C_at_21_over_5(self):
        winner, value, maxima = pure_minimax(POLICIES, AMBIGUITY_VERTICES)
        self.assertEqual(winner, "C")
        self.assertEqual(value, Fraction(21, 5))
        self.assertEqual(
            maxima,
            {"A": Fraction(5, 1), "B": Fraction(23, 5), "C": Fraction(21, 5)},
        )

    def test_declared_mixture_has_constant_state_cost_11_over_3(self):
        vector = mixed_cost_vector(POLICIES, MIXTURE)
        self.assertEqual(vector, (Fraction(11, 3),) * 3)
        for prior in AMBIGUITY_VERTICES:
            self.assertEqual(expected_cost(vector, prior), Fraction(11, 3))

    def test_least_favorable_prior_is_inside_declared_ambiguity_triangle(self):
        weights = ambiguity_barycentric_weights(LEAST_FAVORABLE, AMBIGUITY_VERTICES)
        self.assertEqual(weights, (Fraction(1, 18), Fraction(11, 18), Fraction(1, 3)))
        self.assertEqual(sum(weights), Fraction(1, 1))
        self.assertTrue(all(weight >= 0 for weight in weights))
        self.assertEqual(
            {name: expected_cost(costs, LEAST_FAVORABLE) for name, costs in POLICIES.items()},
            {"A": Fraction(11, 3), "B": Fraction(11, 3), "C": Fraction(11, 3)},
        )

    def test_exact_saddle_closes_minimax_gap_only_after_policy_convexification(self):
        receipt = verify_saddle(POLICIES, AMBIGUITY_VERTICES, MIXTURE, LEAST_FAVORABLE)
        self.assertEqual(receipt["pure_minimax_value"], Fraction(21, 5))
        self.assertEqual(receipt["mixed_minimax_value"], Fraction(11, 3))
        self.assertEqual(receipt["maximin_value"], Fraction(11, 3))
        self.assertTrue(receipt["strict_gap"])
        self.assertTrue(receipt["saddle_closed"])


if __name__ == "__main__":
    unittest.main()
