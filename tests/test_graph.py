import unittest

from dogram.graph import DirectedGraph, GraphInputError


class GraphTests(unittest.TestCase):
    def test_normalizes_serialization_and_rejects_duplicates(self):
        graph = DirectedGraph.from_spec({"nodes": ["b", "a", "c"], "edges": [["a", "c"], ["a", "b"]]})
        self.assertEqual(graph.to_spec(), {"nodes": ["a", "b", "c"], "edges": [["a", "b"], ["a", "c"]]})
        with self.assertRaises(GraphInputError):
            DirectedGraph.from_spec({"nodes": ["a", "a"], "edges": []})
        with self.assertRaises(GraphInputError):
            DirectedGraph.from_spec({"nodes": ["a", "b"], "edges": [["a", "b"], ["a", "b"]]})

    def test_edge_endpoints_must_exist(self):
        with self.assertRaises(GraphInputError):
            DirectedGraph.from_spec({"nodes": ["a"], "edges": [["a", "b"]]})

    def test_shortest_path_tie_breaks_lexicographically(self):
        graph = DirectedGraph.from_spec({"nodes": ["a", "b", "c", "d"], "edges": [["a", "c"], ["a", "b"], ["c", "d"], ["b", "d"]]})
        self.assertEqual(graph.shortest_path("a", "d"), ["a", "b", "d"])

    def test_mutation_is_immutable(self):
        graph = DirectedGraph.from_spec({"nodes": ["a", "b"], "edges": [["a", "b"]]})
        changed = graph.remove_edge("a", "b")
        self.assertTrue(graph.reachable("a", "b"))
        self.assertFalse(changed.reachable("a", "b"))

    def test_reachable_pairs_are_deterministic(self):
        graph = DirectedGraph.from_spec({"nodes": ["a", "b", "c"], "edges": [["a", "b"], ["b", "c"]]})
        self.assertEqual(graph.reachable_pairs(), [["a", "b"], ["a", "c"], ["b", "c"]])


if __name__ == "__main__":
    unittest.main()
