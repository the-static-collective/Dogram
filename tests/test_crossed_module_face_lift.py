from __future__ import annotations

import unittest

from dogram.crossed_module_face_lift import (
    CyclicCrossedModuleInputError,
    analyze_cyclic_face_lifts,
)


class CrossedModuleFaceLiftTests(unittest.TestCase):
    def test_same_boundary_can_have_distinct_higher_face_lifts(self) -> None:
        receipt = analyze_cyclic_face_lifts(
            h_modulus=4,
            g_modulus=2,
            boundary_multiplier=1,
            boundary_value=0,
        )

        self.assertEqual(receipt.kernel, (0, 2))
        self.assertEqual(receipt.face_lifts, (0, 2))
        self.assertEqual(receipt.boundary_images, (0, 0))
        self.assertEqual(receipt.lift_deltas, (2,))
        self.assertTrue(receipt.boundary_forgets_higher_lift)

    def test_injective_boundary_control_has_unique_lift(self) -> None:
        receipt = analyze_cyclic_face_lifts(
            h_modulus=2,
            g_modulus=2,
            boundary_multiplier=1,
            boundary_value=0,
        )

        self.assertEqual(receipt.kernel, (0,))
        self.assertEqual(receipt.face_lifts, (0,))
        self.assertEqual(receipt.lift_deltas, ())
        self.assertFalse(receipt.boundary_forgets_higher_lift)

    def test_receipt_is_explicit_and_bad_cyclic_boundary_is_refused(self) -> None:
        receipt = analyze_cyclic_face_lifts(4, 2, 1, 0)
        self.assertEqual(
            receipt.to_data(),
            {
                "crossed_module": {
                    "H": "Z/4Z",
                    "G": "Z/2Z",
                    "boundary": "h -> 1*h mod 2",
                    "action": "trivial",
                },
                "boundary_value": 0,
                "kernel": [0, 2],
                "face_lifts": [0, 2],
                "boundary_images": [0, 0],
                "lift_deltas": [2],
                "boundary_forgets_higher_lift": True,
            },
        )

        with self.assertRaises(CyclicCrossedModuleInputError):
            analyze_cyclic_face_lifts(3, 2, 1, 0)
        with self.assertRaises(CyclicCrossedModuleInputError):
            analyze_cyclic_face_lifts(4, 2, 1, 2)
        with self.assertRaises(CyclicCrossedModuleInputError):
            analyze_cyclic_face_lifts(0, 2, 1, 0)


if __name__ == "__main__":
    unittest.main()
