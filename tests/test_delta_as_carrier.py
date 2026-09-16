import unittest

from dogram.triangulator import (
    continue_from_delta,
    triangular,
    triangulator_001_receipt,
)


class DeltaAsCarrierTests(unittest.TestCase):
    def test_delta_can_become_new_carrier_without_losing_parent_ancestry(self):
        parent = triangulator_001_receipt()
        child = continue_from_delta(parent, triangular)

        self.assertEqual(child["specimen"], "DELTA-AS-CARRIER-001")
        self.assertEqual(child["carrier"], 100)
        self.assertEqual(child["operator"], "triangular")
        self.assertEqual(child["projection"], 5050)

        ancestry = child["ancestry"]
        self.assertEqual(ancestry["parent_specimen"], "TRIANGULATOR-001")
        self.assertEqual(ancestry["parent_carrier"], 5)
        self.assertEqual(ancestry["parent_operators"], {"first": "square", "second": "triangular"})
        self.assertEqual(ancestry["parent_paths"]["second_after_first"], 325)
        self.assertEqual(ancestry["parent_paths"]["first_after_second"], 225)
        self.assertEqual(ancestry["parent_delta"], 100)
        self.assertEqual(ancestry["parent_classification"], "nonzero_structured")

    def test_child_ancestry_is_a_snapshot_not_an_alias_of_mutable_parent(self):
        parent = triangulator_001_receipt()
        child = continue_from_delta(parent, triangular)

        parent["paths"]["second_after_first"] = -1
        parent["operators"]["first"] = "mutated"

        self.assertEqual(child["ancestry"]["parent_paths"]["second_after_first"], 325)
        self.assertEqual(child["ancestry"]["parent_operators"]["first"], "square")

    def test_parent_receipt_is_not_mutated_by_continuation(self):
        parent = triangulator_001_receipt()
        before = repr(parent)

        continue_from_delta(parent, triangular)

        self.assertEqual(repr(parent), before)

    def test_missing_integer_delta_is_rejected(self):
        with self.assertRaises(ValueError):
            continue_from_delta({"specimen": "broken"}, triangular)


if __name__ == "__main__":
    unittest.main()
