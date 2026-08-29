import json
import unittest
from pathlib import Path

from dogram.ablate import AblateInputError, evaluate_ablate

FIXTURES = Path(__file__).parent / "fixtures" / "ablate"


class AblateTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_edge_ablation_that_survives_independent_paths(self):
        result, consumed = evaluate_ablate(self.load("trust-edge-survives.json"))
        self.assertEqual(result["removed_component"], {"kind": "edge", "source": "A", "target": "B"})
        self.assertEqual(result["gained_reachability"], [])
        self.assertNotIn(["A", "P"], result["lost_reachability"])
        self.assertIn("inputs.graph", consumed)
        self.assertIn("inputs.target", consumed)

    def test_edge_ablation_reports_collapsed_reachability(self):
        result, _ = evaluate_ablate(self.load("trust-edge-collapses.json"))
        self.assertIn(["A", "P"], result["lost_reachability"])
        self.assertFalse(result["requested_targets"][0]["reachable_after"])

    def test_missing_target_refuses(self):
        inputs = self.load("trust-edge-survives.json")
        inputs["target"] = {"kind": "edge", "source": "P", "target": "A"}
        with self.assertRaises(AblateInputError) as ctx:
            evaluate_ablate(inputs)
        self.assertEqual(ctx.exception.reason_code, "MISSING_ABLATION_TARGET")


if __name__ == "__main__":
    unittest.main()
