from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.joint_degree_incidence import analyze_graph


FIXTURE = Path(__file__).parent / "fixtures" / "joint_degree_incidence_001.json"


class JointDegreeIncidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_frozen_pair_preserves_degree_sequence_and_complete_laplacian_spectrum(self) -> None:
        control = analyze_graph(tuple(map(tuple, self.fixture["control"]["edges"])))
        hostile = analyze_graph(tuple(map(tuple, self.fixture["hostile"]["edges"])))

        self.assertEqual(control.degree_sequence, hostile.degree_sequence)
        self.assertEqual(control.laplacian_characteristic_polynomial, hostile.laplacian_characteristic_polynomial)

    def test_joint_degree_incidence_separates_the_pair(self) -> None:
        for key in ("control", "hostile"):
            expected = self.fixture[key]
            result = analyze_graph(tuple(map(tuple, expected["edges"])))
            self.assertEqual(list(result.degree_sequence), expected["degree_sequence"])
            self.assertEqual(
                list(result.laplacian_characteristic_polynomial),
                expected["laplacian_characteristic_polynomial"],
            )
            self.assertEqual(
                [list(item) for item in result.joint_degree_counts],
                expected["joint_degree_counts"],
            )

        control = analyze_graph(tuple(map(tuple, self.fixture["control"]["edges"])))
        hostile = analyze_graph(tuple(map(tuple, self.fixture["hostile"]["edges"])))
        self.assertNotEqual(control.joint_degree_counts, hostile.joint_degree_counts)

    def test_edges_must_define_a_connected_simple_graph_on_consecutive_vertices(self) -> None:
        with self.assertRaises(ValueError):
            analyze_graph(((0, 1), (1, 0)))
        with self.assertRaises(ValueError):
            analyze_graph(((0, 2),))
        with self.assertRaises(ValueError):
            analyze_graph(((0, 1), (2, 3)))


if __name__ == "__main__":
    unittest.main()
