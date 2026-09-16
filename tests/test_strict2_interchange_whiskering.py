from __future__ import annotations

import unittest

from dogram.strict2_interchange_whiskering import (
    analyze_interchange_specimen,
    compose,
    identity,
    transposition_12,
    transposition_23,
)


class Strict2InterchangeWhiskeringTests(unittest.TestCase):
    def test_lawful_interchange_closes_exactly(self) -> None:
        receipt = analyze_interchange_specimen()
        self.assertEqual(receipt.lawful_vertical_then_horizontal, receipt.lawful_horizontal_then_vertical)
        self.assertEqual(receipt.lawful_vertical_then_horizontal, compose(transposition_12(), transposition_23()))

    def test_naive_actionless_horizontal_breaks_interchange(self) -> None:
        receipt = analyze_interchange_specimen()
        self.assertNotEqual(receipt.naive_vertical_then_horizontal, receipt.naive_horizontal_then_vertical)
        self.assertEqual(receipt.naive_vertical_then_horizontal, compose(transposition_12(), transposition_23()))
        self.assertEqual(receipt.naive_horizontal_then_vertical, compose(transposition_23(), transposition_12()))

    def test_whiskering_is_the_attributable_delta(self) -> None:
        receipt = analyze_interchange_specimen()
        self.assertEqual(receipt.left_bottom_h, transposition_12())
        self.assertEqual(receipt.left_top_h, identity())
        self.assertEqual(receipt.right_bottom_h, identity())
        self.assertEqual(receipt.right_top_h, transposition_23())
        self.assertNotEqual(receipt.whiskered_right_top_h, receipt.right_top_h)
        self.assertTrue(receipt.interchange_holds)
        self.assertTrue(receipt.naive_interchange_fails)


if __name__ == "__main__":
    unittest.main()
