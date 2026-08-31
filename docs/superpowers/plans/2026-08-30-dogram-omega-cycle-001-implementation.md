# Dogram Ω-CYCLE-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Dogram's first complete bounded metaoscillation: `EXEC -> REIFY -> META -> PROPOSAL -> PHASE GATE -> EXEC`, with exact execution provenance and no expansion of Dogram's public authority or operator floor.

**Architecture:** Extend the existing deterministic Mathal VM with exact runtime-resolved input provenance, then place a strict inert reification membrane over `Program` and `VMExecution`. Add a single proposal grammar (`program_patch/remove_step`), a structural host gate, one native zero-step META mathal that only copies declared data into a proposal, and a one-cycle orchestrator that re-executes an admitted candidate and compares pre/post results through the native DELTA path.

**Tech Stack:** Python 3.12 stdlib only; `unittest`; canonical JSON + SHA-256 from `dogram.canonical`; existing `dogram.program/v0` Mathal VM; existing bootstrap registry and `stdlib/delta.mathal.json`.

**Spec:** `docs/superpowers/specs/2026-08-30-dogram-omega-cycle-001-design.md`

## Global Constraints

- Keep project dependencies exactly `[]`.
- Keep public `dogram.engine.OPERATORS` exactly `{("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)}`.
- Ω-CYCLE-001 admits exactly one proposal family: `program_patch/remove_step`.
- `NoChange`, `Stop`, branching, composition, peeling, recursive mathal calls, cyclic programs, arbitrary synthesis, and host-intrinsic removal remain out of scope.
- META receives canonical JSON-compatible inert data only; it never receives a live `Program`, `Registry`, callable, exception object, module, file handle, or ambient capability.
- Runtime provenance records only input addresses actually resolved successfully during the execution; syntactic presence is not consumption.
- A failed address resolution must not record the unavailable address as consumed.
- An intrinsic refusal after successful argument resolution must retain those successfully resolved addresses in execution provenance.
- META never selects which step to remove; `declared_target_step` is caller/specimen input.
- Every proposal binds to the exact `base_program_digest` and exact `base_execution_digest`.
- The phase gate performs structural admission only. `GATE ADMIT != EQUIVALENT PROGRAM`.
- Ω-CYCLE-001 permits exactly one META cycle. No recursive orchestrator invocation.
- Reification must fail closed on non-canonical/capability-shaped artifacts; no `repr()` fallback.
- Identical program + input + configs + declared target + proposal id must produce byte-stable cycle receipts.

---

## File Structure

The implementation should keep each responsibility isolated:

- Modify `dogram/vm_types.py` — add exact aggregate consumed-input provenance to `VMExecution`.
- Modify `dogram/vm.py` — collect successful input-address resolutions during execution, including refusal paths.
- Create `dogram/reify.py` — canonical `ProgramData` / `ExecutionData` construction and execution digesting; fail-closed membrane.
- Create `dogram/proposal.py` — strict `dogram.proposal/v0` decoder/encoder for `program_patch/remove_step` only.
- Create `dogram/gate.py` — structural phase gate and `GateDisposition`.
- Create `dogram/stdlib/meta_remove_declared_step.mathal.json` — native META program that constructs a proposal from declared inert inputs without new intrinsics.
- Create `dogram/omega.py` — exactly-one-cycle orchestration and inert cycle receipt.
- Create `tests/test_reify.py`, `tests/test_proposal.py`, `tests/test_gate.py`, `tests/test_meta_mathal.py`, `tests/test_omega.py`.
- Modify `tests/test_vm.py` — provenance behavior and refusal-path coverage.
- Create frozen JSON fixtures under `tests/fixtures/omega/` for positive, result-changing, dangling-step, dangling-result, stale ancestry, target-not-found, and malformed-proposal cases.
- Modify `.github/workflows/ci.yml` — preserve existing constitutional checks and add exact bootstrap-registry assertion; no new dependency or public operator.
- Modify `README.md` only after the executable cycle is green, adding a factual implementation-status sentence without changing Dogram's authority boundary.

---

### Task 1: Record Exact Runtime-Resolved Input Provenance

**Files:**
- Modify: `dogram/vm_types.py`
- Modify: `dogram/vm.py`
- Modify: `tests/test_vm.py`

**Interfaces:**
- Produces: `VMExecution.consumed_input_addresses: tuple[tuple[str | int, ...], ...]`
- Produces: `VMExecution.to_data()["consumed_input_addresses"]` as `list[list[str | int]]`
- Preserves: existing `execute_program(program, inputs, registry, config=None) -> VMExecution`

- [ ] **Step 1: Write failing provenance tests**

Add these cases to `tests/test_vm.py`:

```python
def test_records_successfully_resolved_input_addresses_in_order(self):
    program = program_with_step(
        "core.same@1",
        [
            {"ref": "input", "path": ["left"]},
            {"ref": "input", "path": ["right"]},
        ],
    )
    result = execute_program(program, {"left": 7, "right": 7}, build_bootstrap_registry())
    self.assertEqual(result.status, "OK")
    self.assertEqual(result.consumed_input_addresses, (("left",), ("right",)))


def test_failed_input_path_is_not_recorded_as_consumed(self):
    program = program_with_step(
        "core.same@1",
        [
            {"ref": "input", "path": ["present"]},
            {"ref": "input", "path": ["missing"]},
        ],
    )
    result = execute_program(program, {"present": 1}, build_bootstrap_registry())
    self.assertEqual((result.status, result.reason_code), ("REFUSE", "ADDRESS_NOT_FOUND"))
    self.assertEqual(result.consumed_input_addresses, (("present",),))


def test_intrinsic_refusal_keeps_resolved_input_provenance(self):
    program = program_with_step(
        "core.select_first@1",
        [{"ref": "input", "path": ["items"]}],
    )
    result = execute_program(program, {"items": []}, build_bootstrap_registry())
    self.assertEqual((result.status, result.reason_code), ("REFUSE", "EMPTY_SEQUENCE"))
    self.assertEqual(result.consumed_input_addresses, (("items",),))


def test_repeated_resolution_occurrences_are_preserved(self):
    program = program_with_step(
        "core.same@1",
        [
            {"ref": "input", "path": ["x"]},
            {"ref": "input", "path": ["x"]},
        ],
    )
    result = execute_program(program, {"x": 5}, build_bootstrap_registry())
    self.assertEqual(result.consumed_input_addresses, (("x",), ("x",)))
```

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
python -m unittest tests.test_vm -v
```

Expected: new tests fail because `VMExecution` has no `consumed_input_addresses` field and `_resolve` does not collect resolution events.

- [ ] **Step 3: Implement minimal provenance collection**

In `dogram/vm_types.py`, extend `VMExecution`:

```python
@dataclass(frozen=True)
class VMExecution:
    status: str
    result: Any
    reason_code: str | None
    residuals: tuple[str, ...]
    step_trace: tuple[StepTrace, ...]
    consumed_input_addresses: tuple[tuple[str | int, ...], ...]
    fuel_remaining: int

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "result": self.result,
            "reason_code": self.reason_code,
            "residuals": list(self.residuals),
            "step_trace": [entry.to_data() for entry in self.step_trace],
            "consumed_input_addresses": [list(path) for path in self.consumed_input_addresses],
            "fuel_remaining": self.fuel_remaining,
        }
```

In `dogram/vm.py`, pass one ordered list through all resolution calls. Record an input path only after `_path_get` succeeds:

```python
def _resolve(value: Any, inputs: Any, step_results: dict[str, Any], consumed: list[tuple[str | int, ...]]) -> Any:
    if isinstance(value, list):
        return [_resolve(item, inputs, step_results, consumed) for item in value]
    if not isinstance(value, dict):
        return value
    if set(value) == {"literal"}:
        return value["literal"]
    if value.get("ref") == "input":
        path = tuple(value.get("path", []))
        resolved = _path_get(inputs, list(path))
        consumed.append(path)
        return resolved
    if value.get("ref") == "step":
        base = step_results[value["step"]]
        return _path_get(base, value.get("path", []))
    return {key: _resolve(item, inputs, step_results, consumed) for key, item in value.items()}
```

Update `_refuse(...)` to receive the current `consumed` list and copy it into the returned `VMExecution`. Update successful `VMExecution` construction likewise. Use the same collector for final-result resolution so direct `ref: input` results are included.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_vm -v
```

Expected: all VM tests pass; existing byte-stability test remains green with the new deterministic field.

- [ ] **Step 5: Commit**

```bash
git add dogram/vm.py dogram/vm_types.py tests/test_vm.py
git commit -m "feat: receipt exact VM input provenance"
```

---

### Task 2: Build the Reification Membrane

**Files:**
- Create: `dogram/reify.py`
- Create: `tests/test_reify.py`

**Interfaces:**
- Consumes: `Program`, `VMExecution`, `program_digest()`, `sha256_json()`
- Produces: `ReificationError(reason_code, residual)`
- Produces: `reify_program(program: Program) -> dict[str, Any]`
- Produces: `reify_execution(program: Program, inputs: Any, execution: VMExecution) -> dict[str, Any]`
- Produces: `execution_digest(execution_data: dict[str, Any]) -> str`

- [ ] **Step 1: Write failing reification tests**

Create `tests/test_reify.py` with at least:

```python
import unittest

from dogram.canonical import canonical_json_bytes
from dogram.program import decode_program, program_digest
from dogram.reify import ReificationError, execution_digest, reify_execution, reify_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import execute_program


class ReifyTests(unittest.TestCase):
    def setUp(self):
        self.program = decode_program({
            "schema": "dogram.program/v0",
            "program_id": "test/reify",
            "program_version": 1,
            "steps": [{
                "id": "s1",
                "op": "core.same@1",
                "args": [
                    {"ref": "input", "path": ["x"]},
                    {"literal": 1},
                ],
            }],
            "result": {"ref": "step", "step": "s1"},
        })

    def test_program_data_is_inert_and_digest_bound(self):
        data = reify_program(self.program)
        self.assertEqual(data["schema"], "dogram.program-data/v0")
        self.assertEqual(data["program_digest"], program_digest(self.program))
        canonical_json_bytes(data)

    def test_execution_data_preserves_exact_runtime_provenance(self):
        execution = execute_program(self.program, {"x": 1}, build_bootstrap_registry())
        data = reify_execution(self.program, {"x": 1}, execution)
        self.assertEqual(data["schema"], "dogram.execution-data/v0")
        self.assertEqual(data["consumed_input_addresses"], [["x"]])
        self.assertEqual(data["program_digest"], program_digest(self.program))

    def test_execution_digest_is_byte_stable(self):
        execution = execute_program(self.program, {"x": 1}, build_bootstrap_registry())
        first = reify_execution(self.program, {"x": 1}, execution)
        second = reify_execution(self.program, {"x": 1}, execution)
        self.assertEqual(execution_digest(first), execution_digest(second))

    def test_capability_shaped_input_fails_closed(self):
        execution = execute_program(self.program, {"x": 1}, build_bootstrap_registry())
        with self.assertRaises(ReificationError) as caught:
            reify_execution(self.program, {"x": lambda: None}, execution)
        self.assertEqual(caught.exception.reason_code, "NON_CANONICAL_ARTIFACT")
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_reify -v
```

Expected: import failure because `dogram.reify` does not exist.

- [ ] **Step 3: Implement fail-closed reification**

Create `dogram/reify.py`:

```python
from __future__ import annotations

from typing import Any

from .canonical import canonical_json_bytes, sha256_json
from .program import Program, encode_program, program_digest
from .vm_types import VMExecution


class ReificationError(ValueError):
    def __init__(self, reason_code: str, residual: str):
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


def _require_canonical(value: Any) -> None:
    try:
        canonical_json_bytes(value)
    except (TypeError, ValueError) as exc:
        raise ReificationError("NON_CANONICAL_ARTIFACT", str(exc)) from exc


def reify_program(program: Program) -> dict[str, Any]:
    data = {
        "schema": "dogram.program-data/v0",
        "program": encode_program(program),
        "program_digest": program_digest(program),
    }
    _require_canonical(data)
    return data


def reify_execution(program: Program, inputs: Any, execution: VMExecution) -> dict[str, Any]:
    _require_canonical(inputs)
    payload = execution.to_data()
    data = {
        "schema": "dogram.execution-data/v0",
        "program_digest": program_digest(program),
        "input_digest": sha256_json(inputs),
        **payload,
    }
    _require_canonical(data)
    return data


def execution_digest(execution_data: dict[str, Any]) -> str:
    _require_canonical(execution_data)
    return sha256_json(execution_data)
```

Do not catch errors by stringifying arbitrary values with `repr()`.

- [ ] **Step 4: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_reify -v
```

Expected: all reification tests pass.

- [ ] **Step 5: Commit**

```bash
git add dogram/reify.py tests/test_reify.py
git commit -m "feat: add inert execution reification membrane"
```

---

### Task 3: Add the Strict Proposal Envelope

**Files:**
- Create: `dogram/proposal.py`
- Create: `tests/test_proposal.py`

**Interfaces:**
- Produces: `ProposalDecodeError(reason_code, residual)`
- Produces: immutable `ProgramPatchProposal`
- Produces: `decode_proposal(data: Any) -> ProgramPatchProposal`
- Produces: `encode_proposal(proposal: ProgramPatchProposal) -> dict[str, Any]`

- [ ] **Step 1: Write failing proposal tests**

Create `tests/test_proposal.py`:

```python
import unittest

from dogram.proposal import ProposalDecodeError, decode_proposal, encode_proposal


VALID = {
    "schema": "dogram.proposal/v0",
    "proposal_id": "proposal-001",
    "proposal_version": 1,
    "kind": "program_patch",
    "base_program_digest": "sha256:program",
    "base_execution_digest": "sha256:execution",
    "payload": {"op": "remove_step", "step_id": "diagnostic"},
}


