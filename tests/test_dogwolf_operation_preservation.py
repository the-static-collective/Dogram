from __future__ import annotations

import unittest

from dogram.dogwolf_operation_preservation import probe_operation_preservation
from dogram.operation_reachability_quotient import analyze_operation_reachability


class DogwolfOperationPreservationTests(unittest.TestCase):
    @staticmethod
    def group_specimen():
        carrier = ((0, 0), (0, 1), (1, 0), (1, 1))
        paths = tuple((first, second) for first in carrier for second in carrier)
        states = tuple(f"{first}:{second}" for first in range(4) for second in range(4))
        quotient = tuple(tuple((x + y) % 2 for x, y in zip(first, second)) for first, second in paths)
        return states, quotient, {
            "composite": quotient,
            "first_arrow": tuple(first for first, _ in paths),
        }

    def test_group_hunt_receipts_preservation_and_explicit_loss(self):
        states, quotient, operations = self.group_specimen()
        receipt = probe_operation_preservation(states, quotient, operations)
        self.assertEqual(len(receipt.collapse_classes), 4)
        self.assertEqual(tuple(map(len, receipt.collapse_classes)), (4,) * 4)
        composite, first_arrow = receipt.probes
        self.assertEqual((composite.status, composite.checked_pairs, composite.possible_pairs), ("preserved", 24, 24))
        self.assertIsNone(composite.counterexample)
        self.assertEqual((first_arrow.status, first_arrow.checked_pairs, first_arrow.possible_pairs), ("counterexample", 1, 24))
        self.assertEqual((first_arrow.counterexample.left_state, first_arrow.counterexample.right_state), ("0:0", "1:1"))
        self.assertEqual(first_arrow.counterexample.shared_projection, (0, 0))
        self.assertEqual((first_arrow.counterexample.left_result, first_arrow.counterexample.right_result), ((0, 0), (0, 1)))
        self.assertEqual(len(receipt.input_sha256), 64)
        self.assertEqual(receipt, probe_operation_preservation(states, quotient, operations))

    def test_zero_budget_is_inconclusive_when_comparisons_exist(self):
        states, quotient, operations = self.group_specimen()
        receipt = probe_operation_preservation(states, quotient, operations, max_pair_checks=0)
        self.assertEqual(tuple(probe.status for probe in receipt.probes), ("inconclusive", "inconclusive"))
        self.assertEqual(tuple(probe.checked_pairs for probe in receipt.probes), (0, 0))

    def test_budgeted_found_counterexample_remains_decisive(self):
        states, quotient, operations = self.group_specimen()
        receipt = probe_operation_preservation(states, quotient, operations, max_pair_checks=1)
        self.assertEqual(tuple(probe.status for probe in receipt.probes), ("inconclusive", "counterexample"))

    def test_no_merged_states_proves_preservation_at_zero_budget(self):
        receipt = probe_operation_preservation(("a", "b"), ("a", "b"), {"step": (0, 1)}, max_pair_checks=0)
        self.assertEqual((receipt.probes[0].status, receipt.probes[0].possible_pairs), ("preserved", 0))

    def test_boolean_and_integer_are_not_silently_identified(self):
        distinct = probe_operation_preservation(("a", "b"), (1, True), {"out": ("a", "b")})
        self.assertEqual(distinct.probes[0].status, "preserved")
        self.assertEqual(len(distinct.collapse_classes), 2)
        collapsed = probe_operation_preservation(("a", "b"), (0, 0), {"out": (1, True)})
        self.assertEqual(collapsed.probes[0].status, "counterexample")

    def test_existing_enabledness_case_is_preserved_as_special_case(self):
        states = ("ready", "blocked", "done")
        quotient = ("pending", "pending", "done")
        old = analyze_operation_reachability(states, quotient, ("advance", "reset"), ((True, False), (False, False), (False, True)))
        new = probe_operation_preservation(states, quotient, {"advance": (True, False, False), "reset": (False, False, True)})
        self.assertFalse(old.exact_factorization)
        self.assertEqual(tuple(probe.status for probe in new.probes), ("counterexample", "preserved"))
        self.assertEqual((new.probes[0].counterexample.left_state, new.probes[0].counterexample.right_state), ("ready", "blocked"))

    def test_malformed_inputs_fail_closed(self):
        cases = (
            (("a",), (), {"go": (0,)}, 1),
            (("a", "a"), (0, 0), {"go": (0, 1)}, 1),
            (("a",), ([],), {"go": (0,)}, 1),
            (("a",), (0.0,), {"go": (0,)}, 1),
            (("a",), (0,), {"go": (0.0,)}, 1),
            (("a",), (0,), {"go": ()}, 1),
            (("a",), (0,), {}, 1),
            (("a",), (0,), {"go": (0,)}, -1),
            (("a",), (0,), {"go": (0,)}, True),
        )
        for states, projection, operations, budget in cases:
            with self.subTest(states=states, projection=projection, operations=operations, budget=budget):
                with self.assertRaises(ValueError):
                    probe_operation_preservation(states, projection, operations, max_pair_checks=budget)

    def test_typed_digest_changes_for_different_declarations(self):
        first = probe_operation_preservation(("a", "b"), (0, 0), {"out": (1, 1)})
        second = probe_operation_preservation(("a", "b"), (0, 0), {"out": (True, True)})
        self.assertNotEqual(first.input_sha256, second.input_sha256)


if __name__ == "__main__":
    unittest.main()
