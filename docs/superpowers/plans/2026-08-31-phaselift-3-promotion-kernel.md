# PHASELIFT-3 Promotion Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Dogram's internal `PHASELIFT-3` research evaluator so explicit repeat, transfer, and generation trials can deterministically earn or refuse a local operator-candidate promotion without changing the public Dogram operator floor.

**Architecture:** Add one pure module, `dogram/phaselift.py`, with a narrow `evaluate_phaselift(specimen) -> (result, receipt)` interface. The evaluator validates three role-distinct trial receipts, preserves candidate/transformation identity, checks declared transfer-context distinctions, computes finite `delta_omega` and compositional surplus, rejects circular/self-certifying proofs, and emits a canonical promotion receipt. Frozen JSON fixtures and `unittest` tests drive every production change; no CLI or engine dispatch is added.

**Tech Stack:** Python >=3.12, Python standard library only, `unittest`, existing `dogram.canonical.sha256_json` canonical hashing.

**Spec:** `docs/superpowers/specs/2026-08-31-phaselift-3-promotion-kernel-design.md`

## Global Constraints

- Keep the public operator floor exactly `delta@1`, `rectangle@1`, `ablate@1`, `reach@1`.
- `PHASELIFT-3` is internal research code; do not add a CLI route or engine dispatch entry.
- `PROMOTE` means only that the declared local promotion contract passed; it is not public Dogram operator admission.
- Do not mint truth, evidence, support, authority, historical identity, semantic meaning, or external capability.
- Use no network, file write, clock dependence, randomness, dynamic import, `eval`, or `exec` inside the evaluator.
- Add no third-party dependencies.
- Preserve `THREE APPEARANCES != THREE TRANSFORMATIONS` and `NOVEL VALUE != GENERATED OPERATION`.
- Missing required trial material yields `INSUFFICIENT_TO_TEST`; malformed, contradictory, circular, or scope-violating material yields `REFUSE`.
- Reason-code ordering is deterministic.
- Same specimen bytes as canonical JSON imply the same result and receipt.

---

## File Structure

- Create `dogram/phaselift.py` — pure decoder/checker/evaluator for one PHASELIFT specimen; owns reason ordering, earned-class calculation, proof-cycle detection, and receipt construction.
- Create `tests/test_phaselift.py` — focused behavioral tests using frozen fixtures plus small inline malformed specimens where a fixture would add noise.
- Create `tests/fixtures/phaselift/three-echoes.json` — hostile recurrence-only specimen.
- Create `tests/fixtures/phaselift/novel-output-no-new-verb.json` — hostile novel-value/no-grammar-growth specimen.
- Create `tests/fixtures/phaselift/self-minting-operator.json` — hostile self-certification cycle.
- Create `tests/fixtures/phaselift/lawful-new-verb.json` — positive local promotion control.
- Create `research/phaselift-3-promotion-kernel.md` — research receipt documenting the bounded semantics and non-goals after tests pass.

### Exact production interface

```python
from typing import Any


def evaluate_phaselift(specimen: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    ...
```

The returned `result` contains:

```python
{
    "candidate_id": str | None,
    "earned_class": "REMNANT" | "PATTERN" | "TOOL" | "OPERATOR_CANDIDATE",
    "disposition": "PROMOTE" | "RETAIN" | "REFUSE" | "INSUFFICIENT_TO_TEST",
    "checks": {
        "recurs": bool,
        "transfers": bool,
        "composes": bool,
        "generates": bool,
        "non_circular": bool,
        "provenance_complete": bool,
    },
    "omega_before": list[str],
    "omega_after": list[str],
    "delta_omega": list[str],
    "reason_codes": list[str],
    "residuals": list[str],
    "public_operator_admission": False,
}
```

The returned `receipt` uses schema `dogram.phaselift.receipt/v0`, contains the result fields plus candidate version, input digest, role-to-trial refs, and `receipt_digest`.

### Exact specimen envelope

Every frozen specimen uses:

```json
{
  "schema": "dogram.phaselift.specimen/v0",
  "candidate_id": "candidate/example",
  "candidate_version": 1,
  "trials": []
}
```

Every trial uses:

```json
{
  "schema": "dogram.phaselift.trial/v0",
  "trial_id": "trial/repeat-001",
  "receipt_id": "receipt/repeat-001",
  "role": "REPEAT",
  "candidate_ref": "candidate/example",
  "candidate_digest": "sha256:candidate-example-v1",
  "context_fingerprint": {},
  "distinct_from": null,
  "input_refs": [],
  "output_refs": [],
  "transformation_id": "transform/example",
  "transformation_version": 1,
  "composition_witnesses": [],
  "omega_before": [],
  "generated_operations": [],
  "provenance_refs": [],
  "residuals": []
}
```

