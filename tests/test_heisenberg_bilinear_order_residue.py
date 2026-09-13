from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from dogram.rectangle import evaluate_rectangle


FIXTURE = Path(__file__).parent / "fixtures" / "heisenberg_bilinear_order_residue_001.json"


def _matmul(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def _identity() -> list[list[Fraction]]:
    return [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]


def _exp_square_zero(generator: list[list[Fraction]], scalar: Fraction) -> list[list[Fraction]]:
    ident = _identity()
    return [[ident[i][j] + scalar * generator[i][j] for j in range(3)] for i in range(3)]


def _as_fraction_matrix(raw: list[list[int]]) -> list[list[Fraction]]:
    return [[Fraction(value) for value in row] for row in raw]


def _parameter(raw: dict[str, int]) -> Fraction:
    return Fraction(raw["numerator"], raw["denominator"])


class HeisenbergBilinearOrderResidueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.x = _as_fraction_matrix(cls.fixture["generators"]["X"])
        cls.y = _as_fraction_matrix(cls.fixture["generators"]["Y"])
        cls.s = _parameter(cls.fixture["parameters"]["s"])
        cls.t = _parameter(cls.fixture["parameters"]["t"])

    def test_lie_bracket_is_the_central_generator(self) -> None:
        xy = _matmul(self.x, self.y)
        yx = _matmul(self.y, self.x)
        bracket = [[xy[i][j] - yx[i][j] for j in range(3)] for i in range(3)]
        expected = _as_fraction_matrix(self.fixture["expected"]["bracket"])
        self.assertEqual(bracket, expected)

    def test_order_residue_is_exact_bilinear_central_term(self) -> None:
        a = _exp_square_zero(self.x, self.s)
        b = _exp_square_zero(self.y, self.t)
        forward = _matmul(a, b)
        reverse = _matmul(b, a)
        residue = [[forward[i][j] - reverse[i][j] for j in range(3)] for i in range(3)]
        expected_scalar = _parameter(self.fixture["expected"]["bilinear_residue"])
        self.assertEqual(residue[0][2], expected_scalar)
        self.assertEqual(sum(value != 0 for row in residue for value in row), 1)

        a_inv = _exp_square_zero(self.x, -self.s)
        b_inv = _exp_square_zero(self.y, -self.t)
        commutator = _matmul(_matmul(_matmul(a, b), a_inv), b_inv)
        self.assertEqual(commutator[0][2], expected_scalar)
        self.assertEqual(commutator[0][0], 1)
        self.assertEqual(commutator[1][1], 1)
        self.assertEqual(commutator[2][2], 1)

    def test_existing_rectangle_receipts_the_same_bilinear_residue(self) -> None:
        expected = self.fixture["expected"]
        forward_result, consumed = evaluate_rectangle(
            {
                "axis_a": "sX_present",
                "axis_b": "tY_present",
                "cells": expected["forward_central_rectangle"],
            }
        )
        reverse_result, reverse_consumed = evaluate_rectangle(
            {
                "axis_a": "sX_present",
                "axis_b": "tY_present",
                "cells": expected["reverse_central_rectangle"],
            }
        )

        self.assertEqual(
            forward_result["mixed_delta"],
            {"kind": "rational", "numerator": 10, "denominator": 21},
        )
        self.assertTrue(forward_result["interaction_detected"])
        self.assertEqual(reverse_result["mixed_delta"], {"kind": "integer", "value": 0})
        self.assertFalse(reverse_result["interaction_detected"])
        self.assertEqual(consumed, reverse_consumed)


if __name__ == "__main__":
    unittest.main()
