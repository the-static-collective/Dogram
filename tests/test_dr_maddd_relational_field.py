import json
import unittest
from pathlib import Path

from dogram.delta import evaluate_delta
from dogram.rectangle import evaluate_rectangle
from dogram.reach import evaluate_reach

FIXTURES = Path(__file__).parent / "fixtures" / "dr_maddd"


class DrMadddRelationalFieldTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_precision_fiber_splits_only_when_probe_resolves_hidden_digit(self):
        result, _ = evaluate_delta(self.load("precision-fiber.json"))
        self.assertEqual(result["comparisons"][0]["relation"], "SAME")
        self.assertEqual(result["first_difference"], "p7")

    def test_pure_braid_return_can_close_endpoints_while_retaining_internal_receipt(self):
        result, _ = evaluate_delta(self.load("pure-braid-return.json"))
        self.assertEqual(result["comparisons"][0]["relation"], "SAME")
        self.assertEqual(result["first_difference"], "internal_action")

    def test_subtle_cut_adds_one_seam_and_changes_reachability(self):
        result, _ = evaluate_reach(self.load("subtle-cut.json"))
        query = result["queries"][0]
        self.assertFalse(query["reachable_before"])
        self.assertTrue(query["reachable_after"])
        self.assertEqual(query["path_after"], ["asker", "world_a", "world_b", "target"])

    def test_situated_question_detects_who_when_interaction(self):
        result, _ = evaluate_rectangle(self.load("situated-question.json"))
        self.assertTrue(result["interaction_detected"])
        self.assertTrue(result["equivalent_across_axis_a_when_b0"])
        self.assertFalse(result["equivalent_across_axis_a_when_b1"])

    def test_same_numeric_surface_does_not_hide_different_grammar(self):
        result, _ = evaluate_delta(self.load("numeric-homonym-control.json"))
        self.assertEqual(result["comparisons"][0]["relation"], "SAME")
        self.assertEqual(result["first_difference"], "grammar")


if __name__ == "__main__":
    unittest.main()
