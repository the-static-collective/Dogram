import json
import pathlib
import unittest

from dogram.productive_desync import ReturnRelation, assess_productive_desync


ROOT = pathlib.Path(__file__).parents[1]
RETURN_FIXTURES = ROOT / "tests" / "fixtures" / "return_relation"


def load_return_fixture(name):
    return json.loads((RETURN_FIXTURES / name).read_text())


class ReturnRelationTests(unittest.TestCase):
    def test_return_is_computed_from_declared_quotient_observations(self):
        relation = ReturnRelation(
            relation_id="sheet-return",
            quotient_id="phi-mod-3",
            anchor_before=[0, 0],
            anchor_after=[3, 0],
            quotient_before=0,
            quotient_after=0,
        )
        self.assertTrue(relation.returned)
        self.assertNotEqual(relation.anchor_before, relation.anchor_after)

    def test_nonreturn_is_computed_without_global_inference(self):
        relation = ReturnRelation(
            relation_id="carrier-return",
            quotient_id="exact-state",
            anchor_before=[0, 0],
            anchor_after=[3, 0],
            quotient_before=[0, 0],
            quotient_after=[3, 0],
        )
        self.assertFalse(relation.returned)

    def test_empty_relation_or_quotient_id_refuses(self):
        for field in ("relation_id", "quotient_id"):
            values = {
                "relation_id": "sheet-return",
                "quotient_id": "phi-mod-3",
                "anchor_before": [0, 0],
                "anchor_after": [3, 0],
                "quotient_before": 0,
                "quotient_after": 0,
            }
            values[field] = ""
            with self.assertRaises(ValueError):
                ReturnRelation(**values)


class ProductiveDesyncTests(unittest.TestCase):
    def assess(self, **overrides):
        values = {
            "target_preserved": True,
            "execution_residual": {"step_trace": {"changed": True}},
            "baseline_reach_count": 18,
            "historical_reach_count": 36,
            "closure_reach_count": 54,
            "cut_declared": True,
            "cut_budget": 1,
            "cuts_used": 1,
            "return_relation": ReturnRelation(
                relation_id="bounded-coherence-return",
                quotient_id="declared-coherence-cut",
                anchor_before={"sheet": 0},
                anchor_after={"sheet": 0},
                quotient_before=0,
                quotient_after=0,
            ),
        }
        values.update(overrides)
        return assess_productive_desync(**values)

    def test_historical_expansion_inside_budget_is_witness(self):
        result = self.assess()
        self.assertEqual((result.status, result.reason_code), ("WITNESS", None))
        self.assertTrue(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_closure_only_expansion_is_potential(self):
        result = self.assess(historical_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("POTENTIAL", "CLOSURE_ONLY"))
        self.assertFalse(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_target_failure_refuses_even_when_reach_expands(self):
        result = self.assess(target_preserved=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "TARGET_NOT_PRESERVED"))

    def test_missing_execution_residual_refuses(self):
        result = self.assess(execution_residual={})
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_EXECUTION_RESIDUAL"))

    def test_untyped_cut_refuses(self):
        result = self.assess(cut_declared=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "UNTYPED_CUT"))

    def test_budget_exceeded_refuses(self):
        result = self.assess(cut_budget=1, cuts_used=2)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "CUT_BUDGET_EXCEEDED"))

    def test_no_declared_return_refuses_bounded_desync_label(self):
        relation = ReturnRelation(
            relation_id="bounded-coherence-return",
            quotient_id="declared-coherence-cut",
            anchor_before={"sheet": 0},
            anchor_after={"sheet": 1},
            quotient_before=0,
            quotient_after=1,
        )
        result = self.assess(return_relation=relation)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_COHERENCE_RETURN"))

    def test_assessment_receipt_preserves_return_scope(self):
        result = self.assess()
        relation = result.to_data()["return_relation"]
        self.assertEqual(relation["relation_id"], "bounded-coherence-return")
        self.assertEqual(relation["quotient_id"], "declared-coherence-cut")
        self.assertTrue(relation["returned"])

    def test_coarse_return_can_witness_while_fine_return_refuses_for_same_other_facts(self):
        fixture = load_return_fixture("productive-desync-scope-control.json")
        shared = fixture["assessment"]

        def build_relation(data):
            return ReturnRelation(
                relation_id=data["relation_id"],
                quotient_id=data["quotient_id"],
                anchor_before=data["anchor_before"],
                anchor_after=data["anchor_after"],
                quotient_before=data["quotient_before"],
                quotient_after=data["quotient_after"],
            )

        coarse = assess_productive_desync(**shared, return_relation=build_relation(fixture["coarse_return"]))
        fine = assess_productive_desync(**shared, return_relation=build_relation(fixture["fine_return"]))
        self.assertEqual(coarse.status, fixture["coarse_return"]["expected_status"])
        self.assertEqual(
            (fine.status, fine.reason_code),
            (
                fixture["fine_return"]["expected_status"],
                fixture["fine_return"]["expected_reason_code"],
            ),
        )

    def test_no_reachability_gain_refuses(self):
        result = self.assess(historical_reach_count=18, closure_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_REACHABILITY_EXPANSION"))

    def test_history_cannot_exceed_declared_closure(self):
        with self.assertRaises(ValueError):
            self.assess(historical_reach_count=55, closure_reach_count=54)

    def test_negative_cut_budget_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(cut_budget=-1)

    def test_non_dictionary_residual_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(execution_residual=True)

    def test_non_relation_return_input_refuses(self):
        with self.assertRaises(ValueError):
            self.assess(return_relation=True)


if __name__ == "__main__":
    unittest.main()
