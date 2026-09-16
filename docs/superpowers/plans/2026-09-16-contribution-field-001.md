# CONTRIBUTION-FIELD-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove that one immutable Workmark birth can acquire later typed contribution history that Dogram measures across time-addressed cuts without emitting value, merit, price, authority, human-worth, or causal semantics.

**Architecture:** Add one stdlib-only internal research module, `dogram.contribution_field`, that validates a finite caller-declared contribution vocabulary, lowers typed contribution events into an incidence graph, mints an immutable Workmark birth address, measures the Workmark at a declared cut, compares two neutral receipts, and reuses the existing public `ablate@1` implementation for one structural counterfactual. Freeze the complete synthetic specimen as a Dogram fixture suitable for later read-only consumption by a separately designed Full Measure adapter; no Full Measure runtime code is part of this plan.

**Tech Stack:** Python 3.12 stdlib, existing `dogram.graph.DirectedGraph`, `dogram.canonical.sha256_json`, `dogram.ablate.evaluate_ablate`, `unittest`, existing Dogram CI.

**Spec:** `docs/superpowers/specs/2026-09-16-contribution-field-001-design.md`

## Global Constraints

- No new public Dogram operator or bootstrap-registry entry.
- `GRAPH != ECONOMY`.
- `MEASUREMENT != VALUE`.
- `VALUE != PRICE`.
- `PRICE != HUMAN WORTH`.
- `CONTRIBUTION != HUMAN WORTH`.
- `CENTRALITY != VALUE`.
- `EDGE COUNT != CONTRIBUTION`.
- `DESCENDANT COUNT != MERIT`.
- `LONGEVITY != GOODNESS`.
- `DEPENDENCE != AUTHORITY`.
- `GRAPH PATH != CAUSAL PATH`.
- `GRAPH REACHABILITY != HISTORICAL OCCURRENCE`.
- `STORY != SOURCE`; no Full Measure narration is admitted as source evidence in this plan.
- Later history may enrich the Workmark neighborhood; later history may not rewrite the Workmark birth receipt.
- The contribution relation vocabulary is caller-declared per specimen; this plan does not promote a universal ontology.
- Preserve deterministic, offline, dependency-free Dogram behavior.
- Missing or malformed evidence must fail closed; no inferred contribution edge is created.
- No output field may be named or semantically used as `value`, `merit`, `price`, `score`, `rank`, `deserving`, `trusted`, `importance`, `authority`, or `human_worth`.
- First implementation scope ends at a frozen neutral Dogram handoff fixture. A Full Measure adapter requires its own later owner-local design gate.

---

## File Structure

- Create `dogram/contribution_field.py` — validation, cut construction, immutable Workmark birth, neutral measurement receipts, receipt comparison, and event-node ablation bridge.
- Create `tests/test_contribution_field.py` — unit/hostile contract tests for validation, birth immutability, cut enrichment, typed relation preservation, and neutral output vocabulary.
- Create `tests/fixtures/contribution_field_001.json` — frozen `t0`/`t1` specimen, Workmark, measurement receipts, delta receipt, and structural ablation receipt.
- Create `tests/test_contribution_field_fixture.py` — regenerate the frozen specimen and require exact fixture equality.
- Create `research/CONTRIBUTION-FIELD-001.md` — bounded research receipt, math/graph model, hostile results, Full Measure handoff boundary, and refusals.
- Modify `README.md` — one current-state pointer to the landed research specimen; no promotion to a public operator.

The module uses an **incidence graph** rather than collapsing contribution events directly into entity-to-entity edges:

```text
entity:<source> -> event:<event_id> -> entity:<subject>
```

This preserves parallel typed relations between the same two entities and lets the existing `ablate@1` remove one declared event node without erasing relation kind.

---

### Task 1: Validate typed events and build deterministic contribution cuts

**Files:**
- Create: `dogram/contribution_field.py`
- Create: `tests/test_contribution_field.py`

**Interfaces:**
- Produces constants: `FIELD_SCHEMA`, `WORKMARK_SCHEMA`, `RECEIPT_SCHEMA`, `DELTA_SCHEMA`.
- Produces exception: `ContributionFieldInputError(reason_code: str, residual: str)`.
- Produces: `build_cut(events: list[dict[str, object]], cut: int, declared_relation_kinds: tuple[str, ...]) -> dict[str, object]`.
- Cut result keys: `schema`, `cut`, `declared_relation_kinds`, `events`, `graph`, `field_digest`.
- Event schema is exact for v0: `event_id`, `relation_kind`, `source_ref`, `subject_ref`, `evidence_ref`, `available_from`.

