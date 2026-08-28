import unittest
from dogram.engine import evaluate_specimen
BASE={"schema":"dogram.specimen/v0","specimen_id":"s","operator":"delta","operator_version":1,"inputs":{"boundary_order":["A"],"left":{"A":{"kind":"integer","value":1}},"right":{"A":{"kind":"integer","value":2}}},"assumptions":[],"metadata":{}}
class EngineTests(unittest.TestCase):
    def test_wrong_schema_refuses(self):
        x=dict(BASE); x['schema']='bad'; r=evaluate_specimen(x); self.assertEqual((r['status'],r['reason_code']),('REFUSE','MALFORMED_SPECIMEN'))
    def test_unknown_operator_refuses(self):
        x=dict(BASE); x['operator']='magic'; self.assertEqual(evaluate_specimen(x)['reason_code'],'UNSUPPORTED_OPERATOR')
    def test_wrong_version_refuses(self):
        x=dict(BASE); x['operator_version']=9; self.assertEqual(evaluate_specimen(x)['reason_code'],'UNSUPPORTED_OPERATOR_VERSION')
    def test_valid_delta_ok(self): self.assertEqual(evaluate_specimen(BASE)['status'],'OK')
    def test_malformed_operator_inputs_are_structured(self):
        x=dict(BASE); x['inputs']={}; self.assertIn(evaluate_specimen(x)['status'],('REFUSE','INSUFFICIENT_TO_TEST'))
    def test_metadata_is_nonoperative_but_receipted(self):
        a={**BASE,'metadata':{'interest':'x'}}; b={**BASE,'metadata':{'interest':'y'}}; ra=evaluate_specimen(a); rb=evaluate_specimen(b); self.assertEqual(ra['result'],rb['result']); self.assertEqual(ra['consumed_inputs'],rb['consumed_inputs']); self.assertNotEqual(ra['input_digest'],rb['input_digest']); self.assertNotIn('metadata',ra['consumed_inputs'])
