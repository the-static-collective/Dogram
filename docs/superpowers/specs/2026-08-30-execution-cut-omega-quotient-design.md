# Dogram EXECUTION-CUT / OMEGA-QUOTIENT — Controlled Self-Experiment Design

**Date:** 2026-08-30  
**Status:** DESIGN APPROVED IN CHAT · WOLFRAM-PRESSURED · AWAITING HUMAN REVIEW  
**Repository:** `the-static-collective/Dogram`  
**Baseline main:** `1fa64b373972e6079f2c08783f47e9c47538929a`  
**Parent:** `docs/superpowers/specs/2026-08-30-dogram-omega-cycle-001-design.md`  
**Companion:** `docs/superpowers/specs/2026-08-28-quotient-probe-completion-mathals-design.md`

## 0. Decision

The next seam after `OMEGA-CYCLE-001` is not broader self-modification and not another public operator.

It is the smallest controlled-experiment layer that can distinguish:

```text
THE DECLARED TARGET SURVIVED
!=
NOTHING CHANGED
```

The design has two bounded objects:

```text
EXECUTION-CUT-001
OMEGA-QUOTIENT-001
```

`EXECUTION-CUT-001` reifies the exact runtime-realized contact surface of one Dogram execution.

`OMEGA-QUOTIENT-001` compares one baseline execution and one admitted candidate execution under a target/probe family declared before comparison, while preserving every measured footprint difference that the target quotient intentionally ignores.

The core flow is:

```text
P0 + W
  -> EXEC
  -> e0
  -> EXECUTION CUT F(e0)

P0 -- bounded admitted proposal --> P1

P1 + W
  -> EXEC
  -> e1
  -> EXECUTION CUT F(e1)

PREDECLARED TARGET FAMILY T
  -> compare e0/e1 under T
  -> target-relative equivalence verdict
  -> typed footprint residual Delta_F(e0,e1)
```

The design does **not** allow Dogram to conclude that an admitted candidate is true, meaningful, better, globally equivalent, causally explanatory, evidentiary, or authoritative.

> **THE TARGET MAY SURVIVE WHILE THE CONTACT SURFACE CHANGES. KEEP BOTH RECEIPTS.**

---

## 1. Why this seam exists now

At baseline `1fa64b...`, Dogram has:

- a deterministic acyclic Mathal VM;
- explicit finite execution fuel;
- ordered step traces;
- canonical argument/result digests;
- a versioned bootstrap registry;
- native DELTA conformance;
- the four-public-operator floor `delta@1`, `rectangle@1`, `ablate@1`, `reach@1`;
- `OMEGA-CYCLE-001`, whose approved design requires exact runtime-resolved input provenance before META reflection.

The architectural gap is therefore no longer merely:

```text
execution -> next execution
```

It is:

```text
baseline execution
candidate execution
        X
        | target-relative comparison is too coarse by itself
        v
what changed while the target survived?
```

The quotient/probe work already establishes that equivalence is meaningful only relative to a declared target family.

`OMEGA-CYCLE-001` establishes that Dogram may execute, reify, propose, gate, and execute again.

This design joins those two facts without enlarging Dogram's authority.

---

## 2. Constitutional boundary

The governing laws are:

```text
REIFY BEFORE REFLECT.
DECLARE THE TARGET BEFORE COMPARISON.
PRESERVE THE RESIDUAL AFTER QUOTIENTING.
```

Hard non-collapses:

```text
SAME DECLARED RESULT != SAME EXECUTION
SAME TARGET RESPONSE != GLOBAL EQUIVALENCE
CONSUMED INPUT != CAUSAL SUPPORT
EXECUTED STEP != NECESSARY STEP
REMOVED STEP != IRRELEVANT STEP GLOBALLY
GATE ADMIT != SEMANTIC EQUIVALENCE
FOOTPRINT DELTA != EXPLANATION
SMALLER FOOTPRINT != BETTER PROGRAM
TARGET EQUIVALENCE != TRUTH
TARGET EQUIVALENCE != AUTHORITY
```

Dogram may calculate and receipt the comparison.

It may not decide what the comparison means outside the declared calculational target.

---

## 3. `EXECUTION-CUT-001`

### 3.1 Purpose

An execution cut is an inert, occurrence-bound representation of what one VM execution actually did and touched.