class ProposalTests(unittest.TestCase):
    def test_decodes_exact_remove_step_proposal(self):
        proposal = decode_proposal(VALID)
        self.assertEqual(proposal.step_id, "diagnostic")
        self.assertEqual(encode_proposal(proposal), VALID)

    def test_rejects_unknown_top_level_field(self):
        bad = {**VALID, "authority": "self-granted"}
        with self.assertRaises(ProposalDecodeError) as caught:
            decode_proposal(bad)
        self.assertEqual(caught.exception.reason_code, "MALFORMED_PROPOSAL")

    def test_rejects_unknown_kind(self):
        bad = {**VALID, "kind": "stop"}
        with self.assertRaises(ProposalDecodeError):
            decode_proposal(bad)

    def test_rejects_unknown_patch_operation(self):
        bad = {**VALID, "payload": {"op": "replace_program", "step_id": "diagnostic"}}
        with self.assertRaises(ProposalDecodeError):
            decode_proposal(bad)

    def test_rejects_extra_payload_fields(self):
        bad = {**VALID, "payload": {"op": "remove_step", "step_id": "diagnostic", "code": "eval(...)"}}
        with self.assertRaises(ProposalDecodeError):
            decode_proposal(bad)
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_proposal -v
```

Expected: import failure because `dogram.proposal` does not exist.

- [ ] **Step 3: Implement only `program_patch/remove_step`**

Create `dogram/proposal.py` with an immutable data class and strict key equality:

```python
from dataclasses import dataclass
from typing import Any


class ProposalDecodeError(ValueError):
    def __init__(self, reason_code: str, residual: str):
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


@dataclass(frozen=True)
class ProgramPatchProposal:
    proposal_id: str
    proposal_version: int
    base_program_digest: str
    base_execution_digest: str
    step_id: str


def decode_proposal(data: Any) -> ProgramPatchProposal:
    required = {
        "schema", "proposal_id", "proposal_version", "kind",
        "base_program_digest", "base_execution_digest", "payload",
    }
    if not isinstance(data, dict) or set(data) != required:
        raise ProposalDecodeError("MALFORMED_PROPOSAL", "invalid proposal envelope")
    if data.get("schema") != "dogram.proposal/v0" or data.get("kind") != "program_patch":
        raise ProposalDecodeError("MALFORMED_PROPOSAL", "unsupported proposal schema or kind")
    if not isinstance(data.get("proposal_id"), str) or not data["proposal_id"]:
        raise ProposalDecodeError("MALFORMED_PROPOSAL", "proposal_id must be non-empty")
    if type(data.get("proposal_version")) is not int or data["proposal_version"] != 1:
        raise ProposalDecodeError("MALFORMED_PROPOSAL", "proposal_version must equal 1")
    for key in ("base_program_digest", "base_execution_digest"):
        if not isinstance(data.get(key), str) or not data[key].startswith("sha256:"):
            raise ProposalDecodeError("MALFORMED_PROPOSAL", f"{key} must be a sha256 digest")
    payload = data.get("payload")
    if not isinstance(payload, dict) or set(payload) != {"op", "step_id"}:
        raise ProposalDecodeError("MALFORMED_PROPOSAL", "invalid patch payload")
    if payload.get("op") != "remove_step" or not isinstance(payload.get("step_id"), str) or not payload["step_id"]:
        raise ProposalDecodeError("MALFORMED_PROPOSAL", "only remove_step with a non-empty step_id is admitted")
    return ProgramPatchProposal(
        data["proposal_id"],
        data["proposal_version"],
        data["base_program_digest"],
        data["base_execution_digest"],
        payload["step_id"],
    )
```

Implement `encode_proposal()` as the exact inverse producing the strict envelope.

- [ ] **Step 4: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_proposal -v
```

Expected: all proposal tests pass.

- [ ] **Step 5: Commit**

```bash
git add dogram/proposal.py tests/test_proposal.py
git commit -m "feat: add strict Omega proposal envelope"
```

---

### Task 4: Implement the Structural Phase Gate

**Files:**
- Create: `dogram/gate.py`
- Create: `tests/test_gate.py`

**Interfaces:**
- Consumes: `ProgramPatchProposal`, `Program`, inert `ExecutionData`, `Registry`
- Produces: `GateLimits(max_program_steps: int = 1000)`
- Produces: `GateDisposition(status, reason_code, residuals, program, candidate_program_digest)`
- Produces: `phase_gate(proposal, current_program, execution_data, registry, limits=None) -> GateDisposition`

- [ ] **Step 1: Write failing gate tests**

Create `tests/test_gate.py` with helpers that build decoded programs and exact proposals. Cover at least:

