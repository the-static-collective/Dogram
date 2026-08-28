import json, unittest
from pathlib import Path
from dogram.ablate import evaluate_ablate
class AblateTests(unittest.TestCase):
    def load(self,n): return json.loads((Path(__file__).parent/'fixtures'/'ablate'/n).read_text())
    def test_survives(self):
        r,_=evaluate_ablate(self.load('trust-edge-survives.json')); self.assertEqual(r['gained_reachability'],[]); self.assertTrue(all(x['reachable_after'] for x in r['requested_targets']))
    def test_collapses(self):
        r,_=evaluate_ablate(self.load('trust-edge-collapses.json')); self.assertFalse(r['requested_targets'][0]['reachable_after']); self.assertIn(['A','P'],r['lost_reachability'])
