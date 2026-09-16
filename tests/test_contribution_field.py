from __future__ import annotations

import unittest

from dogram.canonical import sha256_json
from dogram.contribution_field import (
    ContributionFieldInputError,
    ablate_event,
    build_cut,
    compare_measurements,
    measure_workmark,
    mint_workmark,
)


DECLARED = ("CREATED", "REPAIRED", "ENABLED", "CHALLENGED", "CARRIED")
EVENTS = [
    {"event_id": "e-create-x", "relation_kind": "CREATED", "source_ref": "A", "subject_ref": "X", "evidence_ref": "receipt:create-x", "evidence_status": "complete", "available_from": 0},
    {"event_id": "e-repair-x", "relation_kind": "REPAIRED", "source_ref": "B", "subject_ref": "X", "evidence_ref": "receipt:repair-x", "evidence_status": "complete", "available_from": 1},
    {"event_id": "e-enable-y", "relation_kind": "ENABLED", "source_ref": "X", "subject_ref": "Y", "evidence_ref": "receipt:enable-y", "evidence_status": "complete", "available_from": 1},
    {"event_id": "e-challenge-x", "relation_kind": "CHALLENGED", "source_ref": "C", "subject_ref": "X", "evidence_ref": "receipt:challenge-x", "evidence_status": "complete", "available_from": 1},
    {"event_id": "e-carry-z", "relation_kind": "CARRIED", "source_ref": "Y", "subject_ref": "Z", "evidence_ref": "receipt:carry-z", "evidence_status": "complete", "available_from": 1},
]


class ContributionFieldTests(unittest.TestCase):
    def test_cut_is_time_addressed_and_deterministic(self) -> None:
        t0 = build_cut(EVENTS, 0, DECLARED)
        t1 = build_cut(EVENTS, 1, DECLARED)
        self.assertEqual([event["event_id"] for event in t0["events"]], ["e-create-x"])
        self.assertEqual([event["event_id"] for event in t1["events"]], ["e-carry-z", "e-challenge-x", "e-create-x", "e-enable-y", "e-repair-x"])
        self.assertNotEqual(t0["field_digest"], t1["field_digest"])

    def test_incomplete_event_is_preserved_but_not_admitted_to_graph(self) -> None:
        events = [EVENTS[0], {**EVENTS[2], "evidence_status": "incomplete"}]
        cut = build_cut(events, 1, DECLARED)
        self.assertEqual(cut["incomplete_events"], ["e-enable-y"])
        self.assertNotIn("event:e-enable-y", cut["graph"]["nodes"])

    def test_invalid_event_is_preserved_but_not_admitted_to_graph(self) -> None:
        events = [EVENTS[0], {**EVENTS[2], "evidence_status": "invalid"}]
        cut = build_cut(events, 1, DECLARED)
        self.assertEqual(cut["invalid_events"], ["e-enable-y"])
        self.assertNotIn("event:e-enable-y", cut["graph"]["nodes"])

    def test_parallel_relation_kinds_get_distinct_event_nodes(self) -> None:
        review = {**EVENTS[0], "event_id": "e-review-x", "relation_kind": "REVIEWED", "evidence_ref": "receipt:review-x"}
        cut = build_cut([EVENTS[0], review], 0, (*DECLARED, "REVIEWED"))
        self.assertIn(["entity:A", "event:e-create-x"], cut["graph"]["edges"])
        self.assertIn(["entity:A", "event:e-review-x"], cut["graph"]["edges"])

    def test_undeclared_relation_fails_closed(self) -> None:
        with self.assertRaises(ContributionFieldInputError) as caught:
            build_cut([{**EVENTS[0], "relation_kind": "VALUED_AT_9000"}], 0, DECLARED)
        self.assertEqual(caught.exception.reason_code, "UNDECLARED_RELATION_KIND")

    def test_extra_semantic_field_fails_closed(self) -> None:
        with self.assertRaises(ContributionFieldInputError) as caught:
            build_cut([{**EVENTS[0], "value": 9000}], 0, DECLARED)
        self.assertEqual(caught.exception.reason_code, "EVENT_SHAPE_MISMATCH")

    def test_bool_is_not_an_integer_cut(self) -> None:
        with self.assertRaises(ContributionFieldInputError):
            build_cut(EVENTS, True, DECLARED)


def _workmark() -> dict[str, object]:
    return mint_workmark(EVENTS, "e-create-x", 0, DECLARED)


