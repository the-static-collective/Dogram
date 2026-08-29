import unittest

from dogram.receipt import canonical_receipt_bytes, ok_receipt, refusal_receipt


class ReceiptTests(unittest.TestCase):
    def test_ok_receipt_names_consumed_inputs_and_input_digest(self):
        specimen = {"schema": "dogram.specimen/v0", "specimen_id": "s1", "operator": "delta", "operator_version": 1, "inputs": {}, "assumptions": [], "metadata": {"ignored": True}}
        receipt = ok_receipt(specimen, "delta", 1, ["inputs"], {"x": 1})
        self.assertEqual(receipt["schema"], "dogram.receipt/v0")
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(receipt["consumed_inputs"], ["inputs"])
        self.assertTrue(receipt["input_digest"].startswith("sha256:"))

    def test_refusal_is_structured_data(self):
        specimen = {"schema": "dogram.specimen/v0", "specimen_id": "bad"}
        receipt = refusal_receipt(specimen, "delta", 1, "REFUSE", "MALFORMED_SPECIMEN", ["operator missing"])
        self.assertEqual(receipt["status"], "REFUSE")
        self.assertEqual(receipt["reason_code"], "MALFORMED_SPECIMEN")

    def test_canonical_receipt_bytes_are_stable(self):
        specimen = {"schema": "dogram.specimen/v0", "specimen_id": "s1", "operator": "delta", "operator_version": 1, "inputs": {}, "assumptions": [], "metadata": {}}
        a = ok_receipt(specimen, "delta", 1, ["inputs"], {"b": 2, "a": 1})
        b = ok_receipt(specimen, "delta", 1, ["inputs"], {"a": 1, "b": 2})
        self.assertEqual(canonical_receipt_bytes(a), canonical_receipt_bytes(b))


if __name__ == "__main__":
    unittest.main()
