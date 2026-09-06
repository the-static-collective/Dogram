from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.localized_spectral_deck import analyze_graph


FIXTURE = Path(__file__).parent / "fixtures" / "localized_spectral_deck_001.json"


class LocalizedSpectralDeckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_frozen_pair_preserves_coarse_global_receipts(self) -> None:
        control = analyze_graph(tuple(map(tuple, self.fixture["control"]["edges"])))
        hostile = analyze_graph(tuple(map(tuple, self.fixture["hostile"]["edges"])))

        self.assertEqual(control.degree_sequence, hostile.degree_sequence)
        self.assertEqual(control.laplacian_characteristic_polynomial, hostile.laplacian_characteristic_polynomial)
        self.assertEqual(control.articulation_count, hostile.articulation_count)
        self.assertEqual(control.bridge_count, hostile.bridge_count)
        self.assertEqual(control.diameter, hostile.diameter)
        self.assertEqual(control.distance_histogram, hostile.distance_histogram)
        self.assertEqual(control.triangle_count, hostile.triangle_count)

    def test_vertex_deleted_laplacian_deck_separates_pair(self) -> None:
        for key in ("control", "hostile"):
            expected = self.fixture[key]
            result = analyze_graph(tuple(map(tuple, expected["edges"])))
            self.assertEqual(list(result.degree_sequence), expected["degree_sequence"])
            self.assertEqual(list(result.laplacian_characteristic_polynomial), expected["laplacian_characteristic_polynomial"])
            self.assertEqual(result.articulation_count, expected["articulation_count"])
            self.assertEqual(result.bridge_count, expected["bridge_count"])
            self.assertEqual(result.diameter, expected["diameter"])
            self.assertEqual({str(k): v for k, v in result.distance_histogram}, expected["distance_histogram"])
            self.assertEqual(result.triangle_count, expected["triangle_count"])
            self.assertEqual([list(poly) for poly in result.vertex_deleted_laplacian_deck], expected["vertex_deleted_laplacian_deck"])

        control = analyze_graph(tuple(map(tuple, self.fixture["control"]["edges"])))
        hostile = analyze_graph(tuple(map(tuple, self.fixture["hostile"]["edges"])))
        self.assertNotEqual(control.vertex_deleted_laplacian_deck, hostile.vertex_deleted_laplacian_deck)

    def test_edges_must_define_a_connected_simple_graph_on_consecutive_vertices(self) -> None:
        with self.assertRaises(ValueError):
            analyze_graph(((0, 1), (1, 0)))
        with self.assertRaises(ValueError):
            analyze_graph(((0, 2),))
        with self.assertRaises(ValueError):
            analyze_graph(((0, 1), (2, 3)))


if __name__ == "__main__":
    unittest.main()
