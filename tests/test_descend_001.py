from __future__ import annotations

import unittest
from itertools import product

from dogram.descend_001 import analyze_descent


class Descend001Tests(unittest.TestCase):
    def test_identity_descends_even_when_raw_state_ids_differ(self):
        receipt = analyze_descent(
            states=("a", "b", "c"), projection=(0, 0, 1),
            operations={"identity": ("a", "b", "c")},
        )
        probe = receipt.probes[0]
        self.assertEqual((probe.raw.status, probe.projected.status), ("counterexample", "preserved"))
        self.assertEqual(probe.raw.counterexample.states, ("a", "b"))
        self.assertEqual(probe.raw.counterexample.successors, ("a", "b"))
        self.assertEqual(probe.projected.checked_pairs, 1)
        self.assertEqual(receipt.collapse_classes, (("a", "b"), ("c",)))
        self.assertEqual(probe.induced_table, ((0, 0), (1, 1)))

    def test_advance_fails_projected_descent_with_distinct_successors(self):
        receipt = analyze_descent(
            states=("a", "b", "c"), projection=(0, 0, 1),
            operations={"advance": ("a", "c", "c")},
        )
        probe = receipt.probes[0]
        self.assertEqual(probe.projected.status, "counterexample")
        self.assertEqual(probe.projected.counterexample.states, ("a", "b"))
        self.assertEqual(probe.projected.counterexample.successors, ("a", "c"))
        self.assertEqual(probe.projected.counterexample.projected_successors, (0, 1))
        self.assertIsNone(probe.induced_table)

    def test_nonidentity_operation_descends_only_after_projection(self):
        receipt = analyze_descent(
            states=("a", "b", "c"), projection=(0, 0, 1),
            operations={"reset": ("b", "a", "b")},
        )
        self.assertEqual(receipt.probes[0].raw.status, "counterexample")
        self.assertEqual(receipt.probes[0].projected.status, "preserved")
        self.assertEqual(receipt.probes[0].induced_table, ((0, 0), (1, 0)))

    def test_zero_budget_is_inconclusive_not_preservation(self):
        receipt = analyze_descent(
            states=("a", "b"), projection=(0, 0),
            operations={"stay": ("a", "a")}, max_pair_checks=0,
        )
        probe = receipt.probes[0]
        self.assertEqual((probe.raw.status, probe.projected.status), ("inconclusive", "inconclusive"))
        self.assertEqual((probe.raw.checked_pairs, probe.projected.checked_pairs), (0, 0))
        self.assertIsNone(probe.induced_table)

    def test_zero_budget_with_no_collapsed_pairs_is_vacuously_preserved(self):
        receipt = analyze_descent(
            states=("a", "b"), projection=(0, 1),
            operations={"swap": ("b", "a")}, max_pair_checks=0,
        )
        self.assertEqual(receipt.possible_pairs, 0)
        self.assertEqual(receipt.probes[0].projected.status, "preserved")
        self.assertEqual(receipt.probes[0].induced_table, ((0, 1), (1, 0)))

    def test_budget_can_prove_failure_without_proving_other_mode(self):
        receipt = analyze_descent(
            states=("a", "b", "c"), projection=(0, 0, 0),
            operations={"f": ("a", "b", "b")}, max_pair_checks=1,
        )
        probe = receipt.probes[0]
        self.assertEqual(probe.raw.status, "counterexample")
        self.assertEqual(probe.projected.status, "inconclusive")
        self.assertEqual(probe.projected.possible_pairs, 3)

    def test_finite_canonical_receipts_are_deterministic_and_typed(self):
        args = dict(states=("a", "b"), projection=(0, 0), operations={"go": ("a", "b")})
        x = analyze_descent(**args)
        self.assertEqual(x, analyze_descent(**args))
        self.assertEqual(len(x.input_sha256), 64)
        other = analyze_descent(states=("a", "b"), projection=(False, False), operations={"go": ("a", "b")})
        self.assertNotEqual(x.input_sha256, other.input_sha256)
        distinct = analyze_descent(states=("a", "b"), projection=(1, True), operations={"go": ("a", "b")})
        self.assertEqual(len(distinct.collapse_classes), 2)

    def test_operations_have_deterministic_name_order(self):
        receipt = analyze_descent(
            states=("a", "b"), projection=(0, 0),
            operations={"z": ("a", "a"), "a": ("b", "b")},
        )
        self.assertEqual(tuple(p.operation for p in receipt.probes), ("a", "z"))

    def test_all_small_total_maps_match_independent_quotient_definition(self):
        states = ("a", "b", "c")
        for projection in product((0, 1), repeat=3):
            for targets in product(states, repeat=3):
                expected = all(
                    projection[i] != projection[j] or
                    projection[states.index(targets[i])] == projection[states.index(targets[j])]
                    for i in range(3) for j in range(i + 1, 3)
                )
                probe = analyze_descent(states, projection, {"f": targets}).probes[0]
                self.assertEqual(probe.projected.status == "preserved", expected)
                self.assertEqual(probe.induced_table is not None, expected)

    def test_input_validation_refuses_ambiguous_or_unsafe_tables(self):
        valid = dict(states=("a", "b"), projection=(0, 0), operations={"go": ("a", "b")})
        bad = (
            dict(states=("a", "a")),
            dict(states=("a", "")),
            dict(states=("a", "b"), projection=(0,)),
            dict(projection=([1], [1])),
            dict(projection=(0.0, 0.0)),
            dict(operations={}),
            dict(operations={"go": ("a", "unknown")}),
            dict(operations={"go": ("a",)}),
            dict(operations={"go": (True, "b")}),
            dict(operations={"": ("a", "b")}),
            dict(operations={1: ("a", "b")}),
            dict(max_pair_checks=-1),
            dict(max_pair_checks=True),
        )
        for change in bad:
            with self.subTest(change=change), self.assertRaises(ValueError):
                analyze_descent(**{**valid, **change})


if __name__ == "__main__":
    unittest.main()