```python
def test_admits_removal_of_unreferenced_step(self):
    disposition = phase_gate(proposal_for("diagnostic"), program, execution_data, registry)
    self.assertEqual(disposition.status, "ADMIT")
    self.assertEqual([step.id for step in disposition.program.steps], ["value"])


def test_refuses_stale_program_digest(self):
    proposal = replace(proposal_for("diagnostic"), base_program_digest="sha256:" + "0" * 64)
    disposition = phase_gate(proposal, program, execution_data, registry)
    self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "STALE_BASE_PROGRAM"))


def test_refuses_stale_execution_digest(self):
    proposal = replace(proposal_for("diagnostic"), base_execution_digest="sha256:" + "0" * 64)
    disposition = phase_gate(proposal, program, execution_data, registry)
    self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "STALE_BASE_EXECUTION"))


def test_refuses_missing_target(self):
    disposition = phase_gate(proposal_for("missing"), program, execution_data, registry)
    self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "TARGET_NOT_FOUND"))


def test_refuses_dangling_step_reference(self):
    disposition = phase_gate(proposal_for("source"), program_with_later_ref_to_source, execution_data, registry)
    self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "DANGLING_STEP_REFERENCE"))


def test_refuses_dangling_result_reference(self):
    disposition = phase_gate(proposal_for("value"), program, execution_data, registry)
    self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "DANGLING_RESULT_REFERENCE"))
```

Also test `GateLimits(max_program_steps=1)` against a candidate with two remaining steps and expect `PROGRAM_LIMIT_EXCEEDED`, and test a current decoded program containing an unresolved operation so the candidate is refused with `UNKNOWN_OPERATION` before execution.

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_gate -v
```

Expected: import failure because `dogram.gate` does not exist.

- [ ] **Step 3: Implement structural admission only**

Create `dogram/gate.py` with:

```python
@dataclass(frozen=True)
class GateLimits:
    max_program_steps: int = 1000


@dataclass(frozen=True)
class GateDisposition:
    status: str
    reason_code: str | None
    residuals: tuple[str, ...]
    program: Program | None
    candidate_program_digest: str | None

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "residuals": list(self.residuals),
            "candidate_program_digest": self.candidate_program_digest,
            "candidate_program": encode_program(self.program) if self.program is not None else None,
        }
```

Use a recursive helper to detect references to the targeted step before removal:

```python
def _references_step(value: Any, step_id: str) -> bool:
    if isinstance(value, list):
        return any(_references_step(item, step_id) for item in value)
    if not isinstance(value, dict):
        return False
    if value.get("ref") == "step" and value.get("step") == step_id:
        return True
    return any(_references_step(item, step_id) for item in value.values())
```

`phase_gate()` must perform checks in stable order: base program digest, base execution digest, target existence, later-step dangling refs, result dangling ref, candidate step limit, candidate decode, remaining registry resolution, deterministic digest. Return `REFUSE` data; do not raise for ordinary gate rejection.

The gate must never execute the candidate and must never compare behavior.

- [ ] **Step 4: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_gate -v
```

Expected: all gate tests pass.

- [ ] **Step 5: Commit**

```bash
git add dogram/gate.py tests/test_gate.py
git commit -m "feat: add structural Omega phase gate"
```

---

### Task 5: Add the First Native META Mathal

**Files:**
- Create: `dogram/stdlib/meta_remove_declared_step.mathal.json`
- Create: `tests/test_meta_mathal.py`
- Verify unchanged: `dogram/registry.py`

**Interfaces:**
- Consumes inert META input object with `program_data`, `execution_digest`, `declared_target_step`, `proposal_id`
- Produces exact `dogram.proposal/v0` JSON as VM result
- Adds no intrinsic and no public operator

- [ ] **Step 1: Write the failing META-program test**

Create `tests/test_meta_mathal.py`:

```python
import json
import pathlib
import unittest

from dogram.program import decode_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import execute_program


class MetaMathalTests(unittest.TestCase):
    def test_remove_declared_step_mathal_constructs_exact_proposal(self):
        path = pathlib.Path("dogram/stdlib/meta_remove_declared_step.mathal.json")
        program = decode_program(json.loads(path.read_text()))
        inputs = {
            "program_data": {"program_digest": "sha256:" + "1" * 64},
            "execution_digest": "sha256:" + "2" * 64,
            "declared_target_step": "diagnostic",
            "proposal_id": "proposal-001",
        }
        result = execute_program(program, inputs, build_bootstrap_registry())
        self.assertEqual(result.status, "OK")
        self.assertEqual(result.result, {
            "schema": "dogram.proposal/v0",
            "proposal_id": "proposal-001",
            "proposal_version": 1,
            "kind": "program_patch",
            "base_program_digest": "sha256:" + "1" * 64,
            "base_execution_digest": "sha256:" + "2" * 64,
            "payload": {"op": "remove_step", "step_id": "diagnostic"},
        })

    def test_meta_mathal_requires_no_registry_growth(self):
        self.assertEqual(len(build_bootstrap_registry().ids()), 12)
```

