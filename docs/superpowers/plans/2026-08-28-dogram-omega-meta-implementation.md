# Dogram Ω Membrane + META Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add canonical execution reification, read-only meta-mathals, and a deterministic single-successor ProgramPatch gate so Dogram can lawfully alternate `EXEC → REIFY → META → GATE → EXEC` without live self-mutation.

**Architecture:** This plan assumes the Mathal VM + stdlib plan is green. The active VM program is converted into inert `ProgramData`, `ReceiptData`, and `ExecutionData`; META receives only those inert values. META may emit typed proposals, but only the phase gate may validate a `ProgramPatch` and activate a replacement program between executions. Live host objects never cross the reification membrane.

**Tech Stack:** Python >= 3.12, standard library only.

**Spec:** `docs/superpowers/specs/2026-08-28-dogram-metaoscillatory-runtime-design.md`

## Global Constraints

- The Mathal VM + stdlib plan must be green first.
- `ACTIVE PROGRAM != PROGRAM-AS-DATA`.
- `PROGRAM-AS-DATA != EXECUTABLE CAPABILITY`.
- `REFLECTION != MUTATION`.
- `META OUTPUT != NEXT EXECUTION` until the phase gate admits it.
- All reified values are canonical JSON-like data and deterministically digestible.
- Single-successor META only in this plan. Branching is deferred.
- ProgramPatch activation happens only after EXEC has ended.
- The phase gate admits a local next computation only; it does not mint external authority.

---

## File Structure

```text
Dogram/
  dogram/
    reify.py
    proposal.py
    phase_gate.py
    omega.py
    stdlib/meta/
      compare-result.mathal.json
      stop-if-same.mathal.json
  tests/
    test_reify.py
    test_proposal.py
    test_phase_gate.py
    test_meta_readonly.py
    test_omega_cycle.py
    test_omega_hostile.py
```

---

### Task 1: Reify completed execution into inert canonical data

**Files:**
- Create: `dogram/reify.py`
- Create: `tests/test_reify.py`

**Interfaces:**
- Produces immutable `ProgramData`, `ReceiptData`, and `ExecutionData` dataclasses.
- Produces `reify_execution(program: Program, inputs: object, execution: VMExecution) -> ExecutionData`.

- [ ] **Step 1: Write the failing reification test**

```python
class ReifyTests(unittest.TestCase):
    def test_reification_is_canonical_data(self):
        data = reify_execution(program, {"x": 1}, execution).to_data()
        self.assertIsInstance(canonical_json_bytes(data), bytes)
        self.assertEqual(data["program"]["program_digest"], program_digest(program))
        self.assertEqual(data["execution"]["status"], execution.status)
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_reify -v
```

Expected: import failure because `dogram.reify` does not exist.

- [ ] **Step 3: Implement explicit reified schemas**

Use exact schema IDs:

```text
dogram.program-data/v0
dogram.receipt-data/v0
dogram.execution-data/v0
```

`ProgramData` contains encoded program plus digest. `ReceiptData` contains VM status, reason/residuals, step trace, result, fuel remaining, and execution digest. `ExecutionData` contains input digest plus nested program/receipt data.

- [ ] **Step 4: Prove no live host object crosses the membrane**

Recursively inspect `.to_data()` in the test and assert every leaf is one of `None`, `bool`, `int`, `float`, `str`; containers are only `list` and `dict`.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_reify -v
git add dogram/reify.py tests/test_reify.py
git commit -m "feat: reify Dogram execution as inert data"
```

---

### Task 2: Define typed META proposals without activation authority

**Files:**
- Create: `dogram/proposal.py`
- Create: `tests/test_proposal.py`

**Interfaces:**
- Proposal kinds in this plan: `NoChange`, `Stop`, `ProgramPatch`, `Refuse`.
- Produces `decode_proposal(data: dict) -> Proposal`.
- `ProgramPatch` contains `base_program_digest`, complete inert `replacement_program`, and `reason_receipt_digests`.

- [ ] **Step 1: Write RED proposal tests**

```python
class ProposalTests(unittest.TestCase):
    def test_program_patch_requires_base_digest(self):
        with self.assertRaises(ProposalDecodeError) as ctx:
            decode_proposal({"schema":"dogram.proposal/v0","kind":"ProgramPatch","replacement_program":{}})
        self.assertEqual(ctx.exception.reason_code, "MISSING_BASE_PROGRAM_DIGEST")

    def test_unknown_proposal_kind_refuses(self):
        with self.assertRaises(ProposalDecodeError):
            decode_proposal({"schema":"dogram.proposal/v0","kind":"UnknownKind"})
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_proposal -v
```

- [ ] **Step 3: Implement canonical proposal dataclasses**

Canonical `ProgramPatch.to_data()`:

```json
{
  "schema":"dogram.proposal/v0",
  "kind":"ProgramPatch",
  "base_program_digest":"sha256:...",
  "replacement_program":{"schema":"dogram.program/v0"},
  "reason_receipt_digests":["sha256:..."]
}
```

Proposal instances store only data fields, never active VM or registry objects.

- [ ] **Step 4: Run GREEN and commit**

```bash
python -m unittest tests.test_proposal -v
git add dogram/proposal.py tests/test_proposal.py
git commit -m "feat: add inert Dogram meta proposals"
```

---

### Task 3: Add read-only meta-mathals over reified execution

**Files:**
- Create: `dogram/stdlib/meta/compare-result.mathal.json`
- Create: `dogram/stdlib/meta/stop-if-same.mathal.json`
- Create: `tests/test_meta_readonly.py`

**Interfaces:**
- Meta programs are ordinary `dogram.program/v0` programs executed by the same bounded VM.
- META input contains only `current_execution` and optional `previous_execution` reified data.

- [ ] **Step 1: Write RED result-comparison test**

The first meta mathal compares previous/current final result values through `core.get@1` and `core.same@1`; identical results produce `{"same_result": true}`, changed results produce false.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_meta_readonly -v
```

