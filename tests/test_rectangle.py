import json
import unittest
from pathlib import Path

from dogram.rectangle import RectangleInputError, evaluate_rectangle

FIXTURES = Path(__file__).parent / "fixtures" / "rectangle"


class RectangleTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_exact_numeric_mixed_delta(self):
        result, consumed = evaluate_rectangle(self.load("exact-mixed-delta.json"))
        self.assertEqual(result["mode"], "numeric")
        self.assertEqual(result["mixed_delta"], {"kind": "integer", "value": 3})
        self.assertTrue(result["interaction_detected"])
        self.assertIn("inputs.cells.11", consumed)

    def test_opaque_interaction_uses_equivalence_only(self):
        result, _ = evaluate_rectangle(self.load("opaque-interaction.json"))
        self.assertEqual(result, {"mode": "equivalence", "equivalent_across_axis_a_when_b0": True, "equivalent_across_axis_a_when_b1": False, "interaction_detected": True})
        self.assertNotIn("mixed_delta", result)

    def test_mixed_opaque_numeric_refuses(self):
        inputs = self.load("exact-mixed-delta.json")
        inputs["cells"]["00"] = {"kind": "opaque", "value": "x"}
        with self.assertRaises(RectangleInputError) as ctx:
            evaluate_rectangle(inputs)
        self.assertEqual(ctx.exception.reason_code, "MIXED_VALUE_MODES")


if __name__ == "__main__":
    unittest.main()
