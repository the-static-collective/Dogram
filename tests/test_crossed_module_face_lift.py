from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.crossed_module_face_lift import (
    CyclicCrossedModuleInputError,
    analyze_cyclic_face_lifts,
)


FIXTURE = Path(__file__).parent / "fixtures" / "crossed_module_face_lift_001.json"


class CrossedModuleFaceLiftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = json.loads(FIXTURE.read_text())

    def _analyze(self, key: str):
        spec = self.fixture[key]
        return spec, analyze_cyclic_face_lifts(
            h_modulus=spec["h_modulus"],
            g_modulus=spec["g_modulus"],
            boundary_multiplier=spec["boundary_multiplier"],
            boundary_value=spec["boundary_value"],
        )

    def test_same_boundary_can_have_distinct_higher_face_lifts(self) -> None:
        spec, receipt = self._analyze("noninjective_specimen")

        self.assertEqual(receipt.kernel, tuple(spec["expected_kernel"]))
        self.assertEqual(receipt.face_lifts, tuple(spec["expected_face_lifts"]))
        self.assertEqual(
            receipt.boundary_images,
            tuple(spec["expected_boundary_images"]),
        )
        self.assertEqual(receipt.lift_deltas, tuple(spec["expected_lift_deltas"]))
        self.assertEqual(
            receipt.boundary_forgets_higher_lift,
            spec["expected_boundary_forgets_higher_lift"],
        )

    def test_injective_boundary_control_has_unique_lift(self) -> None:
        spec, receipt = self._analyze("injective_control")

        self.assertEqual(receipt.kernel, tuple(spec["expected_kernel"]))
        self.assertEqual(receipt.face_lifts, tuple(spec["expected_face_lifts"]))
        self.assertEqual(receipt.lift_deltas, tuple(spec["expected_lift_deltas"]))
        self.assertEqual(
            receipt.boundary_forgets_higher_lift,
            spec["expected_boundary_forgets_higher_lift"],
        )

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
