from __future__ import annotations

import unittest

from dogram.dogwolf_path_lift import hunt_phantom_path

STATES = ("p", "q_in", "q_out", "r")
QUOTIENT = ("P", "Q", "Q", "R")
EDGES = (("p", "enter", "q_in"), ("q_out", "exit", "r"))


class PathLiftTests(unittest.TestCase):
    def test_two_individually_witnessed_edges_are_a_phantom_composite(self):
        receipt = hunt_phantom_path(STATES, QUOTIENT, EDGES, max_depth=2)
        self.assertEqual(receipt.status, "phantom_found")
        p = receipt.phantom
        self.assertEqual(p.quotient_classes, ("P", "Q", "R"))
        self.assertEqual(p.action_labels, ("enter", "exit"))
        self.assertEqual(p.independent_edge_witnesses, EDGES)
        self.assertEqual(p.concrete_prefix, ("p", "q_in"))
        self.assertEqual(p.reachable_at_join, ("q_in",))
        self.assertEqual(p.next_edge_sources, ("q_out",))
        self.assertEqual(p.join_class, "Q")
        self.assertIn(("exit", "counterexample"), receipt.one_step_statuses)
        self.assertEqual(len(receipt.input_sha256), 64)
        self.assertEqual(receipt, hunt_phantom_path(STATES, QUOTIENT, EDGES, max_depth=2))

    def test_one_step_has_no_phantom_for_declared_may_edges(self):
        receipt = hunt_phantom_path(STATES, QUOTIENT, EDGES, max_depth=1)
        self.assertEqual(receipt.status, "no_phantom_within_bound")
        self.assertIsNone(receipt.phantom)

    def test_glue_edge_repairs_path(self):
        fixed = EDGES + (("q_in", "exit", "r"),)
        receipt = hunt_phantom_path(STATES, QUOTIENT, fixed, max_depth=2)
        self.assertEqual(receipt.status, "no_phantom_within_bound")
        self.assertEqual(dict(receipt.one_step_statuses)["exit"], "preserved")

    def test_full_one_step_factorization_protects_lifts(self):
        edges = (("p", "enter", "q_in"), ("q_in", "exit", "r"), ("q_out", "exit", "r"))
        receipt = hunt_phantom_path(STATES, QUOTIENT, edges, max_depth=3)
        self.assertEqual(receipt.status, "no_phantom_within_bound")
        self.assertTrue(all(status == "preserved" for _, status in receipt.one_step_statuses))

    def test_budget_never_returns_false_proof(self):
        receipt = hunt_phantom_path(STATES, QUOTIENT, EDGES, max_depth=2, max_paths=0)
        self.assertEqual((receipt.status, receipt.examined_paths), ("inconclusive", 0))
        receipt = hunt_phantom_path(STATES, QUOTIENT, EDGES, max_depth=2, max_paths=1)
        self.assertEqual(receipt.status, "inconclusive")

    def test_no_edges_is_exhaustive_even_with_zero_budget(self):
        receipt = hunt_phantom_path(("a",), ("A",), (), max_paths=0)
        self.assertEqual((receipt.status, receipt.examined_paths), ("no_phantom_within_bound", 0))

    def test_duplicate_edges_foreign_endpoint_and_bad_budget_rejected(self):
        for edges in (EDGES + (EDGES[0],), (("p", "go", "missing"),), (("p", 1, "r"),)):
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                hunt_phantom_path(STATES, QUOTIENT, edges)
        for budget in (-1, True, 100001):
            with self.subTest(budget=budget), self.assertRaises(ValueError):
                hunt_phantom_path(STATES, QUOTIENT, EDGES, max_paths=budget)

    def test_more_than_16_action_labels_rejected(self):
        edges = tuple(("p", f"step_{n}", "r") for n in range(17))
        with self.assertRaises(ValueError):
            hunt_phantom_path(STATES, QUOTIENT, edges)

    def test_input_order_does_not_change_digest_or_path_witness(self):
        first = hunt_phantom_path(STATES, QUOTIENT, EDGES)
        second = hunt_phantom_path(STATES, QUOTIENT, tuple(reversed(EDGES)))
        self.assertEqual(first.input_sha256, second.input_sha256)
        self.assertEqual(first.phantom, second.phantom)


if __name__ == "__main__":
    unittest.main()