- [ ] **Step 1: Write the failing cut-construction tests.**

Create `tests/test_contribution_field.py` with this initial contract:

```python
from __future__ import annotations

import unittest

from dogram.contribution_field import ContributionFieldInputError, build_cut


DECLARED = ("CREATED", "REPAIRED", "ENABLED", "CHALLENGED", "CARRIED")
EVENTS = [
    {
        "event_id": "e-create-x",
        "relation_kind": "CREATED",
        "source_ref": "A",
        "subject_ref": "X",
        "evidence_ref": "receipt:create-x",
        "available_from": 0,
    },
    {
        "event_id": "e-repair-x",
        "relation_kind": "REPAIRED",
        "source_ref": "B",
        "subject_ref": "X",
        "evidence_ref": "receipt:repair-x",
        "available_from": 1,
    },
    {
        "event_id": "e-enable-y",
        "relation_kind": "ENABLED",
        "source_ref": "X",
        "subject_ref": "Y",
        "evidence_ref": "receipt:enable-y",
        "available_from": 1,
    },
    {
        "event_id": "e-challenge-x",
        "relation_kind": "CHALLENGED",
        "source_ref": "C",
        "subject_ref": "X",
        "evidence_ref": "receipt:challenge-x",
        "available_from": 1,
    },
    {
        "event_id": "e-carry-z",
        "relation_kind": "CARRIED",
        "source_ref": "Y",
        "subject_ref": "Z",
        "evidence_ref": "receipt:carry-z",
        "available_from": 1,
    },
]


class ContributionFieldTests(unittest.TestCase):
    def test_cut_contains_only_events_available_at_or_before_cut(self) -> None:
        t0 = build_cut(EVENTS, 0, DECLARED)
        t1 = build_cut(EVENTS, 1, DECLARED)

        self.assertEqual([event["event_id"] for event in t0["events"]], ["e-create-x"])
        self.assertEqual(
            [event["event_id"] for event in t1["events"]],
            ["e-carry-z", "e-challenge-x", "e-create-x", "e-enable-y", "e-repair-x"],
        )
        self.assertNotEqual(t0["field_digest"], t1["field_digest"])

    def test_cut_uses_event_nodes_to_preserve_typed_parallel_relations(self) -> None:
        events = [
            EVENTS[0],
            {
                "event_id": "e-review-x",
                "relation_kind": "REVIEWED",
                "source_ref": "A",
                "subject_ref": "X",
                "evidence_ref": "receipt:review-x",
                "available_from": 0,
            },
        ]
        cut = build_cut(events, 0, (*DECLARED, "REVIEWED"))
        self.assertIn(["entity:A", "event:e-create-x"], cut["graph"]["edges"])
        self.assertIn(["event:e-create-x", "entity:X"], cut["graph"]["edges"])
        self.assertIn(["entity:A", "event:e-review-x"], cut["graph"]["edges"])
        self.assertIn(["event:e-review-x", "entity:X"], cut["graph"]["edges"])

    def test_undeclared_relation_kind_fails_closed(self) -> None:
        with self.assertRaises(ContributionFieldInputError) as caught:
            build_cut(
                [{**EVENTS[0], "relation_kind": "VALUED_AT_9000"}],
                0,
                DECLARED,
            )
        self.assertEqual(caught.exception.reason_code, "UNDECLARED_RELATION_KIND")

    def test_event_with_extra_semantic_field_is_rejected(self) -> None:
        with self.assertRaises(ContributionFieldInputError) as caught:
            build_cut([{**EVENTS[0], "value": 9000}], 0, DECLARED)
        self.assertEqual(caught.exception.reason_code, "EVENT_SHAPE_MISMATCH")

    def test_bool_is_not_accepted_as_integer_cut(self) -> None:
        with self.assertRaises(ContributionFieldInputError):
            build_cut(EVENTS, True, DECLARED)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused tests and verify RED.**

Run:

```bash
python -m unittest tests.test_contribution_field -v
```

Expected: import failure because `dogram.contribution_field` does not exist.

- [ ] **Step 3: Implement the minimal deterministic cut builder.**

Create `dogram/contribution_field.py` with this core shape:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_json
from .graph import DirectedGraph


FIELD_SCHEMA = "dogram.contribution-field/v0-experimental"
WORKMARK_SCHEMA = "dogram.workmark/v0-experimental"
RECEIPT_SCHEMA = "dogram.contribution-field-receipt/v0-experimental"
DELTA_SCHEMA = "dogram.contribution-field-delta/v0-experimental"
EVENT_KEYS = {
    "event_id",
    "relation_kind",
    "source_ref",
    "subject_ref",
    "evidence_ref",
    "available_from",
}


@dataclass
class ContributionFieldInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def _nonempty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContributionFieldInputError("INVALID_EVENT_FIELD", f"{field} must be a non-empty string")
    return value


def _validate_relation_kinds(kinds: tuple[str, ...]) -> tuple[str, ...]:
    if not kinds or len(kinds) != len(set(kinds)):
        raise ContributionFieldInputError("INVALID_RELATION_VOCABULARY", "declared relation kinds must be non-empty and unique")
    if any(not isinstance(kind, str) or not kind for kind in kinds):
        raise ContributionFieldInputError("INVALID_RELATION_VOCABULARY", "declared relation kinds must be non-empty strings")
    return tuple(sorted(kinds))


def _validate_event(raw: dict[str, object], declared: set[str]) -> dict[str, object]:
    if not isinstance(raw, dict) or set(raw) != EVENT_KEYS:
        raise ContributionFieldInputError("EVENT_SHAPE_MISMATCH", "event must contain exactly the v0 event keys")
    event_id = _nonempty_string(raw["event_id"], "event_id")
    relation_kind = _nonempty_string(raw["relation_kind"], "relation_kind")
    if relation_kind not in declared:
        raise ContributionFieldInputError("UNDECLARED_RELATION_KIND", relation_kind)
    source_ref = _nonempty_string(raw["source_ref"], "source_ref")
    subject_ref = _nonempty_string(raw["subject_ref"], "subject_ref")
    evidence_ref = _nonempty_string(raw["evidence_ref"], "evidence_ref")
    available_from = raw["available_from"]
    if isinstance(available_from, bool) or not isinstance(available_from, int) or available_from < 0:
        raise ContributionFieldInputError("INVALID_AVAILABLE_FROM", "available_from must be a nonnegative integer")
    return {
        "event_id": event_id,
        "relation_kind": relation_kind,
        "source_ref": source_ref,
        "subject_ref": subject_ref,
        "evidence_ref": evidence_ref,
        "available_from": available_from,
    }


def build_cut(
    events: list[dict[str, object]],
    cut: int,
    declared_relation_kinds: tuple[str, ...],
) -> dict[str, object]:
    if isinstance(cut, bool) or not isinstance(cut, int) or cut < 0:
        raise ContributionFieldInputError("INVALID_CUT", "cut must be a nonnegative integer")
    if not isinstance(events, list) or not events:
        raise ContributionFieldInputError("INVALID_EVENTS", "events must be a non-empty list")

    declared = _validate_relation_kinds(declared_relation_kinds)
    normalized = [_validate_event(event, set(declared)) for event in events]
    ids = [event["event_id"] for event in normalized]
    if len(ids) != len(set(ids)):
        raise ContributionFieldInputError("DUPLICATE_EVENT_ID", "event ids must be unique")

    visible = sorted(
        (event for event in normalized if event["available_from"] <= cut),
        key=lambda event: event["event_id"],
    )
    nodes: set[str] = set()
    edges: list[list[str]] = []
    for event in visible:
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
        "events": visible,
        "graph": graph,
    }
    return {**body, "field_digest": sha256_json(body)}
```

