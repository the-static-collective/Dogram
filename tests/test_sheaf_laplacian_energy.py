from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.sheaf_laplacian_energy import analyze_weighted_path_sheaf


FIXTURE = Path(__file__).parent / "fixtures" / "sheaf_laplacian_energy_001.json"


class SheafLaplacianEnergyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_control_matches_frozen_receipt(self) -> None:
        expected = self.fixture["control"]
        result = analyze_weighted_path_sheaf(tuple(expected["edge_scales"]), tuple(expected["probe"]))
        self.assertEqual(list(result.global_section_basis), expected["global_section_basis"])
        self.assertEqual([list(row) for row in result.laplacian], expected["laplacian"])
        self.assertEqual(list(result.characteristic_polynomial), expected["characteristic_polynomial"])
        self.assertEqual(result.trace, expected["trace"])
        self.assertEqual(result.nonzero_eigenvalue_product, expected["nonzero_eigenvalue_product"])
        self.assertEqual(result.probe_energy, expected["probe_energy"])

    def test_hostile_preserves_global_sections_but_changes_nonzero_spectrum(self) -> None:
        control = analyze_weighted_path_sheaf((1, 1), (1, 0, 0))
        hostile = analyze_weighted_path_sheaf((2, 1), (1, 0, 0))

        self.assertEqual(control.global_section_basis, hostile.global_section_basis)
        self.assertEqual(control.nullity, hostile.nullity)
        self.assertNotEqual(control.characteristic_polynomial, hostile.characteristic_polynomial)
        self.assertEqual(control.nonzero_eigenvalue_product, 3)
        self.assertEqual(hostile.nonzero_eigenvalue_product, 12)
        self.assertEqual(control.probe_energy, 1)
        self.assertEqual(hostile.probe_energy, 4)

    def test_scales_must_be_positive_integers(self) -> None:
        with self.assertRaises(ValueError):
            analyze_weighted_path_sheaf((0, 1), (1, 0, 0))
        with self.assertRaises(ValueError):
            analyze_weighted_path_sheaf((1, -1), (1, 0, 0))


if __name__ == "__main__":
    unittest.main()
