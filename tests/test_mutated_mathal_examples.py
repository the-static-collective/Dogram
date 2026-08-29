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
        for name in (
            "interest-mediated-support.json",
            "hidden-world-policy-rectangle.json",
            "trust-withdrawal.json",
            "same-surface-different-history.json",
        ):
            with self.subTest(name=name):
                receipt = evaluate_specimen(self.load(name))
                self.assertEqual(receipt["status"], "OK")

    def test_interest_metadata_presence_is_not_consumption(self):
        specimen = self.load("interest-mediated-support.json")
        sibling = copy.deepcopy(specimen)
        sibling["metadata"]["interest_note"] = "different metadata only"
        a = evaluate_specimen(specimen)
        b = evaluate_specimen(sibling)
        self.assertEqual(a["result"], b["result"])
        self.assertNotEqual(a["input_digest"], b["input_digest"])
        self.assertFalse(any("metadata" in path for path in a["consumed_inputs"]))

    def test_same_surface_different_history_changes_reachable_future(self):
        left = self.load("same-surface-different-history.json")
        right = copy.deepcopy(left)
        right["specimen_id"] = "same-surface-different-history-sibling"
        right["inputs"]["graph"]["edges"].append(["surface", "future"])

        self.assertEqual(left["metadata"]["surface_label"], right["metadata"]["surface_label"])
        a = evaluate_specimen(left)
        b = evaluate_specimen(right)
        self.assertEqual(a["status"], "OK")
        self.assertEqual(b["status"], "OK")
        self.assertFalse(a["result"]["queries"][0]["reachable_after"])
        self.assertTrue(b["result"]["queries"][0]["reachable_after"])

    def test_examples_do_not_emit_semantic_promotion(self):
        for name in (
            "hidden-world-policy-rectangle.json",
            "trust-withdrawal.json",
            "same-surface-different-history.json",
        ):
            receipt = evaluate_specimen(self.load(name))
            encoded = json.dumps(receipt["result"], sort_keys=True).lower()
            self.assertNotIn("causal", encoded)
            self.assertNotIn("support", encoded)
            self.assertNotIn("historically", encoded)


if __name__ == "__main__":
    unittest.main()
