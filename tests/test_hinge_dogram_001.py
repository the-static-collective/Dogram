import copy
import unittest

from research.hinge_dogram_001 import exact_relation_delta, verify_alex_hinge_receipt


BEFORE = [
    {"selector": "sign:hinge", "relation": "reading:mechanical-joint"},
    {"selector": "sign:wire", "relation": "reading:carrier"},
]

AFTER = [
    {"selector": "sign:hinge", "relation": "reading:constitutive-relation"},
    {"selector": "sign:wire", "relation": "reading:carrier"},
    {"selector": "sign:crossing", "relation": "reading:relation-site"},
]

ALEX_RECEIPT = {
    "added_rules": [
        {"selector": "sign:crossing", "relation": "reading:relation-site"},
    ],
    "removed_rules": [],
    "retargeted_rules": [
        {
            "selector": "sign:hinge",
            "before": "reading:mechanical-joint",
            "after": "reading:constitutive-relation",
        }
    ],
    "unchanged_rules": [
        {"selector": "sign:wire", "relation": "reading:carrier"},
    ],
    "grammar_changed": True,
    "authority": "none",
    "meaning_verdict": "none",
}


class HingeDogram001Tests(unittest.TestCase):
    def test_exact_relation_delta_is_order_independent(self):
        r1 = exact_relation_delta(BEFORE, AFTER)
        r2 = exact_relation_delta(list(reversed(BEFORE)), list(reversed(AFTER)))
        self.assertEqual(r1, r2)
        self.assertEqual(r1["added"], (("sign:crossing", "reading:relation-site"),))
        self.assertEqual(
            r1["retargeted"],
            (("sign:hinge", "reading:mechanical-joint", "reading:constitutive-relation"),),
        )
        self.assertEqual(r1["unchanged"], (("sign:wire", "reading:carrier"),))

    def test_alex_hinge_receipt_recomputes_exactly(self):
        r = verify_alex_hinge_receipt(BEFORE, AFTER, ALEX_RECEIPT)
        self.assertEqual(r["verdict"], "EXACT_MATCH")
        self.assertTrue(r["authority_preserved"])
        self.assertTrue(r["meaning_verdict_preserved"])
        self.assertIn("semantic_truth", r["does_not_establish"])

    def test_tampered_retarget_is_detected(self):
        receipt = copy.deepcopy(ALEX_RECEIPT)
        receipt["retargeted_rules"][0]["after"] = "reading:other"
        r = verify_alex_hinge_receipt(BEFORE, AFTER, receipt)
        self.assertEqual(r["verdict"], "MISMATCH")

    def test_authority_change_does_not_change_math_but_is_exposed(self):
        receipt = copy.deepcopy(ALEX_RECEIPT)
        receipt["authority"] = "granted"
        r = verify_alex_hinge_receipt(BEFORE, AFTER, receipt)
        self.assertEqual(r["verdict"], "EXACT_MATCH")
        self.assertFalse(r["authority_preserved"])

    def test_duplicate_selector_is_refused_by_math_boundary(self):
        bad = BEFORE + [{"selector": "sign:hinge", "relation": "reading:duplicate"}]
        with self.assertRaises(ValueError):
            exact_relation_delta(bad, AFTER)

    def test_same_rules_new_order_has_zero_delta(self):
        r = exact_relation_delta(BEFORE, list(reversed(BEFORE)))
        self.assertFalse(r["grammar_changed"])
        self.assertEqual(r["added"], ())
        self.assertEqual(r["removed"], ())
        self.assertEqual(r["retargeted"], ())


if __name__ == "__main__":
    unittest.main()