class ContributionWorkmarkTests(unittest.TestCase):
    def test_birth_stays_identical_while_history_grows(self) -> None:
        mark = _workmark()
        r0 = measure_workmark(build_cut(EVENTS, 0, DECLARED), mark)
        r1 = measure_workmark(build_cut(EVENTS, 1, DECLARED), mark)
        self.assertEqual(r0["workmark"], r1["workmark"])
        self.assertEqual(r0["measurements"]["reachable_descendant_set"], [])
        self.assertEqual(r1["measurements"]["reachable_descendant_set"], ["Y", "Z"])
        self.assertEqual(r1["measurements"]["descendant_count"], 2)

    def test_relation_counts_preserve_typed_history_touching_root_closure(self) -> None:
        receipt = measure_workmark(build_cut(EVENTS, 1, DECLARED), _workmark())
        self.assertEqual(
            receipt["measurements"]["relation_kind_counts"],
            {"CARRIED": 1, "CHALLENGED": 1, "CREATED": 1, "ENABLED": 1, "REPAIRED": 1},
        )

    def test_rewritten_birth_is_invalid(self) -> None:
        mark = _workmark()
        rewritten = [
            ({**event, "evidence_ref": "receipt:rewritten"} if event["event_id"] == "e-create-x" else event)
            for event in EVENTS
        ]
        with self.assertRaises(ContributionFieldInputError) as caught:
            measure_workmark(build_cut(rewritten, 1, DECLARED), mark)
        self.assertEqual(caught.exception.reason_code, "BIRTH_EVENT_DIGEST_MISMATCH")

    def test_incomplete_source_status_survives_measurement_without_edge_promotion(self) -> None:
        events = [EVENTS[0], {**EVENTS[2], "evidence_status": "incomplete"}]
        receipt = measure_workmark(build_cut(events, 1, DECLARED), _workmark())
        self.assertEqual(receipt["incomplete_events"], ["e-enable-y"])
        self.assertEqual(receipt["measurements"]["reachable_descendant_set"], [])

    def test_measurements_have_no_valuation_fields(self) -> None:
        receipt = measure_workmark(build_cut(EVENTS, 1, DECLARED), _workmark())
        forbidden = {"value", "merit", "price", "score", "rank", "human_worth"}
        self.assertTrue(forbidden.isdisjoint(receipt["measurements"]))


class ContributionDeltaTests(unittest.TestCase):
    def test_delta_reports_change_without_grading_it(self) -> None:
        mark = _workmark()
        before = measure_workmark(build_cut(EVENTS, 0, DECLARED), mark)
        after = measure_workmark(build_cut(EVENTS, 1, DECLARED), mark)
        delta = compare_measurements(before, after)
        self.assertEqual(delta["descendant_count_delta"], 2)
        self.assertEqual(delta["added_reachable_descendants"], ["Y", "Z"])
        self.assertNotIn("improved", delta)
        self.assertNotIn("value", delta)

    def test_ablating_enable_event_loses_y_and_z_reachability(self) -> None:
        field = build_cut(EVENTS, 1, DECLARED)
        receipt = ablate_event(field, _workmark(), "e-enable-y")
        self.assertEqual(receipt["lost_root_entity_reachability"], ["Y", "Z"])
        self.assertEqual(receipt["gained_root_entity_reachability"], [])

    def test_zero_reachability_loss_is_not_called_zero_contribution(self) -> None:
        field = build_cut(EVENTS, 1, DECLARED)
        receipt = ablate_event(field, _workmark(), "e-repair-x")
        self.assertEqual(receipt["lost_root_entity_reachability"], [])
        self.assertNotIn("importance", receipt)
        self.assertNotIn("merit", receipt)


class ContributionReceiptIntegrityTests(unittest.TestCase):
    def test_tampered_field_digest_is_rejected_before_measurement(self) -> None:
        field = build_cut(EVENTS, 1, DECLARED)
        tampered = {**field, "field_digest": "sha256:tampered"}
        with self.assertRaises(ContributionFieldInputError) as caught:
            measure_workmark(tampered, _workmark())
        self.assertEqual(caught.exception.reason_code, "FIELD_DIGEST_MISMATCH")

    def test_tampered_workmark_id_is_rejected(self) -> None:
        mark = {**_workmark(), "workmark_id": "sha256:tampered"}
        with self.assertRaises(ContributionFieldInputError) as caught:
            measure_workmark(build_cut(EVENTS, 1, DECLARED), mark)
        self.assertEqual(caught.exception.reason_code, "WORKMARK_DIGEST_MISMATCH")

    def test_self_consistent_wrong_workmark_address_is_rejected(self) -> None:
        mark = _workmark()
        body = {key: value for key, value in mark.items() if key != "workmark_id"}
        body["graph_address"] = "entity:Y"
        wrong = {**body, "workmark_id": sha256_json(body)}
        with self.assertRaises(ContributionFieldInputError) as caught:
            measure_workmark(build_cut(EVENTS, 1, DECLARED), wrong)
        self.assertEqual(caught.exception.reason_code, "WORKMARK_ADDRESS_MISMATCH")

    def test_tampered_measurement_receipt_is_rejected_before_delta(self) -> None:
        mark = _workmark()
        before = measure_workmark(build_cut(EVENTS, 0, DECLARED), mark)
        after = measure_workmark(build_cut(EVENTS, 1, DECLARED), mark)
        tampered_after = {
            **after,
            "measurements": {**after["measurements"], "descendant_count": 99},
        }
        with self.assertRaises(ContributionFieldInputError) as caught:
            compare_measurements(before, tampered_after)
        self.assertEqual(caught.exception.reason_code, "MEASUREMENT_RECEIPT_DIGEST_MISMATCH")


if __name__ == "__main__":
    unittest.main()
