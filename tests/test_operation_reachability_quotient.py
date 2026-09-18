from __future__ import annotations

import unittest

from dogram.operation_reachability_quotient import analyze_operation_reachability


class OperationReachabilityQuotientTests(unittest.TestCase):
    def test_collapse_can_destroy_exact_enabledness_question(self) -> None:
        receipt = analyze_operation_reachability(
            states=("ready", "blocked", "done"),
            collapsed_projection=("pending", "pending", "done"),
            operations=("advance", "reset"),
            enabled=((True, False), (False, False), (False, True)),
        )
        self.assertFalse(receipt.exact_factorization)
        self.assertEqual(receipt.ambiguous_classes, (("ready", "blocked"),))
        self.assertEqual(
            receipt.lost_operation_questions,
            (("ready", "blocked", "advance", True, False),),
        )

    def test_operation_signature_constant_on_fibers_is_exact(self) -> None:
        receipt = analyze_operation_reachability(
            states=("a0", "a1", "b"),
            collapsed_projection=("a", "a", "b"),
            operations=("go", "stop"),
            enabled=((True, False), (True, False), (False, True)),
        )
        self.assertTrue(receipt.exact_factorization)
        self.assertEqual(receipt.lost_operation_questions, ())

    def test_rejects_integer_aliases_as_boolean_enabledness(self) -> None:
        with self.assertRaises(ValueError):
            analyze_operation_reachability(
                states=("a", "b"),
                collapsed_projection=(0, 0),
                operations=("go",),
                enabled=((1,), (0,)),  # type: ignore[arg-type]
            )


if __name__ == "__main__":
    unittest.main()