- [ ] **Step 2: Run focused tests and verify RED**

```bash
python -m unittest tests.test_meta_mathal -v
```

Expected: failure because the META program file does not exist.

- [ ] **Step 3: Add the zero-step native META program**

Create `dogram/stdlib/meta_remove_declared_step.mathal.json`:

```json
{
  "schema": "dogram.program/v0",
  "program_id": "meta/remove-declared-step",
  "program_version": 1,
  "steps": [],
  "result": {
    "schema": {"literal": "dogram.proposal/v0"},
    "proposal_id": {"ref": "input", "path": ["proposal_id"]},
    "proposal_version": {"literal": 1},
    "kind": {"literal": "program_patch"},
    "base_program_digest": {"ref": "input", "path": ["program_data", "program_digest"]},
    "base_execution_digest": {"ref": "input", "path": ["execution_digest"]},
    "payload": {
      "op": {"literal": "remove_step"},
      "step_id": {"ref": "input", "path": ["declared_target_step"]}
    }
  }
}
```

Do not modify `dogram/registry.py`.

- [ ] **Step 4: Run focused tests and verify GREEN**

```bash
python -m unittest tests.test_meta_mathal -v
```

Expected: both tests pass, including exact registry size 12.

- [ ] **Step 5: Commit**

```bash
git add dogram/stdlib/meta_remove_declared_step.mathal.json tests/test_meta_mathal.py
git commit -m "feat: add native remove-step META mathal"
```

---

### Task 6: Complete One Attributable Ω Cycle

**Files:**
- Create: `dogram/omega.py`
- Create: `tests/test_omega.py`
- Create: `tests/fixtures/omega/positive-program.json`
- Create: `tests/fixtures/omega/result-changed-program.json`
- Create: `tests/fixtures/omega/dangling-step-program.json`
- Create: `tests/fixtures/omega/dangling-result-program.json`
- Create: `tests/fixtures/omega/stale-program-proposal.json`
- Create: `tests/fixtures/omega/stale-execution-proposal.json`
- Create: `tests/fixtures/omega/target-not-found-proposal.json`
- Create: `tests/fixtures/omega/malformed-proposal.json`

**Interfaces:**
- Consumes: VM, reification, proposal decoder, phase gate, native META mathal, native DELTA mathal
- Produces: `OmegaConfig(exec_config, meta_config, gate_limits)`
- Produces: `OmegaCycleResult(status, reason_code, receipt)`
- Produces: `run_omega_cycle(program, inputs, declared_target_step, proposal_id, registry, config=None) -> OmegaCycleResult`
- Receipt contains only inert canonical data; no live `Program` or `Registry`

- [ ] **Step 1: Freeze the positive and hostile program/proposal corpus**

`tests/fixtures/omega/positive-program.json` must have one result-bearing step plus one unreferenced diagnostic step:

```json
{
  "schema": "dogram.program/v0",
  "program_id": "fixture/omega-positive",
  "program_version": 1,
  "steps": [
    {
      "id": "value",
      "op": "core.get@1",
      "args": [
        {"ref": "input"},
        {"literal": ["value"]}
      ]
    },
    {
      "id": "diagnostic",
      "op": "core.length@1",
      "args": [{"ref": "input", "path": ["diagnostic"]}]
    }
  ],
  "result": {"ref": "step", "step": "value"}
}
```

`result-changed-program.json` must make the targeted step structurally removable while still changing the final result through a direct input-based result template after removal is admitted; if the current program grammar makes that exact shape impossible, use a different structurally valid target where pre/post results differ without introducing a dangling reference. The frozen expected assertion remains: gate `ADMIT`, post-cycle DELTA reports `DIFFERENT`.

`dangling-step-program.json` must contain a later step that references the target. `dangling-result-program.json` must use the target in the final result. Proposal fixtures must use the exact strict envelope from `dogram.proposal/v0`, changing only the intended hostile field.

- [ ] **Step 2: Write failing Ω-cycle tests**

Create `tests/test_omega.py` covering:

