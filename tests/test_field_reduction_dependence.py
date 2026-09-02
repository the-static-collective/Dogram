from __future__ import annotations

import unittest

from dogram.field_reduction import (
    FieldReductionInputError,
    compare_prime_field_basis_support,
)


FANO_INTEGER_MATRIX = (
    (1, 0, 0, 1, 1, 0, 1),
    (0, 1, 0, 1, 0, 1, 1),
    (0, 0, 1, 0, 1, 1, 1),
)
LABELS = ("1", "2", "3", "4", "5", "6", "7")


class FieldReductionDependenceTests(unittest.TestCase):
    def test_same_integer_matrix_changes_basis_support_between_gf2_and_gf3(self) -> None:
        result = compare_prime_field_basis_support(
            FANO_INTEGER_MATRIX,
            LABELS,
            rank=3,
            prime_a=2,
            prime_b=3,
        )

        self.assertEqual(result.prime_a_basis_count, 28)
        self.assertEqual(result.prime_b_basis_count, 29)
        self.assertEqual(result.only_a, ())
        self.assertEqual(result.only_b, (("4", "5", "6"),))
        self.assertEqual(result.changed_subsets, (("4", "5", "6"),))

    def test_declared_field_must_be_prime(self) -> None:
        with self.assertRaises(FieldReductionInputError) as caught:
            compare_prime_field_basis_support(
                FANO_INTEGER_MATRIX,
                LABELS,
                rank=3,
                prime_a=4,
                prime_b=3,
            )
        self.assertEqual(caught.exception.reason_code, "FIELD_NOT_PRIME")


if __name__ == "__main__":
    unittest.main()
