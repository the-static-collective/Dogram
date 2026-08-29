import json
import unittest
from pathlib import Path

from dogram.reach import ReachInputError, evaluate_reach

FIXTURES = Path(__file__).parent / "fixtures" / "reach"


class ReachTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_remove_edge_changes_reachable_future(self):
        result, consumed = evaluate_reach(self.load("same-surface-different-history.json"))
        self.assertEqual(result["queries"][0], {"source": "surface", "target": "future", "reachable_before": True, "reachable_after": False, "changed": True, "path_before": ["surface", "h1", "future"], "path_after": None})
        self.assertIn("inputs.mutation", consumed)

    def test_unknown_mutation_refuses(self):
        inputs = self.load("same-surface-different-history.json")
        inputs["mutation"] = {"op": "TELEPORT", "node": "x"}
        with self.assertRaises(ReachInputError) as ctx:
            evaluate_reach(inputs)
        self.assertEqual(ctx.exception.reason_code, "UNSUPPORTED_MUTATION")

    def test_invalid_query_reference_refuses(self):
        inputs = self.load("same-surface-different-history.json")
        inputs["queries"] = [["missing", "future"]]
        with self.assertRaises(ReachInputError) as ctx:
            evaluate_reach(inputs)
        self.assertEqual(ctx.exception.reason_code, "INVALID_GRAPH_REFERENCE")


if __name__ == "__main__":
    unittest.main()
