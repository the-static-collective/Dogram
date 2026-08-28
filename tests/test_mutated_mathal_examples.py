import json, unittest
from pathlib import Path
from dogram.engine import evaluate_specimen
ROOT=Path(__file__).parent.parent/'examples'/'mutated_mathals'
class MutatedMathalExamples(unittest.TestCase):
    def load(self,name): return json.loads((ROOT/name).read_text())
    def test_all_examples_execute_without_special_runtime(self):
        for name in ['interest-mediated-support.json','hidden-world-policy-rectangle.json','trust-withdrawal.json','same-surface-different-history.json']:
            with self.subTest(name=name): self.assertEqual(evaluate_specimen(self.load(name))['status'],'OK')
    def test_frozen_evidence_metadata_does_not_change_result(self):
        x=self.load('interest-mediated-support.json'); base={**x,'inputs':{'boundary_order':['EVIDENCE','SCORE'],'left':{'EVIDENCE':{'kind':'opaque','value':'E'},'SCORE':{'kind':'integer','value':2}},'right':{'EVIDENCE':{'kind':'opaque','value':'E'},'SCORE':{'kind':'integer','value':2}}}}; a={**base,'metadata':{'interest':'no'}}; b={**base,'metadata':{'interest':'yes'}}; ra=evaluate_specimen(a); rb=evaluate_specimen(b); self.assertEqual(ra['result'],rb['result']); self.assertNotEqual(ra['input_digest'],rb['input_digest'])
    def test_rectangle_reports_interaction_not_causality(self):
        r=evaluate_specimen(self.load('hidden-world-policy-rectangle.json'))['result']; self.assertTrue(r['interaction_detected']); self.assertNotIn('causal',r)
    def test_trust_withdrawal_survives_independent_paths(self):
        r=evaluate_specimen(self.load('trust-withdrawal.json'))['result']; self.assertTrue(all(q['reachable_after'] for q in r['requested_targets']))
    def test_state_example_reports_graph_delta_only(self):
        r=evaluate_specimen(self.load('same-surface-different-history.json'))['result']; self.assertTrue(r['queries'][0]['changed']); self.assertNotIn('history_is_causal',r)