A generation composition witness uses:

```json
{
  "left_ref": "artifact/a",
  "verb_id": "verb/compose-example",
  "right_ref": "artifact/b",
  "phase": "PLUS_CO",
  "output_ref": "artifact/composed",
  "left_capability_refs": ["op/a"],
  "right_capability_refs": ["op/b"],
  "output_capability_refs": ["op/a", "op/b", "op/new"],
  "surplus_capability_refs": ["op/new"]
}
```

A generated operation uses:

```json
{
  "operation_id": "op/new",
  "operation_version": 1,
  "input_kinds": ["artifact", "artifact"],
  "output_kind": "artifact",
  "derivation_refs": ["artifact/composed", "receipt/generate-001"],
  "replay_probe_ref": "probe/new-operation-independent"
}
```

The internal proof graph uses dependency edges implied by the data:

- pending promotion receipt -> all three trial ids;
- trial id -> its `provenance_refs`, `output_refs`, generated operation ids, and composition output refs;
- composition output ref -> `left_ref`, `right_ref`, and `surplus_capability_refs`;
- generated operation id -> `derivation_refs` and `replay_probe_ref`.

Use the reserved internal node id `phaselift/receipt-under-construction`. Any cycle in this finite graph that includes this node yields `REFUSE / CIRCULAR_PROMOTION_PROOF`.

### Deterministic reason order

Define exactly this order in production code:

```python
REASON_ORDER = (
    "SCHEMA_INVALID",
    "MISSING_TRIAL",
    "DUPLICATE_TRIAL_RECEIPT",
    "CANDIDATE_IDENTITY_CHANGED",
    "TRANSFORMATION_IDENTITY_CHANGED",
    "PROVENANCE_INCOMPLETE",
    "TRANSFER_CONTEXT_NOT_DISTINCT",
    "PLUS_CO_MISSING_VERB",
    "COMPOSITION_ATTRIBUTION_INCOMPLETE",
    "GENERATED_OPERATION_INVALID",
    "DELTA_OMEGA_EMPTY",
    "COMPOSITIONAL_SURPLUS_EMPTY",
    "CIRCULAR_PROMOTION_PROOF",
)
```

Sort emitted reason codes by this tuple, never by incidental traversal order.

---

### Task 1: Freeze the four promotion specimens and establish the public evaluator contract

**Files:**
- Create: `tests/fixtures/phaselift/three-echoes.json`
- Create: `tests/fixtures/phaselift/novel-output-no-new-verb.json`
- Create: `tests/fixtures/phaselift/self-minting-operator.json`
- Create: `tests/fixtures/phaselift/lawful-new-verb.json`
- Create: `tests/test_phaselift.py`
- Create: `dogram/phaselift.py`

**Interfaces:**
- Consumes: `dogram.canonical.sha256_json(value: Any) -> str`
- Produces: `evaluate_phaselift(specimen: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]`

- [ ] **Step 1: Add the exact hostile `three-echoes.json` fixture**

```json
{
  "schema": "dogram.phaselift.specimen/v0",
  "candidate_id": "candidate/replay-edge",
  "candidate_version": 1,
  "trials": [
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/repeat-001",
      "receipt_id": "receipt/repeat-001",
      "role": "REPEAT",
      "candidate_ref": "candidate/replay-edge",
      "candidate_digest": "sha256:replay-edge-v1",
      "context_fingerprint": {"domain": "trace", "carrier_kind": "ordered", "probe_kind": "first-difference"},
      "distinct_from": null,
      "input_refs": ["input/repeat"],
      "output_refs": ["output/repeat"],
      "transformation_id": "transform/replay-edge",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/existing"],
      "generated_operations": [],
      "provenance_refs": ["source/repeat"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/transfer-001",
      "receipt_id": "receipt/transfer-001",
      "role": "TRANSFER",
      "candidate_ref": "candidate/replay-edge",
      "candidate_digest": "sha256:replay-edge-v1",
      "context_fingerprint": {"domain": "trace", "carrier_kind": "ordered", "probe_kind": "first-difference"},
      "distinct_from": {"trial_ref": "trial/repeat-001", "dimensions": ["domain", "carrier_kind"]},
      "input_refs": ["input/transfer"],
      "output_refs": ["output/transfer"],
      "transformation_id": "transform/replay-edge",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/existing"],
      "generated_operations": [],
      "provenance_refs": ["source/transfer"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/generate-001",
      "receipt_id": "receipt/generate-001",
      "role": "GENERATE",
      "candidate_ref": "candidate/replay-edge",
      "candidate_digest": "sha256:replay-edge-v1",
      "context_fingerprint": {"domain": "trace", "carrier_kind": "ordered", "probe_kind": "first-difference"},
      "distinct_from": null,
      "input_refs": ["artifact/a", "artifact/b"],
      "output_refs": ["artifact/replayed"],
      "transformation_id": "transform/replay-edge",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/existing"],
      "generated_operations": [
        {
          "operation_id": "op/existing",
          "operation_version": 1,
          "input_kinds": ["artifact"],
          "output_kind": "artifact",
          "derivation_refs": ["artifact/replayed"],
          "replay_probe_ref": "probe/existing"
        }
      ],
      "provenance_refs": ["source/generate"],
      "residuals": []
    }
  ]
}
```

