from __future__ import annotations

import unittest

from dogram.contribution_field import ContributionFieldInputError, build_cut


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


if __name__ == "__main__":
    unittest.main()
