# CONTRIBUTION-FIELD-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove that one immutable Workmark birth can acquire later typed contribution history that Dogram measures across time-addressed cuts without emitting value, merit, price, authority, human-worth, or causal semantics.

**Architecture:** Add one stdlib-only internal research module, `dogram.contribution_field`, that consumes caller-declared event/evidence status, lowers only complete events into a typed incidence graph, preserves incomplete/invalid source status in receipts, mints an immutable Workmark birth address, measures two cuts, compares them, and reuses existing `ablate@1` for one structural counterfactual. Freeze a neutral Dogram handoff fixture for a later separately designed Full Measure adapter; no Full Measure runtime code is part of this plan.

**Tech Stack:** Python 3.12 stdlib, `dogram.graph.DirectedGraph`, `dogram.canonical.sha256_json`, `dogram.ablate.evaluate_ablate`, `dogram.anti_collapse_reachability.analyze_collapse`, `unittest`, existing Dogram CI.

**Spec:** `docs/superpowers/specs/2026-09-16-contribution-field-001-design.md`

## Global Constraints

- No new public Dogram operator or bootstrap-registry entry.
- `GRAPH != ECONOMY`; `MEASUREMENT != VALUE`; `VALUE != PRICE`; `PRICE != HUMAN WORTH`.
- `CONTRIBUTION != HUMAN WORTH`; `CENTRALITY != VALUE`; `EDGE COUNT != CONTRIBUTION`; `DESCENDANT COUNT != MERIT`.
- `LONGEVITY != GOODNESS`; `DEPENDENCE != AUTHORITY`; `GRAPH PATH != CAUSAL PATH`; `GRAPH REACHABILITY != HISTORICAL OCCURRENCE`.
- `STORY != SOURCE`; Full Measure narration cannot enter the graph as evidence by narration alone.
- Later history may enrich the Workmark neighborhood; later history may not rewrite the Workmark birth receipt.
- Relation vocabulary is caller-declared per specimen; no universal ontology is introduced.
- Evidence status is supplied by the owning source as one of `complete`, `incomplete`, or `invalid`; Dogram preserves that status and does not promote it.
- Only `complete` events enter the incidence graph. `incomplete` and `invalid` events remain explicit receipt residue.
- Preserve deterministic, offline, dependency-free Dogram behavior.
- No output field may be named or used as `value`, `merit`, `price`, `score`, `rank`, `deserving`, `trusted`, `importance`, `authority`, or `human_worth` except the literal boundary field `authority: "none"`.
- Scope ends at a frozen neutral Dogram handoff fixture. Full Measure adapter implementation is a later owner-local design gate.

---

## File Structure

- Create `dogram/contribution_field.py` — event validation, time cut, incidence graph, Workmark, measurements, delta, event ablation.
- Create `tests/test_contribution_field.py` — unit and hostile contract tests.
- Create `tests/fixtures/contribution_field_001.json` — frozen `t0`/`t1`, Workmark, measurement, delta, ablation, neutral handoff.
- Create `tests/test_contribution_field_fixture.py` — exact fixture regeneration.
- Create `research/CONTRIBUTION-FIELD-001.md` — bounded research receipt and refusals.
- Modify `README.md` — one current-state research pointer.

Graph lowering uses event nodes:

```text
entity:<source> -> event:<event_id> -> entity:<subject>
```

This preserves parallel relation kinds and lets `ablate@1` remove one declared event rather than an ambiguous endpoint pair.

---

### Task 1: Typed evidence events and deterministic cuts

**Files:**
- Create: `dogram/contribution_field.py`
- Create: `tests/test_contribution_field.py`

**Interfaces:**
- `ContributionFieldInputError(reason_code: str, residual: str)`.
- `build_cut(events: list[dict[str, object]], cut: int, declared_relation_kinds: tuple[str, ...]) -> dict[str, object]`.
- Exact event keys: `event_id`, `relation_kind`, `source_ref`, `subject_ref`, `evidence_ref`, `evidence_status`, `available_from`.
- Exact allowed `evidence_status`: `complete`, `incomplete`, `invalid`.
- Cut keys: `schema`, `cut`, `declared_relation_kinds`, `events`, `incomplete_events`, `invalid_events`, `graph`, `field_digest`.

