import json
import unittest
from pathlib import Path

from dogram.phaselift import evaluate_phaselift

FIXTURES = Path(__file__).parent / "fixtures" / "phaselift"


class PhaseLiftTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_lawful_new_verb_promotes_one_local_operator_candidate(self):
        result, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
        self.assertEqual(result["disposition"], "PROMOTE")
        self.assertEqual(result["earned_class"], "OPERATOR_CANDIDATE")
        self.assertEqual(result["delta_omega"], ["op/bind-and-route"])
        self.assertFalse(result["public_operator_admission"])
        self.assertEqual(receipt["schema"], "dogram.phaselift.receipt/v0")

    def test_three_echoes_earns_pattern_but_does_not_transfer(self):
        result, _ = evaluate_phaselift(self.load("three-echoes.json"))
        self.assertEqual(result["earned_class"], "PATTERN")
        self.assertEqual(result["disposition"], "RETAIN")
        self.assertTrue(result["checks"]["recurs"])
        self.assertFalse(result["checks"]["transfers"])
        self.assertEqual(
            result["reason_codes"],
            ["TRANSFER_CONTEXT_NOT_DISTINCT", "DELTA_OMEGA_EMPTY"],
        )

    def test_novel_output_fixture_earns_tool_before_generation_fails(self):
        result, _ = evaluate_phaselift(self.load("novel-output-no-new-verb.json"))
        self.assertTrue(result["checks"]["recurs"])
        self.assertTrue(result["checks"]["transfers"])
        self.assertEqual(result["earned_class"], "TOOL")

    def test_missing_generate_trial_is_insufficient_not_false(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"] = [t for t in specimen["trials"] if t["role"] != "GENERATE"]
        result, receipt = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "INSUFFICIENT_TO_TEST")
        self.assertEqual(result["reason_codes"], ["MISSING_TRIAL"])
        self.assertIsNone(receipt["trial_refs"]["generate"])

    def test_one_receipt_aliased_across_roles_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][1]["receipt_id"] = specimen["trials"][0]["receipt_id"]
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertEqual(result["reason_codes"], ["DUPLICATE_TRIAL_RECEIPT"])

    def test_candidate_digest_change_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][1]["candidate_digest"] = "sha256:different-candidate"
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertEqual(result["reason_codes"], ["CANDIDATE_IDENTITY_CHANGED"])

    def test_transformation_change_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][1]["transformation_id"] = "transform/different"
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertEqual(result["reason_codes"], ["TRANSFORMATION_IDENTITY_CHANGED"])

    def test_incomplete_provenance_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][1]["provenance_refs"] = []
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertEqual(result["reason_codes"], ["PROVENANCE_INCOMPLETE"])
        self.assertFalse(result["checks"]["provenance_complete"])

    def test_novel_value_without_new_operation_does_not_generate(self):
        result, _ = evaluate_phaselift(self.load("novel-output-no-new-verb.json"))
        self.assertFalse(result["checks"]["generates"])
        self.assertEqual(result["delta_omega"], [])
        self.assertEqual(result["reason_codes"], ["DELTA_OMEGA_EMPTY"])
        self.assertEqual(result["earned_class"], "TOOL")

    def test_plus_co_requires_explicit_verb(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["composition_witnesses"][0]["verb_id"] = ""
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "RETAIN")
        self.assertIn("PLUS_CO_MISSING_VERB", result["reason_codes"])

    def test_composition_requires_source_attribution(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["composition_witnesses"][0]["left_ref"] = "artifact/not-an-input"
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertIn("COMPOSITION_ATTRIBUTION_INCOMPLETE", result["reason_codes"])

    def test_compositional_surplus_must_be_non_empty(self):
        specimen = self.load("lawful-new-verb.json")
        witness = specimen["trials"][2]["composition_witnesses"][0]
        witness["output_capability_refs"] = ["op/bind", "op/route"]
        witness["surplus_capability_refs"] = []
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "RETAIN")
        self.assertIn("COMPOSITIONAL_SURPLUS_EMPTY", result["reason_codes"])

    def test_malformed_generated_operation_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["generated_operations"][0]["input_kinds"] = []
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertEqual(result["reason_codes"], ["GENERATED_OPERATION_INVALID"])

    def test_lawful_generation_adds_exactly_one_operation(self):
        result, _ = evaluate_phaselift(self.load("lawful-new-verb.json"))
        self.assertEqual(result["omega_before"], ["op/bind", "op/route"])
        self.assertEqual(result["omega_after"], ["op/bind", "op/bind-and-route", "op/route"])
        self.assertEqual(result["delta_omega"], ["op/bind-and-route"])
        self.assertTrue(result["checks"]["generates"])
        self.assertTrue(result["checks"]["composes"])
        self.assertEqual(result["earned_class"], "OPERATOR_CANDIDATE")

    def test_self_minting_operation_is_refused_as_circular(self):
        result, _ = evaluate_phaselift(self.load("self-minting-operator.json"))
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertFalse(result["checks"]["non_circular"])
        self.assertEqual(result["reason_codes"], ["CIRCULAR_PROMOTION_PROOF"])

    def test_indirect_cycle_through_replay_probe_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["generated_operations"][0]["replay_probe_ref"] = "phaselift/receipt-under-construction"
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertFalse(result["checks"]["non_circular"])
        self.assertIn("CIRCULAR_PROMOTION_PROOF", result["reason_codes"])

    def test_same_specimen_replays_to_identical_result_and_receipt(self):
        specimen = self.load("lawful-new-verb.json")
        self.assertEqual(evaluate_phaselift(specimen), evaluate_phaselift(specimen))

    def test_receipt_digest_hashes_unsigned_receipt(self):
        from dogram.canonical import sha256_json

        _, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
        unsigned = dict(receipt)
        digest = unsigned.pop("receipt_digest")
        self.assertEqual(digest, sha256_json(unsigned))

    def test_receipt_preserves_role_refs(self):
        _, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
        self.assertEqual(
            receipt["trial_refs"],
            {"repeat": "trial/repeat-004", "transfer": "trial/transfer-004", "generate": "trial/generate-004"},
        )

    def test_every_frozen_disposition_denies_public_operator_admission(self):
        for name in (
            "three-echoes.json",
            "novel-output-no-new-verb.json",
            "self-minting-operator.json",
            "lawful-new-verb.json",
        ):
            result, receipt = evaluate_phaselift(self.load(name))
            self.assertFalse(result["public_operator_admission"])
            self.assertFalse(receipt["public_operator_admission"])


if __name__ == "__main__":
    unittest.main()
