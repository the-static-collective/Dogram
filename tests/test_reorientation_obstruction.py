from __future__ import annotations

import unittest

from dogram.reorientation_obstruction import compare_reorientation_signatures


BASES = (
    ("A", "B", "C"),
    ("A", "B", "D"),
    ("A", "B", "E"),
    ("A", "C", "D"),
    ("A", "C", "E"),
    ("A", "D", "E"),
    ("B", "C", "D"),
    ("B", "C", "E"),
    ("B", "D", "E"),
    ("C", "D", "E"),
)


class ReorientationObstructionTests(unittest.TestCase):
    def test_global_sign_reversal_is_equivalent(self) -> None:
        left = (-1, -1, -1, 1, 1, 1, 1, 1, 1, -1)
        right = tuple(-value for value in left)

        result = compare_reorientation_signatures(BASES, left, right)

        self.assertTrue(result.equivalent)
        self.assertEqual(result.obstruction_bases, ())
        self.assertTrue(result.reproduces_right(BASES, left, right))

    def test_single_element_reorientation_is_equivalent(self) -> None:
        left = (-1, -1, -1, 1, 1, 1, 1, 1, 1, -1)
        right = tuple(
            -sign if "A" in basis else sign
            for basis, sign in zip(BASES, left, strict=True)
        )

        result = compare_reorientation_signatures(BASES, left, right)

        self.assertTrue(result.equivalent)
        self.assertEqual(result.obstruction_bases, ())
        self.assertTrue(result.reproduces_right(BASES, left, right))

    def test_same_basis_support_can_have_non_reorientation_equivalent_signatures(self) -> None:
        left = (-1, -1, -1, 1, 1, 1, 1, 1, 1, -1)
        right = (-1, -1, -1, 1, 1, -1, 1, 1, 1, -1)

        result = compare_reorientation_signatures(BASES, left, right)

        self.assertFalse(result.equivalent)
        self.assertIsNone(result.global_flip)
        self.assertEqual(result.reoriented_elements, ())
        self.assertGreaterEqual(len(result.obstruction_bases), 2)
        self.assertEqual(len(result.obstruction_bases) % 2, 0)

        counts = {label: 0 for label in "ABCDE"}
        left_product = 1
        right_product = 1
        lookup = {basis: index for index, basis in enumerate(BASES)}
        for basis in result.obstruction_bases:
            for label in basis:
                counts[label] += 1
            index = lookup[basis]
            left_product *= left[index]
            right_product *= right[index]

        self.assertTrue(all(count % 2 == 0 for count in counts.values()))
        self.assertEqual(left_product, -right_product)


if __name__ == "__main__":
    unittest.main()
