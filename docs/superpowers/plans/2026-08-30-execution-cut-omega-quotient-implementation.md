# EXECUTION-CUT / OMEGA-QUOTIENT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the first bounded receipt-bearing paired Dogram experiment that proves a predeclared target can survive an admitted `remove_step` change while preserving every measured execution-footprint difference.

**Architecture:** Add a small `execution_cut` module that turns existing `dogram.execution-data/v0` records into occurrence-bound cuts and computes typed/component-wise residuals without erasing sequence order. Add an `omega_quotient` module that wraps the existing one-cycle Ω orchestrator, requires a fixed predeclared target family, enforces same-input/same-runtime boundaries, and emits an attributable paired receipt. Do not change the public operator floor, bootstrap registry, proposal grammar, or gate semantics.

**Tech Stack:** Python 3.12 standard library only; `unittest`; existing Dogram VM / Ω runtime.

**Spec:** `docs/superpowers/specs/2026-08-30-execution-cut-omega-quotient-design.md`

## Global Constraints

- Runtime contact is derived only from existing runtime-reified execution data.
- Preserve `consumed_input_addresses` and `step_trace` as ordered sequences.
- Footprint residual is typed/component-wise; no set-only comparison.
- Target family is fixed, deterministic, and declared before comparison.
- Same target response does not imply same execution or global equivalence.
- The first controlled pair requires identical `input_digest` values.
- Same-runtime control is bounded to one orchestrator invocation; cross-runtime claims return `HOLD`.
- Gate admission and target equivalence remain separate phases.
- Add no public Dogram operator and no bootstrap intrinsic.
- Automatic experiment or target selection is out of scope.

---

### Task 1: Freeze the quotient contract in RED tests

**Files:**
- Create: `tests/test_omega_quotient.py`

**Interfaces:**
- Consumes: existing `run_omega_cycle`, `decode_program`, `build_bootstrap_registry`, `VMConfig`.
- Produces expected interfaces for later tasks:
  - `make_execution_cut(execution_data: dict, *, fuel_initial: int) -> dict`
  - `typed_footprint_residual(before: dict, after: dict) -> dict`
  - `TargetFamily(id: str, probes: tuple[str, ...], declared_before_comparison: bool = True)`
  - `compare_execution_cuts(before: dict, after: dict, target: TargetFamily, *, same_runtime_invocation: bool = True) -> QuotientComparison`
  - `run_omega_quotient(...) -> OmegaQuotientResult`

- [ ] **Step 1: Write failing tests** covering the required positive fixture plus hostile controls: target moved, input drift, trace-order erasure, result-only overreach, gate/equivalence separation, runtime-drift hold, and byte stability.
- [ ] **Step 2: Push the tests without production modules.**
- [ ] **Step 3: Verify GitHub Actions fails because `dogram.execution_cut` / `dogram.omega_quotient` do not exist.**

---

### Task 2: Implement occurrence-bound execution cuts and typed residuals

**Files:**
- Create: `dogram/execution_cut.py`
- Test: `tests/test_omega_quotient.py`

**Interfaces:**
- `make_execution_cut(execution_data, fuel_initial=...)` validates `schema == "dogram.execution-data/v0"`, preserves exact ordered contact and trace data, adds `fuel_initial`, and emits `schema == "dogram.execution-cut/v0"`.
- `typed_footprint_residual(before, after)` compares components directly as their native types. For differing components, preserve exact `before` and `after` values. For same result/residual status, emit an explicit `{"relation": "SAME"}` witness rather than deleting the component.

Minimum compared components:

```text
status
result
reason_code
residuals
consumed_input_addresses
step_trace
fuel
```

Fuel residual shape:

```python
{
    "initial": before["fuel_initial"],
    "before_remaining": before["fuel_remaining"],
    "after_remaining": after["fuel_remaining"],
}
```

- [ ] **Step 1: Implement the minimal execution-cut functions required by the RED tests.**
- [ ] **Step 2: Run focused tests; keep any quotient-orchestrator tests RED until Task 3.**
- [ ] **Step 3: Commit only the cut/residual implementation once its focused behaviors are green.**

---

### Task 3: Implement fixed-target quotient comparison and Ω paired orchestration

**Files:**
- Create: `dogram/omega_quotient.py`
- Test: `tests/test_omega_quotient.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class TargetFamily:
    id: str
    probes: tuple[str, ...]
    declared_before_comparison: bool = True

@dataclass(frozen=True)
class QuotientComparison:
    status: str  # OK | REFUSE | HOLD
    reason_code: str | None
    target_verdict: str | None  # EQUIVALENT_UNDER_T | DIFFERENT_UNDER_T
    footprint_residual: dict

@dataclass(frozen=True)
class OmegaQuotientResult:
    status: str
    reason_code: str | None
    receipt: dict
```

`compare_execution_cuts` laws:

```text
if not target.declared_before_comparison -> REFUSE TARGET_NOT_PREDECLARED
if before.input_digest != after.input_digest -> REFUSE INPUT_CUT_MISMATCH
if same_runtime_invocation is False -> HOLD RUNTIME_BODY_UNPINNED
unsupported probe -> REFUSE UNSUPPORTED_TARGET_PROBE
otherwise compare each declared probe exactly and return EQUIVALENT_UNDER_T or DIFFERENT_UNDER_T beside typed residual
```

First supported probes are deliberately inert execution-cut fields: `result`, `status`, `reason_code`, and `residuals`. No ambient I/O or semantic probe registry is added.

`run_omega_quotient` must:

1. refuse a non-predeclared target before running Ω;
2. call existing `run_omega_cycle` with the caller-supplied `Registry` and `OmegaConfig`;
3. require the Ω cycle to complete successfully;
4. derive both cuts from the reified `execution_before` / `execution_after` records using the same `exec_config.max_exec_steps`;
5. compare the cuts using the fixed target family;
6. emit `dogram.omega-quotient/v0` with exact program/execution digests, both cuts, target family, verdict, typed residual, and a `does_not_establish` list including `global_equivalence`, `causal_irrelevance`, `evidence`, `support`, `truth`, `authority`, and `cross-runtime replay`.

- [ ] **Step 1: Implement minimal target/comparison types and hostile-control dispositions.**
- [ ] **Step 2: Implement `run_omega_quotient` as a wrapper around the existing single Ω cycle; do not duplicate mutation/gate logic.**
- [ ] **Step 3: Run the focused quotient suite until GREEN.**
- [ ] **Step 4: Run the full unit suite, compile, constitutional floor, and Ω scope scan.**

---

### Task 4: Preserve a durable receipt slice and factual status note

**Files:**
- Create: `research/OMEGA-QUOTIENT-001-RECEIPT.md`
- Modify: `README.md`

**Interfaces:**
- Research receipt records exact verified branch/head, RED witness, GREEN verification, positive fixture outcome, hostile-control outcomes, and explicit non-claims.
- README adds only a factual sentence that the internal bounded paired-experiment seam exists; it must not claim self-optimization or semantic authority.

- [ ] **Step 1: After fresh exact-head GREEN verification, record the test counts and control outcomes in the research receipt.**
- [ ] **Step 2: Add the minimal README status note.**
- [ ] **Step 3: Run full verification again on the documentation head.**
- [ ] **Step 4: Open a reviewable PR against `main`; do not merge automatically.**
