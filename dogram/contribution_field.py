from __future__ import annotations

from dataclasses import dataclass

from .canonical import sha256_json
from .graph import DirectedGraph

FIELD_SCHEMA = "dogram.contribution-field/v0-experimental"
WORKMARK_SCHEMA = "dogram.workmark/v0-experimental"
RECEIPT_SCHEMA = "dogram.contribution-field-receipt/v0-experimental"
DELTA_SCHEMA = "dogram.contribution-field-delta/v0-experimental"
EVENT_KEYS = {"event_id", "relation_kind", "source_ref", "subject_ref", "evidence_ref", "evidence_status", "available_from"}
EVIDENCE_STATUSES = {"complete", "incomplete", "invalid"}


@dataclass
class ContributionFieldInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def _string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContributionFieldInputError("INVALID_EVENT_FIELD", f"{name} must be a non-empty string")
    return value


def _normalize_event(raw: dict[str, object], declared: set[str]) -> dict[str, object]:
    if not isinstance(raw, dict) or set(raw) != EVENT_KEYS:
        raise ContributionFieldInputError("EVENT_SHAPE_MISMATCH", "event must contain exactly the v0 keys")
    event = {name: raw[name] for name in EVENT_KEYS}
    for name in ("event_id", "relation_kind", "source_ref", "subject_ref", "evidence_ref", "evidence_status"):
        event[name] = _string(event[name], name)
    if event["relation_kind"] not in declared:
        raise ContributionFieldInputError("UNDECLARED_RELATION_KIND", str(event["relation_kind"]))
    if event["evidence_status"] not in EVIDENCE_STATUSES:
        raise ContributionFieldInputError("INVALID_EVIDENCE_STATUS", str(event["evidence_status"]))
    available = event["available_from"]
    if isinstance(available, bool) or not isinstance(available, int) or available < 0:
        raise ContributionFieldInputError("INVALID_AVAILABLE_FROM", "available_from must be a nonnegative integer")
    return event


def build_cut(
    events: list[dict[str, object]],
    cut: int,
    declared_relation_kinds: tuple[str, ...],
) -> dict[str, object]:
    if isinstance(cut, bool) or not isinstance(cut, int) or cut < 0:
        raise ContributionFieldInputError("INVALID_CUT", "cut must be a nonnegative integer")
    if not isinstance(events, list) or not events:
        raise ContributionFieldInputError("INVALID_EVENTS", "events must be a non-empty list")
    if (
        not declared_relation_kinds
        or len(declared_relation_kinds) != len(set(declared_relation_kinds))
        or any(not isinstance(kind, str) or not kind for kind in declared_relation_kinds)
    ):
        raise ContributionFieldInputError(
            "INVALID_RELATION_VOCABULARY",
            "relation vocabulary must be non-empty unique strings",
        )

    declared = tuple(sorted(declared_relation_kinds))
    normalized = [_normalize_event(event, set(declared)) for event in events]
    ids = [str(event["event_id"]) for event in normalized]
    if len(ids) != len(set(ids)):
        raise ContributionFieldInputError("DUPLICATE_EVENT_ID", "event ids must be unique")

    visible = [event for event in normalized if event["available_from"] <= cut]
    complete = sorted(
        (event for event in visible if event["evidence_status"] == "complete"),
        key=lambda event: str(event["event_id"]),
    )
    incomplete = sorted(
        str(event["event_id"])
        for event in visible
        if event["evidence_status"] == "incomplete"
    )
    invalid = sorted(
        str(event["event_id"])
        for event in visible
        if event["evidence_status"] == "invalid"
    )

    nodes: set[str] = set()
    edges: list[list[str]] = []
    for event in complete:
        source = f"entity:{event['source_ref']}"
        event_node = f"event:{event['event_id']}"
        subject = f"entity:{event['subject_ref']}"
        nodes.update((source, event_node, subject))
        edges.extend(([source, event_node], [event_node, subject]))

    graph = DirectedGraph.from_spec({"nodes": sorted(nodes), "edges": edges}).to_spec()
    body = {
        "schema": FIELD_SCHEMA,
        "cut": cut,
        "declared_relation_kinds": list(declared),
        "events": complete,
        "incomplete_events": incomplete,
        "invalid_events": invalid,
        "graph": graph,
    }
    return {**body, "field_digest": sha256_json(body)}


__all__ = [
    "ContributionFieldInputError",
    "DELTA_SCHEMA",
    "FIELD_SCHEMA",
    "RECEIPT_SCHEMA",
    "WORKMARK_SCHEMA",
    "build_cut",
]
