from __future__ import annotations

import json
import unittest
from copy import deepcopy

from dogram.dogwolf_compose_001 import compose_receipt


STATES = ('a', 'b', 'c')
PROJECTION = (0, 0, 1)
F = ('swap', ('b', 'a', 'c'))
G = ('redirect', ('a', 'b', 'a'))
SUCCESSORS = (('a',), ('c',), ())


def specimen(**changes):
    model = dict(states=STATES, projection=PROJECTION, first=F,
                 second=G, successors=SUCCESSORS)
    model.update(changes)
    return compose_receipt(**model)


class DogwolfComposeTests(unittest.TestCase):
    def test_one_model_retains_three_independent_results_and_op_names(self):
        r = specimen()
        self.assertEqual(r['schema'], 'dogram/dogwolf-compose-001/v0')
        self.assertEqual(r['model']['states'], ['a', 'b', 'c'])
        self.assertEqual(r['model']['operations']['first']['name'], 'swap')
        self.assertEqual(r['model']['operations']['second']['name'], 'redirect')
        self.assertEqual(r['results']['descent']['probes'][0]['operation'], 'redirect')
        self.assertEqual(r['results']['descent']['probes'][1]['operation'], 'swap')
        self.assertEqual(r['results']['successor']['projected']['status'], 'counterexample')
        self.assertEqual(r['results']['commutation']['raw']['status'], 'counterexample')
        self.assertEqual(r['results']['commutation']['projected']['status'], 'preserved')
        self.assertEqual(r['results']['successor']['projected']['witness']['states'], ['a', 'b'])
        self.assertEqual(r['results']['commutation']['raw']['witness']['origin'], 'c')
        self.assertEqual(r['results']['commutation']['raw']['witness']['projected_endpoints'], [0, 0])
        self.assertIn('succession', r['model']['successor_relation'])
        self.assertEqual(r['authority'], 'none')
        self.assertNotIn('ready_to_merge', r)
        self.assertNotIn('overall_status', r)
        json.dumps(r, allow_nan=False)

    def test_each_kernel_is_run_on_identical_typed_state_and_projection_declaration(self):
        r = specimen()
        for name in ('descent', 'successor', 'commutation'):
            calc = r['results'][name]
            self.assertEqual(calc['states'], r['model']['states'])
            self.assertEqual(calc['projection'], r['model']['projection'])
            self.assertEqual(len(calc['input_sha256']), 64)
        self.assertEqual(len(r['model_sha256']), 64)
        self.assertEqual(len(r['receipt_sha256']), 64)
        self.assertEqual(r, specimen())

    def test_receipt_digest_changes_when_any_declared_relation_changes(self):
        base = specimen()
        modified = (
            specimen(successors=(('a',), ('b',), ())),
            specimen(projection=(0, 1, 1)),
            specimen(first=('swap', ('a', 'b', 'c'))),
            specimen(second=('redirect', ('a', 'b', 'b'))),
            specimen(max_pair_checks=0),
            specimen(max_state_checks=0),
        )
        for r in modified:
            self.assertNotEqual(r['model_sha256'], base['model_sha256'])
            self.assertNotEqual(r['receipt_sha256'], base['receipt_sha256'])

    def test_receipt_digest_is_derived_from_content_without_digest_field(self):
        from dogram.dogwolf_compose_001 import canonical_sha256
        r = specimen()
        self.assertEqual(r['receipt_sha256'], canonical_sha256({k: v for k, v in r.items() if k != 'receipt_sha256'}))
        changed = deepcopy(r)
        changed['results']['successor']['projected']['status'] = 'preserved'
        self.assertNotEqual(changed['receipt_sha256'], canonical_sha256({k: v for k, v in changed.items() if k != 'receipt_sha256'}))

    def test_zero_budgets_keep_every_incomplete_lens_inconclusive(self):
        r = specimen(max_pair_checks=0, max_state_checks=0)
        for p in r['results']['descent']['probes']:
            self.assertEqual(p['projected']['status'], 'inconclusive')
            self.assertIsNone(p['induced_table'])
        self.assertEqual(r['results']['successor']['projected']['status'], 'inconclusive')
        self.assertIsNone(r['results']['successor']['projected']['induced'])
        self.assertEqual(r['results']['commutation']['projected']['status'], 'inconclusive')
        self.assertEqual(r['results']['commutation']['raw']['status'], 'inconclusive')

    def test_a_different_projection_can_identify_bool_and_int_only_if_explicit(self):
        a = specimen(projection=(1, True, 0))
        b = specimen(projection=(1, 1, 0))
        self.assertNotEqual(a['model_sha256'], b['model_sha256'])
        self.assertEqual(a['results']['descent']['collapse_classes'], [['a'], ['b'], ['c']])
        self.assertEqual(b['results']['descent']['collapse_classes'], [['a', 'b'], ['c']])

    def test_rejects_invalid_or_partial_common_model_without_publishing_receipt(self):
        for patch in (
            {'states': ('a', 'a', 'c')},
            {'first': ('swap', ('b', 'unknown', 'c'))},
            {'second': ('swap', ('a', 'b', 'a'))},
            {'successors': (('a',), ('c',))},
            {'successors': (('a',), ('unknown',), ())},
            {'projection': (0, 0)},
            {'max_pair_checks': True},
            {'max_state_checks': -1},
        ):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                specimen(**patch)

    def test_no_undeclared_successor_relation_inferred_from_operation_targets(self):
        r = specimen(successors=((), (), ()))
        self.assertEqual(r['model']['successors'], [[], [], []])
        self.assertEqual(r['results']['successor']['projected']['status'], 'preserved')
        self.assertEqual(r['results']['commutation']['raw']['status'], 'counterexample')
        self.assertEqual(r['results']['descent']['probes'][0]['projected']['status'], 'preserved')


if __name__ == '__main__':
    unittest.main()
