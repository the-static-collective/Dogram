from __future__ import annotations

from dataclasses import dataclass

from .ablate import evaluate_ablate
from .canonical import sha256_json
from .graph import DirectedGraph

FIELD_SCHEMA = "dogram.contribution-field/v0-experimental"
WORKMARK_SCHEMA = "dogram.workmark/v0-experimental"
RECEIPT_SCHEMA = "dogram.contribution-field-receipt/v0-experimental"
DELTA_SCHEMA = "dogram.contribution-field-delta/v0-experimental"
ABLATION_SCHEMA = "dogram.contribution-field-ablation/v0-experimental"
EVENT_KEYS = {"event_id", "relation_kind", "source_ref", "subject_ref", "evidence_ref", "evidence_status", "available_from"}
EVIDENCE_STATUSES = {"complete", "incomplete", "invalid"}
WORKMARK_KEYS = {
    "schema",
    "workmark_id",
    "contribution_root",
    "birth_cut",
    "birth_event_id",
    "birth_event_digest",
    "graph_address",
}


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


def _event_by_id(events: list[dict[str, object]], event_id: str) -> dict[str, object]:
    matches = [event for event in events if event.get("event_id") == event_id]
    if len(matches) != 1:
        raise ContributionFieldInputError("BIRTH_EVENT_NOT_UNIQUE", event_id)
    return matches[0]


def mint_workmark(
    events: list[dict[str, object]],
    event_id: str,
    birth_cut: int,
    declared_relation_kinds: tuple[str, ...],
) -> dict[str, object]:
    field = build_cut(events, birth_cut, declared_relation_kinds)
    birth = _event_by_id(field["events"], event_id)
    root = str(birth["subject_ref"])
    body = {
        "schema": WORKMARK_SCHEMA,
        "contribution_root": root,
        "birth_cut": birth_cut,
        "birth_event_id": event_id,
        "birth_event_digest": sha256_json(birth),
        "graph_address": f"entity:{root}",
    }
    return {**body, "workmark_id": sha256_json(body)}


def _verify_workmark_birth(field: dict[str, object], workmark: dict[str, object]) -> None:
    if not isinstance(workmark, dict) or set(workmark) != WORKMARK_KEYS:
        raise ContributionFieldInputError("WORKMARK_SHAPE_MISMATCH", "invalid workmark shape")
    events = field.get("events")
    if not isinstance(events, list):
        raise ContributionFieldInputError("INVALID_FIELD", "events missing")
    birth = _event_by_id(events, str(workmark["birth_event_id"]))
    if sha256_json(birth) != workmark["birth_event_digest"]:
        raise ContributionFieldInputError("BIRTH_EVENT_DIGEST_MISMATCH", "birth event changed")
    if birth["subject_ref"] != workmark["contribution_root"]:
        raise ContributionFieldInputError("BIRTH_ROOT_MISMATCH", "birth root changed")


def measure_workmark(field: dict[str, object], workmark: dict[str, object]) -> dict[str, object]:
    _verify_workmark_birth(field, workmark)
    graph = DirectedGraph.from_spec(field["graph"])
    root_node = str(workmark["graph_address"])
    descendants = sorted(
        node.removeprefix("entity:")
        for node in graph.nodes
        if node.startswith("entity:")
        and node != root_node
        and graph.reachable(root_node, node)
    )
    closure = {str(workmark["contribution_root"]), *descendants}
    counts: dict[str, int] = {}
    for event in field["events"]:
        if event["source_ref"] in closure or event["subject_ref"] in closure:
            kind = str(event["relation_kind"])
            counts[kind] = counts.get(kind, 0) + 1
    measurements = {
        "descendant_count": len(descendants),
        "relation_kind_counts": {key: counts[key] for key in sorted(counts)},
        "reachable_descendant_set": descendants,
    }
    body = {
        "schema": RECEIPT_SCHEMA,
        "authority": "none",
        "workmark": workmark,
        "cut": field["cut"],
        "field_digest": field["field_digest"],
        "measurement_version": "CONTRIBUTION-FIELD-001/v0",
        "measurements": measurements,
        "incomplete_events": field["incomplete_events"],
        "invalid_events": field["invalid_events"],
        "source_event_ids": [event["event_id"] for event in field["events"]],
    }
    return {**body, "receipt_digest": sha256_json(body)}