- [ ] **Step 1: Write failing tests.**

Create `tests/test_contribution_field.py`:

```python
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
```

- [ ] **Step 2: Run and confirm RED.**

```bash
python -m unittest tests.test_contribution_field -v
```

Expected: import failure for `dogram.contribution_field`.

- [ ] **Step 3: Implement the cut floor.**

Create `dogram/contribution_field.py` with these exact constants/helpers and equivalent validation logic:

```python
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

def build_cut(events: list[dict[str, object]], cut: int, declared_relation_kinds: tuple[str, ...]) -> dict[str, object]:
    if isinstance(cut, bool) or not isinstance(cut, int) or cut < 0:
        raise ContributionFieldInputError("INVALID_CUT", "cut must be a nonnegative integer")
    if not isinstance(events, list) or not events:
        raise ContributionFieldInputError("INVALID_EVENTS", "events must be a non-empty list")
    if not declared_relation_kinds or len(declared_relation_kinds) != len(set(declared_relation_kinds)) or any(not isinstance(k, str) or not k for k in declared_relation_kinds):
        raise ContributionFieldInputError("INVALID_RELATION_VOCABULARY", "relation vocabulary must be non-empty unique strings")
    declared = tuple(sorted(declared_relation_kinds))
    normalized = [_normalize_event(event, set(declared)) for event in events]
    ids = [str(event["event_id"]) for event in normalized]
    if len(ids) != len(set(ids)):
        raise ContributionFieldInputError("DUPLICATE_EVENT_ID", "event ids must be unique")
    visible = [event for event in normalized if event["available_from"] <= cut]
    complete = sorted((event for event in visible if event["evidence_status"] == "complete"), key=lambda event: str(event["event_id"]))
    incomplete = sorted(str(event["event_id"]) for event in visible if event["evidence_status"] == "incomplete")
    invalid = sorted(str(event["event_id"]) for event in visible if event["evidence_status"] == "invalid")
    nodes: set[str] = set()
    edges: list[list[str]] = []
    for event in complete:
        source = f"entity:{event['source_ref']}"
        event_node = f"event:{event['event_id']}"
        subject = f"entity:{event['subject_ref']}"
        nodes.update((source, event_node, subject))
        edges.extend(([source, event_node], [event_node, subject]))
    graph = DirectedGraph.from_spec({"nodes": sorted(nodes), "edges": edges}).to_spec()
    body = {"schema": FIELD_SCHEMA, "cut": cut, "declared_relation_kinds": list(declared), "events": complete, "incomplete_events": incomplete, "invalid_events": invalid, "graph": graph}
    return {**body, "field_digest": sha256_json(body)}
```

Dogram does not verify whether the upstream `evidence_status` is truthful. It preserves the owning source's supplied status and refuses to silently upgrade `incomplete`/`invalid` into a graph edge.

- [ ] **Step 4: Verify GREEN.**

```bash
python -m unittest tests.test_contribution_field -v
python -m compileall -q dogram tests scripts
```

- [ ] **Step 5: Commit.**

```bash
git add dogram/contribution_field.py tests/test_contribution_field.py
git commit -m "feat: add typed contribution field cuts"
```

---

### Task 2: Immutable Workmark and neutral measurements

**Files:**
- Modify: `dogram/contribution_field.py`
- Modify: `tests/test_contribution_field.py`

**Interfaces:**
- `mint_workmark(events, event_id, birth_cut, declared_relation_kinds) -> dict[str, object]`.
- `measure_workmark(field, workmark) -> dict[str, object]`.
- Workmark keys: `schema`, `workmark_id`, `contribution_root`, `birth_cut`, `birth_event_id`, `birth_event_digest`, `graph_address`.
- Measurement keys: `descendant_count`, `relation_kind_counts`, `reachable_descendant_set`.
- Measurement receipt additionally preserves `incomplete_events` and `invalid_events` copied from the cut.

- [ ] **Step 1: Add failing tests.**

Append:

```python
from dogram.contribution_field import mint_workmark, measure_workmark

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
        self.assertEqual(receipt["measurements"]["relation_kind_counts"], {"CARRIED": 1, "CHALLENGED": 1, "CREATED": 1, "ENABLED": 1, "REPAIRED": 1})

    def test_rewritten_birth_is_invalid(self) -> None:
        mark = _workmark()
        rewritten = [({**event, "evidence_ref": "receipt:rewritten"} if event["event_id"] == "e-create-x" else event) for event in EVENTS]
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
```

- [ ] **Step 2: Verify RED.**

```bash
python -m unittest tests.test_contribution_field -v
```

- [ ] **Step 3: Implement Workmark and measurement.**

Add to `dogram/contribution_field.py`:

```python
WORKMARK_KEYS = {"schema", "workmark_id", "contribution_root", "birth_cut", "birth_event_id", "birth_event_digest", "graph_address"}

def _event_by_id(events: list[dict[str, object]], event_id: str) -> dict[str, object]:
    matches = [event for event in events if event["event_id"] == event_id]
    if len(matches) != 1:
        raise ContributionFieldInputError("BIRTH_EVENT_NOT_UNIQUE", event_id)
    return matches[0]

def mint_workmark(events: list[dict[str, object]], event_id: str, birth_cut: int, declared_relation_kinds: tuple[str, ...]) -> dict[str, object]:
    field = build_cut(events, birth_cut, declared_relation_kinds)
    birth = _event_by_id(field["events"], event_id)
    root = str(birth["subject_ref"])
    body = {"schema": WORKMARK_SCHEMA, "contribution_root": root, "birth_cut": birth_cut, "birth_event_id": event_id, "birth_event_digest": sha256_json(birth), "graph_address": f"entity:{root}"}
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
    descendants = sorted(node.removeprefix("entity:") for node in graph.nodes if node.startswith("entity:") and node != root_node and graph.reachable(root_node, node))
    closure = {str(workmark["contribution_root"]), *descendants}
    counts: dict[str, int] = {}
    for event in field["events"]:
        if event["source_ref"] in closure or event["subject_ref"] in closure:
            kind = str(event["relation_kind"])
            counts[kind] = counts.get(kind, 0) + 1
    measurements = {"descendant_count": len(descendants), "relation_kind_counts": {key: counts[key] for key in sorted(counts)}, "reachable_descendant_set": descendants}
    body = {"schema": RECEIPT_SCHEMA, "authority": "none", "workmark": workmark, "cut": field["cut"], "field_digest": field["field_digest"], "measurement_version": "CONTRIBUTION-FIELD-001/v0", "measurements": measurements, "incomplete_events": field["incomplete_events"], "invalid_events": field["invalid_events"], "source_event_ids": [event["event_id"] for event in field["events"]]}
    return {**body, "receipt_digest": sha256_json(body)}
```

A birth event with `incomplete` or `invalid` evidence cannot mint a Workmark because it is not present in `field["events"]`.

- [ ] **Step 4: Verify GREEN.**

```bash
python -m unittest tests.test_contribution_field -v
```

- [ ] **Step 5: Commit.**

```bash
git add dogram/contribution_field.py tests/test_contribution_field.py
git commit -m "feat: measure immutable workmark history"
```

---

### Task 3: Cut delta and event-node ablation

**Files:**
- Modify: `dogram/contribution_field.py`
- Modify: `tests/test_contribution_field.py`

**Interfaces:**
- `compare_measurements(before, after) -> dict[str, object]`.
- `ablate_event(field, workmark, event_id) -> dict[str, object]`.

- [ ] **Step 1: Add failing tests.**

```python
from dogram.contribution_field import ablate_event, compare_measurements

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
```

- [ ] **Step 2: Verify RED.**

```bash
python -m unittest tests.test_contribution_field -v
```

- [ ] **Step 3: Implement exact delta and reuse `evaluate_ablate`.**

Add import and functions:

