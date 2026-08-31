from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.mapping_torus import (
    analyze_mapping_torus,
    relative_realignment,
    twisted_mode_fraction,
)


FIXTURE = Path(__file__).parent / "fixtures" / "mapping_torus" / "mapping-torus-001.json"


class MappingTorusFixtureTests(unittest.TestCase):
    def test_frozen_72_5_7_fixture_replays_exactly(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        n = fixture["fiber_count"]
        shift_a = fixture["shift_a"]
        shift_b = fixture["shift_b"]
        expected = fixture["expected"]

        left = analyze_mapping_torus(n, shift_a)
        right = analyze_mapping_torus(n, shift_b)
        realignment = relative_realignment(n, shift_a, shift_b)
        mode = twisted_mode_fraction(n, shift_a, longitudinal_index=1, fiber_mode=6)

        self.assertEqual(left.components, expected["shift_a_components"])
        self.assertEqual(left.orbit_length, expected["shift_a_orbit_length"])
        self.assertEqual(right.components, expected["shift_b_components"])
        self.assertEqual(right.orbit_length, expected["shift_b_orbit_length"])
        self.assertEqual(realignment.relative_delta, expected["relative_delta"])
        self.assertEqual(realignment.realignment_period, expected["realignment_period"])
        self.assertEqual(mode.numerator, expected["twisted_mode_1_6"]["numerator"])
        self.assertEqual(mode.denominator, expected["twisted_mode_1_6"]["denominator"])

    def test_same_coarse_surface_retains_distinct_consumed_shift(self) -> None:
        left = analyze_mapping_torus(72, 5)
        right = analyze_mapping_torus(72, 7)
        self.assertEqual(
            (left.components, left.orbit_length),
            (right.components, right.orbit_length),
        )
        self.assertNotEqual(left.shift, right.shift)
        self.assertNotEqual(left.to_data(), right.to_data())

    def test_relative_realignment_period_is_symmetric_and_same_shift_closes_in_one(self) -> None:
        self.assertEqual(
            relative_realignment(72, 5, 7).realignment_period,
            relative_realignment(72, 7, 5).realignment_period,
        )
        self.assertEqual(relative_realignment(72, 5, 5).realignment_period, 1)

    def test_exact_twisted_mode_controls_never_require_float_rounding(self) -> None:
        whole = twisted_mode_fraction(72, 6, longitudinal_index=0, fiber_mode=12)
        negative = twisted_mode_fraction(72, 5, longitudinal_index=-1, fiber_mode=1)
        self.assertEqual((whole.numerator, whole.denominator), (1, 1))
        self.assertEqual((negative.numerator, negative.denominator), (-67, 72))
        self.assertIsInstance(whole.numerator, int)
        self.assertIsInstance(whole.denominator, int)


if __name__ == "__main__":
    unittest.main()