- [ ] **Step 2: Add `novel-output-no-new-verb.json` by using three valid distinct trials, with the generation trial carrying `output_refs: ["value/never-seen-before"]`, `omega_before: ["op/a", "op/b"]`, `generated_operations: []`, and no composition witnesses**

Use repeat context:

```json
{"domain":"sequence","carrier_kind":"ordered_trace","probe_kind":"boundary"}
```

Use transfer context:

```json
{"domain":"graph","carrier_kind":"directed_graph","probe_kind":"boundary"}
```

with:

```json
{"trial_ref":"trial/repeat-002","dimensions":["domain","carrier_kind"]}
```

Use the same candidate digest `sha256:novel-output-v1` and transformation `transform/novel-output@1` in all three trials.

- [ ] **Step 3: Add `self-minting-operator.json` with a valid repeat, valid transfer, and a generation trial whose new `op/promote-self` operation has `derivation_refs: ["phaselift/receipt-under-construction"]`**

The generation trial must otherwise be structurally promotable: `omega_before: ["op/a", "op/b"]`, one `PLUS_CO` witness with computed surplus `op/promote-self`, and one independent-looking replay probe. This fixture must fail only because the proof graph cycles through the receipt under construction.

- [ ] **Step 4: Add `lawful-new-verb.json` with exactly one new operation `op/bind-and-route`**

Use:

```json
"omega_before": ["op/bind", "op/route"]
```

and this generation witness:

```json
{
  "left_ref": "artifact/bind-plan",
  "verb_id": "verb/compose-bind-route",
  "right_ref": "artifact/route-plan",
  "phase": "PLUS_CO",
  "output_ref": "artifact/bound-route",
  "left_capability_refs": ["op/bind"],
  "right_capability_refs": ["op/route"],
  "output_capability_refs": ["op/bind", "op/route", "op/bind-and-route"],
  "surplus_capability_refs": ["op/bind-and-route"]
}
```

The generated operation must be:

```json
{
  "operation_id": "op/bind-and-route",
  "operation_version": 1,
  "input_kinds": ["binding", "route"],
  "output_kind": "bound_route",
  "derivation_refs": ["artifact/bound-route", "receipt/generate-004"],
  "replay_probe_ref": "probe/bind-and-route-independent"
}
```

Use a distinct repeat context (`domain=sequence`, `carrier_kind=ordered_trace`) and transfer context (`domain=graph`, `carrier_kind=directed_graph`) while preserving candidate digest `sha256:bind-route-v1` and transformation `transform/bind-route@1`.

- [ ] **Step 5: Write the first failing test for the positive interface**

```python
import json
import unittest
from pathlib import Path

from dogram.phaselift import evaluate_phaselift

FIXTURES = Path(__file__).parent / "fixtures" / "phaselift"


class PhaseLiftTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_lawful_new_verb_promotes_one_local_operator_candidate(self):
        result, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
        self.assertEqual(result["disposition"], "PROMOTE")
        self.assertEqual(result["earned_class"], "OPERATOR_CANDIDATE")
        self.assertEqual(result["delta_omega"], ["op/bind-and-route"])
        self.assertFalse(result["public_operator_admission"])
        self.assertEqual(receipt["schema"], "dogram.phaselift.receipt/v0")
```

- [ ] **Step 6: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_lawful_new_verb_promotes_one_local_operator_candidate -v
```

Expected: import failure because `dogram.phaselift` does not exist.

- [ ] **Step 7: Create the minimal module and function skeleton**

```python
from __future__ import annotations

from typing import Any


