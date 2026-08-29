import copy
import unittest

from dogram.engine import evaluate_specimen


class EngineTests(unittest.TestCase):
    def specimen(self):
        return {
            "schema": "dogram.specimen/v0",
            "specimen_id": "delta-1",
            "operator": "delta",
            "operator_version": 1,
            "inputs": {"boundary_order": ["x"], "left": {"x": {"kind": "integer", "value": 1}}, "right": {"x": {"kind": "integer", "value": 2}}},
            "assumptions": [],
            "metadata": {},
        }

    def test_wrong_schema_refuses(self):
        specimen = self.specimen(); specimen["schema"] = "wrong"
        receipt = evaluate_specimen(specimen)
        self.assertEqual((receipt["status"], receipt["reason_code"]), ("REFUSE", "MALFORMED_SPECIMEN"))

    def test_unknown_operator_refuses(self):
        specimen = self.specimen(); specimen["operator"] = "mystery"
        self.assertEqual(evaluate_specimen(specimen)["reason_code"], "UNSUPPORTED_OPERATOR")

    def test_wrong_operator_version_refuses(self):
        specimen = self.specimen(); specimen["operator_version"] = 99
        self.assertEqual(evaluate_specimen(specimen)["reason_code"], "UNSUPPORTED_OPERATOR_VERSION")

    def test_valid_delta_returns_ok_receipt(self):
        receipt = evaluate_specimen(self.specimen())
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(receipt["result"]["first_difference"], "x")

    def test_malformed_operator_inputs_return_structured_refusal(self):
        specimen = self.specimen(); specimen["inputs"]["boundary_order"] = []
        receipt = evaluate_specimen(specimen)
        self.assertEqual(receipt["status"], "REFUSE")
        self.assertEqual(receipt["reason_code"], "INVALID_BOUNDARY_ORDER")

    def test_metadata_is_nonoperative_but_receipted(self):
        a = self.specimen(); b = copy.deepcopy(a); b["metadata"] = {"different": True}
        ra = evaluate_specimen(a); rb = evaluate_specimen(b)
        self.assertEqual(ra["result"], rb["result"])
        self.assertEqual(ra["consumed_inputs"], rb["consumed_inputs"])
        self.assertNotEqual(ra["input_digest"], rb["input_digest"])
        self.assertNotIn("metadata", ra["consumed_inputs"])


if __name__ == "__main__":
    unittest.main()
