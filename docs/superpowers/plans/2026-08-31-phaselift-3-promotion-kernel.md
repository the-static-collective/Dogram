# PHASELIFT-3 Promotion Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Dogram's internal `PHASELIFT-3` research evaluator so explicit repeat, transfer, and generation trials can deterministically earn or refuse a local operator-candidate promotion without changing the public Dogram operator floor.

**Architecture:** Add one pure module, `dogram/phaselift.py`, with `evaluate_phaselift(specimen) -> (result, receipt)`. The evaluator validates three attributable role-distinct trials, preserves candidate/transformation identity, checks declared transfer-context differences, computes finite grammar growth and compositional surplus, rejects self-certifying proof cycles, and emits a canonical promotion receipt. Frozen JSON fixtures plus `unittest` tests drive every behavior; no CLI, engine-dispatch, registry, or dependency change is admitted.

**Tech Stack:** Python >=3.12, Python standard library only, `unittest`, existing `dogram.canonical.sha256_json`.

**Spec:** `docs/superpowers/specs/2026-08-31-phaselift-3-promotion-kernel-design.md`

## Global Constraints

- Keep the public operator floor exactly `delta@1`, `rectangle@1`, `ablate@1`, `reach@1`.
- `PHASELIFT-3` is an internal research kernel; do not add a CLI route, engine dispatch entry, or registry admission path.
- `PROMOTE` means only that the supplied local promotion contract passed.
- Never mint truth, evidence, support, authority, historical identity, semantic meaning, or external capability.
- Evaluator execution has no network, file write, clock dependence, randomness, dynamic import, `eval`, or `exec`.
- Add no third-party dependency.
- `THREE APPEARANCES != THREE TRANSFORMATIONS`.
- `NOVEL VALUE != GENERATED OPERATION`.
- Missing required trial material yields `INSUFFICIENT_TO_TEST`.
- Malformed, contradictory, circular, or scope-violating material yields `REFUSE`.
- Reason ordering is deterministic.
- Canonically equal specimens produce identical result and receipt objects.

---

## File Map

Create only these executable-slice files:

```text
dogram/phaselift.py
tests/test_phaselift.py
tests/fixtures/phaselift/three-echoes.json
tests/fixtures/phaselift/novel-output-no-new-verb.json
tests/fixtures/phaselift/self-minting-operator.json
tests/fixtures/phaselift/lawful-new-verb.json
research/phaselift-3-promotion-kernel.md
```

The existing design and this plan remain documentation changes. Do not modify `dogram/engine.py`, `dogram/cli.py`, `dogram/registry.py`, or `pyproject.toml`.

## Production Interface

```python
from typing import Any


def evaluate_phaselift(
    specimen: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return deterministic local promotion result and canonical receipt."""
```

The result shape is fixed:

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

The receipt schema is `dogram.phaselift.receipt/v0`. It contains every result field plus `candidate_version`, `input_digest`, `trial_refs`, and `receipt_digest`.

## Stable Constants

Production code must define these exact values:

```python
SPECIMEN_SCHEMA = "dogram.phaselift.specimen/v0"
TRIAL_SCHEMA = "dogram.phaselift.trial/v0"
RECEIPT_SCHEMA = "dogram.phaselift.receipt/v0"
PENDING_RECEIPT_REF = "phaselift/receipt-under-construction"
REQUIRED_ROLES = ("REPEAT", "TRANSFER", "GENERATE")
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

---

### Task 1: Freeze the four conformance specimens and establish the evaluator surface

**Files:**
- Create: `tests/fixtures/phaselift/three-echoes.json`
- Create: `tests/fixtures/phaselift/novel-output-no-new-verb.json`
- Create: `tests/fixtures/phaselift/self-minting-operator.json`
- Create: `tests/fixtures/phaselift/lawful-new-verb.json`
- Create: `tests/test_phaselift.py`
- Create: `dogram/phaselift.py`

**Interfaces:**
- Consumes: `dogram.canonical.sha256_json(value)` later in the plan.
- Produces: importable `evaluate_phaselift` surface and immutable fixture corpus.

- [ ] **Step 1: Create `three-echoes.json` exactly as follows**

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
      "context_fingerprint": {
        "domain": "trace",
        "carrier_kind": "ordered",
        "probe_kind": "first-difference"
      },
      "distinct_from": null,
      "input_refs": ["input/repeat-001"],
      "output_refs": ["output/repeat-001"],
      "transformation_id": "transform/replay-edge",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/existing"],
      "generated_operations": [],
      "provenance_refs": ["source/repeat-001"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/transfer-001",
      "receipt_id": "receipt/transfer-001",
      "role": "TRANSFER",
      "candidate_ref": "candidate/replay-edge",
      "candidate_digest": "sha256:replay-edge-v1",
      "context_fingerprint": {
        "domain": "trace",
        "carrier_kind": "ordered",
        "probe_kind": "first-difference"
      },
      "distinct_from": {
        "trial_ref": "trial/repeat-001",
        "dimensions": ["domain", "carrier_kind"]
      },
      "input_refs": ["input/transfer-001"],
      "output_refs": ["output/transfer-001"],
      "transformation_id": "transform/replay-edge",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/existing"],
      "generated_operations": [],
      "provenance_refs": ["source/transfer-001"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/generate-001",
      "receipt_id": "receipt/generate-001",
      "role": "GENERATE",
      "candidate_ref": "candidate/replay-edge",
      "candidate_digest": "sha256:replay-edge-v1",
      "context_fingerprint": {
        "domain": "trace",
        "carrier_kind": "ordered",
        "probe_kind": "first-difference"
      },
      "distinct_from": null,
      "input_refs": ["artifact/replay-source"],
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
      "provenance_refs": ["source/generate-001"],
      "residuals": []
    }
  ]
}
```

