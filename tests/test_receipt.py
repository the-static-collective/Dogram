import unittest
from dogram.receipt import canonical_receipt_bytes, ok_receipt, refusal_receipt
class ReceiptTests(unittest.TestCase):
    def test_ok_receipt_names_consumed_inputs_and_input_digest(self):
        s={"schema":"dogram.specimen/v0","specimen_id":"s1","operator":"delta","operator_version":1,"inputs":{},"assumptions":[],"metadata":{"ignored":True}}; r=ok_receipt(s,"delta",1,["inputs"],{"x":1}); self.assertEqual(r["status"],"OK"); self.assertEqual(r["consumed_inputs"],["inputs"]); self.assertTrue(r["input_digest"].startswith("sha256:"))
    def test_refusal_is_structured_data(self): self.assertEqual(refusal_receipt({"specimen_id":"bad"},"delta",1,"REFUSE","MALFORMED_SPECIMEN")["reason_code"],"MALFORMED_SPECIMEN")
    def test_canonical_receipt_bytes_are_stable(self):
        s={"schema":"dogram.specimen/v0","specimen_id":"s1","operator":"delta","operator_version":1,"inputs":{},"assumptions":[],"metadata":{}}; self.assertEqual(canonical_receipt_bytes(ok_receipt(s,"delta",1,["inputs"],{"b":2,"a":1})),canonical_receipt_bytes(ok_receipt(s,"delta",1,["inputs"],{"a":1,"b":2})))
