from __future__ import annotations

import unittest
from itertools import product

from dogram.successor_descent_001 import analyze_successor_descent


class SuccessorDescentTests(unittest.TestCase):
    def test_different_raw_successors_can_have_same_projected_future(self):
        r = analyze_successor_descent(
            ('r0', 'r1', 'a', 'b'), ('ready', 'ready', 'done', 'done'),
            (('a',), ('b',), (), ()),
        )
        self.assertEqual(r.raw.status, 'counterexample')
        self.assertEqual(r.projected.status, 'preserved')
        self.assertEqual(r.projected.induced, (('ready', ('done',)), ('done', ())))
        self.assertEqual(r.raw.witness.states, ('r0', 'r1'))
        self.assertEqual(r.raw.witness.raw_successors, (('a',), ('b',)))
        self.assertEqual(r.raw.witness.projected_successors, (('done',), ('done',)))

    def test_a_distinguishing_projected_successor_breaks_descent(self):
        r = analyze_successor_descent(
            ('r0', 'r1', 'a', 'b', 'c'), ('ready', 'ready', 'near', 'near', 'far'),
            (('a', 'b'), ('a', 'c'), (), (), ()),
        )
        self.assertEqual(r.projected.status, 'counterexample')
        self.assertEqual(r.projected.witness.states, ('r0', 'r1'))
        self.assertEqual(r.projected.witness.left_only, ())
        self.assertEqual(r.projected.witness.right_only, ('far',))
        self.assertIsNone(r.projected.induced)

    def test_empty_and_nonempty_successors_are_not_identified(self):
        r = analyze_successor_descent(('r0', 'r1', 'a'), (0, 0, 1), ((), ('a',), ()))
        self.assertEqual(r.projected.status, 'counterexample')
        self.assertEqual(r.projected.witness.right_only, (1,))

    def test_identical_successor_sets_are_independent_of_table_order(self):
        x = analyze_successor_descent(('r0','r1','a','b'), (0,0,1,1),
                                      (('b','a'), ('a','b'), (), ()))
        y = analyze_successor_descent(('r0','r1','a','b'), (0,0,1,1),
                                      (('a','b'), ('b','a'), (), ()))
        self.assertEqual(x, y)
        self.assertEqual(x.raw.status, 'preserved')
        self.assertEqual(x.projected.status, 'preserved')
        self.assertEqual(x.projected.induced, ((0,(1,)), (1,())))

    def test_zero_budget_is_inconclusive_when_collapsed_pairs_exist(self):
        r = analyze_successor_descent(('a','b'), (0,0), ((),()), max_pair_checks=0)
        self.assertEqual(r.raw.status, 'inconclusive')
        self.assertEqual(r.projected.status, 'inconclusive')
        self.assertEqual(r.projected.checked_pairs, 0)
        self.assertIsNone(r.projected.induced)

    def test_zero_budget_is_vacuously_preserved_when_no_collapsed_pair(self):
        r = analyze_successor_descent(('a','b'), (0,1), (('b',),()), max_pair_checks=0)
        self.assertEqual(r.projected.status, 'preserved')
        self.assertEqual(r.projected.induced, ((0,(1,)), (1,())))

    def test_counterexample_found_with_budget_one_is_conclusive(self):
        r = analyze_successor_descent(('a','b','c'), (0,0,0), (('a',),('c',),()), max_pair_checks=1)
        self.assertEqual(r.projected.status, 'inconclusive')
        self.assertEqual(r.raw.status, 'counterexample')
        r2 = analyze_successor_descent(('a','b','c'), (0,0,1), (('a',),('c',),()), max_pair_checks=1)
        self.assertEqual(r2.projected.status, 'counterexample')
        self.assertEqual(r2.projected.checked_pairs, 1)

    def test_bool_and_int_do_not_collapse(self):
        r = analyze_successor_descent(('a','b'), (True,1), (('a',),('b',)), max_pair_checks=0)
        self.assertEqual(r.collapse_classes, (('a',), ('b',)))
        self.assertEqual(r.possible_pairs, 0)
        r2 = analyze_successor_descent(('a','b'), (0,0), (('a',),('b',)), max_pair_checks=0)
        self.assertNotEqual(r.input_sha256, r2.input_sha256)

    def test_reject_malformed_inputs(self):
        valid = dict(states=('a','b'), projection=(0,0), successors=(('a',),('b',)))
        for patch in (
            dict(states=('a','a')), dict(states=('a','')), dict(states=()),
            dict(projection=(0,)), dict(projection=(0.0,0)), dict(projection=([1],[1])),
            dict(successors=(('a',),)), dict(successors=(('a',),('missing',))),
            dict(successors=(('a','a'),('b',))), dict(successors=(('a',),["b"])),
            dict(successors=(('a',),(True,))), dict(successors=(('a',),('b',)), max_pair_checks=True),
            dict(max_pair_checks=-1),
        ):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                analyze_successor_descent(**{**valid, **patch})

    def test_exhaustive_tiny_relation_oracle(self):
        states=('a','b','c')
        successor_sets = tuple(tuple(states[i] for i in range(3) if mask & (1 << i)) for mask in range(8))
        for projection in product((0,1), repeat=3):
            for successors in product(successor_sets, repeat=3):
                projected = [frozenset(projection[states.index(t)] for t in row) for row in successors]
                expected = all(projection[i] != projection[j] or projected[i] == projected[j]
                               for i in range(3) for j in range(i+1,3))
                receipt = analyze_successor_descent(states, projection, successors)
                self.assertEqual(receipt.projected.status == 'preserved', expected)
                self.assertEqual(receipt.projected.induced is not None, expected)


if __name__ == '__main__':
    unittest.main()
