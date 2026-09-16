from __future__ import annotations

import unittest

from dogram.anti_collapse_reachability import analyze_collapse


class AntiCollapseReachabilityTests(unittest.TestCase):
    def test_bool_int_collapse_receipts_lost_type_distinctions(self) -> None:
        result = analyze_collapse(
            states=("int:1", "bool:true", "int:0", "bool:false"),
            rich_projection=(("int", 1), ("bool", True), ("int", 0), ("bool", False)),
            collapsed_projection=(1, True, 0, False),
        )

        self.assertTrue(result.lawful_quotient)
        self.assertEqual(
            result.lost_distinctions,
            (("int:1", "bool:true"), ("int:0", "bool:false")),
        )
        self.assertEqual(
            result.collapse_classes,
            (("int:1", "bool:true"), ("int:0", "bool:false")),
        )

    def test_erasing_relation_kind_loses_only_same_address_distinction(self) -> None:
        result = analyze_collapse(
            states=("spine@A", "braid@A", "spine@B"),
            rich_projection=(("A", "spine"), ("A", "braid"), ("B", "spine")),
            collapsed_projection=("A", "A", "B"),
        )

        self.assertTrue(result.lawful_quotient)
        self.assertEqual(result.lost_distinctions, (("spine@A", "braid@A"),))
        self.assertIn(("spine@A", "spine@B"), result.preserved_distinctions)
        self.assertIn(("braid@A", "spine@B"), result.preserved_distinctions)

    def test_identity_collapse_has_zero_loss(self) -> None:
        result = analyze_collapse(
            states=("a", "b", "c"),
            rich_projection=("a", "b", "c"),
            collapsed_projection=("a", "b", "c"),
        )

        self.assertTrue(result.lawful_quotient)
        self.assertEqual(result.lost_distinctions, ())
        self.assertEqual(result.collapse_classes, (("a",), ("b",), ("c",)))

    def test_projection_that_adds_information_is_not_a_lawful_collapse(self) -> None:
        result = analyze_collapse(
            states=("a", "b"),
            rich_projection=(0, 0),
            collapsed_projection=(0, 1),
        )

        self.assertFalse(result.lawful_quotient)
        self.assertIsNone(result.factorization_witness)
        self.assertEqual(result.lost_distinctions, ())
        self.assertEqual(result.preserved_distinctions, ())

    def test_rejects_mismatched_lengths_and_duplicate_state_names(self) -> None:
        with self.assertRaises(ValueError):
            analyze_collapse(("a",), (0, 1), (0, 1))
        with self.assertRaises(ValueError):
            analyze_collapse(("a", "a"), (0, 1), (0, 1))


if __name__ == "__main__":
    unittest.main()