It is not reconstructed from everything the program *could* have touched.

Conceptually:

```math
F(e) = (A, C, Tau, Phi, Rho)
```

where:

- `A` = terminal execution outcome;
- `C` = ordered runtime-resolved input contact sequence;
- `Tau` = ordered executed-step trace;
- `Phi` = finite execution-budget state;
- `Rho` = explicit execution residual/refusal state.

The existing `program_digest` and `input_digest` from `OMEGA-CYCLE-001` bind the cut to the exact program and supplied world/input cut.

### 3.2 Candidate inert shape

Research/design shape only; no schema promotion from this document:

```json
{
  "schema": "dogram.execution-cut/v0-candidate",
  "program_digest": "sha256:...",
  "input_digest": "sha256:...",
  "status": "OK",
  "result": {},
  "reason_code": null,
  "residuals": [],
  "consumed_input_addresses": [
    ["value"],
    ["diagnostic"]
  ],
  "step_trace": [],
  "fuel_initial": 10,
  "fuel_remaining": 8
}
```

`consumed_input_addresses` is an ordered runtime witness.

Do not silently coerce it into a mathematical set. Order may reveal early stop/refusal boundaries even when the unique address inventory is identical.

### 3.3 Successful resolution only

Preserve the parent law:

```text
SYNTACTIC INPUT REFERENCE
!=
SUCCESSFULLY RESOLVED INPUT ADDRESS
```

A failed address resolution does not become a successful consumed address.

If all arguments resolve and the intrinsic later refuses, those successfully resolved addresses remain in the execution contact sequence.

### 3.4 Contact is not causation

The cut proves only runtime contact under this exact execution.

```text
TOUCHED
!=
USED AS CAUSAL SUPPORT
```

A diagnostic field can be resolved and executed without being necessary for the declared final result.

Conversely, absence from one execution cut does not prove global irrelevance under other programs, inputs, targets, or reachable futures.

---

## 4. Typed footprint residual

### 4.1 Do not use one untyped symmetric difference

A tempting notation is:

```math
Delta_F = F(e0) triangle F(e1)
```

That notation is acceptable only as informal shorthand.

It is **not** the implementation law.

Different footprint components have different structure:

- results are canonical values;
- consumed addresses are ordered paths;
- step traces are ordered records;
- fuel is numeric state;
- residuals/refusals are structured records.

A set symmetric difference can erase differences that matter.

Example:

```text
trace A = [get-value, diagnostic, compare]
trace B = [diagnostic, get-value, compare]
```

As sets, they are identical.

As execution histories, they are not.

### 4.2 Component-wise residual

Use a typed residual family:

```math
Delta_F(e0,e1)
  = (
      delta_A(A0,A1),
      delta_C(C0,C1),
      delta_Tau(Tau0,Tau1),
      delta_Phi(Phi0,Phi1),
      delta_Rho(Rho0,Rho1)
    )
```

The minimum lawful representation may simply preserve exact `before` and `after` values for every differing component.

Candidate shape:

```json
{
  "result": {"relation": "SAME"},
  "consumed_input_addresses": {
    "before": [["value"], ["diagnostic"]],
    "after": [["value"]]
  },
  "step_trace": {
    "before": ["value", "diagnostic"],
    "after": ["value"]
  },
  "fuel": {
    "initial": 10,
    "before_remaining": 8,
    "after_remaining": 9
  },
  "residuals": {"relation": "SAME"}
}
```

Derived conveniences such as added/removed addresses may be calculated, but the exact ordered source values remain authoritative for the comparison witness.

---

## 5. Target family `T`

### 5.1 Definition

Let `T` be a finite ordered family of declared probes/observations:

```math
T = {p1, p2, ..., pn}
```

Each probe maps an execution witness to a canonical observation value:

```math
p_i : E -> O_i
```

For the first slice, probes must be:

- declared before baseline/candidate comparison;
- deterministic;
- total over the admitted fixture domain;
- canonicalizable;
- incapable of acquiring ambient authority or hidden I/O.

A probe that would otherwise be partial must map non-answer/refusal into an explicit canonical observation rather than silently disappear from the comparison.

### 5.2 Target-relative equivalence

For fixed `T`:

```math
e0 ~_T e1
iff
forall p in T,
  p(e0) = p(e1)
```

The relation is about the declared observations only.

It does not collapse the execution cuts themselves.

```text
~_T lives beside Delta_F.
It does not erase Delta_F.
```

### 5.3 Equivalence law

When `T` is fixed and every probe is deterministic and total, `~_T` is an equivalence relation:

```text
reflexive
symmetric
transitive
```

This gives a lawful target-relative quotient of the admitted execution domain.

### 5.4 Target refinement law

For two fixed target families:

```math
T1 subseteq T2
```

then:

```math
e0 ~_{T2} e1
=>
e0 ~_{T1} e1
```

Adding declared probes can split an equivalence class.

It cannot lawfully merge states that were already distinguished by the smaller family.

So the quotient partition refines monotonically as declared observation pressure increases.

### 5.5 Why predeclaration is load-bearing

If the target family is chosen adaptively per pair after looking at outcomes, the object is no longer one fixed equivalence relation.

A simple counterexample can satisfy:

```text
A ~ B under probe x
B ~ C under probe y
A !~ C under probes x+y
```

That pair-dependent chooser breaks transitivity.

Therefore:

> **A TARGET FAMILY THAT MOVES WITH THE ANSWER CANNOT PAY FOR AN EQUIVALENCE CLAIM.**

This is the mathematical reason predeclaration is not administrative ceremony.

---

## 6. `OMEGA-QUOTIENT-001`

### 6.1 Purpose

`OMEGA-QUOTIENT-001` is one paired Dogram experiment:

```math
Q = (P0, e0, P1, e1, T, V_T, Delta_F)
```

where:

- `P0` = exact baseline program;
- `e0` = baseline execution;
- `P1` = exact gate-admitted candidate program;
- `e1` = candidate execution;
- `T` = predeclared target family;
- `V_T` = target-relative comparison verdict;
- `Delta_F` = typed execution-footprint residual.

The first candidate is the exact `OMEGA-CYCLE-001` positive fixture:

```text
P0 contains:
  operative value step
  dispensable diagnostic step

proposal:
  remove_step(diagnostic)

P1:
  diagnostic step absent
```

### 6.2 First target family

Keep the first target intentionally narrow:

```text
T_result = [declared operative result]
```

Expected:

```text
P0 ~T_result P1
```

while:

```text
Delta_F != empty
```

because at minimum the diagnostic step and its resolved diagnostic input contact disappear, and fuel use changes.

The useful receipt is therefore not:

```text
P0 == P1
```

It is:

```text
THE DECLARED RESULT SURVIVED THIS EXACT ABLATION.
THE EXECUTION CONTACT SURFACE DID NOT REMAIN IDENTICAL.
```

### 6.3 Same world cut

The paired experiment must use the same canonical input/world payload:

```text
input_digest(e0) == input_digest(e1)
```

Any mismatch refuses the comparison as a controlled `OMEGA-QUOTIENT-001` specimen.

### 6.4 Same runtime constitution — bounded first proof

The first paired specimen must execute `e0` and `e1` inside one bounded orchestrator invocation using:

- the same `Registry` instance;
- the same `VMConfig` value;
- the same VM implementation body for that invocation.

This is a within-run experimental control.

**Current Dogram receipts do not yet prove a durable cross-run implementation identity for the VM/intrinsic bodies.**

Therefore this design does **not** claim that an archived quotient receipt alone is sufficient for historical cross-version replay.

A future runtime-body/constitution pin may be justified if cross-run reproduction demonstrates information not already captured by program/input/operation versions and repository provenance.

Do not smuggle that future requirement into this slice as a fake solved problem.

### 6.5 Gate relation

The phase gate still decides only structural admission.

```text
GATE ADMIT
!=
TARGET EQUIVALENT
```

Correct order:

```text
proposal
-> structural gate
-> candidate execution
-> target comparison
-> footprint residual
```

The gate must not pre-compute or assume the quotient verdict.

---

## 7. Candidate comparison receipt

Research/design shape only:

```json
{
  "schema": "dogram.omega-quotient/v0-candidate",
  "baseline": {
    "program_digest": "sha256:P0",
    "execution_digest": "sha256:E0"
  },
  "candidate": {
    "program_digest": "sha256:P1",
    "execution_digest": "sha256:E1"
  },
  "input_digest": "sha256:W",
  "target_family": {
    "id": "T_result",
    "declared_before_comparison": true,
    "probes": ["result"]
  },
  "target_verdict": "EQUIVALENT_UNDER_T",
  "footprint_residual": {},
  "does_not_establish": [
    "global_equivalence",
    "causal_irrelevance",
    "evidence",
    "support",
    "truth",
    "authority",
    "cross-runtime replay"
  ]
}
```

The receipt should be attributable to both exact execution digests.

No candidate may reuse a quotient verdict generated from a different baseline/candidate pair.

---

## 8. Wolfram pressure checks

The design was pressure-tested computationally before writing.

### 8.1 Fixed-target equivalence

Toy states were compared under a fixed family containing `result` and `reachability` probes.

Observed relation matrix:

```text
P0 P1 equivalent
P0 P2 not equivalent
P0 P3 not equivalent
```

The generated relation satisfied:

```text
reflexive  = true
symmetric  = true
transitive = true
```

### 8.2 Target refinement

With:

```text
T1 = [result]
T2 = [result, reachability]
T1 subset T2
```

observed quotient classes were:

```text
under T1:
  {P0, P1, P2}
  {P3}

under T2:
  {P0, P1}
  {P2}
  {P3}
```

and every `T2` equivalence implied `T1` equivalence.

This matches the refinement law.

### 8.3 Result survived / footprint changed

Toy baseline and candidate executions both returned `7` while the candidate removed one diagnostic contact.

Observed residual contained differences in:

```text
consumed input addresses
executed steps
fuel remaining
```

while `result` stayed equal.

That is the exact seam this design preserves.

### 8.4 Untyped symmetric-difference failure

Two ordered traces with the same members but different order produced an empty set symmetric difference while remaining unequal as sequences.

Therefore the implementation residual must be typed/component-wise.

### 8.5 Adaptive-target transitivity failure

A pair-dependent target chooser was constructed with:

```text
A ~ B = true
B ~ C = true
A ~ C = false
```

This demonstrates why `T` must be fixed/predeclared for an equivalence claim.

These checks validate the formal shape only. They are not Dogram runtime evidence.

---

## 9. Required positive fixture

### `OMEGA-QUOTIENT-POSITIVE-001`

Freeze:

```text
P0
W
T_result
remove_step(diagnostic)
```

Required flow:

```text
EXEC(P0,W) -> e0 OK
REIFY -> execution cut F0
META -> proposal remove diagnostic
GATE -> ADMIT P1
EXEC(P1,W) -> e1 OK
REIFY -> execution cut F1
COMPARE under T_result
```

Required assertions:

```text
input_digest(e0) == input_digest(e1)
result(e0) == result(e1)
e0 ~T_result e1
F0 != F1
Delta_F records diagnostic contact removal
Delta_F records diagnostic step removal
fuel_used(P1) < fuel_used(P0)
```

The fuel inequality is fixture-specific, not a universal optimization law.

---

## 10. Required hostile fixtures

### 10.1 `OMEGA-QUOTIENT-TARGET-MOVED-001`

Choose or alter `T` only after observing baseline/candidate results.

Expected:

```text
REFUSE TARGET_NOT_PREDECLARED
```

### 10.2 `OMEGA-QUOTIENT-INPUT-DRIFT-001`

Run candidate against a different input digest.

Expected:

```text
REFUSE INPUT_CUT_MISMATCH
```

### 10.3 `OMEGA-QUOTIENT-ORDER-ERASURE-001`

Provide two traces with identical member sets and different order.

Expected:

```text
typed trace residual != empty
```

Any set-only comparison fails the fixture.

### 10.4 `OMEGA-QUOTIENT-RESULT-ONLY-OVERREACH-001`

Same declared result, different contact surface.

Expected lawful conclusion:

```text
EQUIVALENT_UNDER_T_result
```

Expected refused conclusion:

```text
GLOBALLY_EQUIVALENT
```

### 10.5 `OMEGA-QUOTIENT-GATE-CONFLATION-001`

Gate admits structurally valid candidate but declared target changes.

Expected:

```text
GATE = ADMIT
TARGET VERDICT = DIFFERENT_UNDER_T
```

This proves admission and semantic survival remain separate phases.