Expected final result: `PATTERN`, `RETAIN`, reasons `TRANSFER_CONTEXT_NOT_DISTINCT` then `DELTA_OMEGA_EMPTY`.

- [ ] **Step 2: Create `novel-output-no-new-verb.json` exactly as follows**

```json
{
  "schema": "dogram.phaselift.specimen/v0",
  "candidate_id": "candidate/novel-output",
  "candidate_version": 1,
  "trials": [
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/repeat-002",
      "receipt_id": "receipt/repeat-002",
      "role": "REPEAT",
      "candidate_ref": "candidate/novel-output",
      "candidate_digest": "sha256:novel-output-v1",
      "context_fingerprint": {
        "domain": "sequence",
        "carrier_kind": "ordered_trace",
        "probe_kind": "boundary"
      },
      "distinct_from": null,
      "input_refs": ["input/repeat-002"],
      "output_refs": ["output/repeat-002"],
      "transformation_id": "transform/novel-output",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/a", "op/b"],
      "generated_operations": [],
      "provenance_refs": ["source/repeat-002"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/transfer-002",
      "receipt_id": "receipt/transfer-002",
      "role": "TRANSFER",
      "candidate_ref": "candidate/novel-output",
      "candidate_digest": "sha256:novel-output-v1",
      "context_fingerprint": {
        "domain": "graph",
        "carrier_kind": "directed_graph",
        "probe_kind": "boundary"
      },
      "distinct_from": {
        "trial_ref": "trial/repeat-002",
        "dimensions": ["domain", "carrier_kind"]
      },
      "input_refs": ["input/transfer-002"],
      "output_refs": ["output/transfer-002"],
      "transformation_id": "transform/novel-output",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/a", "op/b"],
      "generated_operations": [],
      "provenance_refs": ["source/transfer-002"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/generate-002",
      "receipt_id": "receipt/generate-002",
      "role": "GENERATE",
      "candidate_ref": "candidate/novel-output",
      "candidate_digest": "sha256:novel-output-v1",
      "context_fingerprint": {
        "domain": "composition",
        "carrier_kind": "value",
        "probe_kind": "novelty"
      },
      "distinct_from": null,
      "input_refs": ["value/a", "value/b"],
      "output_refs": ["value/never-seen-before"],
      "transformation_id": "transform/novel-output",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/a", "op/b"],
      "generated_operations": [],
      "provenance_refs": ["source/generate-002"],
      "residuals": []
    }
  ]
}
```

Expected final result: `TOOL`, `RETAIN`, reason `DELTA_OMEGA_EMPTY`.

- [ ] **Step 3: Create `self-minting-operator.json` exactly as follows**

```json
{
  "schema": "dogram.phaselift.specimen/v0",
  "candidate_id": "candidate/self-mint",
  "candidate_version": 1,
  "trials": [
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/repeat-003",
      "receipt_id": "receipt/repeat-003",
      "role": "REPEAT",
      "candidate_ref": "candidate/self-mint",
      "candidate_digest": "sha256:self-mint-v1",
      "context_fingerprint": {
        "domain": "sequence",
        "carrier_kind": "ordered_trace",
        "probe_kind": "promotion"
      },
      "distinct_from": null,
      "input_refs": ["input/repeat-003"],
      "output_refs": ["output/repeat-003"],
      "transformation_id": "transform/self-mint",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/a", "op/b"],
      "generated_operations": [],
      "provenance_refs": ["source/repeat-003"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/transfer-003",
      "receipt_id": "receipt/transfer-003",
      "role": "TRANSFER",
      "candidate_ref": "candidate/self-mint",
      "candidate_digest": "sha256:self-mint-v1",
      "context_fingerprint": {
        "domain": "graph",
        "carrier_kind": "directed_graph",
        "probe_kind": "promotion"
      },
      "distinct_from": {
        "trial_ref": "trial/repeat-003",
        "dimensions": ["domain", "carrier_kind"]
      },
      "input_refs": ["input/transfer-003"],
      "output_refs": ["output/transfer-003"],
      "transformation_id": "transform/self-mint",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/a", "op/b"],
      "generated_operations": [],
      "provenance_refs": ["source/transfer-003"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/generate-003",
      "receipt_id": "receipt/generate-003",
      "role": "GENERATE",
      "candidate_ref": "candidate/self-mint",
      "candidate_digest": "sha256:self-mint-v1",
      "context_fingerprint": {
        "domain": "composition",
        "carrier_kind": "typed_pair",
        "probe_kind": "promotion"
      },
      "distinct_from": null,
      "input_refs": ["artifact/a", "artifact/b"],
      "output_refs": ["artifact/self-promoting"],
      "transformation_id": "transform/self-mint",
      "transformation_version": 1,
      "composition_witnesses": [
        {
          "left_ref": "artifact/a",
          "verb_id": "verb/self-compose",
          "right_ref": "artifact/b",
          "phase": "PLUS_CO",
          "output_ref": "artifact/self-promoting",
          "left_capability_refs": ["op/a"],
          "right_capability_refs": ["op/b"],
          "output_capability_refs": ["op/a", "op/b", "op/promote-self"],
          "surplus_capability_refs": ["op/promote-self"]
        }
      ],
      "omega_before": ["op/a", "op/b"],
      "generated_operations": [
        {
          "operation_id": "op/promote-self",
          "operation_version": 1,
          "input_kinds": ["artifact", "artifact"],
          "output_kind": "promotion_claim",
          "derivation_refs": ["artifact/self-promoting", "phaselift/receipt-under-construction"],
          "replay_probe_ref": "probe/self-mint-independent"
        }
      ],
      "provenance_refs": ["source/generate-003"],
      "residuals": []
    }
  ]
}
```

