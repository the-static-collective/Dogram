from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.field_reduction import (
    FieldReductionInputError,
    compare_prime_field_basis_support,
)


FIXTURE = Path(__file__).parent / "fixtures" / "field_reduction_dependence_001.json"


def _load_fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class FieldReductionDependenceTests(unittest.TestCase):
    def test_same_integer_matrix_changes_basis_support_between_gf2_and_gf3(self) -> None:
        fixture = _load_fixture()
        expected = fixture["expected"]
        result = compare_prime_field_basis_support(
            tuple(tuple(row) for row in fixture["matrix"]),
            tuple(fixture["labels"]),
            rank=fixture["rank"],
            prime_a=fixture["prime_a"],
            prime_b=fixture["prime_b"],
        )

        self.assertEqual(result.prime_a_basis_count, expected["prime_a_basis_count"])
        self.assertEqual(result.prime_b_basis_count, expected["prime_b_basis_count"])
        self.assertEqual(result.only_a, tuple(tuple(x) for x in expected["only_a"]))
        self.assertEqual(result.only_b, tuple(tuple(x) for x in expected["only_b"]))
        self.assertEqual(
            result.changed_subsets,
            tuple(tuple(x) for x in expected["changed_subsets"]),
        )

    def test_declared_field_must_be_prime(self) -> None:
        fixture = _load_fixture()
        with self.assertRaises(FieldReductionInputError) as caught:
            compare_prime_field_basis_support(
                tuple(tuple(row) for row in fixture["matrix"]),
                tuple(fixture["labels"]),
                rank=fixture["rank"],
                prime_a=4,
                prime_b=fixture["prime_b"],
            )
        self.assertEqual(caught.exception.reason_code, "FIELD_NOT_PRIME")


if __name__ == "__main__":
    unittest.main()
