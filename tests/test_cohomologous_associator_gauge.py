import json
import unittest
from pathlib import Path

from dogram.cohomologous_associator_gauge import (
    associator,
    coboundary,
    shifted_associator,
    cocycle_residuals,
    normalized_2cochains_matching,
    table_delta,
)


FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "cohomologous_associator_gauge_001.json").read_text()
)


class CohomologousAssociatorGaugeTests(unittest.TestCase):
    def test_shifted_associator_is_pointwise_different_but_differs_by_declared_coboundary(self):
        expected_delta = {
            tuple(item["triple"]): item["delta"]
            for item in FIXTURE["table_delta"]
        }
        delta = table_delta()
        self.assertEqual(delta, expected_delta)
        for triple, value in delta.items():
            self.assertEqual(value, coboundary(*triple))
            self.assertEqual(
                shifted_associator(*triple),
                (associator(*triple) + value) % 3,
            )

    def test_both_associator_tables_are_normalized_3cocycles(self):
        for cochain in (associator, shifted_associator):
            self.assertEqual(
                sorted(set(cocycle_residuals(cochain).values())),
                FIXTURE["pentagon_residual_values"],
            )
            for g in range(3):
                for h in range(3):
                    for k in range(3):
                        if 0 in (g, h, k):
                            self.assertEqual(cochain(g, h, k), 0)

    def test_base_associator_is_not_a_normalized_2cochain_coboundary(self):
        self.assertEqual(FIXTURE["normalized_2cochain_count"], 81)
        matches = normalized_2cochains_matching(associator)
        self.assertEqual(matches, [])
        self.assertFalse(FIXTURE["base_associator_is_coboundary"])


if __name__ == "__main__":
    unittest.main()
