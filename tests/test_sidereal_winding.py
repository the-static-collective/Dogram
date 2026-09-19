from __future__ import annotations

import unittest
from fractions import Fraction

from dogram.sidereal_winding import DualClockInputError, project_dual_clock


class SiderealWindingTests(unittest.TestCase):
    def test_projection_delta_exactly_receipts_orbital_winding(self) -> None:
        result = project_dual_clock(Fraction(17, 3), Fraction(2, 5))

        self.assertEqual(result.sidereal_turns, Fraction(17, 3))
        self.assertEqual(result.solar_turns, Fraction(79, 15))
        self.assertEqual(result.winding_receipt, Fraction(2, 5))
        self.assertEqual(
            result.sidereal_turns - result.solar_turns,
            result.orbit_turns,
        )

    def test_one_orbit_carries_one_extra_sidereal_rotation(self) -> None:
        result = project_dual_clock(366, 1)

        self.assertEqual(result.sidereal_turns, 366)
        self.assertEqual(result.solar_turns, 365)
        self.assertEqual(result.winding_receipt, 1)

    def test_fractional_year_specimen_remains_exact(self) -> None:
        result = project_dual_clock(Fraction(1831211, 5000), 1)

        self.assertEqual(result.sidereal_turns, Fraction(1831211, 5000))
        self.assertEqual(result.solar_turns, Fraction(1826211, 5000))
        self.assertEqual(result.winding_receipt, 1)

    def test_same_solar_projection_can_hide_distinct_winding(self) -> None:
        first = project_dual_clock(10, 3)
        second = project_dual_clock(11, 4)

        self.assertEqual(first.solar_turns, second.solar_turns)
        self.assertNotEqual(first.sidereal_turns, second.sidereal_turns)
        self.assertNotEqual(first.winding_receipt, second.winding_receipt)
        self.assertNotEqual(first.to_data(), second.to_data())

    def test_float_inputs_are_refused_to_preserve_exact_receipts(self) -> None:
        for value in (1.0, 0.5, True, "1"):
            with self.assertRaises(DualClockInputError) as caught:
                project_dual_clock(value, 1)  # type: ignore[arg-type]
            self.assertEqual(caught.exception.reason_code, "NON_EXACT_INPUT")


if __name__ == "__main__":
    unittest.main()
