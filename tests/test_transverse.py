from collections import deque
import json
import pathlib
import unittest

from dogram.transverse import (
    TransverseInputError,
    analyze_transverse,
    bounded_history_reach_count,
    bounded_history_sheet_trace,
    exact_carrier_return_period,
    quotient_return_period,
    return_debt,
    sheet_coordinate,
)


ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "transverse"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())


def brute_reach_count(m, n, generators):
    start = (0, 0)
    queue = deque([start])
    seen = {start}
    moves = ((1, 1),) + tuple((r, 0) for r in generators)
    while queue:
        a, b = queue.popleft()
        for da, db in moves:
            nxt = ((a + da) % m, (b + db) % n)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen)


def brute_quotient_return_period(m, n, r):
    from math import gcd

    d = gcd(m, n)
    sheet = 0
    for k in range(1, d + 1):
        sheet = (sheet + r) % d
        if sheet == 0:
            return k
    raise AssertionError((m, n, r, "quotient period not found"))


def brute_exact_carrier_return_period(m, r):
    state = 0
    for k in range(1, m + 1):
        state = (state + r) % m
        if state == 0:
            return k
    raise AssertionError((m, r, "carrier period not found"))


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

    def test_z6_x_z9_r1_returns_to_sheet_before_carrier(self):
        self.assertEqual(quotient_return_period(6, 9, 1), 3)
        self.assertEqual(exact_carrier_return_period(6, 1), 6)
        self.assertEqual(return_debt(6, 9, 1), 2)

    def test_z8_x_z12_r4_is_quotient_inert_but_not_exactly_returned(self):
        self.assertEqual(quotient_return_period(8, 12, 4), 1)
        self.assertEqual(exact_carrier_return_period(8, 4), 2)
        self.assertEqual(return_debt(8, 12, 4), 2)

    def test_coprime_world_has_trivial_quotient_return_period(self):
        self.assertEqual(quotient_return_period(5, 7, 1), 1)
        self.assertEqual(exact_carrier_return_period(5, 1), 5)
        self.assertEqual(return_debt(5, 7, 1), 5)

    def test_r_divisible_by_m_is_exact_return_in_one_cycle(self):
        self.assertEqual(quotient_return_period(6, 9, 6), 1)
        self.assertEqual(exact_carrier_return_period(6, 6), 1)
        self.assertEqual(return_debt(6, 9, 6), 1)

    def test_return_period_helpers_reject_invalid_generators(self):
        for bad in (True, 1.5, "1"):
            with self.assertRaises(TransverseInputError) as caught:
                quotient_return_period(6, 9, bad)
            self.assertEqual(caught.exception.reason_code, "INVALID_GENERATOR")

    def test_exact_return_period_rejects_invalid_dimension(self):
        with self.assertRaises(TransverseInputError) as caught:
            exact_carrier_return_period(0, 1)
        self.assertEqual(caught.exception.reason_code, "INVALID_DIMENSION")

    def test_return_period_formulas_match_independent_bounded_oracle(self):
        checked = 0
        for m in range(2, 21):
            for n in range(2, 21):
                for r in range(1, 21):
                    quotient = quotient_return_period(m, n, r)
                    exact = exact_carrier_return_period(m, r)
                    self.assertEqual(quotient, brute_quotient_return_period(m, n, r), (m, n, r))
                    self.assertEqual(exact, brute_exact_carrier_return_period(m, r), (m, n, r))
                    self.assertEqual(exact % quotient, 0, (m, n, r))
                    self.assertEqual(return_debt(m, n, r), exact // quotient, (m, n, r))
                    checked += 1
        self.assertEqual(checked, 7220)

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

    def test_single_generator_lift_formula_matches_405_bruteforce_cases(self):
        checked = 0
        for m in range(2, 11):
            for n in range(2, 11):
                for r in range(1, 6):
                    analysis = analyze_transverse(m, n, (r,))
                    self.assertEqual(
                        analysis.closure_reach_count,
                        brute_reach_count(m, n, (r,)),
                        (m, n, r),
                    )
                    checked += 1
        self.assertEqual(checked, 405)

    def test_complementary_generators_match_bruteforce_closure(self):
        analysis = analyze_transverse(12, 18, (2, 3))
        self.assertEqual(analysis.closure_reach_count, 216)
        self.assertEqual(analysis.closure_reach_count, brute_reach_count(12, 18, (2, 3)))


if __name__ == "__main__":
    unittest.main()