```python
from .ablate import evaluate_ablate

def compare_measurements(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    if before.get("workmark") != after.get("workmark"):
        raise ContributionFieldInputError("WORKMARK_MISMATCH", "receipts must measure the same workmark")
    b = before["measurements"]
    a = after["measurements"]
    b_desc = set(b["reachable_descendant_set"])
    a_desc = set(a["reachable_descendant_set"])
    body = {"schema": DELTA_SCHEMA, "authority": "none", "workmark_id": before["workmark"]["workmark_id"], "before_receipt_digest": before["receipt_digest"], "after_receipt_digest": after["receipt_digest"], "descendant_count_delta": a["descendant_count"] - b["descendant_count"], "added_reachable_descendants": sorted(a_desc - b_desc), "removed_reachable_descendants": sorted(b_desc - a_desc), "relation_kind_counts_before": b["relation_kind_counts"], "relation_kind_counts_after": a["relation_kind_counts"], "incomplete_events_before": before["incomplete_events"], "incomplete_events_after": after["incomplete_events"], "invalid_events_before": before["invalid_events"], "invalid_events_after": after["invalid_events"]}
    return {**body, "delta_digest": sha256_json(body)}

def ablate_event(field: dict[str, object], workmark: dict[str, object], event_id: str) -> dict[str, object]:
    _verify_workmark_birth(field, workmark)
    events = field["events"]
    event = next((item for item in events if item["event_id"] == event_id), None)
    if event is None:
        raise ContributionFieldInputError("EVENT_NOT_IN_CUT", event_id)
    graph = DirectedGraph.from_spec(field["graph"])
    root = str(workmark["graph_address"])
    event_node = f"event:{event_id}"
    targets = [node for node in graph.nodes if node.startswith("entity:") and node != root]
    result, _ = evaluate_ablate({"graph": graph.to_spec(), "target": {"kind": "node", "node": event_node}, "requested_targets": [[root, target] for target in targets]})
    lost = sorted(report["target"].removeprefix("entity:") for report in result["requested_targets"] if report["reachable_before"] and not report["reachable_after"])
    gained = sorted(report["target"].removeprefix("entity:") for report in result["requested_targets"] if not report["reachable_before"] and report["reachable_after"])
    body = {"schema": "dogram.contribution-field-ablation/v0-experimental", "authority": "none", "workmark_id": workmark["workmark_id"], "field_digest": field["field_digest"], "removed_event_id": event_id, "removed_relation_kind": event["relation_kind"], "lost_root_entity_reachability": lost, "gained_root_entity_reachability": gained, "ablate_receipt": result}
    return {**body, "receipt_digest": sha256_json(body)}
```

- [ ] **Step 4: Verify GREEN and run full unit suite.**

```bash
python -m unittest tests.test_contribution_field -v
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit.**

```bash
git add dogram/contribution_field.py tests/test_contribution_field.py
git commit -m "feat: receipt contribution field deltas"
```

---

### Task 4: Freeze specimen and hostile boundaries

**Files:**
- Create: `tests/fixtures/contribution_field_001.json`
- Create: `tests/test_contribution_field_fixture.py`
- Modify: `tests/test_contribution_field.py`

**Interfaces:**
- Fixture sections: `workmark`, `t0`, `t1`, `delta`, `ablation_enable_y`, `ablation_repair_x`, `full_measure_handoff_fixture`.
- Handoff fixture is inert/read-only and contains only exact Dogram receipt references plus allowed/forbidden use labels.

- [ ] **Step 1: Write fixture test before fixture exists.**

Create `tests/test_contribution_field_fixture.py`:

```python
from __future__ import annotations
import json
import unittest
from pathlib import Path
from dogram.contribution_field import ablate_event, build_cut, compare_measurements, measure_workmark, mint_workmark
from tests.test_contribution_field import DECLARED, EVENTS

FIXTURE = Path(__file__).parent / "fixtures" / "contribution_field_001.json"

def build_frozen_specimen() -> dict[str, object]:
    mark = mint_workmark(EVENTS, "e-create-x", 0, DECLARED)
    f0 = build_cut(EVENTS, 0, DECLARED)
    f1 = build_cut(EVENTS, 1, DECLARED)
    t0 = measure_workmark(f0, mark)
    t1 = measure_workmark(f1, mark)
    delta = compare_measurements(t0, t1)
    return {
        "workmark": mark,
        "t0": t0,
        "t1": t1,
        "delta": delta,
        "ablation_enable_y": ablate_event(f1, mark, "e-enable-y"),
        "ablation_repair_x": ablate_event(f1, mark, "e-repair-x"),
        "full_measure_handoff_fixture": {
            "source": "Dogram",
            "authority": "none",
            "workmark_id": mark["workmark_id"],
            "measurement_receipt_digest": t1["receipt_digest"],
            "delta_receipt_digest": delta["delta_digest"],
            "allowed_use": ["read-only story proposal input", "read-only quest proposal input", "read-only participation-opening input"],
            "forbidden_promotion": ["source fact by narration", "economic value", "human worth", "sheet-changing authority"],
        },
    }

