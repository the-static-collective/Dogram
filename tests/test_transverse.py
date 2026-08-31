import unittest

from dogram.transverse import (
    TransverseInputError,
    analyze_transverse,
    historical_reach_count,
    historical_sheet_trace,
    sheet_coordinate,
)


class TransverseTests(unittest.TestCase):
    def test_z6_x_z4_has_two_twelve_state_sync_sheets(self):
        result = analyze_transverse(6, 4, (1,))
        self.assertEqual(result.state_capacity, 24)
        self.assertEqual(result.sync_sheet_size, 12)
        self.assertEqual(result.sheet_count, 2)
        self.assertEqual(result.closure_lift_index, 2)
        self.assertEqual(result.closure_reach_count, 24)

    def test_sheet_coordinate_is_preserved_by_sync_motion(self):
        before = sheet_coordinate(8, 12, 3, 7)
        after = sheet_coordinate(8, 12, 4, 8)
        self.assertEqual(before, after)

    def test_transverse_cut_changes_sheet_coordinate(self):
        before = sheet_coordinate(8, 12, 3, 7)
        after = sheet_coordinate(8, 12, 5, 7)
        self.assertNotEqual(before, after)

    def test_invalid_dimension_refuses(self):
        with self.assertRaises(TransverseInputError) as caught:
            analyze_transverse(0, 4, (1,))
        self.assertEqual(caught.exception.reason_code, "INVALID_DIMENSION")

    def test_empty_generator_family_refuses(self):
        with self.assertRaises(TransverseInputError) as caught:
            analyze_transverse(6, 4, ())
        self.assertEqual(caught.exception.reason_code, "EMPTY_GENERATOR_FAMILY")

    def test_z6_x_z9_one_cut_reaches_36_but_closure_reaches_54(self):
        result = analyze_transverse(6, 9, (1,))
        self.assertEqual(result.sync_sheet_size, 18)
        self.assertEqual(result.sheet_count, 3)
        self.assertEqual(historical_sheet_trace(6, 9, (1,)), (0, 1))
        self.assertEqual(historical_reach_count(6, 9, (1,)), 36)
        self.assertEqual(result.closure_reach_count, 54)

    def test_repeated_bounded_cut_can_visit_third_sheet(self):
        self.assertEqual(historical_sheet_trace(6, 9, (1, 1)), (0, 1, 2))
        self.assertEqual(historical_reach_count(6, 9, (1, 1)), 54)

    def test_inert_cut_changes_no_sheet(self):
        result = analyze_transverse(8, 12, (4,))
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(result.closure_reach_count, 24)
        self.assertEqual(historical_sheet_trace(8, 12, (4,)), (0, 0))

    def test_coprime_dimensions_have_no_hidden_sheet(self):
        result = analyze_transverse(5, 7, (1,))
        self.assertEqual(result.sheet_count, 1)
        self.assertEqual(result.sync_sheet_size, 35)
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(result.closure_reach_count, 35)


if __name__ == "__main__":
    unittest.main()
