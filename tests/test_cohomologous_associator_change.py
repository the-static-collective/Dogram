import json
from pathlib import Path
import unittest

from dogram.cohomologous_associator_change import (
    Z3,
    coboundary_table,
    delta3_of_shifted,
    nonzero_coboundary_entries,
    normalized_shifted_associator,
    specimen_receipt,
)


FIXTURE = Path(__file__).parent / "fixtures" / "cohomologous_associator_change_001.json"


class CohomologousAssociatorChangeTests(unittest.TestCase):
    def test_frozen_receipt(self):
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(specimen_receipt(), expected)

    def test_raw_tables_differ_at_exactly_four_triples(self):
        self.assertEqual(
            nonzero_coboundary_entries(),
            {
                (1, 1, 2): 2,
                (1, 2, 2): 1,
                (2, 1, 1): 1,
                (2, 2, 1): 2,
            },
        )
        self.assertEqual(sum(value != 0 for value in coboundary_table().values()), 4)
        self.assertTrue(normalized_shifted_associator())

    def test_coboundary_associator_closes_every_pentagon(self):
        residuals = [
            delta3_of_shifted(g, h, k, ell)
            for g in Z3
            for h in Z3
            for k in Z3
            for ell in Z3
        ]
        self.assertEqual(len(residuals), 81)
        self.assertTrue(all(value == 0 for value in residuals))


if __name__ == "__main__":
    unittest.main()
