from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.orientation_signature import analyze_orientation_signature


FIXTURE = Path(__file__).parent / "fixtures" / "orientation_signature_001.json"


class OrientationSignatureTests(unittest.TestCase):
    def test_same_basis_support_can_have_different_orientation_signature(self) -> None:
        data = json.loads(FIXTURE.read_text())
        left = analyze_orientation_signature(
            {key: tuple(value) for key, value in data["square"].items()}, rank=3
        )
        right = analyze_orientation_signature(
            {key: tuple(value) for key, value in data["interior"].items()}, rank=3
        )

        expected_bases = (
            ("A", "B", "C"),
            ("A", "B", "D"),
            ("A", "C", "D"),
            ("B", "C", "D"),
        )
        self.assertEqual(left.nonzero_bases, expected_bases)
        self.assertEqual(right.nonzero_bases, expected_bases)
        self.assertEqual(left.signs, (1, 1, 1, 1))
        self.assertEqual(right.signs, (1, 1, -1, 1))
        self.assertEqual(left.determinants, (4, 4, 4, 4))
        self.assertEqual(right.determinants, (4, 2, -2, 4))
        self.assertNotEqual(left.signs, right.signs)

    def test_zero_determinant_is_not_silently_signed(self) -> None:
        result = analyze_orientation_signature(
            {
                "A": (0, 0, 1),
                "B": (2, 0, 1),
                "C": (1, 0, 1),
            },
            rank=3,
        )
        self.assertEqual(result.nonzero_bases, ())
        self.assertEqual(result.determinants, ())
        self.assertEqual(result.signs, ())


if __name__ == "__main__":
    unittest.main()
