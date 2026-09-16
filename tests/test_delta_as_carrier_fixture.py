import json
import unittest
from pathlib import Path

from dogram.triangulator import continue_from_delta, triangular, triangulator_001_receipt


FIXTURE = Path(__file__).parent / "fixtures" / "delta_as_carrier_001.json"


class DeltaAsCarrierFixtureTests(unittest.TestCase):
    def test_frozen_continuation_receipt_matches_fixture(self):
        expected = json.loads(FIXTURE.read_text())
        actual = continue_from_delta(triangulator_001_receipt(), triangular)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