The implementation must not inspect or infer semantics from `relation_kind`; it only validates membership in the declared local vocabulary and preserves the string.

- [ ] **Step 4: Run focused and constitutional checks and verify GREEN.**

Run:

```bash
python -m unittest tests.test_contribution_field -v
python -m compileall -q dogram tests scripts
```

Expected: all focused tests pass and compilation succeeds.

- [ ] **Step 5: Commit the cut floor.**

```bash
git add dogram/contribution_field.py tests/test_contribution_field.py
git commit -m "feat: add typed contribution field cuts"
```

---

### Task 2: Mint immutable Workmarks and measure enrichment across cuts

**Files:**
- Modify: `dogram/contribution_field.py`
- Modify: `tests/test_contribution_field.py`

**Interfaces:**
- Produces: `mint_workmark(events: list[dict[str, object]], event_id: str, birth_cut: int, declared_relation_kinds: tuple[str, ...]) -> dict[str, object]`.
- Produces: `measure_workmark(field: dict[str, object], workmark: dict[str, object]) -> dict[str, object]`.
- Workmark exact keys: `schema`, `workmark_id`, `contribution_root`, `birth_cut`, `birth_event_id`, `birth_event_digest`, `graph_address`.
- Measurement receipt exact semantic payload: `descendant_count`, `relation_kind_counts`, `reachable_descendant_set`; no scalar valuation field.

- [ ] **Step 1: Add failing tests for immutable birth and neutral measurements.**

