import unittest
from dogram.graph import DirectedGraph, GraphInputError
class GraphTests(unittest.TestCase):
    def test_normalizes_and_paths_deterministically(self):
        g=DirectedGraph.from_spec({'nodes':['C','A','B','D'],'edges':[['A','C'],['A','B'],['B','D'],['C','D']]}); self.assertEqual(g.nodes,('A','B','C','D')); self.assertEqual(g.shortest_path('A','D'),['A','B','D'])
    def test_duplicate_rejected(self):
        with self.assertRaises(GraphInputError): DirectedGraph.from_spec({'nodes':['A','A'],'edges':[]})
    def test_mutation_is_immutable(self):
        g=DirectedGraph.from_spec({'nodes':['A','B'],'edges':[['A','B']]}); g2=g.remove_edge('A','B'); self.assertTrue(g.reachable('A','B')); self.assertFalse(g2.reachable('A','B'))
