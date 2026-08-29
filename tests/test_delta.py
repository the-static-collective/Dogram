import json
import unittest
from pathlib import Path

from dogram.delta import DeltaInputError, evaluate_delta

FIXTURES = Path(__file__).parent / "fixtures" / "delta"


class DeltaTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_first_opaque_break_and_later_numeric_delta(self):
        result, consumed = evaluate_delta(self.load("first-opaque-break.json"))
        self.assertEqual(result["first_difference"], "PROJECTION")
        self.assertEqual(result["comparisons"][0], {"boundary": "LOADOUT", "relation": "SAME"})
        self.assertEqual(result["comparisons"][1], {"boundary": "PROJECTION", "relation": "DIFFERENT"})
        self.assertEqual(result["comparisons"][2]["delta"], {"kind": "integer", "value": 3})
        self.assertIn("inputs.left.PROJECTION", consumed)

    def test_exact_rational_delta_remains_exact(self):
        result, _ = evaluate_delta(self.load("exact-rational-delta.json"))
        self.assertEqual(result["comparisons"][0]["delta"], {"kind": "rational", "numerator": 2, "denominator": 3})

    def test_all_same_has_no_first_difference(self):
        inputs = {"boundary_order": ["a"], "left": {"a": {"kind": "integer", "value": 1}}, "right": {"a": {"kind": "integer", "value": 1}}}
        result, _ = evaluate_delta(inputs)
        self.assertIsNone(result["first_difference"])

    def test_duplicate_boundary_refuses(self):
        with self.assertRaises(DeltaInputError) as ctx:
            evaluate_delta({"boundary_order": ["a", "a"], "left": {}, "right": {}})
        self.assertEqual(ctx.exception.reason_code, "INVALID_BOUNDARY_ORDER")


if __name__ == "__main__":
    unittest.main()
