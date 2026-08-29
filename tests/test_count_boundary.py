import unittest

from dogram.count_boundary import (
    FROZEN_OPERATOR_NAMES,
    apply_operator,
    audit_edge,
    induced_edges,
    trace_path,
)


class CountBoundaryTests(unittest.TestCase):
    def test_operator_family_is_frozen_and_small(self):
        self.assertEqual(
            FROZEN_OPERATOR_NAMES,
            (
                "pred",
                "succ",
                "prime_pi",
                "nth_prime",
                "divisor_count",
                "totient",
                "pair_count",
            ),
        )

    def test_original_pair_maps_cleanly_to_180_181_under_prime_counting(self):
        self.assertEqual(apply_operator("prime_pi", 1078), 180)
        self.assertEqual(apply_operator("prime_pi", 1087), 181)

    def test_two_original_branches_reconverge_at_180(self):
        self.assertEqual(apply_operator("prime_pi", 1078), 180)
        self.assertEqual(apply_operator("totient", apply_operator("prime_pi", 1087)), 180)

    def test_count_boundary_spine_is_exact(self):
        receipt = trace_path(
            1087,
            (
                "prime_pi",
                "pred",
                "divisor_count",
                "pred",
                "pair_count",
                "succ",
                "prime_pi",
            ),
        )
        self.assertEqual(receipt["nodes"], (1087, 181, 180, 18, 17, 136, 137, 33))
        self.assertTrue(receipt["exact"])

    def test_pair_count_reconnects_17_to_existing_136_137_mathal(self):
        self.assertEqual(apply_operator("pair_count", 17), 136)
        self.assertEqual(apply_operator("succ", 136), 137)
        self.assertEqual(apply_operator("prime_pi", 137), 33)
        self.assertEqual(apply_operator("nth_prime", 33), 137)

    def test_arbitrary_affine_rescue_is_refused(self):
        receipt = audit_edge(17, 1087, "affine_64x_minus_1")
        self.assertEqual(receipt["status"], "REFUSE_UNKNOWN_OPERATOR")
        self.assertFalse(receipt["exact"])

    def test_wrong_target_under_lawful_operator_is_failed_not_rewritten(self):
        receipt = audit_edge(17, 1087, "pair_count")
        self.assertEqual(receipt["status"], "NO_MATCH")
        self.assertEqual(receipt["calculated"], 136)
        self.assertFalse(receipt["exact"])

    def test_induced_edges_find_only_predeclared_relations_inside_old_mathals(self):
        corpus = (12, 13, 17, 18, 27, 81, 82, 107, 108, 136, 137, 180, 181, 666, 1078, 1087)
        edges = induced_edges(corpus)
        triples = {(edge["source"], edge["operator"], edge["target"]) for edge in edges}

        self.assertIn((1078, "prime_pi", 180), triples)
        self.assertIn((1087, "prime_pi", 181), triples)
        self.assertIn((180, "divisor_count", 18), triples)
        self.assertIn((17, "pair_count", 136), triples)
        self.assertIn((108, "divisor_count", 12), triples)
        self.assertIn((666, "divisor_count", 12), triples)
        self.assertNotIn((17, "affine_64x_minus_1", 1087), triples)


if __name__ == "__main__":
    unittest.main()
