import json
import unittest
from pathlib import Path

from dogram.triangulator import triangulator_001_receipt


FIXTURE = Path(__file__).parent / "fixtures" / "triangulator_001.json"


class TriangulatorFixtureTests(unittest.TestCase):
    def test_frozen_receipt_matches_fixture(self):
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(triangulator_001_receipt(), expected)


if __name__ == "__main__":
    unittest.main()
