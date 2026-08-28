import json, unittest
from pathlib import Path
from dogram.reach import evaluate_reach, ReachInputError
class ReachTests(unittest.TestCase):
    def load(self,n): return json.loads((Path(__file__).parent/'fixtures'/'reach'/n).read_text())
    def test_mutation_changes_reachability(self):
        r,_=evaluate_reach(self.load('same-surface-different-history.json')); q=r['queries'][0]; self.assertTrue(q['reachable_before']); self.assertFalse(q['reachable_after']); self.assertEqual(q['path_before'],['surface','h1','future']); self.assertIsNone(q['path_after']); self.assertNotIn('history_is_causal',r)
    def test_unknown_mutation_refuses(self):
        x=self.load('same-surface-different-history.json'); x['mutation']={'op':'WARP'};
        with self.assertRaises(ReachInputError): evaluate_reach(x)
