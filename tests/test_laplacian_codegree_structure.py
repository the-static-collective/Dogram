from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.laplacian_codegree_structure import analyze_graph


FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "laplacian_codegree_structure_001.json").read_text()
)


class LaplacianCodegreeStructureTest(unittest.TestCase):
    def _receipt(self, key: str):
        return analyze_graph(
            FIXTURE["vertices"],
            tuple(tuple(edge) for edge in FIXTURE[key]),
        )

    def test_complete_laplacian_spectrum_and_degree_multiset_collide(self):
        a = self._receipt("graph_a_edges")
        b = self._receipt("graph_b_edges")
        expected_poly = tuple(FIXTURE["expected_laplacian_characteristic_polynomial"])
        expected_degrees = tuple(FIXTURE["expected_degree_sequence"])

        self.assertEqual(a.characteristic_polynomial, expected_poly)
        self.assertEqual(b.characteristic_polynomial, expected_poly)
        self.assertEqual(a.degree_sequence, expected_degrees)
        self.assertEqual(b.degree_sequence, expected_degrees)

    def test_cut_geometry_still_differs(self):
        a = self._receipt("graph_a_edges")
        b = self._receipt("graph_b_edges")

        self.assertEqual(
            a.articulation_vertices,
            tuple(FIXTURE["expected_graph_a_articulation_vertices"]),
        )
        self.assertEqual(
            b.articulation_vertices,
            tuple(FIXTURE["expected_graph_b_articulation_vertices"]),
        )
        self.assertEqual(a.diameter, FIXTURE["expected_graph_a_diameter"])
        self.assertEqual(b.diameter, FIXTURE["expected_graph_b_diameter"])
        self.assertNotEqual(a.articulation_vertices, b.articulation_vertices)
        self.assertNotEqual(a.diameter, b.diameter)

    def test_receipt_keeps_consumed_edges(self):
        a = self._receipt("graph_a_edges")
        self.assertEqual(a.edges, tuple(tuple(edge) for edge in FIXTURE["graph_a_edges"]))


if __name__ == "__main__":
    unittest.main()
