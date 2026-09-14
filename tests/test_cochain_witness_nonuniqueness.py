import json
import unittest
from pathlib import Path

from dogram.cochain_witness_nonuniqueness import receipt


FIXTURE = Path(__file__).parent / "fixtures" / "cochain_witness_nonuniqueness_001.json"


class CochainWitnessNonuniquenessTests(unittest.TestCase):
    def test_receipt_matches_frozen_fixture(self):
        expected = json.loads(FIXTURE.read_text())
        actual = receipt()

        self.assertEqual(expected["group"], actual["group"])
        self.assertEqual(expected["coefficients"], actual["coefficients"])
        self.assertEqual(expected["action"], actual["action"])
        self.assertEqual(expected["beta_one_support"], [list(x) for x in actual["beta_one_support"]])
        self.assertEqual(expected["beta_two_support"], [list(x) for x in actual["beta_two_support"]])
        self.assertEqual(
            expected["witness_difference_support"],
            [list(x) for x in actual["witness_difference_support"]],
        )
        self.assertEqual(
            expected["delta_beta_support"],
            [list(x) for x in actual["delta_beta_one_support"]],
        )
        self.assertEqual(actual["delta_beta_one_support"], actual["delta_beta_two_support"])
        self.assertEqual(expected["same_endpoint_delta"], actual["same_endpoint_delta"])
        self.assertEqual(expected["witnesses_distinct"], actual["witnesses_distinct"])
        self.assertEqual(expected["difference_is_two_cocycle"], actual["difference_is_two_cocycle"])
        self.assertEqual(expected["difference_is_one_coboundary"], actual["difference_is_one_coboundary"])
        self.assertEqual(
            expected["normalized_one_cochains_exhausted"],
            actual["normalized_one_cochains_exhausted"],
        )

    def test_same_nonzero_associator_change_has_two_distinct_witnesses(self):
        actual = receipt()
        self.assertTrue(actual["same_endpoint_delta"])
        self.assertTrue(actual["witnesses_distinct"])
        self.assertEqual(4, len(actual["delta_beta_one_support"]))

    def test_witness_difference_is_nontrivial_h2_residue_in_declared_model(self):
        actual = receipt()
        self.assertTrue(actual["difference_is_two_cocycle"])
        self.assertFalse(actual["difference_is_one_coboundary"])
        self.assertEqual(9, actual["normalized_one_cochains_exhausted"])


if __name__ == "__main__":
    unittest.main()