Expected final result: `REFUSE`, reason `CIRCULAR_PROMOTION_PROOF`; no local promotion survives the cycle override.

- [ ] **Step 4: Create `lawful-new-verb.json` exactly as follows**

```json
{
  "schema": "dogram.phaselift.specimen/v0",
  "candidate_id": "candidate/bind-route",
  "candidate_version": 1,
  "trials": [
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/repeat-004",
      "receipt_id": "receipt/repeat-004",
      "role": "REPEAT",
      "candidate_ref": "candidate/bind-route",
      "candidate_digest": "sha256:bind-route-v1",
      "context_fingerprint": {
        "domain": "sequence",
        "carrier_kind": "ordered_trace",
        "probe_kind": "binding"
      },
      "distinct_from": null,
      "input_refs": ["input/repeat-004"],
      "output_refs": ["output/repeat-004"],
      "transformation_id": "transform/bind-route",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/bind", "op/route"],
      "generated_operations": [],
      "provenance_refs": ["source/repeat-004"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/transfer-004",
      "receipt_id": "receipt/transfer-004",
      "role": "TRANSFER",
      "candidate_ref": "candidate/bind-route",
      "candidate_digest": "sha256:bind-route-v1",
      "context_fingerprint": {
        "domain": "graph",
        "carrier_kind": "directed_graph",
        "probe_kind": "binding"
      },
      "distinct_from": {
        "trial_ref": "trial/repeat-004",
        "dimensions": ["domain", "carrier_kind"]
      },
      "input_refs": ["input/transfer-004"],
      "output_refs": ["output/transfer-004"],
      "transformation_id": "transform/bind-route",
      "transformation_version": 1,
      "composition_witnesses": [],
      "omega_before": ["op/bind", "op/route"],
      "generated_operations": [],
      "provenance_refs": ["source/transfer-004"],
      "residuals": []
    },
    {
      "schema": "dogram.phaselift.trial/v0",
      "trial_id": "trial/generate-004",
      "receipt_id": "receipt/generate-004",
      "role": "GENERATE",
      "candidate_ref": "candidate/bind-route",
      "candidate_digest": "sha256:bind-route-v1",
      "context_fingerprint": {
        "domain": "composition",
        "carrier_kind": "typed_pair",
        "probe_kind": "binding"
      },
      "distinct_from": null,
      "input_refs": ["artifact/bind-plan", "artifact/route-plan"],
      "output_refs": ["artifact/bound-route"],
      "transformation_id": "transform/bind-route",
      "transformation_version": 1,
      "composition_witnesses": [
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
      ],
      "omega_before": ["op/bind", "op/route"],
      "generated_operations": [
        {
          "operation_id": "op/bind-and-route",
          "operation_version": 1,
          "input_kinds": ["binding", "route"],
          "output_kind": "bound_route",
          "derivation_refs": ["artifact/bound-route", "receipt/generate-004"],
          "replay_probe_ref": "probe/bind-and-route-independent"
        }
      ],
      "provenance_refs": ["source/generate-004"],
      "residuals": []
    }
  ]
}
```

Expected final result: `OPERATOR_CANDIDATE`, `PROMOTE`, `delta_omega == ["op/bind-and-route"]`, `public_operator_admission == false`.

- [ ] **Step 5: Create the first focused test**

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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 6: Run the test and verify RED**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_lawful_new_verb_promotes_one_local_operator_candidate -v
```

Expected: `ModuleNotFoundError: No module named 'dogram.phaselift'`.

- [ ] **Step 7: Create only the importable production skeleton**

```python
from __future__ import annotations

from typing import Any


