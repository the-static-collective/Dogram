from __future__ import annotations

import itertools
import json
import unittest
from pathlib import Path

from dogram.sheaf_holonomy_global_section import analyze_rank_one_triangle


FIXTURE = Path(__file__).parent / "fixtures" / "sheaf_holonomy_global_section_001.json"


class SheafHolonomyGlobalSectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_frozen_pair_keeps_local_shape_but_changes_global_section_space(self) -> None:
        base = self.fixture["base_graph"]
        self.assertEqual(base["vertex_stalk_dimensions"], [1, 1, 1])
        self.assertEqual(base["edge_stalk_dimensions"], [1, 1, 1])
        self.assertEqual(base["absolute_transport_values"], [1, 1, 1])

        for key in ("flat", "twisted"):
            expected = self.fixture[key]
            result = analyze_rank_one_triangle(tuple(expected["transports"]))
            self.assertEqual(result.transport_product, expected["transport_product"])
            self.assertEqual([list(row) for row in result.constraint_matrix], expected["constraint_matrix"])
            self.assertEqual(result.constraint_rank, expected["constraint_rank"])
            self.assertEqual(result.global_section_dimension, expected["global_section_dimension"])
            self.assertEqual([list(row) for row in result.laplacian], expected["laplacian"])
            self.assertEqual(list(result.laplacian_charpoly), expected["laplacian_charpoly"])
            self.assertEqual(result.laplacian_determinant, expected["laplacian_determinant"])

        flat = analyze_rank_one_triangle((1, 1, 1))
        twisted = analyze_rank_one_triangle((1, 1, -1))
        self.assertEqual(flat.global_section_dimension, 1)
        self.assertEqual(twisted.global_section_dimension, 0)
        self.assertNotEqual(flat.laplacian_determinant, twisted.laplacian_determinant)

    def test_all_eight_sign_assignments_are_classified_by_cycle_product(self) -> None:
        for transports in itertools.product((-1, 1), repeat=3):
            result = analyze_rank_one_triangle(transports)
            expected_dimension = 1 if result.transport_product == 1 else 0
            expected_determinant = 0 if result.transport_product == 1 else 4
            self.assertEqual(result.global_section_dimension, expected_dimension)
            self.assertEqual(result.laplacian_determinant, expected_determinant)

    def test_transport_domain_is_explicit(self) -> None:
        with self.assertRaises(ValueError):
            analyze_rank_one_triangle((1, 1))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            analyze_rank_one_triangle((1, 1, 2))


if __name__ == "__main__":
    unittest.main()