def evaluate_phaselift(specimen: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    raise NotImplementedError


__all__ = ["evaluate_phaselift"]
```

- [ ] **Step 8: Re-run the focused test and verify it now fails at `NotImplementedError`**

Run the same command. Expected: ERROR at `evaluate_phaselift`; the test is now connected to the intended production surface.

- [ ] **Step 9: Commit the frozen corpus and evaluator surface**

```bash
git add dogram/phaselift.py tests/test_phaselift.py tests/fixtures/phaselift
git commit -m "test: freeze PHASELIFT promotion corpus"
```

---

### Task 2: Implement schema, role, identity, repeat, and transfer evaluation

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: specimen/trial envelopes defined in Task 1.
- Produces: deterministic role mapping, `recurs`, `transfers`, and highest earned class through `TOOL`.

- [ ] **Step 1: Add failing tests for recurrence-only retention, distinct transfer, missing material, duplicate receipts, and identity drift**

```python
def test_three_echoes_earns_pattern_but_does_not_transfer(self):
    result, _ = evaluate_phaselift(self.load("three-echoes.json"))
    self.assertEqual(result["earned_class"], "PATTERN")
    self.assertEqual(result["disposition"], "RETAIN")
    self.assertTrue(result["checks"]["recurs"])
    self.assertFalse(result["checks"]["transfers"])
    self.assertIn("TRANSFER_CONTEXT_NOT_DISTINCT", result["reason_codes"])


def test_novel_output_fixture_earns_tool_before_generation_fails(self):
    result, _ = evaluate_phaselift(self.load("novel-output-no-new-verb.json"))
    self.assertTrue(result["checks"]["recurs"])
    self.assertTrue(result["checks"]["transfers"])
    self.assertEqual(result["earned_class"], "TOOL")


def test_missing_generate_trial_is_insufficient_not_false(self):
    specimen = self.load("lawful-new-verb.json")
    specimen["trials"] = [trial for trial in specimen["trials"] if trial["role"] != "GENERATE"]
    result, _ = evaluate_phaselift(specimen)
    self.assertEqual(result["disposition"], "INSUFFICIENT_TO_TEST")
    self.assertEqual(result["reason_codes"], ["MISSING_TRIAL"])


def test_one_receipt_aliased_across_roles_is_refused(self):
    specimen = self.load("lawful-new-verb.json")
    specimen["trials"][1]["receipt_id"] = specimen["trials"][0]["receipt_id"]
    result, _ = evaluate_phaselift(specimen)
    self.assertEqual(result["disposition"], "REFUSE")
    self.assertEqual(result["reason_codes"], ["DUPLICATE_TRIAL_RECEIPT"])


def test_candidate_digest_change_is_refused(self):
    specimen = self.load("lawful-new-verb.json")
    specimen["trials"][1]["candidate_digest"] = "sha256:different-candidate"
    result, _ = evaluate_phaselift(specimen)
    self.assertEqual(result["disposition"], "REFUSE")
    self.assertIn("CANDIDATE_IDENTITY_CHANGED", result["reason_codes"])
```

- [ ] **Step 2: Run Task 2 tests and verify RED**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: all new behavioral tests fail because only the skeleton exists.

- [ ] **Step 3: Implement exact constants and defensive decoding helpers**

Add:

```python
SPECIMEN_SCHEMA = "dogram.phaselift.specimen/v0"
TRIAL_SCHEMA = "dogram.phaselift.trial/v0"
RECEIPT_SCHEMA = "dogram.phaselift.receipt/v0"
REQUIRED_ROLES = ("REPEAT", "TRANSFER", "GENERATE")
PENDING_RECEIPT_REF = "phaselift/receipt-under-construction"
REASON_ORDER = (...exact tuple from this plan header...)
```

Implement `_ordered_reasons`, `_empty_checks`, `_base_result`, and `_find_trials`. `_find_trials` must distinguish:

- missing required role -> `INSUFFICIENT_TO_TEST / MISSING_TRIAL`;
- duplicate `trial_id` or duplicate `receipt_id` -> `REFUSE / DUPLICATE_TRIAL_RECEIPT`;
- wrong specimen/trial schema, wrong role name, non-list trials -> `REFUSE / SCHEMA_INVALID`.

- [ ] **Step 4: Implement candidate and transformation identity checks**

All three trials must have `candidate_ref == specimen["candidate_id"]`, one identical non-empty `candidate_digest`, one identical non-empty `transformation_id`, and one identical integer `transformation_version`.

Emit:

- `CANDIDATE_IDENTITY_CHANGED` for candidate ref/digest divergence;
- `TRANSFORMATION_IDENTITY_CHANGED` for transformation id/version divergence.

Treat either as `REFUSE`.

- [ ] **Step 5: Implement provenance completeness for the trial floor**

Every trial must have a non-empty list of string `provenance_refs` and a non-empty list of string `output_refs`. Empty or malformed provenance yields `REFUSE / PROVENANCE_INCOMPLETE`.

- [ ] **Step 6: Implement repeat and transfer checks**

`recurs = True` when the repeat trial is structurally valid after identity/provenance checks.

For transfer:

1. Require `distinct_from` to be an object with `trial_ref` equal to the repeat trial id.
2. Require `dimensions` to be a non-empty list of strings.
3. For every named dimension, require both fingerprints to contain the key and require `transfer_value != repeat_value`.
4. If any named dimension is absent or equal, set `transfers=False` and add `TRANSFER_CONTEXT_NOT_DISTINCT`.
5. Otherwise set `transfers=True`.

Earned class at this point:

```python
"REMNANT" if not recurs else "PATTERN" if not transfers else "TOOL"
```

- [ ] **Step 7: Run Task 2 tests and verify GREEN for the non-generation cases**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: missing/duplicate/identity/three-echoes/novel-output class tests pass; positive promotion still fails because generation is not implemented.

- [ ] **Step 8: Commit the trial-floor evaluator**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: evaluate PHASELIFT repeat and transfer trials"
```

---

### Task 3: Implement finite grammar growth, lawful composition, and local promotion

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: valid `GENERATE` trial and its `omega_before`, `generated_operations`, and `composition_witnesses`.
- Produces: `omega_after`, `delta_omega`, `composes`, `generates`, `OPERATOR_CANDIDATE`, and `PROMOTE` when all non-circular conditions pass.

- [ ] **Step 1: Add failing generation/composition tests**

```python
def test_novel_value_without_new_operation_does_not_generate(self):
    result, _ = evaluate_phaselift(self.load("novel-output-no-new-verb.json"))
    self.assertFalse(result["checks"]["generates"])
    self.assertEqual(result["delta_omega"], [])
    self.assertIn("DELTA_OMEGA_EMPTY", result["reason_codes"])
    self.assertEqual(result["earned_class"], "TOOL")


def test_plus_co_requires_explicit_verb(self):
    specimen = self.load("lawful-new-verb.json")
    specimen["trials"][2]["composition_witnesses"][0]["verb_id"] = ""
    result, _ = evaluate_phaselift(specimen)
    self.assertEqual(result["disposition"], "RETAIN")
    self.assertIn("PLUS_CO_MISSING_VERB", result["reason_codes"])


def test_compositional_surplus_must_be_non_empty(self):
    specimen = self.load("lawful-new-verb.json")
    witness = specimen["trials"][2]["composition_witnesses"][0]
    witness["output_capability_refs"] = ["op/bind", "op/route"]
    witness["surplus_capability_refs"] = []
    result, _ = evaluate_phaselift(specimen)
    self.assertEqual(result["disposition"], "RETAIN")
    self.assertIn("COMPOSITIONAL_SURPLUS_EMPTY", result["reason_codes"])


def test_lawful_generation_adds_exactly_one_operation(self):
    result, _ = evaluate_phaselift(self.load("lawful-new-verb.json"))
    self.assertEqual(result["omega_before"], ["op/bind", "op/route"])
    self.assertEqual(result["omega_after"], ["op/bind", "op/bind-and-route", "op/route"])
    self.assertEqual(result["delta_omega"], ["op/bind-and-route"])
    self.assertTrue(result["checks"]["composes"])
    self.assertTrue(result["checks"]["generates"])
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_novel_value_without_new_operation_does_not_generate tests.test_phaselift.PhaseLiftTests.test_plus_co_requires_explicit_verb tests.test_phaselift.PhaseLiftTests.test_compositional_surplus_must_be_non_empty tests.test_phaselift.PhaseLiftTests.test_lawful_generation_adds_exactly_one_operation -v
```

Expected: failures on missing generation/composition behavior.

- [ ] **Step 3: Implement generated-operation validation**

A generated operation is valid only when:

- `operation_id` is a non-empty string;
- `operation_version` is an integer >= 1;
- `input_kinds` is a non-empty list of non-empty strings;
- `output_kind` is a non-empty string;
- `derivation_refs` is a non-empty list of non-empty strings;
- `replay_probe_ref` is a non-empty string.

Any malformed generated operation adds `GENERATED_OPERATION_INVALID` and makes the specimen `REFUSE`.

- [ ] **Step 4: Compute finite grammar growth deterministically**

For the generation trial:

```python
omega_before = sorted(set(trial["omega_before"]))
generated_ids = sorted({op["operation_id"] for op in generated_operations})
omega_after = sorted(set(omega_before) | set(generated_ids))
delta_omega = sorted(set(omega_after) - set(omega_before))
```

If `delta_omega` is empty, set `generates=False` and add `DELTA_OMEGA_EMPTY`. Novel `output_refs` alone never affect this result.

- [ ] **Step 5: Implement `PLUS_CO` witness validation and source attribution**

For each generation witness:

- ignore `NOT_PLUS_CO` witnesses for promotion;
- a `PLUS_CO` witness requires non-empty `left_ref`, `verb_id`, `right_ref`, and `output_ref`;
- `left_ref` and `right_ref` must both occur in generation `input_refs`;
- `output_ref` must occur in generation `output_refs`;
- `left_capability_refs`, `right_capability_refs`, `output_capability_refs`, and `surplus_capability_refs` must each be lists of strings.

Missing `verb_id` adds `PLUS_CO_MISSING_VERB` and yields `RETAIN`.

Missing source/output attribution adds `COMPOSITION_ATTRIBUTION_INCOMPLETE` and yields `REFUSE`.

- [ ] **Step 6: Compute and validate compositional surplus**

For every valid `PLUS_CO` witness:

```python
computed_surplus = set(output_capability_refs) - (
    set(left_capability_refs) | set(right_capability_refs)
)
declared_surplus = set(surplus_capability_refs)
```

The witness has lawful surplus only when:

```python
bool(declared_surplus) and declared_surplus <= computed_surplus
```

At least one declared surplus id must also occur in `delta_omega`.

If no `PLUS_CO` witness meets those conditions, set `composes=False` and add `COMPOSITIONAL_SURPLUS_EMPTY` unless a more specific `PLUS_CO_MISSING_VERB` or attribution failure already explains the failure.

- [ ] **Step 7: Compute earned class and preliminary disposition**

After structural/refusal checks:

```python
if not recurs:
    earned_class = "REMNANT"
elif not transfers:
    earned_class = "PATTERN"
elif not (generates and composes):
    earned_class = "TOOL"
else:
    earned_class = "OPERATOR_CANDIDATE"
```

Use `PROMOTE` only when the earned class is `OPERATOR_CANDIDATE` and no reason code remains. Otherwise use `RETAIN` for earned-but-failed later conditions.

- [ ] **Step 8: Run the generation/composition tests and verify GREEN except the self-cycle fixture**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: positive local promotion and non-circular hostile fixtures pass; self-minting test is not yet asserted.

- [ ] **Step 9: Commit grammar-growth and composition behavior**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: evaluate PHASELIFT grammar growth"
```

---

### Task 4: Refuse circular/self-certifying promotion proofs

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: the finite dependency graph implied by trials, witnesses, operations, and the reserved pending receipt node.
- Produces: `checks.non_circular` and `REFUSE / CIRCULAR_PROMOTION_PROOF`.

- [ ] **Step 1: Add failing cycle tests**

```python
def test_self_minting_operation_is_refused_as_circular(self):
    result, _ = evaluate_phaselift(self.load("self-minting-operator.json"))
    self.assertEqual(result["disposition"], "REFUSE")
    self.assertFalse(result["checks"]["non_circular"])
    self.assertEqual(result["reason_codes"], ["CIRCULAR_PROMOTION_PROOF"])


def test_indirect_cycle_through_generated_operation_is_refused(self):
    specimen = self.load("lawful-new-verb.json")
    operation = specimen["trials"][2]["generated_operations"][0]
    operation["derivation_refs"] = ["artifact/bound-route", "node/cycle-a"]
    specimen["trials"][2]["provenance_refs"].append("node/cycle-a")
    specimen["trials"][2]["output_refs"].append("node/cycle-a")
    specimen["trials"][2]["composition_witnesses"].append({
        "left_ref": "artifact/bind-plan",
        "verb_id": "verb/cycle-carrier",
        "right_ref": "artifact/route-plan",
        "phase": "NOT_PLUS_CO",
        "output_ref": "node/cycle-a",
        "left_capability_refs": [],
        "right_capability_refs": [],
        "output_capability_refs": [],
        "surplus_capability_refs": []
    })
    operation["replay_probe_ref"] = "phaselift/receipt-under-construction"
    result, _ = evaluate_phaselift(specimen)
    self.assertEqual(result["disposition"], "REFUSE")
    self.assertIn("CIRCULAR_PROMOTION_PROOF", result["reason_codes"])
```

- [ ] **Step 2: Run the cycle tests and verify RED**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_self_minting_operation_is_refused_as_circular tests.test_phaselift.PhaseLiftTests.test_indirect_cycle_through_generated_operation_is_refused -v
```

Expected: self-minting specimen currently promotes or retains instead of refusing.

- [ ] **Step 3: Implement proof-graph construction**

Create a `dict[str, set[str]]` adjacency map where each node points to the refs it depends on. Always add:

```python
graph[PENDING_RECEIPT_REF] = {
    repeat_trial["trial_id"],
    transfer_trial["trial_id"],
    generate_trial["trial_id"],
}
```

For each trial add edges to its provenance refs, output refs, generated operation ids, and composition output refs. For each composition output add edges to left/right refs and surplus capability refs. For each generated operation add edges to derivation refs and replay probe ref.

- [ ] **Step 4: Implement deterministic DFS cycle detection**

Use sorted neighbor traversal. Detect any directed cycle containing `PENDING_RECEIPT_REF`; unrelated cycles are retained in the receipt graph only if later work needs them and do not become a promotion verdict in this slice.

When such a cycle exists:

```python
checks["non_circular"] = False
reason_codes.append("CIRCULAR_PROMOTION_PROOF")
disposition = "REFUSE"
```

Do not let `PROMOTE` survive this override.

- [ ] **Step 5: Run all PHASELIFT tests and verify GREEN**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: all focused PHASELIFT tests pass.

- [ ] **Step 6: Commit anti-self-certification**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: refuse circular PHASELIFT proofs"
```

---

### Task 5: Canonicalize the promotion receipt and prove deterministic replay

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: final local evaluation state from Tasks 2-4 and `sha256_json`.
- Produces: stable `dogram.phaselift.receipt/v0` with `input_digest` and self-independent `receipt_digest`.

- [ ] **Step 1: Add failing canonical-receipt tests**

```python
def test_same_specimen_replays_to_identical_result_and_receipt(self):
    specimen = self.load("lawful-new-verb.json")
    first = evaluate_phaselift(specimen)
    second = evaluate_phaselift(specimen)
    self.assertEqual(first, second)


def test_receipt_digest_hashes_receipt_without_its_digest_field(self):
    from dogram.canonical import sha256_json

    _, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
    unsigned = dict(receipt)
    digest = unsigned.pop("receipt_digest")
    self.assertEqual(digest, sha256_json(unsigned))


def test_receipt_preserves_role_trial_refs_and_non_admission_boundary(self):
    _, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
    self.assertEqual(receipt["trial_refs"], {
        "repeat": "trial/repeat-004",
        "transfer": "trial/transfer-004",
        "generate": "trial/generate-004",
    })
    self.assertFalse(receipt["public_operator_admission"])
```

- [ ] **Step 2: Run canonical receipt tests and verify RED**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_same_specimen_replays_to_identical_result_and_receipt tests.test_phaselift.PhaseLiftTests.test_receipt_digest_hashes_receipt_without_its_digest_field tests.test_phaselift.PhaseLiftTests.test_receipt_preserves_role_trial_refs_and_non_admission_boundary -v
```

Expected: receipt fields/digests are missing or incomplete.

- [ ] **Step 3: Implement canonical result and receipt construction**

Import:

```python
from .canonical import sha256_json
```

Construct the result with sorted unique omega/reason/residual arrays and the fixed check-key order shown in this plan.

Construct the receipt as:

```python
receipt = {
    "schema": RECEIPT_SCHEMA,
    "candidate_id": candidate_id,
    "candidate_version": candidate_version,
    "input_digest": sha256_json(specimen),
    "trial_refs": {
        "repeat": repeat_trial["trial_id"],
        "transfer": transfer_trial["trial_id"],
        "generate": generate_trial["trial_id"],
    },
    **result,
}
receipt["receipt_digest"] = sha256_json(receipt)
```

Important: compute `receipt_digest` before adding the field itself; the exact code should therefore create `unsigned_receipt`, hash it, then copy/add `receipt_digest`.

For `INSUFFICIENT_TO_TEST` where a role is missing, set that missing role's `trial_refs` value to `None` and still emit a deterministic receipt.

- [ ] **Step 4: Ensure deterministic residuals**

Residuals must be concise strings keyed to failed structural checks, for example:

```text
TRANSFER_CONTEXT_NOT_DISTINCT:domain
DELTA_OMEGA_EMPTY
CIRCULAR_PROMOTION_PROOF:phaselift/receipt-under-construction
```

Sort residuals lexicographically after reason ordering has been applied.

- [ ] **Step 5: Run PHASELIFT tests and then the full existing suite**

```bash
python -m unittest tests.test_phaselift -v
python -m unittest discover -s tests -v
```

Expected: all tests pass; no public operator tests change.

- [ ] **Step 6: Commit deterministic receipts**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: receipt PHASELIFT promotion decisions"
```

---

### Task 6: Document the research kernel and verify the constitutional boundary

**Files:**
- Create: `research/phaselift-3-promotion-kernel.md`
- Modify: `tests/test_phaselift.py`
- Verify only: `dogram/engine.py`, `dogram/cli.py`, `README.md`

**Interfaces:**
- Consumes: completed evaluator behavior and frozen test corpus.
- Produces: durable research note plus an explicit regression test that no public admission flag can become true.

- [ ] **Step 1: Add the final boundary regression test**

```python
def test_every_disposition_explicitly_denies_public_operator_admission(self):
    for name in (
        "three-echoes.json",
        "novel-output-no-new-verb.json",
        "self-minting-operator.json",
        "lawful-new-verb.json",
    ):
        result, receipt = evaluate_phaselift(self.load(name))
        self.assertFalse(result["public_operator_admission"])
        self.assertFalse(receipt["public_operator_admission"])
```

- [ ] **Step 2: Run the boundary test and verify GREEN**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_every_disposition_explicitly_denies_public_operator_admission -v
```

Expected: PASS from the already implemented invariant.

- [ ] **Step 3: Write `research/phaselift-3-promotion-kernel.md` with this exact constitutional summary**

```markdown
# PHASELIFT-3 Promotion Kernel

PHASELIFT-3 is an internal deterministic research evaluator for one narrow question:

> Did a caller-declared candidate satisfy the local REPEAT -> TRANSFER -> GENERATE -> LIFT contract under supplied attributable trials?

It does not discover candidates, infer semantic importance, mint evidence or truth, mutate the runtime, or admit public Dogram operators.

## Frozen controls

- `three-echoes.json`: recurrence survives; transfer/generation do not.
- `novel-output-no-new-verb.json`: context transfer survives; novel value does not enlarge grammar.
- `self-minting-operator.json`: local-looking generativity is refused because the proof depends on the receipt being computed.
- `lawful-new-verb.json`: one attributable `PLUS_CO` composition yields exactly one new finite operation identity and an acyclic independent replay probe.

## Local law

`PROMOTE != PUBLIC OPERATOR ADMISSION`

The evaluator's only authority is to report whether its bounded declared contract passed.
```

- [ ] **Step 4: Verify no public routing changed**

Run:

```bash
git diff main...HEAD -- dogram/engine.py dogram/cli.py README.md
```

Expected: no diff for these files.

- [ ] **Step 5: Run full verification**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Expected: all tests pass and compilation exits 0.

- [ ] **Step 6: Inspect final diff for scope**

```bash
git diff --stat main...HEAD
git status --short
```

Expected changed implementation surface after the design/plan docs:

```text
dogram/phaselift.py
tests/test_phaselift.py
tests/fixtures/phaselift/*.json
research/phaselift-3-promotion-kernel.md
```

No dependency, CLI, engine-dispatch, registry, or public operator file should be modified.

- [ ] **Step 7: Commit the research receipt**

```bash
git add research/phaselift-3-promotion-kernel.md tests/test_phaselift.py
git commit -m "docs: receipt PHASELIFT-3 research kernel"
```

---

## Acceptance Mapping

| Spec acceptance requirement | Implemented / proven by |
| --- | --- |
| Four public operators unchanged | Task 6 diff check |
| Pure deterministic evaluator | Tasks 2-5 + replay test |
| Four frozen fixtures exact dispositions | Tasks 1-4 |
| Three aliases cannot satisfy three roles | Task 2 duplicate receipt test |
| Novel output without `delta_omega` cannot promote | Task 3 novel-value test |
| Context rename without changed declared dimensions cannot transfer | Task 2 `three-echoes` |
| `PLUS_CO` without verb cannot compose | Task 3 explicit-verb test |
| Self-referential proof refused | Task 4 cycle tests |
| Positive fixture promotes exactly one new operation | Tasks 1 and 3 |
| Local promotion is not public admission | Tasks 1, 5, 6 |
| Full existing suite passes | Tasks 5 and 6 |

## Final Self-Review Checklist

- No `TBD`, `TODO`, or deferred implementation language remains in this plan.
- Every production behavior is introduced by a failing test first.
- The evaluator has one public function and no ambient side effects.
- `receipt_digest` never includes itself in its own hash input.
- `delta_omega` is computed from finite operation identities, never inferred from output novelty.
- `PLUS_CO` cannot pass without a verb, source attribution, and non-empty computed surplus.
- Cycle detection is bounded to the finite supplied proof graph and only makes a constitutional claim about self-certification.
- `PROMOTE` remains local and cannot mutate Dogram's registry or dispatch surface.