Append to `tests/test_contribution_field.py`:

```python
from dogram.contribution_field import mint_workmark, measure_workmark


def _workmark() -> dict[str, object]:
    return mint_workmark(EVENTS, "e-create-x", 0, DECLARED)


class ContributionWorkmarkTests(unittest.TestCase):
    def test_workmark_birth_is_identical_across_later_cuts(self) -> None:
        mark = _workmark()
        t0 = build_cut(EVENTS, 0, DECLARED)
        t1 = build_cut(EVENTS, 1, DECLARED)

        r0 = measure_workmark(t0, mark)
        r1 = measure_workmark(t1, mark)

        self.assertEqual(r0["workmark"], r1["workmark"])
        self.assertEqual(r0["workmark"]["birth_event_digest"], mark["birth_event_digest"])
        self.assertEqual(r0["measurements"]["descendant_count"], 0)
        self.assertEqual(r1["measurements"]["reachable_descendant_set"], ["Y", "Z"])
        self.assertEqual(r1["measurements"]["descendant_count"], 2)

    def test_relation_counts_preserve_declared_kinds_touching_root_closure(self) -> None:
        receipt = measure_workmark(build_cut(EVENTS, 1, DECLARED), _workmark())
        self.assertEqual(
            receipt["measurements"]["relation_kind_counts"],
            {
                "CARRIED": 1,
                "CHALLENGED": 1,
                "CREATED": 1,
                "ENABLED": 1,
                "REPAIRED": 1,
            },
        )

    def test_rewriting_birth_event_invalidates_workmark(self) -> None:
        mark = _workmark()
        rewritten = [
            ({**event, "evidence_ref": "receipt:rewritten"} if event["event_id"] == "e-create-x" else event)
            for event in EVENTS
        ]
        field = build_cut(rewritten, 1, DECLARED)
        with self.assertRaises(ContributionFieldInputError) as caught:
            measure_workmark(field, mark)
        self.assertEqual(caught.exception.reason_code, "BIRTH_EVENT_DIGEST_MISMATCH")

    def test_measurement_receipt_contains_no_valuation_vocabulary(self) -> None:
        receipt = measure_workmark(build_cut(EVENTS, 1, DECLARED), _workmark())
        forbidden = {"value", "merit", "price", "score", "rank", "human_worth", "authority"}
        self.assertTrue(forbidden.isdisjoint(receipt["measurements"]))
```

- [ ] **Step 2: Run focused tests and verify RED.**

Run:

```bash
python -m unittest tests.test_contribution_field -v
```

Expected: import or attribute failures for `mint_workmark` / `measure_workmark`.

- [ ] **Step 3: Implement immutable Workmark minting and neutral measurement.**

Add these helpers and functions to `dogram/contribution_field.py`:

```python
WORKMARK_KEYS = {
    "schema",
    "workmark_id",
    "contribution_root",
    "birth_cut",
    "birth_event_id",
    "birth_event_digest",
    "graph_address",
}


def _event_by_id(events: list[dict[str, object]], event_id: str) -> dict[str, object]:
    matches = [event for event in events if event["event_id"] == event_id]
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
    birth_digest = sha256_json(birth)
    body = {
        "schema": WORKMARK_SCHEMA,
        "contribution_root": root,
        "birth_cut": birth_cut,
        "birth_event_id": event_id,
        "birth_event_digest": birth_digest,
        "graph_address": f"entity:{root}",
    }
    return {**body, "workmark_id": sha256_json(body)}


def _field_events(field: dict[str, object]) -> list[dict[str, object]]:
    raw = field.get("events")
    if not isinstance(raw, list):
        raise ContributionFieldInputError("INVALID_FIELD", "field events must be a list")
    return raw


def _verify_workmark_birth(field: dict[str, object], workmark: dict[str, object]) -> dict[str, object]:
    if not isinstance(workmark, dict) or set(workmark) != WORKMARK_KEYS:
        raise ContributionFieldInputError("WORKMARK_SHAPE_MISMATCH", "invalid workmark shape")
    event = _event_by_id(_field_events(field), str(workmark["birth_event_id"]))
    if sha256_json(event) != workmark["birth_event_digest"]:
        raise ContributionFieldInputError("BIRTH_EVENT_DIGEST_MISMATCH", "birth event changed")
    if event["subject_ref"] != workmark["contribution_root"]:
        raise ContributionFieldInputError("BIRTH_ROOT_MISMATCH", "birth subject no longer matches workmark root")
    return event


def _forward_entity_descendants(graph: DirectedGraph, root_node: str) -> list[str]:
    descendants: list[str] = []
    for node in graph.nodes:
        if node.startswith("entity:") and node != root_node and graph.reachable(root_node, node):
            descendants.append(node.removeprefix("entity:"))
    return sorted(descendants)


def measure_workmark(field: dict[str, object], workmark: dict[str, object]) -> dict[str, object]:
    _verify_workmark_birth(field, workmark)
    graph = DirectedGraph.from_spec(field["graph"])
    root_node = str(workmark["graph_address"])
    if root_node not in graph.nodes:
        raise ContributionFieldInputError("WORKMARK_ROOT_MISSING", root_node)

    descendants = _forward_entity_descendants(graph, root_node)
    closure = {str(workmark["contribution_root"]), *descendants}
    counts: dict[str, int] = {}
    for event in _field_events(field):
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
        "source_event_ids": [event["event_id"] for event in _field_events(field)],
    }
    return {**body, "receipt_digest": sha256_json(body)}
```