```python
def test_positive_cycle_executes_reifies_meta_gates_executes_and_matches(self):
    result = run_fixture("positive-program.json", target="diagnostic")
    self.assertEqual(result.status, "OK")
    self.assertEqual(result.receipt["gate"]["status"], "ADMIT")
    self.assertEqual(result.receipt["comparison"]["first_difference"], None)
    self.assertNotEqual(
        result.receipt["program_before"]["program_digest"],
        result.receipt["program_after"]["program_digest"],
    )


def test_meta_refusal_never_reaches_gate(self):
    config = OmegaConfig(meta_config=VMConfig(max_exec_steps=0))
    result = run_fixture("positive-program.json", target="diagnostic", config=config)
    self.assertEqual((result.status, result.reason_code), ("REFUSE", "META_EXECUTION_REFUSED"))
    self.assertIsNone(result.receipt["gate"])
    self.assertIsNone(result.receipt["execution_after"])


def test_structurally_valid_result_change_is_reported_not_gate_refused(self):
    result = run_fixture("result-changed-program.json", target="diagnostic")
    self.assertEqual(result.receipt["gate"]["status"], "ADMIT")
    self.assertEqual(result.receipt["comparison"]["first_difference"], "result_digest")


def test_identical_cycles_are_byte_stable(self):
    first = run_fixture("positive-program.json", target="diagnostic", proposal_id="proposal-stable")
    second = run_fixture("positive-program.json", target="diagnostic", proposal_id="proposal-stable")
    self.assertEqual(canonical_json_bytes(first.receipt), canonical_json_bytes(second.receipt))
```

Also cover stale program, stale execution, target missing, dangling step, dangling result, malformed proposal, and reification capability leak. The capability leak test may construct the invalid Python input directly because JSON cannot contain a callable.

- [ ] **Step 3: Run focused tests and verify RED**

```bash
python -m unittest tests.test_omega -v
```

Expected: import failure because `dogram.omega` does not exist.

- [ ] **Step 4: Implement the one-cycle orchestrator**

Create `dogram/omega.py`. Keep loading deterministic and local:

```python
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .canonical import sha256_json
from .gate import GateLimits, phase_gate
from .program import Program, decode_program
from .proposal import ProposalDecodeError, decode_proposal
from .reify import ReificationError, execution_digest, reify_execution, reify_program
from .registry import Registry
from .values import ScalarValue, encode_value
from .vm import VMConfig, execute_program


_STDLIB = Path(__file__).with_name("stdlib")


def _load_program(name: str) -> Program:
    return decode_program(json.loads((_STDLIB / name).read_text()))


@dataclass(frozen=True)
class OmegaConfig:
    exec_config: VMConfig = VMConfig()
    meta_config: VMConfig = VMConfig(max_exec_steps=32)
    gate_limits: GateLimits = GateLimits()


@dataclass(frozen=True)
class OmegaCycleResult:
    status: str
    reason_code: str | None
    receipt: dict[str, Any]
```

Use exactly one META execution. Build META inputs only from inert data:

```python
meta_inputs = {
    "program_data": program_data,
    "execution_data": execution_data,
    "execution_digest": execution_digest(execution_data),
    "declared_target_step": declared_target_step,
    "proposal_id": proposal_id,
}
```

After gate admission, re-execute the candidate with the same `inputs` and `exec_config`.

For exact pre/post result comparison, use the existing native DELTA mathal over canonical result digests. Do not invent a new comparison operator:

```python
def _result_value(result: Any) -> dict[str, Any]:
    return encode_value(ScalarValue("opaque", sha256_json(result)))


delta_inputs = {
    "boundary_order": ["result_digest"],
    "left": {"result_digest": _result_value(before.result)},
    "right": {"result_digest": _result_value(after.result)},
}
comparison_execution = execute_program(
    _load_program("delta.mathal.json"),
    delta_inputs,
    registry,
    config.exec_config,
)
```

Require the comparison execution itself to be `OK`; otherwise the Ω cycle refuses with `COMPARISON_EXECUTION_REFUSED` and receipts the comparison refusal.

The cycle receipt must contain canonical inert data only, with stable field names:

```text
schema = dogram.omega-cycle-receipt/v0
proposal_id
program_before
execution_before
execution_before_digest
meta_execution
gate
program_after
execution_after
comparison
```

On early refusal, keep later phases as `None`; do not fabricate results for phases that were never reached.

Catch `ReificationError` as `REIFICATION_REFUSED` and `ProposalDecodeError` as `MALFORMED_PROPOSAL`. Ordinary gate refusal uses the gate's exact reason code.

- [ ] **Step 5: Run focused Ω tests and verify GREEN**

```bash
python -m unittest tests.test_omega -v
```

Expected: positive and hostile Ω tests all pass; positive cycle completes exactly one META round.

- [ ] **Step 6: Run all new Ω-area tests together**

