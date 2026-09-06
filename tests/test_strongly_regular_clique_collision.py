from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.strongly_regular_clique_collision import analyze_graph


FIXTURE = Path(__file__).parent / "fixtures" / "strongly_regular_clique_collision_001.json"


class StronglyRegularCliqueCollisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_pair_preserves_spectrum_degree_joint_degree_and_triangle_count(self) -> None:
        rook = analyze_graph(tuple(map(tuple, self.fixture["rook_4x4"]["edges"])))
        shrikhande = analyze_graph(tuple(map(tuple, self.fixture["shrikhande"]["edges"])))

        self.assertEqual(rook.degree_sequence, shrikhande.degree_sequence)
        self.assertEqual(rook.joint_degree_counts, shrikhande.joint_degree_counts)
        self.assertEqual(rook.laplacian_spectrum, shrikhande.laplacian_spectrum)
        self.assertEqual(rook.triangle_count, shrikhande.triangle_count)

    def test_k4_structure_separates_the_pair(self) -> None:
        for key in ("rook_4x4", "shrikhande"):
            expected = self.fixture[key]
            result = analyze_graph(tuple(map(tuple, expected["edges"])))
            self.assertEqual(list(result.degree_sequence), expected["degree_sequence"])
            self.assertEqual([list(item) for item in result.joint_degree_counts], expected["joint_degree_counts"])
            self.assertEqual([list(item) for item in result.laplacian_spectrum], expected["laplacian_spectrum"])
            self.assertEqual(result.triangle_count, expected["triangle_count"])
            self.assertEqual(result.k4_count, expected["k4_count"])
            self.assertEqual(result.clique_number, expected["clique_number"])

        rook = analyze_graph(tuple(map(tuple, self.fixture["rook_4x4"]["edges"])))
        shrikhande = analyze_graph(tuple(map(tuple, self.fixture["shrikhande"]["edges"])))
        self.assertNotEqual(rook.k4_count, shrikhande.k4_count)
        self.assertNotEqual(rook.clique_number, shrikhande.clique_number)

    def test_input_must_be_a_connected_simple_graph_on_consecutive_vertices(self) -> None:
        with self.assertRaises(ValueError):
            analyze_graph(((0, 1), (1, 0)))
        with self.assertRaises(ValueError):
            analyze_graph(((0, 2),))
        with self.assertRaises(ValueError):
            analyze_graph(((0, 1), (2, 3)))


if __name__ == "__main__":
    unittest.main()