### 10.6 `OMEGA-QUOTIENT-RUNTIME-DRIFT-HOLD-001`

Attempt to compare executions produced in distinct unpinned runtime bodies and claim historical controlled equivalence.

Expected first-design disposition:

```text
HOLD / OUTSIDE CLAIM BOUNDARY
```

Do not fabricate a cross-runtime proof from version strings alone.

---

## 11. Existing-operator lowering

No new public Dogram operator is justified.

The first slice can lower into:

```text
delta@1
```

for ordered footprint/observation records plus ordinary host fixture bookkeeping required by `OMEGA-CYCLE-001` reification and orchestration.

`ablate@1` remains useful for separate declared structural pressure.

`reach@1` may become a target probe only when a specific fixture predeclares reachability as part of `T`.

`rectangle@1` is not required merely to complete the public operator set.

Do not add:

```text
equivalent@1
experiment@1
footprint@1
quotient@1
compare@1
```

from this design.

---

## 12. Future pressure — explicitly not this slice

Once `OMEGA-QUOTIENT-001` exists as a receipt-bearing paired experiment, a later design may ask whether META can consume the residual and propose a next discriminating experiment.

Potential future loop:

```text
paired experiment
-> residual
-> candidate discriminator / ablation proposal
-> local phase gate
-> next paired experiment
```

That would move Dogram from self-contact toward bounded experiment generation.

It is **not** authorized here.

Keep out of scope:

- automatic experiment selection;
- automatic target-family selection;
- automatic interpretation of residual significance;
- multi-cycle autonomous optimization;
- scalar fitness functions;
- self-declared necessity/irrelevance;
- self-declared evidence/support/truth;
- authority expansion;
- network or filesystem effects.

The first lawful proof is much smaller:

> **DOGRAM CAN RECEIPT THAT A DECLARED TARGET SURVIVED AN EXACT ADMITTED CHANGE WHILE PRESERVING WHAT ELSE CHANGED.**

---

## 13. Cross-stack compatibility

This design remains Dogram-local but fits the neighboring project boundaries without merging their ontologies.

### LOADOUT

Continuity may cross into a receiver-local next world while authority is reconstituted locally.

Dogram analogue:

```text
proposal ancestry may cross the gate
!=
gate admission grants semantic truth
```

### 3rdi

A present projection may change while historical attribution remains pinned.

Dogram analogue:

```text
target quotient may hide a distinction for T
!=
execution cut deletes the distinction historically
```

### ALEX

A continuing logical identity may survive rebinding while historical consequences stay bound to the exact producing body.

Dogram analogue:

```text
candidate program may be equivalent under T
!=
baseline execution becomes attributable to candidate program
```

Shared membrane candidate:

```text
NEXT STATE MAY FORM.
ANCESTRY STAYS PINNED.
LOCAL ADMISSION DOES NOT RETROACTIVELY REWRITE THE PRIOR CUT.
```

This is architectural resonance, not a master ontology.

---

## 14. Promotion gate

Implementation should not begin until human review accepts at least these decisions:

1. execution contact must be runtime-realized, not syntactically inferred;
2. consumed-address order is preserved;
3. footprint residual is typed/component-wise;
4. `T` is fixed/predeclared and deterministic;
5. same target result does not imply same execution;
6. same input digest is required for the first controlled pair;
7. same-runtime control is bounded to one orchestrator invocation until durable runtime-body pinning is separately justified;
8. gate admission and target equivalence remain separate phases;
9. no new public operator is added;
10. automatic experiment selection remains out of scope.

If any of those boundaries cannot survive hostile fixtures, narrow the design before implementation.

---

## 15. Seal

```text
EXECUTE.
WITNESS CONTACT.
CHANGE ONE DECLARED THING.
GATE THE NEXT PROGRAM.
EXECUTE AGAIN.
COMPARE ONLY WHAT WAS DECLARED.
KEEP EVERYTHING ELSE THAT CHANGED.
```

> **A SURVIVING TARGET IS A RECEIPT ABOUT THAT TARGET, NOT A LICENSE TO ERASE THE RESIDUAL.**

> **DOGRAM MAY LEARN TO RUN BETTER QUESTIONS BEFORE IT EVER CLAIMS TO KNOW BETTER ANSWERS.**
