import unittest

from dogram.count_boundary import (
    FROZEN_OPERATOR_IDS,
    expand_pair,
    prime_count_pair_fiber_size,
    walk_registry,
)


REGISTRY = {
    (12, 13),
    (17, 18),
    (81, 82),
    (107, 108),
    (136, 137),
    (180, 181),
    (207, 208),
    (1007, 1008),
    (1078, 1087),
    (1107, 1108),
}


class CountBoundaryTests(unittest.TestCase):
    def test_prime_count_pair_image_preserves_whole_pair_and_reports_lossy_fiber(self):
        receipts = expand_pair((1078, 1087))
        hit = next(
            r for r in receipts
            if r["operator"] == "prime_count@1" and r["mode"] == "pair_image"
        )
        self.assertEqual(hit["derived_pair"], [180, 181])
        self.assertEqual(hit["fiber_size"], 72)
        self.assertEqual(prime_count_pair_fiber_size((1078, 1087)), 72)

    def test_divisor_count_promotes_only_strict_record_holders(self):
        receipts = expand_pair((180, 181))
        pairs = {
            (r["operator"], r["mode"], tuple(r["derived_pair"]))
            for r in receipts
        }
        self.assertIn(("divisor_count_record@1", "left_predecessor", (17, 18)), pairs)
        self.assertIn(("divisor_count_record@1", "left_successor", (18, 19)), pairs)

        control = expand_pair((107, 108))
        self.assertFalse(any(r["operator"] == "divisor_count_record@1" for r in control))

    def test_pair_count_lift_emits_both_boundary_directions(self):
        receipts = expand_pair((17, 18))
        left = {
            (r["mode"], tuple(r["derived_pair"]))
            for r in receipts
            if r["operator"] == "pair_count@1" and r["source_side"] == "left"
        }
        self.assertEqual(
            left,
            {
                ("left_predecessor", (135, 136)),
                ("left_successor", (136, 137)),
            },
        )

    def test_receipts_expose_actual_dependency_arity(self):
        first = next(
            r for r in expand_pair((1078, 1087))
            if r["operator"] == "prime_count@1"
        )
        self.assertEqual(first["support_arity"], 2)
        self.assertEqual(first["support_values"], [1078, 1087])

        second = next(
            r for r in expand_pair((180, 181))
            if r["operator"] == "divisor_count_record@1"
            and r["mode"] == "left_predecessor"
        )
        self.assertEqual(second["support_arity"], 1)
        self.assertEqual(second["support_values"], [180])

        third = next(
            r for r in expand_pair((17, 18))
            if r["operator"] == "pair_count@1"
            and r["mode"] == "left_successor"
        )
        self.assertEqual(third["support_arity"], 1)
        self.assertEqual(third["support_values"], [17])

    def test_operator_constitution_is_frozen_and_totient_is_not_a_traverser(self):
        self.assertEqual(
            FROZEN_OPERATOR_IDS,
            ("prime_count@1", "divisor_count_record@1", "pair_count@1"),
        )
        self.assertFalse(any("totient" in op for op in FROZEN_OPERATOR_IDS))

    def test_registry_walk_recovers_only_the_hardened_existing_cascade(self):
        result = walk_registry((1078, 1087), REGISTRY, max_depth=4)
        edges = {
            (tuple(e["source_pair"]), e["operator"], e["mode"], tuple(e["derived_pair"]))
            for e in result["edges"]
        }
        self.assertIn(((1078, 1087), "prime_count@1", "pair_image", (180, 181)), edges)
        self.assertIn(((180, 181), "divisor_count_record@1", "left_predecessor", (17, 18)), edges)
        self.assertIn(((17, 18), "pair_count@1", "left_successor", (136, 137)), edges)
        self.assertEqual(result["visited_pairs"], [[1078, 1087], [180, 181], [17, 18], [136, 137]])

        controls = {(81, 82), (207, 208), (1007, 1008), (1107, 1108)}
        for control in controls:
            control_result = walk_registry(control, REGISTRY, max_depth=2)
            self.assertEqual(control_result["visited_pairs"], [list(control)])


if __name__ == "__main__":
    unittest.main()
