import copy
import json
import unittest
from pathlib import Path

from dogram.engine import evaluate_specimen

EXAMPLES = Path(__file__).parent.parent / "examples" / "mutated_mathals"


class MutatedMathalExampleTests(unittest.TestCase):
    def load(self, name):
        return json.loads((EXAMPLES / name).read_text())

    def test_all_examples_execute_without_runtime_special_cases(self):
        for name in ("interest-mediated-support.json", "hidden-world-policy-rectangle.json", "trust-withdrawal.json", "same-surface-different-history.json"):
            with self.subTest(name=name):
                self.assertEqual(evaluate_specimen(self.load(name))["status"], "OK")

    def test_interest_metadata_presence_is_not_consumption(self):
        specimen = self.load("interest-mediated-support.json")
        sibling = copy.deepcopy(specimen); sibling["metadata"]["interest_note"] = "different metadata only"
        a = evaluate_specimen(specimen); b = evaluate_specimen(sibling)
        self.assertEqual(a["result"], b["result"])
        self.assertNotEqual(a["input_digest"], b["input_digest"])
        self.assertFalse(any("metadata" in path for path in a["consumed_inputs"]))

    def test_examples_do_not_emit_semantic_promotion(self):
        for name in ("hidden-world-policy-rectangle.json", "trust-withdrawal.json", "same-surface-different-history.json"):
            encoded = json.dumps(evaluate_specimen(self.load(name))["result"], sort_keys=True).lower()
            self.assertNotIn("causal", encoded)
            self.assertNotIn("support", encoded)
            self.assertNotIn("historically", encoded)


if __name__ == "__main__":
    unittest.main()
