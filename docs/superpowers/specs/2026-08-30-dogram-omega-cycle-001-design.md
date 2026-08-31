# Dogram Ω-CYCLE-001 — First Lawful Metaoscillation

**Date:** 2026-08-30  
**Status:** DESIGN APPROVED IN CHAT · WRITTEN SPEC AWAITING HUMAN REVIEW  
**Repository:** `the-static-collective/Dogram`  
**Baseline main:** `bf8eaa6b64489a08463286f266050ae8647d4317`  
**Parent architecture:** `docs/superpowers/specs/2026-08-28-dogram-metaoscillatory-runtime-design.md`

## 0. Decision

Dogram's next architectural slice is not another public operator and not a broad META engine.

The next slice is the smallest complete metaoscillatory vertical path:

```text
EXEC(P0, W)
  -> VMExecution r0
  -> REIFY(P0, W, r0)
  -> inert ProgramData + ExecutionData
  -> META(reified data + declared patch target)
  -> ProposalData q0
  -> PHASE GATE(q0, P0, r0)
  -> P1 | REFUSE
  -> EXEC(P1, W)
  -> VMExecution r1
  -> explicit comparison witness
```

The first admitted proposal operation is deliberately narrow:

```text
ProgramPatch.remove_step
```

META does not choose which step should be removed. The target step is declared by the caller/specimen. META constructs a proposal bound to the exact current program and execution receipt. The phase gate performs deterministic structural admission only.

The first successful fixture removes one structurally dispensable step from a frozen program, re-executes the admitted candidate, and demonstrates that the declared operative result is unchanged under the existing DELTA/conformance machinery.

This is the first slice where Dogram executes, encounters an inert attributable representation of its own execution, proposes a bounded next program state, crosses a separate gate, and executes again.

> **FIRST MAKE THE MACHINE SEE ITS OWN FOOTPRINT. THEN LET IT PROPOSE WHERE TO PUT THE NEXT FOOT.**

---

## 1. Current baseline

At baseline `bf8eaa6b64489a08463286f266050ae8647d4317`, Dogram already has:

- the public Phase A oracle floor: `delta@1`, `rectangle@1`, `ablate@1`, `reach@1`;
- inert canonical `dogram.program/v0` programs;
- a deterministic acyclic Mathal VM;
- explicit VM fuel;
- ordered step traces with operation identity and argument/result digests;
- a 12-intrinsic bootstrap registry;
- direct Python reference/oracle implementations;
- native `stdlib/delta.mathal.json` conformance against the Python DELTA path;
- CI checks that preserve zero project dependencies and the exact four-operator public floor.

The important architectural gap is no longer program execution.

The gap is:

```text
VMExecution
    X
    | no reification/meta/gate cycle yet
    v
next executable program
```

Ω-CYCLE-001 closes exactly that gap.

---

## 2. Constitutional boundary

The slice must preserve all existing Dogram boundaries.

```text
DOGRAM CALCULATES.
DOGRAM RECEIPTS.
DOGRAM MAY PROPOSE A NEXT DOGRAM CALCULATION.
DOGRAM DOES NOT DECLARE ITS OWN PROPOSAL TRUE.
```

Hard non-collapses:

```text
ACTIVE PROGRAM != PROGRAM-AS-DATA
VM EXECUTION != EXECUTION-AS-DATA
PROGRAM-AS-DATA != EXECUTABLE CAPABILITY
RECEIPT != AUTHORITY
META OUTPUT != NEXT EXECUTION
PHASE GATE != WORLD CONSTITUTION
PROGRAM ADMISSION != EVIDENCE
PROGRAM ADMISSION != SUPPORT
PROGRAM ADMISSION != TRUTH
PROGRAM ADMISSION != EXTERNAL AUTHORITY
```

The phase gate may decide only:

> Is this candidate a structurally lawful next Dogram computation under the local bounded runtime contract?

It may not decide:

> Is this candidate meaningful, historically correct, causally explanatory, evidentiary, morally correct, or externally authorized?

---

## 3. Scope

Ω-CYCLE-001 adds only enough machinery for one complete bounded cycle.

### In scope

