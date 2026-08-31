import json
import unittest
from pathlib import Path

from dogram.ablate import evaluate_ablate
from dogram.delta import evaluate_delta
from dogram.reach import evaluate_reach
from dogram.rectangle import evaluate_rectangle

FIXTURES = Path(__file__).parent / "fixtures" / "phaselift_flow"


class PhaseliftFlowGapMathalTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_ternary_to_quaternary_first_difference_is_affine_rank(self):
        result, _ = evaluate_delta(self.load("ternary-to-quaternary.json"))
        self.assertEqual(result["first_difference"], "affine_rank")
        by_boundary = {item["boundary"]: item for item in result["comparisons"]}
        self.assertEqual(by_boundary["member_count"]["relation"], "SAME")
        self.assertEqual(by_boundary["affine_rank"]["delta"], {"kind": "integer", "value": 1})
        self.assertEqual(by_boundary["tetra_volume"]["delta"], {"kind": "rational", "numerator": 1, "denominator": 6})

    def test_authority_transfer_rectangle_separates_local_authorization_from_source_authority(self):
        fixture = self.load("authority-transfer-rectangle.json")
        lawful, _ = evaluate_rectangle(fixture["lawful"])
        hostile, _ = evaluate_rectangle(fixture["hostile"])
        self.assertEqual(lawful["mixed_delta"], {"kind": "integer", "value": 0})
        self.assertFalse(lawful["interaction_detected"])
        self.assertEqual(hostile["mixed_delta"], {"kind": "integer", "value": -1})
        self.assertTrue(hostile["interaction_detected"])

    def test_threshold_birth_edge_creates_reachability(self):
        result, _ = evaluate_reach(self.load("threshold-birth.json"))
        reports = {(q["source"], q["target"]): q for q in result["queries"]}
        self.assertFalse(reports[("H", "W_PRIME")]["reachable_before"])
        self.assertTrue(reports[("H", "W_PRIME")]["reachable_after"])
        self.assertEqual(reports[("H", "W_PRIME")]["path_after"], ["H", "THETA", "W_PRIME"])
        self.assertFalse(reports[("H", "WORK")]["reachable_before"])
        self.assertEqual(reports[("H", "WORK")]["path_after"], ["H", "THETA", "W_PRIME", "WORK"])

    def test_home_ablation_breaks_declared_attributable_continuation(self):
        result, _ = evaluate_ablate(self.load("home-ablation.json"))
        reports = {(q["source"], q["target"]): q for q in result["requested_targets"]}
        self.assertTrue(reports[("H", "W_PRIME")]["reachable_before"])
        self.assertFalse(reports[("H", "W_PRIME")]["reachable_after"])
        self.assertTrue(reports[("H", "NEXT")]["reachable_before"])
        self.assertFalse(reports[("H", "NEXT")]["reachable_after"])

    def test_same_fourth_different_decoder_has_nonzero_interaction(self):
        result, _ = evaluate_rectangle(self.load("same-fourth-different-decoder.json"))
        self.assertEqual(result["mixed_delta"], {"kind": "integer", "value": 1})
        self.assertTrue(result["interaction_detected"])

    def test_one_point_two_histories_preserves_endpoint_but_distinguishes_approach(self):
        result, _ = evaluate_delta(self.load("one-point-two-histories.json"))
        by_boundary = {item["boundary"]: item for item in result["comparisons"]}
        self.assertEqual(by_boundary["endpoint"]["relation"], "SAME")
        self.assertEqual(result["first_difference"], "approach_orientation")

    def test_release_removes_resistance_without_creating_next_edge(self):
        result, _ = evaluate_ablate(self.load("flow-has-next.json"))
        reports = {(q["source"], q["target"]): q for q in result["requested_targets"]}
        self.assertTrue(reports[("SELF", "NEXT")]["reachable_before"])
        self.assertTrue(reports[("SELF", "NEXT")]["reachable_after"])
        self.assertTrue(reports[("SELF", "RESIST")]["reachable_before"])
        self.assertFalse(reports[("SELF", "RESIST")]["reachable_after"])
        self.assertEqual(result["gained_reachability"], [])

    def test_shared_alignment_witness_does_not_create_contact(self):
        result, _ = evaluate_reach(self.load("alignment-without-contact.json"))
        reports = {(q["source"], q["target"]): q for q in result["queries"]}
        self.assertFalse(reports[("A_TOUCH", "B_TOUCH")]["reachable_before"])
        self.assertFalse(reports[("A_TOUCH", "B_TOUCH")]["reachable_after"])
        self.assertFalse(reports[("B_TOUCH", "A_TOUCH")]["reachable_before"])
        self.assertFalse(reports[("B_TOUCH", "A_TOUCH")]["reachable_after"])
        self.assertFalse(reports[("A_TOUCH", "SYNC")]["reachable_before"])
        self.assertTrue(reports[("A_TOUCH", "SYNC")]["reachable_after"])

    def test_synchrony_contributes_zero_interaction_to_crossability(self):
        result, _ = evaluate_rectangle(self.load("synchrony-bridge-rectangle.json"))
        self.assertEqual(result["mixed_delta"], {"kind": "integer", "value": 0})
        self.assertFalse(result["interaction_detected"])

    def test_bridge_birth_creates_cross_wheel_future(self):
        result, _ = evaluate_reach(self.load("bridge-birth.json"))
        reports = {(q["source"], q["target"]): q for q in result["queries"]}
        self.assertFalse(reports[("A_PRE", "B_NEXT")]["reachable_before"])
        self.assertTrue(reports[("A_PRE", "B_NEXT")]["reachable_after"])
        self.assertEqual(reports[("A_PRE", "B_NEXT")]["path_after"], ["A_PRE", "A_TOUCH", "B_TOUCH", "B_NEXT"])


if __name__ == "__main__":
    unittest.main()