Important implementation note: `_verify_workmark_birth` requires the birth event to remain present at later cuts. A cut before `birth_cut` therefore cannot measure this Workmark and must fail closed.

- [ ] **Step 4: Verify GREEN.**

Run:

```bash
python -m unittest tests.test_contribution_field -v
python -m compileall -q dogram tests scripts
```

Expected: all tests pass.

- [ ] **Step 5: Commit immutable Workmark measurement.**

```bash
git add dogram/contribution_field.py tests/test_contribution_field.py
git commit -m "feat: measure immutable workmark history"
```

---

### Task 3: Compare cuts and reuse `ablate@1` for structural counterfactuals

**Files:**
- Modify: `dogram/contribution_field.py`
- Modify: `tests/test_contribution_field.py`

**Interfaces:**
- Produces: `compare_measurements(before: dict[str, object], after: dict[str, object]) -> dict[str, object]`.
- Produces: `ablate_event(field: dict[str, object], workmark: dict[str, object], event_id: str) -> dict[str, object]`.
- `compare_measurements` reports only exact before/after measurement data and set/count deltas; it does not interpret improvement or decline.
- `ablate_event` delegates reachability calculation to existing `dogram.ablate.evaluate_ablate` by removing `event:<event_id>` from the incidence graph.

- [ ] **Step 1: Add failing comparison and ablation tests.**

Append:

```python
from dogram.contribution_field import ablate_event, compare_measurements


class ContributionDeltaTests(unittest.TestCase):
    def test_compare_measurements_shows_history_delta_without_grading_it(self) -> None:
        mark = _workmark()
        before = measure_workmark(build_cut(EVENTS, 0, DECLARED), mark)
        after = measure_workmark(build_cut(EVENTS, 1, DECLARED), mark)
        delta = compare_measurements(before, after)

        self.assertEqual(delta["descendant_count_delta"], 2)
        self.assertEqual(delta["added_reachable_descendants"], ["Y", "Z"])
        self.assertEqual(delta["removed_reachable_descendants"], [])
        self.assertNotIn("improved", delta)
        self.assertNotIn("value", delta)

    def test_ablating_enable_event_removes_y_and_z_from_root_reachability(self) -> None:
        mark = _workmark()
        field = build_cut(EVENTS, 1, DECLARED)
        receipt = ablate_event(field, mark, "e-enable-y")

        self.assertEqual(receipt["removed_event_id"], "e-enable-y")
        self.assertEqual(receipt["lost_root_entity_reachability"], ["Y", "Z"])
        self.assertEqual(receipt["gained_root_entity_reachability"], [])
        self.assertEqual(receipt["authority"], "none")

    def test_ablating_repair_event_does_not_claim_repair_was_unimportant(self) -> None:
        mark = _workmark()
        field = build_cut(EVENTS, 1, DECLARED)
        receipt = ablate_event(field, mark, "e-repair-x")
        self.assertEqual(receipt["lost_root_entity_reachability"], [])
        self.assertNotIn("importance", receipt)
        self.assertNotIn("merit", receipt)
```

- [ ] **Step 2: Run focused tests and verify RED.**

```bash
python -m unittest tests.test_contribution_field -v
```

Expected: missing `compare_measurements` / `ablate_event`.

- [ ] **Step 3: Implement exact delta and ablation bridge.**

Add import:

```python
from .ablate import evaluate_ablate
```

Then add:

```python
def compare_measurements(
    before: dict[str, object],
    after: dict[str, object],
) -> dict[str, object]:
    if before.get("workmark") != after.get("workmark"):
        raise ContributionFieldInputError("WORKMARK_MISMATCH", "receipts must measure the same immutable workmark")
    b = before.get("measurements")
    a = after.get("measurements")
    if not isinstance(b, dict) or not isinstance(a, dict):
        raise ContributionFieldInputError("INVALID_MEASUREMENT_RECEIPT", "missing measurements")
    b_desc = set(b["reachable_descendant_set"])
    a_desc = set(a["reachable_descendant_set"])
    body = {
        "schema": DELTA_SCHEMA,
        "authority": "none",
        "workmark_id": before["workmark"]["workmark_id"],
        "before_receipt_digest": before["receipt_digest"],
        "after_receipt_digest": after["receipt_digest"],
        "descendant_count_delta": a["descendant_count"] - b["descendant_count"],
        "added_reachable_descendants": sorted(a_desc - b_desc),
        "removed_reachable_descendants": sorted(b_desc - a_desc),
        "relation_kind_counts_before": b["relation_kind_counts"],
        "relation_kind_counts_after": a["relation_kind_counts"],
    }
    return {**body, "delta_digest": sha256_json(body)}


def ablate_event(
    field: dict[str, object],
    workmark: dict[str, object],
    event_id: str,
) -> dict[str, object]:
    _verify_workmark_birth(field, workmark)
    events = _field_events(field)
    event = _event_by_id(events, event_id)
    root = str(workmark["graph_address"])
    graph = DirectedGraph.from_spec(field["graph"])
    event_node = f"event:{event_id}"
    if event_node not in graph.nodes:
        raise ContributionFieldInputError("EVENT_NOT_IN_CUT", event_id)

    entity_targets = [node for node in graph.nodes if node.startswith("entity:") and node != root]
    result, _ = evaluate_ablate(
        {
            "graph": graph.to_spec(),
            "target": {"kind": "node", "node": event_node},
            "requested_targets": [[root, target] for target in entity_targets],
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
        "schema": "dogram.contribution-field-ablation/v0-experimental",
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
```

The `e-repair-x` control is essential: zero forward reachability loss is **not** interpreted as zero contribution. This is an explicit executable guard against turning one graph measure into an economic conclusion.

- [ ] **Step 4: Verify GREEN and run the full unit suite.**

```bash
python -m unittest tests.test_contribution_field -v
python -m unittest discover -s tests -v
```

Expected: focused and existing suites pass.

- [ ] **Step 5: Commit the delta/ablation slice.**

```bash
git add dogram/contribution_field.py tests/test_contribution_field.py
git commit -m "feat: receipt contribution field deltas"
```

---

### Task 4: Freeze the first falsifiable specimen and hostile controls

**Files:**
- Create: `tests/fixtures/contribution_field_001.json`
- Create: `tests/test_contribution_field_fixture.py`
- Modify: `tests/test_contribution_field.py`

**Interfaces:**
- Produces frozen specimen sections: `workmark`, `t0`, `t1`, `delta`, `ablation_enable_y`, `ablation_repair_x`, `full_measure_handoff_fixture`.
- `full_measure_handoff_fixture` is neutral data only; it contains no narrative, quest, Deed, Harvest, reward, reputation, or valuation output.

- [ ] **Step 1: Add the fixture-regeneration test before creating the fixture.**

