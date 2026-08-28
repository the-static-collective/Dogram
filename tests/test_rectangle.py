import json, unittest
from pathlib import Path
from dogram.rectangle import evaluate_rectangle, RectangleInputError
class RectangleTests(unittest.TestCase):
    def load(self,n): return json.loads((Path(__file__).parent/'fixtures'/'rectangle'/n).read_text())
    def test_exact_mixed_delta(self):
        r,_=evaluate_rectangle(self.load('exact-mixed-delta.json')); self.assertEqual(r['mixed_delta'],{'kind':'integer','value':3}); self.assertTrue(r['interaction_detected']); self.assertEqual(r['mode'],'numeric')
    def test_opaque_interaction(self):
        r,_=evaluate_rectangle(self.load('opaque-interaction.json')); self.assertTrue(r['equivalent_across_axis_a_when_b0']); self.assertFalse(r['equivalent_across_axis_a_when_b1']); self.assertTrue(r['interaction_detected']); self.assertNotIn('mixed_delta',r)
    def test_mixed_kinds_refuse(self):
        x=self.load('opaque-interaction.json'); x['cells']['11']={'kind':'integer','value':1};
        with self.assertRaises(RectangleInputError): evaluate_rectangle(x)
