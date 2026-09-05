import json
from pathlib import Path
import unittest

from dogram.local_global_cycle_cohomology import analyze_cycle_constraints


FIXTURE = Path(__file__).parent / "fixtures" / "local_global_cycle_cohomology_001.json"


class LocalGlobalCycleCohomologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())

    def test_even_cycle_parity_glues(self):
        case = self.fixture["control"]
        receipt = analyze_cycle_constraints(case["edge_bits"])
        self.assertEqual(receipt["cycle_parity"], 0)
        self.assertEqual(receipt["cohomology_class"], 0)
        self.assertEqual(receipt["global_solutions"], case["global_solutions"])
        self.assertTrue(receipt["globally_glueable"])
        self.assertTrue(all(receipt["local_edge_satisfiable"]))

    def test_odd_cycle_parity_is_local_to_global_obstruction(self):
        case = self.fixture["hostile"]
        receipt = analyze_cycle_constraints(case["edge_bits"])
        self.assertEqual(receipt["cycle_parity"], 1)
        self.assertEqual(receipt["cohomology_class"], 1)
        self.assertEqual(receipt["global_solutions"], [])
        self.assertFalse(receipt["globally_glueable"])
        self.assertTrue(all(receipt["local_edge_satisfiable"]))

    def test_complete_edge_table_splits_by_one_h1_bit(self):
        glueable = []
        obstructed = []
        for n in range(8):
            bits = [(n >> shift) & 1 for shift in (2, 1, 0)]
            receipt = analyze_cycle_constraints(bits)
            target = glueable if receipt["globally_glueable"] else obstructed
            target.append(bits)
        self.assertEqual(len(glueable), 4)
        self.assertEqual(len(obstructed), 4)
        self.assertTrue(all(sum(bits) % 2 == 0 for bits in glueable))
        self.assertTrue(all(sum(bits) % 2 == 1 for bits in obstructed))


if __name__ == "__main__":
    unittest.main()
