from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.orientation_signature import analyze_orientation_signature
from dogram.reorientation_obstruction import compare_reorientation_signatures


FIXTURE = Path(__file__).parent / "fixtures" / "reorientation_obstruction_001.json"


def _load_fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text())


def _bases(data: dict[str, object]) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(basis) for basis in data["expected_bases"])  # type: ignore[index]


class ReorientationObstructionTests(unittest.TestCase):
    def test_global_sign_reversal_is_equivalent(self) -> None:
        data = _load_fixture()
        bases = _bases(data)
        left = tuple(data["expected_left_signs"])  # type: ignore[arg-type]
        right = tuple(-value for value in left)

        result = compare_reorientation_signatures(bases, left, right)

        self.assertTrue(result.equivalent)
        self.assertEqual(result.obstruction_bases, ())
        self.assertTrue(result.reproduces_right(bases, left, right))

    def test_single_element_reorientation_is_equivalent(self) -> None:
        data = _load_fixture()
        bases = _bases(data)
        left = tuple(data["expected_left_signs"])  # type: ignore[arg-type]
        right = tuple(
            -sign if "A" in basis else sign
            for basis, sign in zip(bases, left, strict=True)
        )

        result = compare_reorientation_signatures(bases, left, right)

        self.assertTrue(result.equivalent)
        self.assertEqual(result.obstruction_bases, ())
        self.assertTrue(result.reproduces_right(bases, left, right))

    def test_two_exact_realizations_can_obstruct_reorientation_equivalence(self) -> None:
        data = _load_fixture()
        rank = data["rank"]
        left_vectors = {
            label: tuple(vector)
            for label, vector in data["left_vectors"].items()  # type: ignore[union-attr]
        }
        right_vectors = {
            label: tuple(vector)
            for label, vector in data["right_vectors"].items()  # type: ignore[union-attr]
        }

        left_signature = analyze_orientation_signature(left_vectors, rank)  # type: ignore[arg-type]
        right_signature = analyze_orientation_signature(right_vectors, rank)  # type: ignore[arg-type]

        expected_bases = _bases(data)
        self.assertEqual(left_signature.nonzero_bases, expected_bases)
        self.assertEqual(right_signature.nonzero_bases, expected_bases)
        self.assertEqual(
            left_signature.determinants,
            tuple(data["expected_left_determinants"]),  # type: ignore[arg-type]
        )
        self.assertEqual(
            right_signature.determinants,
            tuple(data["expected_right_determinants"]),  # type: ignore[arg-type]
        )

        result = compare_reorientation_signatures(
            expected_bases,
            left_signature.signs,
            right_signature.signs,
        )

        self.assertFalse(result.equivalent)
        self.assertIsNone(result.global_flip)
        self.assertEqual(result.reoriented_elements, ())
        self.assertEqual(
            result.obstruction_bases,
            tuple(tuple(basis) for basis in data["expected_obstruction_bases"]),  # type: ignore[index]
        )

        counts = {label: 0 for label in "ABCDE"}
        left_product = 1
        right_product = 1
        lookup = {basis: index for index, basis in enumerate(expected_bases)}
        for basis in result.obstruction_bases:
            for label in basis:
                counts[label] += 1
            index = lookup[basis]
            left_product *= left_signature.signs[index]
            right_product *= right_signature.signs[index]

        self.assertEqual(len(result.obstruction_bases) % 2, 0)
        self.assertTrue(all(count % 2 == 0 for count in counts.values()))
        self.assertEqual(left_product, -right_product)


if __name__ == "__main__":
    unittest.main()
