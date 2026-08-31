import json
import pathlib
import unittest

from dogram.transverse import (
    TransverseInputError,
    analyze_transverse,
    bounded_history_reach_count,
    bounded_history_sheet_trace,
    sheet_coordinate,
)


ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "transverse"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())


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

    def test_z6_x_z9_one_cut_is_36_while_closure_is_54(self):
        result = analyze_transverse(6, 9, (1,))
        self.assertEqual(result.sync_sheet_size, 18)
        self.assertEqual(result.sheet_count, 3)
        self.assertEqual(bounded_history_sheet_trace(6, 9, (1,)), (0, 1))
        self.assertEqual(bounded_history_reach_count(6, 9, (1,)), 36)
        self.assertEqual(result.closure_reach_count, 54)

    def test_second_bounded_cut_can_reach_third_sheet(self):
        self.assertEqual(bounded_history_sheet_trace(6, 9, (1, 1)), (0, 1, 2))
        self.assertEqual(bounded_history_reach_count(6, 9, (1, 1)), 54)

    def test_inert_cut_stays_on_same_sheet(self):
        result = analyze_transverse(8, 12, (4,))
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(bounded_history_sheet_trace(8, 12, (4,)), (0, 0))
        self.assertEqual(bounded_history_reach_count(8, 12, (4,)), 24)

    def test_coprime_dimensions_have_no_hidden_sheet(self):
        result = analyze_transverse(5, 7, (1,))
        self.assertEqual(result.sheet_count, 1)
        self.assertEqual(result.sync_sheet_size, 35)
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(result.closure_reach_count, 35)

    def test_frozen_specimens_match_exact_history_closure_and_budget(self):
        names = sorted(path.name for path in FIXTURES.glob("*.json"))
        self.assertEqual(len(names), 6)
        for name in names:
            fixture = load_fixture(name)
            system = fixture["system"]
            cuts = tuple(fixture["cuts"])
            generators = tuple(fixture["generators"])
            self.assertLessEqual(len(cuts), fixture["cut_budget"], name)
            analysis = analyze_transverse(system["m"], system["n"], generators)
            self.assertEqual(analysis.to_data(), fixture["expected"]["analysis"], name)
            self.assertEqual(
                list(bounded_history_sheet_trace(system["m"], system["n"], cuts)),
                fixture["expected"]["bounded_history_sheet_trace"],
                name,
            )
            self.assertEqual(
                bounded_history_reach_count(system["m"], system["n"], cuts),
                fixture["expected"]["bounded_history_reach_count"],
                name,
            )

    def test_complementary_generators_span_more_than_either_alone(self):
        left = analyze_transverse(12, 18, (2,))
        right = analyze_transverse(12, 18, (3,))
        together = analyze_transverse(12, 18, (2, 3))
        self.assertEqual(left.closure_reach_count, 108)
        self.assertEqual(right.closure_reach_count, 72)
        self.assertEqual(together.closure_reach_count, 216)
        self.assertLess(left.closure_reach_count, together.closure_reach_count)
        self.assertLess(right.closure_reach_count, together.closure_reach_count)


if __name__ == "__main__":
    unittest.main()
