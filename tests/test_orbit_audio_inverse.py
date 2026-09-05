from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.orbit_audio_inverse import identify_orbits, recover_period_days


FIXTURE = Path(__file__).parent / "fixtures" / "orbit_audio_inverse_001.json"


class OrbitAudioInverseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.period_items = tuple(cls.fixture["period_days"].items())
        cls.scale = cls.fixture["declared_scale_hz_days"]

    def test_known_scale_recovers_frozen_periods(self) -> None:
        names = tuple(self.fixture["period_days"])
        frequencies = tuple(self.fixture["tones_hz"][name] for name in names)

        recovered = recover_period_days(frequencies, self.scale)

        for name, period in zip(names, recovered, strict=True):
            self.assertAlmostEqual(period, self.fixture["period_days"][name], places=9)

    def test_unknown_scale_recovers_labels_from_ratios(self) -> None:
        receipt = identify_orbits(
            tuple(self.fixture["scrambled_observed_hz"]),
            self.period_items,
        )

        self.assertEqual(receipt.assignment, tuple(self.fixture["expected_assignment"]))
        self.assertAlmostEqual(receipt.estimated_scale_hz_days, self.scale, places=8)
        self.assertLess(receipt.max_relative_scale_residual, 1e-12)

    def test_global_pitch_shift_preserves_assignment_but_changes_scale(self) -> None:
        shifted = tuple(value * 1.75 for value in self.fixture["scrambled_observed_hz"])

        receipt = identify_orbits(shifted, self.period_items)

        self.assertEqual(receipt.assignment, tuple(self.fixture["expected_assignment"]))
        self.assertAlmostEqual(receipt.estimated_scale_hz_days, self.scale * 1.75, places=8)
        self.assertLess(receipt.max_relative_scale_residual, 1e-12)

    def test_one_tone_perturbation_leaves_nonzero_residue(self) -> None:
        perturbed = list(self.fixture["scrambled_observed_hz"])
        perturbed[0] *= 1.01

        receipt = identify_orbits(tuple(perturbed), self.period_items)

        self.assertEqual(receipt.assignment, tuple(self.fixture["expected_assignment"]))
        self.assertGreater(receipt.max_relative_scale_residual, 0.005)

    def test_inputs_must_be_positive_finite_and_cardinalities_must_match(self) -> None:
        with self.assertRaises(ValueError):
            recover_period_days((0.0, 440.0), self.scale)
        with self.assertRaises(ValueError):
            identify_orbits((440.0,), self.period_items)
        with self.assertRaises(ValueError):
            identify_orbits((440.0, float("inf")), (("Earth", 365.26), ("Mars", 686.98)))


if __name__ == "__main__":
    unittest.main()