class ContributionFieldFixtureTests(unittest.TestCase):
    def test_frozen_specimen_matches_exactly(self) -> None:
        self.assertEqual(build_frozen_specimen(), json.loads(FIXTURE.read_text()))
```

- [ ] **Step 2: Run and confirm RED due to missing fixture.**

```bash
python -m unittest tests.test_contribution_field_fixture -v
```

- [ ] **Step 3: Generate the exact fixture mechanically.**

```bash
python - <<'PY'
import json
from pathlib import Path
from tests.test_contribution_field_fixture import build_frozen_specimen
path = Path("tests/fixtures/contribution_field_001.json")
path.write_text(json.dumps(build_frozen_specimen(), indent=2, sort_keys=True) + "\n")
print(path)
PY
python -m unittest tests.test_contribution_field_fixture -v
```

- [ ] **Step 4: Add hostile anti-collapse and person-score tests.**

Append:

```python
from dogram.anti_collapse_reachability import analyze_collapse

class ContributionHostileBoundaryTests(unittest.TestCase):
    def test_relation_kind_collapse_loses_a_declared_distinction(self) -> None:
        receipt = analyze_collapse(
            states=("created:A->X", "reviewed:A->X", "enabled:X->Y"),
            rich_projection=(("A", "X", "CREATED"), ("A", "X", "REVIEWED"), ("X", "Y", "ENABLED")),
            collapsed_projection=(("A", "X"), ("A", "X"), ("X", "Y")),
        )
        self.assertTrue(receipt.lawful_quotient)
        self.assertEqual(receipt.lost_distinctions, (("created:A->X", "reviewed:A->X"),))

    def test_no_person_score_surface_exists(self) -> None:
        import dogram.contribution_field as module
        forbidden = {"score_person", "rank_people", "calculate_value", "price_contribution", "award_reputation"}
        self.assertTrue(forbidden.isdisjoint(set(dir(module))))
```

- [ ] **Step 5: Run full CI-equivalent floor.**

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
assert set(OPERATORS) == {("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)}
assert set(build_bootstrap_registry().ids()) == {"core.get@1", "core.same@1", "core.add@1", "core.sub@1", "core.length@1", "core.gt@1", "core.select_first@1", "trace.compare_ordered@1", "graph.apply_mutation@1", "graph.reachable_pairs@1", "graph.query_paths@1", "set.difference@1"}
print("constitutional floor OK")
PY
```

Expected: all tests pass, no dependency is added, and public operator/registry sets remain unchanged.

- [ ] **Step 6: Commit.**

```bash
git add tests/test_contribution_field.py tests/test_contribution_field_fixture.py tests/fixtures/contribution_field_001.json
git commit -m "test: freeze contribution field specimen"
```

---

### Task 5: Research receipt and README exposure

**Files:**
- Create: `research/CONTRIBUTION-FIELD-001.md`
- Modify: `README.md`

**Interfaces:**
- Research doc names the exact fixture/module/tests, exact measured outputs, incomplete/invalid evidence behavior, and Full Measure handoff boundary.
- README adds one bounded research paragraph; no public operator claim.

- [ ] **Step 1: Create the research receipt.**

Create `research/CONTRIBUTION-FIELD-001.md` with these required sections and exact claims:

```markdown
# CONTRIBUTION-FIELD-001

**Status:** bounded internal research specimen  
**Authority:** none  
**Public operator:** none

## Question
Can one immutable contribution birth acquire later typed graph history that Dogram measures without pricing, ranking, or narratively promoting the contributor?

## Frozen history
`A CREATED X` is visible at `t0`. At `t1`, `B REPAIRED X`, `X ENABLED Y`, `C CHALLENGED X`, and `Y CARRIED Z` become available. The Workmark remains anchored to the exact digest of `e-create-x`.

## Evidence status
Source owners supply `complete`, `incomplete`, or `invalid`. Dogram does not verify that status, does not upgrade it, and admits only `complete` events to the incidence graph. Incomplete/invalid event ids remain receipt residue.

## Representation
Each admitted typed event is reified as `entity:<source> -> event:<event_id> -> entity:<subject>` so relation kind and parallel relations are not silently erased.

## Measurements
The first specimen receipts only descendant count, relation-kind counts touching the root/forward-descendant closure, reachable descendant set, and one event-node ablation reachability delta.

## Hostile controls
Rewritten birth evidence is invalid; undeclared relation kinds and extra semantic fields fail closed; incomplete/invalid source evidence is retained but not promoted into edges; relation-kind collapse is exposed through `ANTI-COLLAPSE-REACHABILITY-001`; zero forward-reachability loss is not called zero contribution; no person-score/value/rank operator exists.

## Full Measure handoff
The frozen fixture contains inert read-only references to exact Dogram receipts. It is not Full Measure runtime integration and grants no story, witness, economic, or sheet-changing authority.

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

Copy exact digests/counts from `tests/fixtures/contribution_field_001.json` after generation; do not hand-calculate them.

- [ ] **Step 2: Add README pointer.**

After the current anti-collapse paragraph, add:

```markdown
`CONTRIBUTION-FIELD-001` is a bounded internal contribution-history specimen. It preserves one immutable Workmark birth across two time-addressed typed incidence-graph cuts, preserves incomplete/invalid source status without promoting it, receipts neutral descendant/relation measurements and one event-node ablation delta, and freezes a read-only handoff fixture for a later Full Measure story adapter. It adds no public operator, person score, economic valuation, causal semantics, story authority, or Full Measure runtime integration. See `research/CONTRIBUTION-FIELD-001.md`.
```

- [ ] **Step 3: Run final verification and scope scan.**

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
git diff main...HEAD --stat
git diff main...HEAD -- dogram/contribution_field.py tests/test_contribution_field.py tests/test_contribution_field_fixture.py tests/fixtures/contribution_field_001.json research/CONTRIBUTION-FIELD-001.md README.md
```

- [ ] **Step 4: Commit documentation.**

```bash
git add research/CONTRIBUTION-FIELD-001.md README.md
git commit -m "research: receipt CONTRIBUTION-FIELD-001"
```

- [ ] **Step 5: Acceptance gate.**

All must be true:

```text
same Workmark birth at t0 and t1
later field digest differs
reachable descendants: [] -> [Y, Z]
typed relation counts retained
incomplete and invalid source events remain explicit but do not enter graph
rewritten birth rejected
undeclared relation rejected
relation-kind collapse visibly loses a distinction
enable-event ablation loses Y and Z reachability
repair-event ablation may lose zero forward reachability without semantic judgment
fixture regenerates exactly
public Dogram operator set unchanged
bootstrap registry unchanged
Full Measure handoff remains inert/read-only data
no value/merit/price/rank/human-worth output
```

If any item fails, stop at that boundary and report the mismatch against the approved design rather than widening the implementation silently.

---

## Self-Review Map

- Immutable Workmark birth: Task 2.
- Time-addressed graph enrichment: Tasks 1–3.
- Missing witness/evidence lineage remains `incomplete`: Tasks 1–2.
- Invalid supplied evidence status remains explicit and unpromoted: Tasks 1–2.
- Typed relation preservation: Task 1 incidence graph; Task 4 anti-collapse hostile control.
- Neutral measurement vector and delta: Tasks 2–3.
- Counterfactual reachability without valuation: Task 3.
- No person score/economic policy: global constraints plus Tasks 2–5.
- Frozen neutral Full Measure handoff only: Task 4 fixture and Task 5 docs.
- Dependency/operator/registry floors unchanged: Tasks 4–5.
- Creative/economic horizons beyond the first specimen remain in the approved design spec and are intentionally not implemented here.

## Execution Boundary

This plan implements only the Dogram first proof. After it lands and survives hostile review, the next architectural gate is a separate **Full Measure contribution-story adapter** design consuming the frozen neutral handoff fixture without gaining authority to manufacture graph history.