def compare_measurements(
    before: dict[str, object],
    after: dict[str, object],
) -> dict[str, object]:
    before_mark = before.get("workmark")
    after_mark = after.get("workmark")
    if not isinstance(before_mark, dict) or not isinstance(after_mark, dict):
        raise ContributionFieldInputError("INVALID_MEASUREMENT_RECEIPT", "workmark missing")
    if before_mark.get("workmark_id") != after_mark.get("workmark_id"):
        raise ContributionFieldInputError("WORKMARK_MISMATCH", "measurement receipts address different workmarks")

    before_measurements = before.get("measurements")
    after_measurements = after.get("measurements")
    if not isinstance(before_measurements, dict) or not isinstance(after_measurements, dict):
        raise ContributionFieldInputError("INVALID_MEASUREMENT_RECEIPT", "measurements missing")

    before_descendants = set(before_measurements.get("reachable_descendant_set", []))
    after_descendants = set(after_measurements.get("reachable_descendant_set", []))
    body = {
        "schema": DELTA_SCHEMA,
        "authority": "none",
        "workmark_id": before_mark["workmark_id"],
        "before_receipt_digest": before.get("receipt_digest"),
        "after_receipt_digest": after.get("receipt_digest"),
        "descendant_count_delta": int(after_measurements["descendant_count"]) - int(before_measurements["descendant_count"]),
        "added_reachable_descendants": sorted(after_descendants - before_descendants),
        "removed_reachable_descendants": sorted(before_descendants - after_descendants),
        "relation_kind_counts_before": before_measurements["relation_kind_counts"],
        "relation_kind_counts_after": after_measurements["relation_kind_counts"],
        "incomplete_events_before": before.get("incomplete_events", []),
        "incomplete_events_after": after.get("incomplete_events", []),
        "invalid_events_before": before.get("invalid_events", []),
        "invalid_events_after": after.get("invalid_events", []),
    }
    return {**body, "delta_digest": sha256_json(body)}


def ablate_event(
    field: dict[str, object],
    workmark: dict[str, object],
    event_id: str,
) -> dict[str, object]:
    _verify_workmark_birth(field, workmark)
    events = field.get("events")
    if not isinstance(events, list):
        raise ContributionFieldInputError("INVALID_FIELD", "events missing")
    matches = [event for event in events if event.get("event_id") == event_id]
    if len(matches) != 1:
        raise ContributionFieldInputError("ABLATION_EVENT_NOT_UNIQUE", event_id)
    event = matches[0]

    graph = DirectedGraph.from_spec(field["graph"])
    root = str(workmark["graph_address"])
    event_node = f"event:{event_id}"
    targets = sorted(
        node
        for node in graph.nodes
        if node.startswith("entity:") and node != root
    )
    result, _ = evaluate_ablate(
        {
            "graph": graph.to_spec(),
            "target": {"kind": "node", "node": event_node},
            "requested_targets": [[root, target] for target in targets],
        }
    )
    reports = result["requested_targets"]
    lost = sorted(
        report["target"].removeprefix("entity:")
        for report in reports
        if report["reachable_before"] and not report["reachable_after"]
    )
    gained = sorted(
        report["target"].removeprefix("entity:")
        for report in reports
        if not report["reachable_before"] and report["reachable_after"]
    )
    body = {
        "schema": ABLATION_SCHEMA,
        "authority": "none",
        "workmark_id": workmark["workmark_id"],
        "field_digest": field["field_digest"],
        "removed_event_id": event_id,
        "removed_relation_kind": event["relation_kind"],
        "lost_root_entity_reachability": lost,
        "gained_root_entity_reachability": gained,
        "ablate_receipt": result,
    }
    return {**body, "receipt_digest": sha256_json(body)}


__all__ = [
    "ABLATION_SCHEMA",
    "ContributionFieldInputError",
    "DELTA_SCHEMA",
    "FIELD_SCHEMA",
    "RECEIPT_SCHEMA",
    "WORKMARK_SCHEMA",
    "ablate_event",
    "build_cut",
    "compare_measurements",
    "measure_workmark",
    "mint_workmark",
]
