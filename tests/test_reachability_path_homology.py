from __future__ import annotations

import unittest

from dogram.path_homology import first_betti_number, reachability_closure


class ReachabilityPathHomologyTests(unittest.TestCase):
    def test_same_reachability_closure_can_hide_different_path_homology(self) -> None:
        vertices = (0, 1, 2)
        directed_cycle = ((0, 1), (1, 2), (2, 0))
        bidirected_triangle = tuple(
            (source, target)
            for source in vertices
            for target in vertices
            if source != target
        )

        cycle_closure = reachability_closure(vertices, directed_cycle)
        triangle_closure = reachability_closure(vertices, bidirected_triangle)

        self.assertEqual(cycle_closure, triangle_closure)
        self.assertEqual(len(cycle_closure), 9)
        self.assertEqual(first_betti_number(vertices, directed_cycle), 1)
        self.assertEqual(first_betti_number(vertices, bidirected_triangle), 0)

    def test_reachability_receipt_includes_reflexive_and_indirect_pairs(self) -> None:
        vertices = (0, 1, 2)
        directed_cycle = ((0, 1), (1, 2), (2, 0))

        closure = reachability_closure(vertices, directed_cycle)

        self.assertEqual(
            closure,
            tuple((source, target) for source in vertices for target in vertices),
        )


if __name__ == "__main__":
    unittest.main()
