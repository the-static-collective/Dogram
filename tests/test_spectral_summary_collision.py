from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.sheaf_laplacian_energy import analyze_weighted_path_sheaf


FIXTURE = Path(__file__).parent / "fixtures" / "spectral_summary_collision_001.json"


class SpectralSummaryCollisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_same_kernel_and_trace_do_not_fix_characteristic_polynomial(self) -> None:
        control_expected = self.fixture["control"]
        hostile_expected = self.fixture["hostile"]

        control = analyze_weighted_path_sheaf(tuple(control_expected["edge_scales"]), (1, 0, 0))
        hostile = analyze_weighted_path_sheaf(tuple(hostile_expected["edge_scales"]), (1, 0, 0))

        self.assertEqual(control.global_section_basis, hostile.global_section_basis)
        self.assertEqual(control.nullity, hostile.nullity)
        self.assertEqual(control.trace, hostile.trace)
        self.assertEqual(control.trace, 130)

        self.assertEqual(list(control.characteristic_polynomial), control_expected["characteristic_polynomial"])
        self.assertEqual(list(hostile.characteristic_polynomial), hostile_expected["characteristic_polynomial"])
        self.assertNotEqual(control.characteristic_polynomial, hostile.characteristic_polynomial)

    def test_nonzero_product_exposes_hidden_spectral_delta(self) -> None:
        control = analyze_weighted_path_sheaf((1, 8), (1, 0, 0))
        hostile = analyze_weighted_path_sheaf((4, 7), (1, 0, 0))

        self.assertEqual(control.trace, hostile.trace)
        self.assertEqual(control.nonzero_eigenvalue_product, 192)
        self.assertEqual(hostile.nonzero_eigenvalue_product, 2352)
        self.assertNotEqual(
            control.nonzero_eigenvalue_product,
            hostile.nonzero_eigenvalue_product,
        )

    def test_collision_is_exact_sum_of_squares_identity(self) -> None:
        self.assertEqual(1**2 + 8**2, 4**2 + 7**2)
        self.assertEqual(1**2 + 8**2, 65)
        self.assertNotEqual((1 * 8) ** 2, (4 * 7) ** 2)


if __name__ == "__main__":
    unittest.main()
