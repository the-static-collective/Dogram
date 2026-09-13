from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from dogram.fractional_isomorphism_coupling import analyze_pair


FIXTURE = Path(__file__).parent / "fixtures" / "fractional_isomorphism_coupling_001.json"


class FractionalIsomorphismCouplingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.result = analyze_pair(
            tuple(map(tuple, cls.fixture["cycle_6"]["edges"])),
            tuple(map(tuple, cls.fixture["two_triangles"]["edges"])),
        )

    def test_uniform_witness_is_exact_fractional_isomorphism(self) -> None:
        result = self.result
        self.assertTrue(result.witness_is_doubly_stochastic)
        self.assertTrue(result.intertwining_holds)
        self.assertTrue(result.same_degree_sequence)
        self.assertEqual(result.witness[0][0], Fraction(1, 6))
        self.assertTrue(all(entry == Fraction(1, 6) for row in result.witness for entry in row))

    def test_fractional_collision_preserves_structural_residuals(self) -> None:
        result = self.result
        self.assertEqual(result.left.vertex_count, 6)
        self.assertEqual(result.right.vertex_count, 6)
        self.assertEqual(result.left.degree_sequence, (2, 2, 2, 2, 2, 2))
        self.assertEqual(result.right.degree_sequence, (2, 2, 2, 2, 2, 2))
        self.assertEqual(result.left.component_count, self.fixture["cycle_6"]["component_count"])
        self.assertEqual(result.right.component_count, self.fixture["two_triangles"]["component_count"])
        self.assertEqual(result.left.triangle_count, self.fixture["cycle_6"]["triangle_count"])
        self.assertEqual(result.right.triangle_count, self.fixture["two_triangles"]["triangle_count"])
        self.assertEqual(result.component_delta, 1)
        self.assertEqual(result.triangle_delta, 2)

    def test_uniform_witness_refuses_out_of_scope_pairs(self) -> None:
        with self.assertRaises(ValueError):
            analyze_pair(((0, 1), (1, 2)), ((0, 1), (1, 2)))
        with self.assertRaises(ValueError):
            analyze_pair(((0, 1),), ((0, 1), (1, 2), (0, 2)))
        with self.assertRaises(ValueError):
            analyze_pair(((0, 1), (1, 2), (2, 3), (3, 0)), ((0, 1), (1, 2), (2, 0)))


if __name__ == "__main__":
    unittest.main()
