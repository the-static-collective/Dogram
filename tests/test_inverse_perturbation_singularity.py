from fractions import Fraction
import json
from pathlib import Path
import unittest

from dogram.inverse_perturbation_singularity import (
    family_receipt,
    forward_delta,
    inverse_delta,
    inverse_delta_ratio,
    resolvent_identity_holds,
)


FIXTURE = Path(__file__).parent / "fixtures" / "inverse_perturbation_singularity_001.json"


class InversePerturbationSingularityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_forward_delta_matches_frozen_values(self):
        got = [str(forward_delta(n)) for n in self.fixture["frozen_parameters"]]
        self.assertEqual(got, self.fixture["forward_deltas"])

    def test_inverse_delta_matches_frozen_values(self):
        got = [str(inverse_delta(n)) for n in self.fixture["frozen_parameters"]]
        self.assertEqual(got, self.fixture["inverse_deltas"])

    def test_amplification_ratio_matches_exact_formula(self):
        got = [str(inverse_delta_ratio(n)) for n in self.fixture["frozen_parameters"]]
        self.assertEqual(got, self.fixture["amplification_ratios"])
        for n in self.fixture["frozen_parameters"]:
            self.assertEqual(inverse_delta_ratio(n), Fraction(n * n, 2))

    def test_receipt_keeps_singularity_margin(self):
        for index, n in enumerate(self.fixture["frozen_parameters"]):
            receipt = family_receipt(n)
            self.assertEqual(receipt["operator_norm_A"], Fraction(1))
            self.assertEqual(receipt["operator_norm_B"], Fraction(1))
            self.assertEqual(str(receipt["distance_to_singularity_A"]), self.fixture["distance_to_singularity_A"][index])
            self.assertEqual(str(receipt["distance_to_singularity_B"]), self.fixture["distance_to_singularity_B"][index])
            self.assertTrue(receipt["resolvent_identity_holds"])

    def test_resolvent_identity_closes_exactly(self):
        for n in self.fixture["frozen_parameters"]:
            self.assertTrue(resolvent_identity_holds(n))


if __name__ == "__main__":
    unittest.main()
