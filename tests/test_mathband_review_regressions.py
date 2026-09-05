from __future__ import annotations

import unittest

from dogram.mathband import ProbeObservation, evaluate_bridge


class MathBandReviewRegressionTests(unittest.TestCase):
    def test_numeric_probe_does_not_collapse_adjacent_53_bit_integers(self) -> None:
        left = 2**53
        right = left + 1
        receipt = evaluate_bridge(
            bridge_ref="precision-control",
            voice_a_ref="integer-a",
            voice_b_ref="integer-b",
            required_assumptions=(),
            provided_assumptions=(),
            probes=(
                ProbeObservation(
                    "precision-control",
                    left,
                    right,
                    comparison="numeric",
                    tolerance=0,
                    decisive=True,
                ),
            ),
        )

        outcome = receipt.outcomes[0]
        self.assertEqual(outcome.status, "BROKEN")
        self.assertEqual(outcome.residual, 1)
        self.assertEqual(receipt.first_decisive_probe, "precision-control")

    def test_numeric_probe_accepts_arbitrarily_large_finite_python_integers(self) -> None:
        left = 10**1000
        right = left + 1
        receipt = evaluate_bridge(
            bridge_ref="large-integer-control",
            voice_a_ref="integer-a",
            voice_b_ref="integer-b",
            required_assumptions=(),
            provided_assumptions=(),
            probes=(
                ProbeObservation(
                    "large-integer-control",
                    left,
                    right,
                    comparison="numeric",
                    tolerance=0,
                    decisive=True,
                ),
            ),
        )

        outcome = receipt.outcomes[0]
        self.assertEqual(outcome.status, "BROKEN")
        self.assertEqual(outcome.residual, 1)


if __name__ == "__main__":
    unittest.main()
