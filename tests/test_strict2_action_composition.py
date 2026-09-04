from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.strict2_action_composition import (
    analyze_strict2_action_composition,
    horizontal_compose,
    inversion_action_z3_by_z2,
)


FIXTURE = Path(__file__).parent / "fixtures" / "strict2_action_composition_001.json"


class Strict2ActionCompositionTests(unittest.TestCase):
    def test_declared_crossed_module_action(self) -> None:
        self.assertEqual(inversion_action_z3_by_z2(0, 1), 1)
        self.assertEqual(inversion_action_z3_by_z2(1, 1), 2)
        self.assertEqual(inversion_action_z3_by_z2(1, 2), 1)

    def test_same_outer_product_same_h_labels_different_higher_composite(self) -> None:
        even = horizontal_compose(left_h=1, left_g=0, right_h=1, right_g=0)
        odd = horizontal_compose(left_h=1, left_g=1, right_h=1, right_g=1)

        self.assertEqual(even.total_g, 0)
        self.assertEqual(odd.total_g, 0)
        self.assertEqual(even.composite_h, 2)
        self.assertEqual(odd.composite_h, 0)
        self.assertEqual(even.naive_h_without_action, 2)
        self.assertEqual(odd.naive_h_without_action, 2)

    def test_receipt_attributes_delta_to_internal_action_context(self) -> None:
        receipt = analyze_strict2_action_composition()
        self.assertTrue(receipt.same_outer_g)
        self.assertTrue(receipt.same_h_labels)
        self.assertEqual(receipt.even_factorization.composite_h, 2)
        self.assertEqual(receipt.odd_factorization.composite_h, 0)
        self.assertEqual(receipt.higher_composite_delta, 1)
        self.assertTrue(receipt.naive_composition_collapses_delta)

    def test_frozen_fixture_replays_exact_composition_surface(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        receipt = analyze_strict2_action_composition()

        self.assertEqual(fixture["higher_labels"], [1, 1])
        self.assertEqual(
            fixture["even_factorization"]["composite_h"],
            receipt.even_factorization.composite_h,
        )
        self.assertEqual(
            fixture["odd_factorization"]["composite_h"],
            receipt.odd_factorization.composite_h,
        )
        self.assertEqual(
            fixture["higher_composite_delta_mod_3"],
            receipt.higher_composite_delta,
        )


if __name__ == "__main__":
    unittest.main()
