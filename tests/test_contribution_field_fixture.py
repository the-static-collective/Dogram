from __future__ import annotations

import json
import unittest
from pathlib import Path

import dogram.contribution_field as contribution_field
from dogram.anti_collapse_reachability import analyze_collapse
from dogram.contribution_field import (
    ablate_event,
    build_cut,
    compare_measurements,
    measure_workmark,
    mint_workmark,
)
from tests.test_contribution_field import DECLARED, EVENTS


FIXTURE = Path(__file__).parent / "fixtures" / "contribution_field_001.json"


def build_frozen_specimen() -> dict[str, object]:
    workmark = mint_workmark(EVENTS, "e-create-x", 0, DECLARED)
    field_t0 = build_cut(EVENTS, 0, DECLARED)
    field_t1 = build_cut(EVENTS, 1, DECLARED)
    receipt_t0 = measure_workmark(field_t0, workmark)
    receipt_t1 = measure_workmark(field_t1, workmark)
    delta = compare_measurements(receipt_t0, receipt_t1)
    return {
        "workmark": workmark,
        "t0": receipt_t0,
        "t1": receipt_t1,
        "delta": delta,
        "ablation_enable_y": ablate_event(field_t1, workmark, "e-enable-y"),
        "ablation_repair_x": ablate_event(field_t1, workmark, "e-repair-x"),
        "full_measure_handoff_fixture": {
            "source": "Dogram",
            "authority": "none",
            "workmark_id": workmark["workmark_id"],
            "measurement_receipt_digest": receipt_t1["receipt_digest"],
            "delta_receipt_digest": delta["delta_digest"],
            "allowed_use": [
                "read-only story proposal input",
                "read-only quest proposal input",
                "read-only participation-opening input",
            ],
            "forbidden_promotion": [
                "source fact by narration",
                "economic value",
                "human worth",
                "sheet-changing authority",
            ],
        },
    }


class ContributionFieldFixtureTests(unittest.TestCase):
    def test_frozen_specimen_matches_exact_receipts(self) -> None:
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(build_frozen_specimen(), expected)

    def test_full_measure_handoff_is_inert_and_read_only(self) -> None:
        handoff = build_frozen_specimen()["full_measure_handoff_fixture"]
        self.assertEqual(handoff["source"], "Dogram")
        self.assertEqual(handoff["authority"], "none")
        self.assertIn("source fact by narration", handoff["forbidden_promotion"])
        self.assertIn("sheet-changing authority", handoff["forbidden_promotion"])


class ContributionHostileBoundaryTests(unittest.TestCase):
    def test_relation_kind_collapse_exposes_lost_distinction(self) -> None:
        receipt = analyze_collapse(
            states=("created@A-X", "reviewed@A-X"),
            rich_projection=(("A", "X", "CREATED"), ("A", "X", "REVIEWED")),
            collapsed_projection=(("A", "X"), ("A", "X")),
        )
        self.assertTrue(receipt.lawful_quotient)
        self.assertEqual(receipt.lost_distinctions, (("created@A-X", "reviewed@A-X"),))

    def test_contribution_field_exposes_no_person_scoring_surface(self) -> None:
        forbidden = {
            "score_person",
            "rank_people",
            "calculate_value",
            "price_contribution",
            "award_reputation",
        }
        self.assertTrue(forbidden.isdisjoint(dir(contribution_field)))


if __name__ == "__main__":
    unittest.main()