def evaluate_phaselift(
    specimen: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    raise NotImplementedError("PHASELIFT-3 evaluator not implemented")


__all__ = ["evaluate_phaselift"]
```

- [ ] **Step 8: Re-run and verify RED moved to the intended function**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_lawful_new_verb_promotes_one_local_operator_candidate -v
```

Expected: `NotImplementedError: PHASELIFT-3 evaluator not implemented`.

- [ ] **Step 9: Commit the conformance corpus**

```bash
git add dogram/phaselift.py tests/test_phaselift.py tests/fixtures/phaselift
git commit -m "test: freeze PHASELIFT promotion corpus"
```

---

### Task 2: Implement schema, attribution, identity, repeat, and transfer

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: exact Task 1 specimen/trial envelopes.
- Produces: deterministic trial mapping, `recurs`, `transfers`, and earned class through `TOOL`.

- [ ] **Step 1: Add these tests inside `PhaseLiftTests`**

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
        specimen["trials"] = [
            trial for trial in specimen["trials"] if trial["role"] != "GENERATE"
        ]
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
        self.assertEqual(result["reason_codes"], ["CANDIDATE_IDENTITY_CHANGED"])

    def test_transformation_change_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][1]["transformation_id"] = "transform/different"
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertEqual(result["reason_codes"], ["TRANSFORMATION_IDENTITY_CHANGED"])
```

- [ ] **Step 2: Run the focused module and verify RED**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: tests fail because the evaluator still raises `NotImplementedError`.

- [ ] **Step 3: Replace the skeleton with constants and deterministic helpers**

```python
from __future__ import annotations

from typing import Any

SPECIMEN_SCHEMA = "dogram.phaselift.specimen/v0"
TRIAL_SCHEMA = "dogram.phaselift.trial/v0"
RECEIPT_SCHEMA = "dogram.phaselift.receipt/v0"
PENDING_RECEIPT_REF = "phaselift/receipt-under-construction"
REQUIRED_ROLES = ("REPEAT", "TRANSFER", "GENERATE")
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
REASON_RANK = {reason: index for index, reason in enumerate(REASON_ORDER)}


def _ordered_reasons(reasons: set[str]) -> list[str]:
    return sorted(reasons, key=lambda reason: (REASON_RANK.get(reason, 10_000), reason))


def _empty_checks() -> dict[str, bool]:
    return {
        "recurs": False,
        "transfers": False,
        "composes": False,
        "generates": False,
        "non_circular": True,
        "provenance_complete": True,
    }
```

- [ ] **Step 4: Implement `_decode_trial_roles` with exactly these outcomes**

```python
def _decode_trial_roles(specimen: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], str | None, str | None]:
    if specimen.get("schema") != SPECIMEN_SCHEMA:
        return {}, "REFUSE", "SCHEMA_INVALID"
    trials = specimen.get("trials")
    if not isinstance(trials, list):
        return {}, "REFUSE", "SCHEMA_INVALID"

    role_map: dict[str, dict[str, Any]] = {}
    seen_trial_ids: set[str] = set()
    seen_receipt_ids: set[str] = set()
    for trial in trials:
        if not isinstance(trial, dict) or trial.get("schema") != TRIAL_SCHEMA:
            return {}, "REFUSE", "SCHEMA_INVALID"
        role = trial.get("role")
        trial_id = trial.get("trial_id")
        receipt_id = trial.get("receipt_id")
        if role not in REQUIRED_ROLES or not isinstance(trial_id, str) or not isinstance(receipt_id, str):
            return {}, "REFUSE", "SCHEMA_INVALID"
        if role in role_map or trial_id in seen_trial_ids or receipt_id in seen_receipt_ids:
            return {}, "REFUSE", "DUPLICATE_TRIAL_RECEIPT"
        role_map[role] = trial
        seen_trial_ids.add(trial_id)
        seen_receipt_ids.add(receipt_id)

    if any(role not in role_map for role in REQUIRED_ROLES):
        return role_map, "INSUFFICIENT_TO_TEST", "MISSING_TRIAL"
    return role_map, None, None
```

- [ ] **Step 5: Implement identity and provenance checks**

```python
def _identity_reason(specimen: dict[str, Any], trials: dict[str, dict[str, Any]]) -> str | None:
    candidate_id = specimen.get("candidate_id")
    candidate_refs = {trial.get("candidate_ref") for trial in trials.values()}
    candidate_digests = {trial.get("candidate_digest") for trial in trials.values()}
    if candidate_refs != {candidate_id} or len(candidate_digests) != 1 or None in candidate_digests:
        return "CANDIDATE_IDENTITY_CHANGED"

    transforms = {
        (trial.get("transformation_id"), trial.get("transformation_version"))
        for trial in trials.values()
    }
    if len(transforms) != 1 or next(iter(transforms))[0] in (None, ""):
        return "TRANSFORMATION_IDENTITY_CHANGED"
    return None


