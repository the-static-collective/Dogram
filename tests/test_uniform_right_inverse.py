from fractions import Fraction
import json
from pathlib import Path
import unittest

from dogram.uniform_right_inverse import (
    apply_map,
    canonical_section,
    escape_uniform_bound,
    optimal_section_norm,
    section_receipt,
)


FIXTURE = Path(__file__).parent / "fixtures" / "uniform_right_inverse_001.json"


class UniformRightInverseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_canonical_section_is_exact_right_inverse(self):
        for n in self.fixture["frozen_parameters"]:
            for q in ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(3, 2), Fraction(-7, 3))):
                self.assertEqual(apply_map(n, canonical_section(n, q)), q)

    def test_optimal_norm_matches_frozen_values(self):
        got = [str(optimal_section_norm(n)) for n in self.fixture["frozen_parameters"]]
        self.assertEqual(got, self.fixture["frozen_optimal_section_norms"])

    def test_receipt_exposes_normalized_forward_and_inverse_blowup(self):
        for n in self.fixture["frozen_parameters"]:
            receipt = section_receipt(n)
            self.assertEqual(receipt["operator_norm"], Fraction(1))
            self.assertEqual(receipt["smallest_positive_singular_value"], Fraction(1, n))
            self.assertEqual(receipt["lower_bound_any_right_inverse"], Fraction(n))
            self.assertEqual(receipt["canonical_section_norm"], Fraction(n))
            self.assertTrue(receipt["lower_bound_attained"])

    def test_every_declared_uniform_bound_has_explicit_escape_parameter(self):
        for control in self.fixture["uniform_bound_controls"]:
            bound = Fraction(control["bound"])
            witness = escape_uniform_bound(bound)
            self.assertEqual(witness, control["witness_n"])
            self.assertGreater(optimal_section_norm(witness), bound)


if __name__ == "__main__":
    unittest.main()