1. Canonical inert reification of the current program and one VM execution.
2. Exact digests for reified execution artifacts.
3. Strict typed proposal decoding for a minimal `dogram.proposal/v0` envelope.
4. Initial proposal kinds:
   - `NoChange`;
   - `Stop`;
   - `ProgramPatch` with exactly one admitted patch operation: `remove_step`.
5. One native META mathal that emits a `remove_step` proposal from declared inputs.
6. A deterministic host phase gate for the minimal proposal family.
7. One-cycle orchestration with explicit phase boundaries.
8. Frozen positive and hostile fixtures.
9. Exact post-cycle conformance comparison.
10. CI preservation of the current public operator floor and zero-dependency constitution.

### Explicitly out of scope

- native `rectangle`, `ablate`, or `reach` lowering;
- recursive mathal calls;
- cyclic programs;
- general branching;
- arbitrary composition proposals;
- automatic experiment selection;
- automatic selection of which program step to remove;
- `PeelProposal` execution;
- host-intrinsic removal;
- multi-cycle autonomous reflection;
- arbitrary program synthesis;
- dynamic code payloads;
- network/file-system capabilities;
- evidence/support/truth/authority semantics;
- promotion of `fiber@1`, `trace@1`, `phase@1`, `meta@1`, or any new public calculation operator.

The public `dogram.engine.OPERATORS` set remains exactly:

```text
{delta@1, rectangle@1, ablate@1, reach@1}
```

---

## 4. Reification membrane

The governing law is:

> **REIFY BEFORE REFLECT.**

META must never receive the live `Program` object, `Registry`, intrinsic callable, Python exception, module object, file handle, or other ambient capability.

It receives canonical JSON-compatible data only.

### 4.1 ProgramData

`ProgramData` is the canonical encoded form of the active `Program` plus its exact digest.

Conceptual shape:

```json
{
  "schema": "dogram.program-data/v0",
  "program": { "schema": "dogram.program/v0", "...": "..." },
  "program_digest": "sha256:..."
}
```

`program_digest` is computed from the canonical `dogram.program/v0` representation, not from Python object identity.

### 4.2 ExecutionData

`ExecutionData` is the canonical inert representation of one completed `VMExecution` bound to the exact program and input state that produced it.

Required fields:

```text
schema
program_digest
input_digest
status
result
reason_code
residuals
step_trace
consumed_input_addresses
fuel_remaining
```

Each reified step trace preserves at least:

```text
step_id
op
arg_digest
result_digest
fuel_before
fuel_after
```

### 4.3 Consumed input addresses

The existing VM resolves explicit `ref: input` addresses before invoking each intrinsic. Ω-CYCLE-001 must preserve those addresses as reified consumption provenance.

Because `dogram.program/v0` is acyclic and executes steps in declared order, the initial implementation may derive actual consumed input addresses from:

- step argument templates for steps that were actually reached/executed;
- the final result template only when final result resolution occurs.

This is an execution receipt, not a semantic statement about which inputs were causally important.

Hard law:

```text
RESOLVED / CONSUMED INPUT != CAUSAL SUPPORT
```

### 4.4 Execution digest

After canonicalization, `ExecutionData` receives an exact digest:

```text
execution_digest = sha256(canonical ExecutionData)
```

A proposal that claims to arise from an execution must bind to this digest.

### 4.5 Reification refusal

Reification must refuse or fail closed if an artifact cannot be represented canonically without leaking an active capability.

No fallback such as `repr(object)` is permitted.

---

## 5. ProposalData v0

META returns inert data.

It does not return a `Program` object.

Strict envelope:

```json
{
  "schema": "dogram.proposal/v0",
  "proposal_id": "...",
  "proposal_version": 1,
  "kind": "program_patch",
  "base_program_digest": "...",
  "base_execution_digest": "...",
  "payload": {
    "op": "remove_step",
    "step_id": "diagnostic-step"
  }
}
```

The decoder rejects unknown top-level fields and unknown payload fields.

### 5.1 Initial kinds

The initial proposal family is:

```text
no_change
stop
program_patch
```

`program_patch` supports only:

```text
remove_step
```

No generic mutation language is admitted in this slice.

### 5.2 Proposal identity

`proposal_id` is attributable data supplied/generated under deterministic local rules. It is not authority.

`proposal_version` versions the proposal instance format, not the truth of the proposal.

### 5.3 Exact ancestry binding

Every `program_patch` proposal must bind to:

```text
base_program_digest
base_execution_digest
```

This prevents a structurally valid proposal created for one machine cut from silently applying to another.

Hard law:

> **A PATCH MAY TRAVEL ONLY WITH THE PROGRAM AND EXECUTION CUT THAT PAID FOR IT.**

---

## 6. First META mathal

META itself should already use the native Mathal VM rather than a bespoke Python decision function.

The first admitted META program is intentionally stupid:

```text
meta/remove-declared-step@1
```

Inputs include only inert reified data plus a caller-declared target:

```text
program_data
execution_data
execution_digest
declared_target_step
proposal_id
```

The META program constructs a `dogram.proposal/v0` object that:

- copies the exact `program_digest`;
- copies the exact `execution_digest`;
- names `program_patch`;
- names `remove_step`;
- copies the declared target step.

It does not search for a dispensable step.

It does not rank steps.

It does not decide whether removal is useful.

It does not inspect hidden runtime state.

Its significance is architectural rather than intelligent:

> **A native mathal can consume inert data about a Dogram execution and emit an attributable candidate next Dogram program state.**

---

## 7. Phase gate v0

The first phase gate remains a small deterministic host component.

Conceptually:

```text
G(proposal, current_program, current_execution_data, registry, limits)
    -> GateDisposition
```

`GateDisposition` is inert data with one of:

```text
ADMIT
REFUSE
```

If admitted, the gate also returns the newly decoded candidate `Program` plus its digest.

### 7.1 Required checks

For `program_patch/remove_step`, the gate checks at least:

1. exact proposal schema/version;
2. known proposal kind;
3. exact `base_program_digest` match;
4. exact `base_execution_digest` match;
5. target step exists in the current program;
6. exactly one step is targeted;
7. removing the step does not create a dangling step reference;
8. removing the step does not create a dangling final-result reference;
9. resulting program still decodes as `dogram.program/v0`;
10. every remaining operation resolves in the already-admitted local registry;
11. no forward/cyclic reference is introduced;
12. resulting program remains within declared step limits;
13. proposal contains no unknown fields or executable payload;
14. candidate canonicalizes deterministically;
15. candidate digest is computed before execution.

### 7.2 Gate ignorance

The gate does **not** test whether removing the step preserves semantics.

That is subsequent calculation pressure.

Therefore:

```text
GATE ADMIT != EQUIVALENT PROGRAM
```

The gate says only that the candidate is structurally runnable under the current local constitution.

---

## 8. One-cycle orchestrator

Ω-CYCLE-001 introduces one explicit orchestration boundary rather than hidden chaining.

Conceptual host flow:

```python
r0 = execute_program(P0, W, registry, exec_config)
D0 = reify(P0, W, r0)
q0 = execute_program(META_PROGRAM, meta_inputs(D0, target), registry, meta_config)
p0 = decode_proposal(q0.result)
g0 = phase_gate(p0, P0, D0, registry, limits)
if g0.status == "ADMIT":
    r1 = execute_program(g0.program, W, registry, exec_config)
```

The orchestration layer is not allowed to invent or modify the proposal.

It may only:

- run phases in order;
- pass canonical inert artifacts between phases;
- stop/refuse on malformed phase output;
- preserve phase receipts and digests.

### 8.1 Separate phase fuel

EXEC and META use explicit finite VM configurations.

The first slice permits exactly one META cycle.

There is no recursive call from META back into the Ω orchestrator.

```text
MAX META CYCLES = 1 for Ω-CYCLE-001
```

The exact numeric step budgets belong to implementation tests/configuration, but both phases must be finite and deterministic.

---

## 9. First positive fixture

Freeze a tiny program `P0` with:

- one operative step used by the final result;
- one diagnostic/dispensable step whose result is not referenced by any later step or final result.

Illustrative shape:

```text
step value:
  core.get@1(input, ["value"])

step diagnostic:
  core.length@1(input["diagnostic"])

result:
  ref step value
```

The specimen declares:

```text
declared_target_step = diagnostic
```

Required flow:

```text
EXEC P0 -> OK / result R
REIFY -> D0
META -> remove_step(diagnostic) proposal
GATE -> ADMIT / P1
EXEC P1 -> OK / result R'
COMPARE R vs R'
```

Expected comparison under the declared result lens:

```text
R == R'
```

The useful proof is not that the diagnostic step was metaphysically unnecessary.

The useful proof is:

> **Dogram completed one attributable self-contact cycle and the declared operative result survived this exact structural ablation.**

---

## 10. Required hostile fixtures

At minimum freeze the following controls.

### 10.1 `OMEGA-STALE-PROGRAM-001`

Proposal carries the wrong `base_program_digest`.

Expected:

```text
REFUSE / STALE_BASE_PROGRAM
```

### 10.2 `OMEGA-STALE-EXECUTION-001`

Proposal carries the wrong `base_execution_digest`.

Expected:

```text
REFUSE / STALE_BASE_EXECUTION
```

### 10.3 `OMEGA-TARGET-NOT-FOUND-001`

Target step does not exist.

Expected:

```text
REFUSE / TARGET_NOT_FOUND
```

### 10.4 `OMEGA-DANGLING-STEP-001`

Target is referenced by a later step.

Expected:

```text
REFUSE / DANGLING_STEP_REFERENCE
```

### 10.5 `OMEGA-DANGLING-RESULT-001`

Target is referenced by the final result.

Expected:

```text
REFUSE / DANGLING_RESULT_REFERENCE
```

### 10.6 `OMEGA-MALFORMED-PROPOSAL-001`

Proposal contains unknown fields, unknown patch operations, or executable/capability-shaped payload.

Expected:

```text
REFUSE / MALFORMED_PROPOSAL
```

### 10.7 `OMEGA-UNKNOWN-OP-POSTPATCH-001`

A candidate program fails registry resolution under the current local constitution.

Expected:

```text
REFUSE / UNKNOWN_OPERATION
```

This can be tested with a deliberately malformed candidate/gate specimen; `remove_step` itself cannot create a new operation.

### 10.8 `OMEGA-RESULT-CHANGED-001`

A structurally lawful patch is admitted but changes the declared operative result.

Expected:

```text
GATE: ADMIT
POST-CYCLE COMPARISON: NONZERO / DIFFERENT
```

This is essential.

It proves:

```text
STRUCTURAL ADMISSION != BEHAVIORAL EQUIVALENCE
```

The gate must not refuse merely because the result changed.

---

## 11. Reified cycle receipt

The orchestrator should preserve an inert cycle receipt sufficient to inspect/replay the exact transition.

Conceptual fields:

```text
schema: dogram.omega-cycle/v0
cycle_id
initial_program_digest
initial_execution_digest
meta_program_digest
meta_execution_digest
proposal_digest
gate_status
gate_reason_code
candidate_program_digest | null
candidate_execution_digest | null
```

The cycle receipt may additionally include canonical nested phase data where bounded and useful.

It may not include live `Program`, `Registry`, callable, or interpreter objects.

Hard law:

> **THE CYCLE RECEIPT DESCRIBES THE CROSSING. IT DOES NOT BECOME AUTHORITY TO CROSS AGAIN.**

---

## 12. Error/status discipline

The existing VM status family remains:

```text
OK
REFUSE
```

for the currently implemented `VMExecution` surface; the broader parent architecture retains `INSUFFICIENT_TO_TEST` as an architectural/public possibility where/when implemented.

Ω-CYCLE-001 must not invent semantic success statuses.

The phase gate has its own structural disposition:

```text
ADMIT
REFUSE
```

These are not interchangeable:

```text
VM OK != GATE ADMIT
VM REFUSE != GATE REFUSE
```

A META VM execution can be `OK` while the proposal it emitted is structurally refused by the phase gate.

That distinction must be receipted.

---

## 13. Determinism requirements

For identical:

```text
P0
W
META program
declared target
registry
phase configs
gate limits
```

Dogram must produce byte-stable canonical artifacts/digests for:

```text
ProgramData
ExecutionData
META result
ProposalData
GateDisposition
candidate ProgramData
cycle receipt
```

where fields are defined as canonical output.

No host dictionary iteration order, object address, wall clock, random value, environment variable, filesystem state, or network state may influence the result.

---

## 14. Security / capability floor

Ω-CYCLE-001 must preserve the current offline inert-machine model.

Explicit prohibitions:

```text
NO eval
NO exec
NO dynamic import from proposal data
NO callable serialization
NO arbitrary file reads
NO arbitrary file writes
NO network
NO shell
NO environment-derived authority
NO proposal-supplied Python module/function identity
```

All executable operation identity continues to resolve through the explicit admitted local registry.

---

## 15. Verification gate

Implementation is not complete until fresh verification demonstrates all of the following on the exact final head:

1. full unit test suite passes;
2. `python -m compileall -q dogram tests` passes;
3. zero project dependencies remain asserted;
4. public operator floor remains exactly four operators;
5. native `stdlib/delta` conformance remains green;
6. reification artifacts are canonical/deterministic;
7. the positive Ω cycle completes exactly one META round;
8. all required hostile fixtures produce their declared refusals/differences;
9. no proposal can bypass the phase gate;
10. no live capability appears in any reified artifact;
11. result-changing but structurally valid patches are admitted and reported as behaviorally different rather than gate-refused;
12. repeated identical cycles produce identical canonical digests/receipts.

No success claim may be based only on the positive fixture.

---

## 16. Migration order after Ω-CYCLE-001

If this slice survives review and implementation pressure, the preferred next sequence is:

```text
Ω1  reify + META + gate + one re-execution
Ω2  lower rectangle into native stdlib
Ω3  lower ablate into native stdlib
Ω4  lower reach into native stdlib
Ω5  admit bounded explicit branch proposals
Ω6  make conformance/residual corpora first-class reified inputs
Ω7  introduce PeelProposal as proposal-only data
Ω8  attempt the first host-intrinsic peel trial
Ω9  shrink one bootstrap intrinsic only after conformance proof
```

Open frontier work such as `RESIDUAL-SIGNATURE-001` and `AMBIGUITY-DEBT-001` becomes especially valuable after Ω1 because it can supply plural, typed, non-semantic META input without asking Dogram to choose which story is true.

This sequence is a roadmap, not blanket implementation approval.

Each architectural expansion receives its own design/pressure gate.

---

## 17. Kill conditions

Stop, demote, or redesign Ω-CYCLE-001 if any of the following becomes necessary:

- META needs live Python/runtime objects to do useful work;
- proposal data must carry arbitrary executable code;
- the gate must decide semantic/evidentiary quality to admit a candidate;
- a general rewrite language is required just to remove one declared step;
- the first cycle requires hidden recursion or unbounded reflection;
- reification cannot preserve exact ancestry without ambient state;
- the implementation silently changes the existing public operator floor;
- a structurally valid result-changing patch cannot be distinguished from a structurally invalid patch;
- the proposed machinery is more complex than completing the same experiment as an explicit host-side two-run harness with receipts.

That final kill condition matters: metaoscillation must pay for its constitutional complexity by preserving a real, inspectable phase boundary that the simpler harness lacks.

---

## 18. Seals

> **REIFY BEFORE REFLECT.**

> **META OUTPUT != NEXT EXECUTION.**

> **A PATCH MAY TRAVEL ONLY WITH THE PROGRAM AND EXECUTION CUT THAT PAID FOR IT.**

> **STRUCTURAL ADMISSION != BEHAVIORAL EQUIVALENCE.**

> **DOGRAM MAY LEARN TO PROPOSE ITS NEXT CALCULATION. IT MAY NOT LEARN TO DECLARE ITS OWN PROPOSAL TRUE.**

> **FIRST MAKE THE MACHINE SEE ITS OWN FOOTPRINT. THEN LET IT PROPOSE WHERE TO PUT THE NEXT FOOT.**
