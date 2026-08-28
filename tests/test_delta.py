import json, unittest
from pathlib import Path
from dogram.delta import evaluate_delta, DeltaInputError
class DeltaTests(unittest.TestCase):
    def load(self,n): return json.loads((Path(__file__).parent/'fixtures'/'delta'/n).read_text())
    def test_first_opaque_break(self):
        r,c=evaluate_delta(self.load('first-opaque-break.json')); self.assertEqual(r['first_difference'],'PROJECTION'); self.assertEqual(r['comparisons'][0],{'boundary':'LOADOUT','relation':'SAME'}); self.assertEqual(r['comparisons'][1],{'boundary':'PROJECTION','relation':'DIFFERENT'}); self.assertEqual(r['comparisons'][2]['delta'],{'kind':'integer','value':3}); self.assertIn('inputs.left.PROJECTION',c)
    def test_exact_rational_delta(self): self.assertEqual(evaluate_delta(self.load('exact-rational-delta.json'))[0]['comparisons'][0]['delta'],{'kind':'rational','numerator':2,'denominator':3})
    def test_duplicate_boundary_refuses(self):
        with self.assertRaises(DeltaInputError): evaluate_delta({'boundary_order':['A','A'],'left':{},'right':{}})
