"""COMMUTE-001: frozen path and endpoint comparison contracts."""
from __future__ import annotations

from itertools import product
import unittest

from dogram.commute_001 import analyze_commutation


class Commute001Tests(unittest.TestCase):
    def test_raw_difference_can_vanish_under_projection_and_paths_stay_distinct(self):
        receipt = analyze_commutation(
            states=("a", "b", "c"), projection=(0, 0, 1),
            first=("swap", ("b", "a", "c")),
            second=("redirect", ("a", "b", "a")),
        )
        self.assertEqual(receipt.raw.status, "counterexample")
        self.assertEqual(receipt.projected.status, "preserved")
        witness = receipt.raw.witness
        self.assertEqual(witness.origin, "c")
        self.assertEqual(witness.first_then_second, ("c", "c", "a"))
        self.assertEqual(witness.second_then_first, ("c", "a", "b"))
        self.assertEqual(witness.projected_endpoints, (0, 0))
        self.assertEqual(receipt.paths[2].first_then_second, ("c", "c", "a"))
        self.assertEqual(receipt.paths[2].second_then_first, ("c", "a", "b"))

    def test_projected_endpoint_divergence_has_a_specific_witness(self):
        receipt = analyze_commutation(
            states=("a", "b", "c"), projection=(0, 0, 1),
            first=("cycle", ("b", "c", "a")),
            second=("fold", ("a", "a", "c")),
        )
        self.assertEqual(receipt.projected.status, "counterexample")
        witness = receipt.projected.witness
        self.assertEqual(witness.origin, "b")
        self.assertEqual(witness.first_then_second, ("b", "c", "c"))
        self.assertEqual(witness.second_then_first, ("b", "a", "b"))
        self.assertEqual(witness.projected_endpoints, (1, 0))

    def test_two_distinct_paths_can_commute_exactly(self):
        receipt = analyze_commutation(
            states=("a", "b", "c"), projection=(0, 0, 1),
            first=("swap", ("b", "a", "c")),
            second=("identity", ("a", "b", "c")),
        )
        self.assertEqual(receipt.raw.status, "preserved")
        self.assertEqual(receipt.projected.status, "preserved")
        self.assertEqual(receipt.raw.checked_states, 3)
        self.assertEqual(receipt.raw.total_states, 3)
        self.assertEqual(receipt.paths[0].first_then_second, ("a", "b", "b"))
        self.assertEqual(receipt.paths[0].second_then_first, ("a", "a", "b"))

    def test_budget_zero_is_inconclusive_even_for_equal_tables(self):
        receipt = analyze_commutation(
            states=("a", "b"), projection=(0, 0),
            first=("id", ("a", "b")), second=("stay", ("a", "b")),
            max_state_checks=0,
        )
        self.assertEqual(receipt.raw.status, "inconclusive")
        self.assertEqual(receipt.projected.status, "inconclusive")
        self.assertEqual(receipt.raw.checked_states, 0)
        self.assertEqual(len(receipt.paths), 2)

    def test_early_raw_failure_does_not_prove_projected_pass(self):
        receipt = analyze_commutation(
            states=("a", "b", "c"), projection=(0, 0, 1),
            first=("swap", ("b", "a", "c")),
            second=("redirect", ("a", "b", "a")),
            max_state_checks=1,
        )
        self.assertEqual(receipt.raw.status, "inconclusive")
        self.assertEqual(receipt.projected.status, "inconclusive")
        self.assertIsNone(receipt.projected.witness)

    def test_budget_one_can_find_projected_failure_and_retain_raw_failure(self):
        receipt = analyze_commutation(
            states=("a", "b", "c"), projection=(0, 0, 1),
            first=("swap", ("b", "a", "c")),
            second=("redirect", ("c", "b", "c")),
            max_state_checks=1,
        )
        self.assertEqual(receipt.raw.status, "counterexample")
        self.assertEqual(receipt.projected.status, "counterexample")
        self.assertEqual(receipt.projected.checked_states, 1)

    def test_bool_int_projection_type_distinction_and_digest(self):
        kwargs = dict(states=("a", "b"), first=("f", ("a", "b")), second=("g", ("a", "b")))
        a = analyze_commutation(projection=(True, 1), **kwargs)
        b = analyze_commutation(projection=(1, 1), **kwargs)
        self.assertNotEqual(a.input_sha256, b.input_sha256)
        self.assertEqual(len(a.input_sha256), 64)
        self.assertEqual(a, analyze_commutation(projection=(True, 1), **kwargs))

    def test_independent_exhaustive_three_state_oracle(self):
        states = ("a", "b", "c")
        for f, g in product(product(states, repeat=3), repeat=2):
            for q in product((0, 1), repeat=3):
                raw_equal = all(g[states.index(f[i])] == f[states.index(g[i])] for i in range(3))
                projected_equal = all(q[states.index(g[states.index(f[i])])] == q[states.index(f[states.index(g[i])])] for i in range(3))
                receipt = analyze_commutation(states, q, ("f", f), ("g", g))
                self.assertEqual(receipt.raw.status == "preserved", raw_equal)
                self.assertEqual(receipt.projected.status == "preserved", projected_equal)
                self.assertEqual(receipt.raw.witness is None, raw_equal)
                self.assertEqual(receipt.projected.witness is None, projected_equal)

    def test_refuse_invalid_specimens_and_unbounded_or_executable_inputs(self):
        valid = dict(states=("a", "b"), projection=(0, 0), first=("f", ("a", "b")), second=("g", ("a", "b")))
        cases = (
            dict(states=()), dict(states=("a", "a")), dict(states=("", "b")),
            dict(states=(True, "b")), dict(states=["a", "b"]),
            dict(projection=(0,)), dict(projection=([0], [0])), dict(projection=(1.0, 1.0)),
            dict(first=("f", ("a", "missing"))), dict(first=("f", ("a",))),
            dict(first=("f", (True, "b"))), dict(first=("f", ["a", "b"])),
            dict(first=("", ("a", "b"))), dict(first=("g", ("a", "b"))),
            dict(second=("g", (lambda x: x, "a"))),
            dict(max_state_checks=-1), dict(max_state_checks=True),
        )
        for patch in cases:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                analyze_commutation(**{**valid, **patch})


if __name__ == "__main__":
    unittest.main()