- [ ] **Step 3: Implement the two data-only meta programs**

`stop-if-same.mathal.json` emits proposal-shaped data:

```text
same result     -> Stop
different result -> NoChange
```

If the VM does not yet have conditional data selection, add and independently test generic `core.choose@1(condition, when_true, when_false)`. Do not add a META-specific shortcut intrinsic.

- [ ] **Step 4: Assert current program/execution digests are unchanged after META**

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_meta_readonly -v
git add dogram/stdlib/meta dogram/intrinsics tests/test_meta_readonly.py
git commit -m "feat: add read-only Dogram meta mathals"
```

---

### Task 4: Build the deterministic ProgramPatch phase gate

**Files:**
- Create: `dogram/phase_gate.py`
- Create: `tests/test_phase_gate.py`

**Interfaces:**
- Produces `GateDecision(status: str, reason_code: str | None, next_program: Program | None, proposal_digest: str)`.
- Produces `evaluate_phase_gate(current_program: Program, proposal: Proposal, registry: Registry, limits: GateLimits) -> GateDecision`.

- [ ] **Step 1: Write RED stale-base and unadmitted-operation tests**

```python
class PhaseGateTests(unittest.TestCase):
    def test_stale_base_refuses(self):
        decision = evaluate_phase_gate(current, stale_patch, registry, GateLimits())
        self.assertEqual(decision.reason_code, "STALE_PROGRAM_BASE")

    def test_unadmitted_operation_refuses(self):
        decision = evaluate_phase_gate(current, patch_with_unknown_op, registry, GateLimits())
        self.assertEqual(decision.reason_code, "UNADMITTED_OPERATION")
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_phase_gate -v
```

- [ ] **Step 3: Implement structural-only validation**

For `ProgramPatch`, validate in this order:

```text
proposal schema/kind
base digest == current digest
replacement program decodes under dogram.program/v0
step count <= max_program_steps
all operations resolve in static registry
program references remain acyclic and valid
```

`NoChange` returns the current program. `Stop` returns `ADMIT_STOP` with no next program. `Refuse` remains a structured local refusal.

- [ ] **Step 4: Add non-data replacement hostile test**

Feed a replacement program containing a non-JSON object and assert deterministic refusal before activation.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_phase_gate -v
git add dogram/phase_gate.py tests/test_phase_gate.py
git commit -m "feat: gate Dogram program patches between phases"
```

---

### Task 5: Add a single-successor Ω cycle orchestrator

**Files:**
- Create: `dogram/omega.py`
- Create: `tests/test_omega_cycle.py`

**Interfaces:**
- Produces `OmegaConfig(vm: VMConfig, gate: GateLimits, max_meta_cycles: int = 8)`.
- Produces `run_omega_cycle(exec_program, exec_inputs, meta_program, previous_execution, registry, config) -> OmegaCycleResult`.
- `OmegaCycleResult.to_data()` uses schema `dogram.oscillation-receipt/v0`.

- [ ] **Step 1: Write RED `EXEC → REIFY → META → GATE` test**

Use a tiny exec program returning a literal and a meta program returning `NoChange`. Assert the cycle receipt separates exec program/receipt digests, meta program/proposal digests, gate status, and exec/meta fuel accounting.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_omega_cycle -v
```

- [ ] **Step 3: Implement strict phase ordering**

META starts only after EXEC returns and `reify_execution()` succeeds. The meta output is decoded as a proposal, then passed to the phase gate. The returned next program is not run inside the same function; an outer loop owns the next cycle.

- [ ] **Step 4: Add deterministic replay test**

Run the same cycle twice from identical program/input/configuration and assert byte-identical canonical cycle payloads.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_omega_cycle -v
git add dogram/omega.py tests/test_omega_cycle.py
git commit -m "feat: add single-successor Dogram omega cycle"
```

---

### Task 6: Add Ω hostile membrane verification

**Files:**
- Create: `tests/test_omega_hostile.py`

**Interfaces:**
- No new runtime API.

- [ ] **Step 1: Encode the architecture's hostile cases**

Cover:

```text
META-LIVE-MUTATION-001
DATA-CAPABILITY-COLLAPSE-001
PATCH-STALE-BASE-001
META-FUEL-001
REPLAY-META-001
```

`META-FUEL-001` must return `REFUSE / FUEL_EXHAUSTED` at the same cycle on repeated runs.

- [ ] **Step 2: Run the complete suite**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

- [ ] **Step 3: Commit verification-only fixes separately, rerun the full suite, and record exact test count/head SHA in the PR receipt**

---

## Plan Self-Review

- **Spec coverage:** reification, proposal typing, read-only META, ProgramPatch gate, single-successor cycle, deterministic fuel behavior, and hostile membrane cases are all assigned.
- **Placeholder scan:** no TODO/TBD placeholders remain.
- **Type consistency:** `ExecutionData`, `Proposal`, `ProgramPatch`, `GateDecision`, `OmegaConfig`, and `OmegaCycleResult` remain stable throughout.
- **Capability boundary:** all reflective work operates on inert data; only the gate may reactivate a decoded program between executions.
- **Scope control:** branching, multiway execution, and bootstrap peeling remain excluded and belong to the next plan.