def _provenance_complete(trials: dict[str, dict[str, Any]]) -> bool:
    for trial in trials.values():
        refs = trial.get("provenance_refs")
        outputs = trial.get("output_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref for ref in refs):
            return False
        if not isinstance(outputs, list) or not outputs or not all(isinstance(ref, str) and ref for ref in outputs):
            return False
    return True
```

- [ ] **Step 6: Implement transfer distinction**

```python
def _transfer_distinct(repeat: dict[str, Any], transfer: dict[str, Any]) -> tuple[bool, list[str]]:
    distinct = transfer.get("distinct_from")
    if not isinstance(distinct, dict) or distinct.get("trial_ref") != repeat.get("trial_id"):
        return False, ["TRANSFER_CONTEXT_NOT_DISTINCT:trial_ref"]
    dimensions = distinct.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions or not all(isinstance(item, str) and item for item in dimensions):
        return False, ["TRANSFER_CONTEXT_NOT_DISTINCT:dimensions"]
    left = repeat.get("context_fingerprint")
    right = transfer.get("context_fingerprint")
    if not isinstance(left, dict) or not isinstance(right, dict):
        return False, ["TRANSFER_CONTEXT_NOT_DISTINCT:fingerprint"]
    failures = [
        dimension
        for dimension in dimensions
        if dimension not in left or dimension not in right or left[dimension] == right[dimension]
    ]
    return not failures, [f"TRANSFER_CONTEXT_NOT_DISTINCT:{item}" for item in sorted(failures)]
```

- [ ] **Step 7: Implement the evaluator through the transfer boundary**

At this stage `evaluate_phaselift` must:

1. initialize empty checks/reasons/residuals;
2. decode role trials;
3. return deterministic `REFUSE` or `INSUFFICIENT_TO_TEST` result/receipt-shaped placeholder for early schema/material failures;
4. refuse identity drift;
5. refuse incomplete provenance;
6. set `recurs=True` after valid repeat structure;
7. evaluate transfer distinction;
8. earn `PATTERN` when repeat passes but transfer fails;
9. earn `TOOL` when repeat and transfer pass;
10. leave generation/composition false until Task 3.

Use this exact class helper:

```python
def _earned_class(checks: dict[str, bool]) -> str:
    if not checks["recurs"]:
        return "REMNANT"
    if not checks["transfers"]:
        return "PATTERN"
    if not (checks["generates"] and checks["composes"]):
        return "TOOL"
    return "OPERATOR_CANDIDATE"
```

- [ ] **Step 8: Run and verify the transfer-floor tests**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: missing/duplicate/identity/three-echoes/novel-output class tests pass. The positive promotion test remains RED because generation is not implemented.

- [ ] **Step 9: Commit**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: evaluate PHASELIFT repeat and transfer"
```

---

### Task 3: Implement finite grammar growth and lawful `PLUS_CO` composition

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: valid `GENERATE` trial.
- Produces: `omega_before`, `omega_after`, `delta_omega`, `generates`, `composes`, and local `PROMOTE` before circularity pressure.

- [ ] **Step 1: Add these failing tests**

```python
    def test_novel_value_without_new_operation_does_not_generate(self):
        result, _ = evaluate_phaselift(self.load("novel-output-no-new-verb.json"))
        self.assertFalse(result["checks"]["generates"])
        self.assertEqual(result["delta_omega"], [])
        self.assertEqual(result["reason_codes"], ["DELTA_OMEGA_EMPTY"])
        self.assertEqual(result["earned_class"], "TOOL")

    def test_plus_co_requires_explicit_verb(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["composition_witnesses"][0]["verb_id"] = ""
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "RETAIN")
        self.assertIn("PLUS_CO_MISSING_VERB", result["reason_codes"])

    def test_composition_requires_source_attribution(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["composition_witnesses"][0]["left_ref"] = "artifact/not-an-input"
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertIn("COMPOSITION_ATTRIBUTION_INCOMPLETE", result["reason_codes"])

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
        self.assertTrue(result["checks"]["generates"])
        self.assertTrue(result["checks"]["composes"])
        self.assertEqual(result["earned_class"], "OPERATOR_CANDIDATE")
```

- [ ] **Step 2: Run these tests and verify RED**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: generation/composition assertions fail.

- [ ] **Step 3: Add generated-operation validation**

```python
def _valid_generated_operation(operation: Any) -> bool:
    if not isinstance(operation, dict):
        return False
    if not isinstance(operation.get("operation_id"), str) or not operation["operation_id"]:
        return False
    if type(operation.get("operation_version")) is not int or operation["operation_version"] < 1:
        return False
    input_kinds = operation.get("input_kinds")
    if not isinstance(input_kinds, list) or not input_kinds or not all(isinstance(item, str) and item for item in input_kinds):
        return False
    if not isinstance(operation.get("output_kind"), str) or not operation["output_kind"]:
        return False
    derivation_refs = operation.get("derivation_refs")
    if not isinstance(derivation_refs, list) or not derivation_refs or not all(isinstance(item, str) and item for item in derivation_refs):
        return False
    return isinstance(operation.get("replay_probe_ref"), str) and bool(operation["replay_probe_ref"])
```

Malformed generated operation => `REFUSE / GENERATED_OPERATION_INVALID`.

- [ ] **Step 4: Compute finite grammar growth exactly**

```python
def _grammar_growth(generate: dict[str, Any]) -> tuple[list[str], list[str], list[str], str | None]:
    omega_raw = generate.get("omega_before")
    operations_raw = generate.get("generated_operations")
    if not isinstance(omega_raw, list) or not all(isinstance(item, str) and item for item in omega_raw):
        return [], [], [], "SCHEMA_INVALID"
    if not isinstance(operations_raw, list):
        return [], [], [], "SCHEMA_INVALID"
    if any(not _valid_generated_operation(operation) for operation in operations_raw):
        return [], [], [], "GENERATED_OPERATION_INVALID"
    omega_before = sorted(set(omega_raw))
    generated_ids = sorted({operation["operation_id"] for operation in operations_raw})
    omega_after = sorted(set(omega_before) | set(generated_ids))
    delta_omega = sorted(set(omega_after) - set(omega_before))
    return omega_before, omega_after, delta_omega, None
```

If `delta_omega` is empty, add `DELTA_OMEGA_EMPTY`, set `generates=False`, and do not add a secondary `COMPOSITIONAL_SURPLUS_EMPTY` reason.

- [ ] **Step 5: Add composition validation helpers**

```python
def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        return None
    return value


def _composition_check(
    generate: dict[str, Any],
    delta_omega: list[str],
) -> tuple[bool, str | None, list[str]]:
    witnesses = generate.get("composition_witnesses")
    if not isinstance(witnesses, list):
        return False, "SCHEMA_INVALID", []
    inputs = set(generate.get("input_refs", []))
    outputs = set(generate.get("output_refs", []))
    delta = set(delta_omega)
    saw_plus_co = False

    for witness in witnesses:
        if not isinstance(witness, dict):
            return False, "SCHEMA_INVALID", []
        if witness.get("phase") != "PLUS_CO":
            continue
        saw_plus_co = True
        if not isinstance(witness.get("verb_id"), str) or not witness["verb_id"]:
            return False, "PLUS_CO_MISSING_VERB", []
        left_ref = witness.get("left_ref")
        right_ref = witness.get("right_ref")
        output_ref = witness.get("output_ref")
        if left_ref not in inputs or right_ref not in inputs or output_ref not in outputs:
            return False, "COMPOSITION_ATTRIBUTION_INCOMPLETE", []

        left_caps = _string_list(witness.get("left_capability_refs"))
        right_caps = _string_list(witness.get("right_capability_refs"))
        output_caps = _string_list(witness.get("output_capability_refs"))
        declared_surplus = _string_list(witness.get("surplus_capability_refs"))
        if None in (left_caps, right_caps, output_caps, declared_surplus):
            return False, "COMPOSITION_ATTRIBUTION_INCOMPLETE", []

        computed = set(output_caps) - (set(left_caps) | set(right_caps))
        declared = set(declared_surplus)
        if declared and declared <= computed and bool(declared & delta):
            return True, None, sorted(declared)

    if saw_plus_co:
        return False, "COMPOSITIONAL_SURPLUS_EMPTY", []
    return False, "COMPOSITIONAL_SURPLUS_EMPTY", []
```

- [ ] **Step 6: Integrate generation into `evaluate_phaselift`**

After repeat/transfer succeed:

- compute grammar growth;
- if generated-operation validation fails, `REFUSE`;
- if `delta_omega` empty, add `DELTA_OMEGA_EMPTY` and retain `TOOL`;
- otherwise set `generates=True` and run composition check;
- `PLUS_CO_MISSING_VERB` => `RETAIN`;
- `COMPOSITION_ATTRIBUTION_INCOMPLETE` => `REFUSE`;
- `COMPOSITIONAL_SURPLUS_EMPTY` => `RETAIN`;
- valid surplus intersecting `delta_omega` => `composes=True`;
- `generates=True` plus `composes=True` earns `OPERATOR_CANDIDATE` and preliminary `PROMOTE`.

- [ ] **Step 7: Run and verify GREEN for all non-cycle tests**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: every Task 1-3 assertion passes. The self-minting fixture has not yet been asserted.

- [ ] **Step 8: Commit**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: evaluate PHASELIFT grammar growth"
```

---

### Task 4: Refuse self-certifying proof cycles

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: finite proof dependencies already present in the specimen.
- Produces: `checks.non_circular` and a constitutional `REFUSE` override.

- [ ] **Step 1: Add these cycle tests**

```python
    def test_self_minting_operation_is_refused_as_circular(self):
        result, _ = evaluate_phaselift(self.load("self-minting-operator.json"))
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertFalse(result["checks"]["non_circular"])
        self.assertEqual(result["reason_codes"], ["CIRCULAR_PROMOTION_PROOF"])

    def test_indirect_cycle_through_replay_probe_is_refused(self):
        specimen = self.load("lawful-new-verb.json")
        specimen["trials"][2]["generated_operations"][0]["replay_probe_ref"] = (
            "phaselift/receipt-under-construction"
        )
        result, _ = evaluate_phaselift(specimen)
        self.assertEqual(result["disposition"], "REFUSE")
        self.assertFalse(result["checks"]["non_circular"])
        self.assertIn("CIRCULAR_PROMOTION_PROOF", result["reason_codes"])
```

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_phaselift.PhaseLiftTests.test_self_minting_operation_is_refused_as_circular tests.test_phaselift.PhaseLiftTests.test_indirect_cycle_through_replay_probe_is_refused -v
```

Expected: current evaluator promotes the otherwise-valid cycle specimen.

- [ ] **Step 3: Build the bounded dependency graph**

```python
def _proof_graph(trials: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {
        PENDING_RECEIPT_REF: {trials[role]["trial_id"] for role in REQUIRED_ROLES}
    }
    for trial in trials.values():
        trial_id = trial["trial_id"]
        deps = graph.setdefault(trial_id, set())
        deps.update(trial.get("provenance_refs", []))
        deps.update(trial.get("output_refs", []))
        for witness in trial.get("composition_witnesses", []):
            output_ref = witness.get("output_ref")
            if isinstance(output_ref, str) and output_ref:
                deps.add(output_ref)
                graph.setdefault(output_ref, set()).update(
                    ref
                    for ref in (
                        witness.get("left_ref"),
                        witness.get("right_ref"),
                    )
                    if isinstance(ref, str) and ref
                )
                graph[output_ref].update(witness.get("surplus_capability_refs", []))
        for operation in trial.get("generated_operations", []):
            operation_id = operation.get("operation_id")
            if not isinstance(operation_id, str) or not operation_id:
                continue
            deps.add(operation_id)
            graph.setdefault(operation_id, set()).update(operation.get("derivation_refs", []))
            probe = operation.get("replay_probe_ref")
            if isinstance(probe, str) and probe:
                graph[operation_id].add(probe)
    return graph
```

- [ ] **Step 4: Add deterministic cycle detection rooted at the pending receipt**

```python
def _pending_receipt_is_cyclic(graph: dict[str, set[str]]) -> bool:
    def visit(node: str, active: set[str], seen: set[str]) -> bool:
        if node in active:
            return node == PENDING_RECEIPT_REF
        if node in seen:
            return False
        active.add(node)
        for neighbor in sorted(graph.get(node, set())):
            if neighbor == PENDING_RECEIPT_REF:
                return True
            if visit(neighbor, active, seen):
                return True
        active.remove(node)
        seen.add(node)
        return False

    return visit(PENDING_RECEIPT_REF, set(), set())
```

The evaluator does not interpret unrelated graph cycles as metaphysical or semantic failure. This slice asks only whether the proof depends on the receipt being computed.

- [ ] **Step 5: Apply the constitutional override**

After all ordinary checks:

```python
graph = _proof_graph(trials)
if _pending_receipt_is_cyclic(graph):
    checks["non_circular"] = False
    reasons.add("CIRCULAR_PROMOTION_PROOF")
    residuals.add(f"CIRCULAR_PROMOTION_PROOF:{PENDING_RECEIPT_REF}")
    disposition = "REFUSE"
```

`REFUSE` overrides a preliminary `PROMOTE`.

- [ ] **Step 6: Run all PHASELIFT tests and verify GREEN**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: all Task 1-4 tests pass.

- [ ] **Step 7: Commit**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: refuse circular PHASELIFT proofs"
```

---

### Task 5: Canonicalize receipts and prove deterministic replay

**Files:**
- Modify: `dogram/phaselift.py`
- Modify: `tests/test_phaselift.py`

**Interfaces:**
- Consumes: final evaluation state plus `sha256_json`.
- Produces: stable `dogram.phaselift.receipt/v0` and deterministic replay.

- [ ] **Step 1: Add these receipt tests**

```python
    def test_same_specimen_replays_to_identical_result_and_receipt(self):
        specimen = self.load("lawful-new-verb.json")
        self.assertEqual(evaluate_phaselift(specimen), evaluate_phaselift(specimen))

    def test_receipt_digest_hashes_unsigned_receipt(self):
        from dogram.canonical import sha256_json

        _, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
        unsigned = dict(receipt)
        digest = unsigned.pop("receipt_digest")
        self.assertEqual(digest, sha256_json(unsigned))

    def test_receipt_preserves_role_refs(self):
        _, receipt = evaluate_phaselift(self.load("lawful-new-verb.json"))
        self.assertEqual(
            receipt["trial_refs"],
            {
                "repeat": "trial/repeat-004",
                "transfer": "trial/transfer-004",
                "generate": "trial/generate-004",
            },
        )

    def test_every_frozen_disposition_denies_public_operator_admission(self):
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

- [ ] **Step 2: Run and verify RED on missing canonical fields**

```bash
python -m unittest tests.test_phaselift -v
```

Expected: receipt digest/role-ref assertions fail until final receipt construction is wired.

- [ ] **Step 3: Import canonical hashing and construct result deterministically**

```python
from .canonical import sha256_json
```

Before return:

```python
result = {
    "candidate_id": candidate_id,
    "earned_class": earned_class,
    "disposition": disposition,
    "checks": {
        "recurs": checks["recurs"],
        "transfers": checks["transfers"],
        "composes": checks["composes"],
        "generates": checks["generates"],
        "non_circular": checks["non_circular"],
        "provenance_complete": checks["provenance_complete"],
    },
    "omega_before": sorted(set(omega_before)),
    "omega_after": sorted(set(omega_after)),
    "delta_omega": sorted(set(delta_omega)),
    "reason_codes": _ordered_reasons(reasons),
    "residuals": sorted(residuals),
    "public_operator_admission": False,
}
```

- [ ] **Step 4: Build the receipt without self-hashing**

```python
trial_refs = {
    "repeat": trials.get("REPEAT", {}).get("trial_id"),
    "transfer": trials.get("TRANSFER", {}).get("trial_id"),
    "generate": trials.get("GENERATE", {}).get("trial_id"),
}
unsigned_receipt = {
    "schema": RECEIPT_SCHEMA,
    "candidate_id": candidate_id,
    "candidate_version": specimen.get("candidate_version"),
    "input_digest": sha256_json(specimen),
    "trial_refs": trial_refs,
    **result,
}
receipt = {
    **unsigned_receipt,
    "receipt_digest": sha256_json(unsigned_receipt),
}
return result, receipt
```

Early `REFUSE` and `INSUFFICIENT_TO_TEST` paths must use the same receipt builder; a missing role maps to `None` in `trial_refs` rather than suppressing the receipt.

- [ ] **Step 5: Ensure top-level dispositions follow one precedence table**

Implement this exact precedence:

```text
1. Missing role material -> INSUFFICIENT_TO_TEST
2. Schema / duplicate / identity / provenance / generated-operation / attribution failure -> REFUSE
3. Pending-receipt proof cycle -> REFUSE
4. Full repeat + transfer + generate + compose -> PROMOTE
5. Otherwise -> RETAIN
```

No later successful check may overwrite an earlier `REFUSE`.

- [ ] **Step 6: Run focused and full suites**

```bash
python -m unittest tests.test_phaselift -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit**

```bash
git add dogram/phaselift.py tests/test_phaselift.py
git commit -m "feat: receipt PHASELIFT promotion decisions"
```

---

### Task 6: Receipt the research slice and verify no public-surface drift

**Files:**
- Create: `research/phaselift-3-promotion-kernel.md`
- Verify only: `dogram/engine.py`
- Verify only: `dogram/cli.py`
- Verify only: `dogram/registry.py`
- Verify only: `pyproject.toml`

**Interfaces:**
- Consumes: completed evaluator and green corpus.
- Produces: durable research note plus branch-level verification evidence.

- [ ] **Step 1: Create `research/phaselift-3-promotion-kernel.md` exactly as follows**

```markdown
# PHASELIFT-3 Promotion Kernel

PHASELIFT-3 is an internal deterministic research evaluator for one bounded question:

> Did a caller-declared candidate satisfy the local REPEAT -> TRANSFER -> GENERATE -> LIFT contract under supplied attributable trials?

It does not discover candidates, infer semantic importance, mint evidence or truth, mutate the runtime, or admit public Dogram operators.

## Frozen controls

- `three-echoes.json`: recurrence survives; transfer and generation do not.
- `novel-output-no-new-verb.json`: transfer survives; novel value does not enlarge executable grammar.
- `self-minting-operator.json`: apparent generativity is refused because the proof depends on the receipt being computed.
- `lawful-new-verb.json`: one attributable `PLUS_CO` composition yields exactly one new finite operation identity with an independent replay probe.

## Local law

`PROMOTE != PUBLIC OPERATOR ADMISSION`

The evaluator's only authority is to report whether its bounded declared promotion contract passed.
```

- [ ] **Step 2: Run complete verification**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Expected: all tests pass; compile exits 0.

- [ ] **Step 3: Verify the public runtime surface stayed untouched**

```bash
git diff main...HEAD -- dogram/engine.py dogram/cli.py dogram/registry.py pyproject.toml
```

Expected: no diff.

- [ ] **Step 4: Verify final scope**

```bash
git diff --stat main...HEAD
git status --short
```

Expected executable/research additions beyond the approved design/plan docs:

```text
dogram/phaselift.py
tests/test_phaselift.py
tests/fixtures/phaselift/lawful-new-verb.json
tests/fixtures/phaselift/novel-output-no-new-verb.json
tests/fixtures/phaselift/self-minting-operator.json
tests/fixtures/phaselift/three-echoes.json
research/phaselift-3-promotion-kernel.md
```

- [ ] **Step 5: Commit the research receipt**

```bash
git add research/phaselift-3-promotion-kernel.md
git commit -m "docs: receipt PHASELIFT-3 research kernel"
```

---

## Acceptance Mapping

| Specification requirement | Proof in this plan |
| --- | --- |
| Four public operators unchanged | Task 6 public-surface diff |
| Pure deterministic evaluator | Tasks 2-5 plus replay test |
| Four frozen fixtures exact dispositions | Tasks 1-4 |
| Three aliases cannot satisfy three roles | Task 2 duplicate receipt test |
| Novel output without `delta_omega` cannot promote | Task 3 novel-output test |
| Fake context rename cannot satisfy transfer | Task 2 plus `three-echoes` |
| `PLUS_CO` without verb cannot compose | Task 3 explicit-verb test |
| Source attribution cannot be silently dropped | Task 3 attribution test |
| Self-referential proof is refused | Task 4 |
| Positive fixture produces exactly one new operation | Tasks 1 and 3 |
| Promotion is never public admission | Tasks 1 and 5 |
| Existing suite remains green | Tasks 5 and 6 |

## Plan Self-Review

- Every frozen fixture is present byte-for-byte in this plan.
- Every production behavior begins with an explicit failing test.
- No task requires a third-party package or ambient service.
- `delta_omega` derives only from finite declared operation identities.
- Novel output values never affect grammar-growth calculation.
- `PLUS_CO` requires an explicit verb, source attribution, and non-empty computed surplus intersecting `delta_omega`.
- The proof-cycle detector makes only the bounded self-certification claim defined by the design.
- The receipt digest hashes the unsigned receipt exactly once.
- `PROMOTE` cannot mutate Dogram registry, engine dispatch, CLI, or public operator floor.