Create `tests/test_contribution_field_fixture.py`:

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

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
    mark = mint_workmark(EVENTS, "e-create-x", 0, DECLARED)
    t0_field = build_cut(EVENTS, 0, DECLARED)
    t1_field = build_cut(EVENTS, 1, DECLARED)
    t0 = measure_workmark(t0_field, mark)
    t1 = measure_workmark(t1_field, mark)
    delta = compare_measurements(t0, t1)
    enable_ablation = ablate_event(t1_field, mark, "e-enable-y")
    repair_ablation = ablate_event(t1_field, mark, "e-repair-x")
    return {
        "workmark": mark,
        "t0": t0,
        "t1": t1,
        "delta": delta,
        "ablation_enable_y": enable_ablation,
        "ablation_repair_x": repair_ablation,
        "full_measure_handoff_fixture": {
            "source": "Dogram",
            "authority": "none",
            "workmark_id": mark["workmark_id"],
            "measurement_receipt_digest": t1["receipt_digest"],
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
    def test_frozen_specimen_matches_exactly(self) -> None:
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(build_frozen_specimen(), expected)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run fixture test and verify RED because the fixture is absent.**

```bash
python -m unittest tests.test_contribution_field_fixture -v
```

Expected: `FileNotFoundError` for `tests/fixtures/contribution_field_001.json`.

- [ ] **Step 3: Generate and commit the exact JSON fixture from the implementation.**

Use this one-shot command from the repository root:

```bash
python - <<'PY'
import json
from pathlib import Path
from tests.test_contribution_field_fixture import build_frozen_specimen

path = Path("tests/fixtures/contribution_field_001.json")
path.write_text(json.dumps(build_frozen_specimen(), indent=2, sort_keys=True) + "\n")
print(path)
PY
```

Then run:

```bash
python -m unittest tests.test_contribution_field_fixture -v
```

Expected: PASS.

- [ ] **Step 4: Add hostile tests for relation-kind collapse and person-score pressure.**

Append to `tests/test_contribution_field.py`:

```python
from dogram.anti_collapse_reachability import analyze_collapse


class ContributionHostileBoundaryTests(unittest.TestCase):
    def test_collapsing_relation_kind_to_endpoint_pair_loses_declared_distinction(self) -> None:
        states = ("created:A->X", "reviewed:A->X", "enabled:X->Y")
        rich = (("A", "X", "CREATED"), ("A", "X", "REVIEWED"), ("X", "Y", "ENABLED"))
        collapsed = (("A", "X"), ("A", "X"), ("X", "Y"))
        receipt = analyze_collapse(states, rich, collapsed)
        self.assertTrue(receipt.lawful_quotient)
        self.assertEqual(receipt.lost_distinctions, (("created:A->X", "reviewed:A->X"),))

    def test_module_exposes_no_person_score_operator(self) -> None:
        import dogram.contribution_field as module

        forbidden_exports = {
            "score_person",
            "rank_people",
            "calculate_value",
            "price_contribution",
            "award_reputation",
        }
        self.assertTrue(forbidden_exports.isdisjoint(set(dir(module))))
```

This explicitly composes the already-landed anti-collapse instrument instead of reimplementing it inside `contribution_field.py`.

- [ ] **Step 5: Run the complete test/compile/constitutional floor locally.**

Run:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests scripts
python - <<'PY'
import pathlib
import tomllib
from dogram.engine import OPERATORS
from dogram.registry import build_bootstrap_registry

pyproject = tomllib.loads(pathlib.Path("pyproject.toml").read_text())
assert pyproject["project"]["dependencies"] == []
assert set(OPERATORS) == {
    ("delta", 1),
    ("rectangle", 1),
    ("ablate", 1),
    ("reach", 1),
}
assert set(build_bootstrap_registry().ids()) == {
    "core.get@1",
    "core.same@1",
    "core.add@1",
    "core.sub@1",
    "core.length@1",
    "core.gt@1",
    "core.select_first@1",
    "trace.compare_ordered@1",
    "graph.apply_mutation@1",
    "graph.reachable_pairs@1",
    "graph.query_paths@1",
    "set.difference@1",
}
print("constitutional floor OK")
PY
```

Expected: all tests and checks pass with the public operator/registry sets unchanged.

- [ ] **Step 6: Commit frozen specimen and hostile controls.**

```bash
git add tests/test_contribution_field.py tests/test_contribution_field_fixture.py tests/fixtures/contribution_field_001.json
git commit -m "test: freeze contribution field specimen"
```

---

### Task 5: Receipt the research boundary and expose the future seam

**Files:**
- Create: `research/CONTRIBUTION-FIELD-001.md`
- Modify: `README.md`

**Interfaces:**
- Research document must name the exact frozen fixture, exact module/tests, the four first measurements, the neutral Full Measure handoff fixture, and all non-authority boundaries.
- README gets one bounded paragraph beside the current lineage/anti-collapse research entries.

- [ ] **Step 1: Write the research receipt with exact landed behavior.**

Create `research/CONTRIBUTION-FIELD-001.md` with these required sections and content:

```markdown
# CONTRIBUTION-FIELD-001

**Status:** bounded internal research specimen  
**Authority:** none  
**Public operator:** none

## Question
Can one immutable contribution birth acquire later typed graph history that Dogram measures without pricing, ranking, or narratively promoting the contributor?

## Frozen history
`A CREATED X` is visible at `t0`. At `t1`, `B REPAIRED X`, `X ENABLED Y`, `C CHALLENGED X`, and `Y CARRIED Z` become available. The Workmark remains anchored to the exact digest of `e-create-x`.

## Representation
Each typed event is reified as an incidence node:
`entity:<source> -> event:<event_id> -> entity:<subject>`.
This preserves relation kind and parallel relations instead of silently collapsing them into one endpoint pair.

## Measurements
The first specimen receipts only:
- descendant count;
- relation-kind counts touching the root/forward-descendant closure;
- reachable descendant set;
- event-node ablation reachability delta.

## Hostile controls
- rewritten birth evidence is invalid;
- undeclared relation kinds fail closed;
- extra semantic event fields fail closed;
- relation-kind collapse is exposed by `ANTI-COLLAPSE-REACHABILITY-001`;
- an ablated repair edge with zero forward-reachability loss is not called unimportant;
- no person-score/value/rank operator exists.

## Full Measure handoff
The frozen fixture contains a neutral read-only handoff envelope referencing exact Dogram receipt digests. It is not executable Full Measure integration and grants no story, witness, sheet-changing, or economic authority. A Full Measure adapter is a separate owner-local future gate.

## Boundaries
`GRAPH != ECONOMY`  
`MEASUREMENT != VALUE`  
`DESCENDANT COUNT != MERIT`  
`ABLATION DELTA != ECONOMIC ENTITLEMENT`  
`GRAPH REACHABILITY != HISTORICAL OCCURRENCE`  
`STORY != SOURCE`

## Working seal
> **THE GRAPH PRESERVES CONTRIBUTION HISTORY. IT DOES NOT PRICE THE CONTRIBUTOR.**

> **WORK MINES THE MARKER. TIME ASSAYS THE ORE.**

> **DOGRAM MEASURES THE FIELD. FULL MEASURE TELLS THE PLAYABLE STORY.**
```

Add exact generated hashes/counts from `tests/fixtures/contribution_field_001.json` only after the fixture exists; copy them verbatim rather than recomputing by hand.

- [ ] **Step 2: Add one README current-state paragraph.**

Immediately after the `ANTI-COLLAPSE-REACHABILITY-001` paragraph, add a paragraph with this semantic content:

```markdown
`CONTRIBUTION-FIELD-001` is a bounded internal contribution-history specimen. It preserves one immutable Workmark birth across two time-addressed typed incidence-graph cuts, receipts neutral descendant/relation measurements and one event-node ablation delta, and freezes a read-only handoff fixture for a later Full Measure story adapter. It adds no public operator, person score, economic valuation, causal semantics, story authority, or Full Measure runtime integration. See `research/CONTRIBUTION-FIELD-001.md`.
```

- [ ] **Step 3: Run final CI-equivalent verification.**

Run exactly:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests scripts
python - <<'PY'
from pathlib import Path

forbidden = ["eval(", "exec(", "importlib", "subprocess", "socket.", "requests."]
for path in Path("dogram").rglob("*.py"):
    text = path.read_text()
    for token in forbidden:
        assert token not in text, (path, token)
print("scope scan OK")
PY
```

Also inspect `git diff main...HEAD --stat` and `git diff main...HEAD -- dogram/contribution_field.py tests/test_contribution_field.py tests/test_contribution_field_fixture.py research/CONTRIBUTION-FIELD-001.md README.md` to verify no unrelated surface entered the change.

- [ ] **Step 4: Commit the research/documentation receipt.**

```bash
git add research/CONTRIBUTION-FIELD-001.md README.md
git commit -m "research: receipt CONTRIBUTION-FIELD-001"
```

- [ ] **Step 5: Final acceptance checks.**

Acceptance requires all of the following:

```text
same Workmark birth at t0 and t1
later field digest differs
reachable descendants: [] -> [Y, Z]
typed relation counts retained
rewritten birth rejected
undeclared relation rejected
relation-kind collapse visibly loses a distinction
enable-event ablation loses Y and Z reachability
repair-event ablation may lose zero forward reachability without semantic judgment
fixture regenerates byte-for-semantic-object exactly
public Dogram operator set unchanged
bootstrap registry unchanged
Full Measure handoff remains inert/read-only data
no value/merit/price/rank/human-worth output
```

If any acceptance item fails, do not widen the design to make the test pass; stop at the failing boundary and report the mismatch against the approved spec.

---

## Self-Review Map

- Immutable Workmark birth: Tasks 2 and 4.
- Time-addressed graph enrichment: Tasks 1, 2, and 4.
- Typed relation preservation: incidence graph in Task 1; anti-collapse hostile control in Task 4.
- Neutral measurement vector: Task 2.
- Delta across cuts: Task 3.
- Counterfactual reachability only: Task 3.
- No economic/person-score semantics: Global Constraints plus Tasks 2–5 tests/docs.
- Frozen neutral Full Measure handoff, no adapter code: Task 4 fixture and Task 5 documentation.
- Dependency/public-operator floors unchanged: Tasks 4–5 verification.
- Creative/economic horizons beyond this specimen: intentionally remain in the approved design spec, not implementation scope.

## Execution Boundary

This plan implements only the Dogram first proof. After it lands and survives hostile review, the next architectural gate is a separate **Full Measure contribution-story adapter** design that consumes the frozen neutral handoff fixture without gaining authority to manufacture graph history.