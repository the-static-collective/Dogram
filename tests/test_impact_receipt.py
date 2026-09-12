import unittest

from dogram.impact_receipt import ImpactReceiptInputError, evaluate_impact_receipt


class ImpactReceiptTests(unittest.TestCase):
    def test_receipts_structural_and_path_delta_without_interpreting_it(self):
        inputs = {
            "baseline": {
                "nodes": ["source", "fast", "safe", "output"],
                "edges": [
                    ["source", "fast"],
                    ["fast", "output"],
                    ["source", "safe"],
                    ["safe", "output"],
                ],
            },
            "candidate": {
                "nodes": ["source", "fast", "safe", "output", "receipt"],
                "edges": [
                    ["fast", "output"],
                    ["source", "safe"],
                    ["safe", "output"],
                    ["output", "receipt"],
                ],
            },
            "queries": [["source", "output"], ["source", "receipt"]],
        }

        result, consumed = evaluate_impact_receipt(inputs)

        self.assertEqual(result["node_delta"], {"added": ["receipt"], "removed": []})
        self.assertEqual(
            result["edge_delta"],
            {
                "added": [["output", "receipt"]],
                "removed": [["source", "fast"]],
            },
        )
        self.assertIn(["source", "fast"], result["reachability_delta"]["lost"])
        self.assertIn(["source", "receipt"], result["reachability_delta"]["gained"])

        source_to_output = result["queries"][0]
        self.assertEqual(source_to_output["path_before"], ["source", "fast", "output"])
        self.assertEqual(source_to_output["path_after"], ["source", "safe", "output"])
        self.assertTrue(source_to_output["changed"])
        self.assertTrue(source_to_output["reachable_before"])
        self.assertTrue(source_to_output["reachable_after"])

        source_to_receipt = result["queries"][1]
        self.assertIsNone(source_to_receipt["path_before"])
        self.assertEqual(source_to_receipt["path_after"], ["source", "safe", "output", "receipt"])
        self.assertTrue(source_to_receipt["changed"])

        self.assertNotEqual(result["graph_before_digest"], result["graph_after_digest"])
        self.assertEqual(
            consumed,
            ["inputs.baseline", "inputs.candidate", "inputs.queries"],
        )

    def test_query_must_name_nodes_present_in_at_least_one_side(self):
        inputs = {
            "baseline": {"nodes": ["a"], "edges": []},
            "candidate": {"nodes": ["a"], "edges": []},
            "queries": [["missing", "a"]],
        }

        with self.assertRaises(ImpactReceiptInputError) as ctx:
            evaluate_impact_receipt(inputs)

        self.assertEqual(ctx.exception.reason_code, "INVALID_QUERY_REFERENCE")


if __name__ == "__main__":
    unittest.main()
