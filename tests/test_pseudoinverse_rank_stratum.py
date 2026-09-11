import json
import unittest
from fractions import Fraction
from pathlib import Path

from dogram.pseudoinverse_rank_stratum import (
    family_receipt,
    pseudoinverse,
    rank,
)


FIXTURE = Path(__file__).parent / "fixtures" / "pseudoinverse_rank_stratum_001.json"


class PseudoinverseRankStratumTests(unittest.TestCase):
    def test_frozen_fixture(self):
        data = json.loads(FIXTURE.read_text())
        self.assertEqual(data["parameters"], [2, 5, 10])
        self.assertEqual(data["limit"], ["1", "0"])

    def test_diagonal_pseudoinverse_and_rank(self):
        self.assertEqual(pseudoinverse((Fraction(1), Fraction(1, 5))), (Fraction(1), Fraction(5)))
        self.assertEqual(pseudoinverse((Fraction(1), Fraction(0))), (Fraction(1), Fraction(0)))
        self.assertEqual(rank((Fraction(1), Fraction(1, 5))), 2)
        self.assertEqual(rank((Fraction(1), Fraction(0))), 1)

    def test_rank_changing_approach_diverges(self):
        r = family_receipt(10)
        self.assertEqual(r["rank_changing_forward_delta"], Fraction(1, 10))
        self.assertEqual(r["rank_changing_pseudoinverse_delta"], Fraction(10))
        self.assertEqual(r["rank_changing_rank"], 2)
        self.assertEqual(r["limit_rank"], 1)

    def test_rank_preserving_approach_converges(self):
        r = family_receipt(10)
        self.assertEqual(r["rank_preserving_forward_delta"], Fraction(1, 10))
        self.assertEqual(r["rank_preserving_pseudoinverse_delta"], Fraction(1, 11))
        self.assertEqual(r["rank_preserving_rank"], 1)
        self.assertTrue(r["same_forward_limit"])
        self.assertTrue(r["rank_stratum_delta_exposed"])


if __name__ == "__main__":
    unittest.main()