```bash
python -m unittest tests.test_vm tests.test_reify tests.test_proposal tests.test_gate tests.test_meta_mathal tests.test_omega -v
```

Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add dogram/omega.py tests/test_omega.py tests/fixtures/omega
git commit -m "feat: complete first bounded Dogram Omega cycle"
```

---

### Task 7: Constitutional CI, Documentation, and Full Verification

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Verify: `pyproject.toml`
- Verify: all `dogram/`, `tests/`, fixtures, stdlib programs

**Interfaces:**
- No new runtime interface beyond Tasks 1-6.
- CI must enforce both public operator floor and unchanged 12-intrinsic bootstrap registry.

- [ ] **Step 1: Add CI assertions before changing documentation**

Extend the existing constitutional-floor Python block in `.github/workflows/ci.yml`:

```python
from dogram.engine import OPERATORS
from dogram.registry import build_bootstrap_registry

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
```

Keep `assert pyproject["project"]["dependencies"] == []` unchanged.

- [ ] **Step 2: Run full verification before README claims**

Run:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
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
assert len(build_bootstrap_registry().ids()) == 12
print("constitutional floor OK")
PY
```

Expected: full suite passes; compile passes; final script prints `constitutional floor OK`.

- [ ] **Step 3: Add one factual README status paragraph**

Under `## Destination architecture`, after the existing paragraph describing the Mathal VM destination, add:

```markdown
The first bounded Ω cycle is implemented as an explicit `EXEC -> REIFY -> META -> PROPOSAL -> PHASE GATE -> EXEC` path. Its META surface can only construct a caller-declared `remove_step` proposal from inert execution data; structural admission remains separate from behavioral comparison, and the public four-operator calculation floor is unchanged.
```

Do not describe Dogram as autonomous, self-authorizing, evidentiary, or truth-seeking.

- [ ] **Step 4: Re-run full verification after README/CI edits**

Run the exact commands from Step 2 again.

Expected: same green results.

- [ ] **Step 5: Scan for forbidden expansion and placeholders**

Run:

```bash
python - <<'PY'
from pathlib import Path

forbidden = ["eval(", "exec(", "importlib", "subprocess", "socket.", "requests."]
for path in Path("dogram").rglob("*.py"):
    text = path.read_text()
    for token in forbidden:
        assert token not in text, (path, token)

for path in [
    Path("dogram/proposal.py"),
    Path("dogram/gate.py"),
    Path("dogram/omega.py"),
    Path("dogram/reify.py"),
]:
    text = path.read_text()
    for token in ("TODO", "TBD", "FIXME", "PLACEHOLDER"):
        assert token not in text, (path, token)

print("scope scan OK")
PY
```

Expected: `scope scan OK`.

- [ ] **Step 6: Commit final integration surfaces**

```bash
git add .github/workflows/ci.yml README.md
git commit -m "chore: lock Omega cycle constitutional floor"
```

- [ ] **Step 7: Final branch verification**

Run once more:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Then inspect the branch diff against the implementation baseline and confirm:

```text
no dependency additions
no public operator additions
no bootstrap intrinsic additions
exactly one META proposal semantics
exactly one META cycle
all reified outputs canonical
all required hostile controls represented
```

Only after this evidence is green should the implementation branch be offered for PR/review/merge.

---

## Self-Review Receipt

**Spec coverage:**
- Reification membrane -> Task 2.
- Exact consumed-input provenance, including refusal paths -> Task 1.
- Strict `dogram.proposal/v0` and only `remove_step` -> Task 3.
- Native META mathal, no new intrinsic -> Task 5.
- Exact ancestry binding and structural phase gate -> Task 4.
- One-cycle orchestration and separate EXEC/META fuel -> Task 6.
- Positive fixture and all required hostile classes -> Tasks 2, 4, and 6.
- Exact post-cycle comparison through native DELTA -> Task 6.
- Deterministic cycle receipts -> Task 6.
- Zero dependencies, exact four public operators, no bootstrap expansion -> Task 7.
- No evidence/support/truth/authority promotion -> Global Constraints + gate/orchestrator design.

**Placeholder scan:** No `TODO`, `TBD`, `FIXME`, `PLACEHOLDER`, "similar to", or undefined implementation steps remain in this plan.

**Type consistency:** The plan uses one consistent chain: `VMExecution` -> inert `ExecutionData` -> `ProgramPatchProposal` -> `GateDisposition` -> `OmegaCycleResult`. `Program` objects stay host-local and never appear in reified META inputs or cycle receipt data.

## Execution Checkpoints

The implementation is reviewable after each independent commit:

1. exact VM provenance;
2. reification membrane;
3. strict proposal grammar;
4. structural gate;
5. native META mathal;
6. first complete Ω cycle;
7. CI/documentation constitutional lock.

Each checkpoint must be green before the next task begins.
