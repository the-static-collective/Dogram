# PHASELIFT-3 — Promotion Kernel Design

**Date:** 2026-08-31  
**Status:** APPROVED ARCHITECTURAL DIRECTION · SPECIFICATION FOR REVIEW  
**Repository:** `the-static-collective/Dogram`  
**Branch:** `design/phaselift-3-promotion-kernel`  
**Amends:** `docs/superpowers/specs/2026-08-28-dogram-metaoscillatory-runtime-design.md`

## 0. Decision

Dogram will add an **internal PHASELIFT-3 promotion research kernel** that can pressure whether a recurring candidate has earned promotion from remnant/pattern/tool behavior toward an operator candidate.

PHASELIFT-3 is **not** a fifth public Dogram calculation operator. It does not mint truth, evidence, support, authority, historical identity, semantic meaning, or external capability. It accepts explicit attributed trial receipts and returns a deterministic local disposition about whether the declared promotion contract was satisfied.

The governing compression is:

```text
REPEAT -> TRANSFER -> GENERATE -> LIFT
```

The kernel exists to prevent a dangerous collapse:

```text
THREE APPEARANCES != THREE TRANSFORMATIONS
RECURRENCE != PORTABILITY
PORTABILITY != GENERATIVITY
GENERATIVITY != EXTERNAL AUTHORITY
LOCAL PROMOTION != WORLD ADMISSION
```

The central product is not another interesting artifact. It is an attributable claim that a candidate has demonstrated a bounded, replayable enlargement of a caller-declared executable grammar under three distinct trial roles.

---

## 1. Position inside Dogram

The existing public operator floor remains unchanged:

```text
delta@1
rectangle@1
ablate@1
reach@1
```

PHASELIFT-3 lives beside the existing internal research kernels and may consume receipts produced by the public operators, Dogram Ω execution, or explicit frozen fixtures. It may not silently reinterpret those receipts.

Conceptually:

```text
candidate x
   |
   +-- repeat trial ------ receipt r1
   +-- transfer trial ---- receipt r2
   +-- generate trial ---- receipt r3
                              |
                              v
                     PHASELIFT-3
                              |
                 promotion receipt p
                              |
                 PROMOTE / RETAIN / REFUSE
```

`PROMOTE` means only:

> the declared local promotion contract was satisfied by the supplied attributable trials.

It does not mean that the candidate becomes part of Dogram's public operator registry automatically.

---

## 2. Candidate classes

PHASELIFT-3 distinguishes four conceptual classes without pretending that Dogram can infer metaphysical categories from data:

```text
REMNANT -> PATTERN -> TOOL -> OPERATOR-CANDIDATE
```

Definitions are operational and local.

### 2.1 REMNANT

A named attributable object or procedure for which no successful recurrence has yet been demonstrated under the declared lens.

### 2.2 PATTERN

A candidate that can be replayed with materially equivalent declared behavior in at least one repeat trial.

### 2.3 TOOL

A candidate that can transfer into a caller-declared distinct context while preserving its declared transformation identity.

### 2.4 OPERATOR-CANDIDATE

A tool that, under a generation trial, produces a declared reusable capability not present in the caller-supplied pre-trial grammar.

Hard boundary:

```text
OPERATOR-CANDIDATE != PUBLIC DOGRAM OPERATOR
OPERATOR-CANDIDATE != ADMITTED AUTHORITY
```

---

## 3. Formal model

Let a bounded machine context be:

```math
K = (S, Omega, C)
```

where:

- `S` is the explicit working state;
- `Omega` is the caller-declared finite set of available operations before the trial;
- `C` is the explicit trial context and constraints.

A candidate `x` is tested through three role-distinct trials.

### 3.1 Repeat

```math
x(K_1) -> y_1
```

The repeat trial asks whether the candidate can replay its declared transformation identity under a materially equivalent role.

### 3.2 Transfer

```math
x(K_2) -> y_2,  K_2 !~= K_1
```

The transfer trial asks whether the candidate can preserve its declared transformation identity under a caller-declared context distinction.

The kernel does not invent what counts as distinct. The fixture must carry explicit `context_fingerprint` and `distinct_from` declarations, and the trial evaluator validates only the declared structural distinctions.

### 3.3 Generate

```math
x(K_3) -> y_3
```

The generation trial asks whether the resulting attributable receipt declares at least one reusable operation in:

```math
DeltaOmega = Omega_after - Omega_before
```

with:

```math
DeltaOmega != empty
```

A generated operation must have a stable local identifier, a declared input/output contract, and an attributable derivation reference. Mere output novelty does not count.

### 3.4 Lift

Conceptually:

```math
LIFTS(x)
=> RECURS(x)
and TRANSFERS(x)
and GENERATES(x)
and COMPOSES(x)
```

`COMPOSES` is satisfied when the candidate's generation trial contains an explicit lawful composition edge and a non-empty compositional surplus declaration that survives the kernel's structural checks.

---

## 4. `+Co` / `Not+Co` relation discipline

PHASELIFT-3 preserves the distinction between coexistence and composition.

Each relation witness is represented conceptually as:

```text
(a, verb, b, phase)
```

where:

```text
phase in {NOT_PLUS_CO, PLUS_CO}
```

`NOT_PLUS_CO` means the two attributable elements may coexist without being collapsed into a new object.

`PLUS_CO` means the caller declares that a specific composition verb binds the two elements for this trial.

A valid composition witness must include:

```text
left_ref
verb_id
right_ref
phase
output_ref
surplus_capability_refs
```

Hard laws:

```text
A + B IS NOT A COMPOSITION WITNESS
PLUS_CO REQUIRES A VERB
PLUS_CO DOES NOT ERASE NOT_PLUS_CO IDENTITY
COMPOSITION OUTPUT MUST RETAIN SOURCE ATTRIBUTION
```

The kernel does not decide whether the verb is philosophically correct. It validates that the declared composition is typed, attributable, replayable, and non-circular under the bounded fixture.

---

## 5. Promotion state machine

The state machine is deliberately small.

```text
SEED
  |
  | repeat passes
  v
REPEATED
  |
  | transfer passes
  v
TRANSFERRED
  |
  | generation + composition pass
  v
GENERATIVE
  |
  | all invariants satisfied
  v
PROMOTABLE
```

Any failed earned transition yields `RETAIN`, not retroactive erasure of previous receipts.

Malformed, contradictory, circular, or scope-violating inputs yield `REFUSE`.

The top-level dispositions are:

```text
PROMOTE
RETAIN
REFUSE
INSUFFICIENT_TO_TEST
```

Meaning:

- `PROMOTE`: every required transition and invariant passed.
- `RETAIN`: the candidate remains at the highest earned class; one or more later promotion conditions failed.
- `REFUSE`: the kernel could not lawfully evaluate the supplied contract because of malformed, circular, contradictory, or forbidden input.
- `INSUFFICIENT_TO_TEST`: required attributed trial material is missing or explicitly unresolved.

Dogram's ordinary calculation `OK` status is not reused as promotion semantics.

---

## 6. Receipt schema

The first schema is:

```text
dogram.phaselift.receipt/v0
```

Conceptual shape:

```json
{
  "schema": "dogram.phaselift.receipt/v0",
  "candidate_id": "candidate/example",
  "candidate_version": 1,
  "input_digest": "sha256:...",
  "trial_refs": {
    "repeat": "trial/repeat-001",
    "transfer": "trial/transfer-001",
    "generate": "trial/generate-001"
  },
  "checks": {
    "recurs": true,
    "transfers": true,
    "composes": true,
    "generates": true,
    "non_circular": true,
    "provenance_complete": true
  },
  "omega_before": ["op/a", "op/b"],
  "omega_after": ["op/a", "op/b", "op/new"],
  "delta_omega": ["op/new"],
  "earned_class": "OPERATOR_CANDIDATE",
  "disposition": "PROMOTE",
  "reason_codes": [],
  "residuals": [],
  "receipt_digest": "sha256:..."
}
```

Canonicalization and digest behavior must reuse Dogram's existing canonical JSON discipline where possible.

---

## 7. Trial schema

Frozen trials use:

```text
dogram.phaselift.trial/v0
```

Required fields:

```text
schema
trial_id
role
candidate_ref
candidate_digest
context_fingerprint
input_refs
output_refs
transformation_id
transformation_version
composition_witnesses
omega_before
generated_operations
provenance_refs
residuals
```

Role is exactly one of:

```text
REPEAT
TRANSFER
GENERATE
```

The kernel rejects a single trial reused under multiple roles unless the fixture explicitly demonstrates independent executions with distinct receipt identities. Three aliases to one receipt are not three trials.

---

## 8. Generativity and compositional surplus

PHASELIFT-3 must distinguish output novelty from grammar growth.

A generation trial may emit any number of novel values, but it counts as generative only if at least one `generated_operation` is present and valid.

Each generated operation declares:

```text
operation_id
operation_version
input_kinds
output_kind
derivation_refs
replay_probe_ref
```

The compositional surplus for a witness is represented as the subset of generated capability refs attributable to the declared composition and absent from both declared input capability sets.

Conceptually:

```math
sigma(a,b,f) = Capabilities(f(a,b)) - (Capabilities(a) union Capabilities(b))
```

The implementation does not attempt general theorem proving over capability sets. The fixture supplies finite explicit capability identities; the kernel computes finite set difference deterministically.

Required condition:

```text
sigma != empty
```

for at least one generation composition witness.

---

## 9. Anti-self-certification rule

A candidate may not earn promotion solely by declaring or generating its own promotion predicate.

Forbidden circular forms include:

```text
candidate x generates op/promote-x
op/promote-x is the only witness that x generated capability
```

or:

```text
trial receipt cites the PHASELIFT result being computed as provenance for an earned transition
```

The kernel computes a bounded dependency graph over trial refs, composition refs, generated-operation derivations, and the promotion receipt under construction.

Any cycle reaching the receipt-under-construction yields:

```text
disposition: REFUSE
reason_code: CIRCULAR_PROMOTION_PROOF
```

---

## 10. Identity and transfer law

Transfer cannot be proven by changing the candidate until it becomes a different transformation.

Every trial carries:

```text
candidate_digest
transformation_id
transformation_version
```

Repeat and transfer require the same candidate digest and transformation identity unless the contract explicitly names a permitted inert adapter whose own digest is included in provenance.

A material change to the candidate implementation without an explicit version transition makes the supplied three-trial promotion sequence non-conformant.

Required distinction:

```text
CONTEXT CHANGED != CANDIDATE CHANGED
```

---

## 11. Distinct-context test

The kernel cannot know semantic context difference from arbitrary JSON. Instead, the transfer fixture carries an explicit finite context descriptor:

```json
{
  "context_fingerprint": {
    "domain": "graph",
    "carrier_kind": "directed_graph",
    "input_shape": "four_nodes",
    "probe_kind": "reachability"
  },
  "distinct_from": {
    "trial_ref": "trial/repeat-001",
    "dimensions": ["domain", "carrier_kind"]
  }
}
```

The evaluator checks that every named distinct dimension actually differs.

If not:

```text
disposition: RETAIN
reason_code: TRANSFER_CONTEXT_NOT_DISTINCT
```

No hidden semantic inference is performed.

---

## 12. Required invariants

The kernel must enforce at least these invariants:

```text
P3-001 THREE RECEIPTS != THREE ROLES
P3-002 ROLE RECEIPTS MUST BE ATTRIBUTABLE AND DISTINCT
P3-003 REPEAT MUST PRESERVE DECLARED TRANSFORMATION IDENTITY
P3-004 TRANSFER MUST CHANGE DECLARED CONTEXT, NOT CANDIDATE IDENTITY
P3-005 GENERATE REQUIRES NON-EMPTY DELTA_OMEGA
P3-006 NOVEL VALUE != GENERATED OPERATION
P3-007 PLUS_CO REQUIRES AN EXPLICIT VERB
P3-008 COMPOSITION MUST PRESERVE SOURCE ATTRIBUTION
P3-009 GENERATION REQUIRES NON-EMPTY COMPOSITIONAL SURPLUS
P3-010 PROMOTION PROOF MUST BE ACYCLIC
P3-011 PHASELIFT RECEIPT CANNOT CERTIFY ITS OWN PREMISES
P3-012 PROMOTE != PUBLIC OPERATOR ADMISSION
P3-013 RETAIN DOES NOT ERASE PREVIOUSLY EARNED CLASS
P3-014 SAME INPUT + SAME TRIALS + SAME CONFIG = SAME RECEIPT
P3-015 MISSING MATERIAL -> INSUFFICIENT_TO_TEST, NOT FALSE CERTAINTY
```

---

## 13. Adversarial fixtures

The first implementation is admitted only with at least three hostile fixtures designed to defeat naive promotion logic.

### 13.1 `three-echoes.json`

Purpose: prove that recurrence alone cannot promote.

Shape:

```text
repeat: pass
transfer: same context disguised by new receipt id
generate: repeats existing operation only
```

Expected:

```text
earned_class: PATTERN
disposition: RETAIN
reason_codes:
  - TRANSFER_CONTEXT_NOT_DISTINCT
  - DELTA_OMEGA_EMPTY
```

### 13.2 `novel-output-no-new-verb.json`

Purpose: defeat the collapse `new output == new operator`.

Shape:

```text
repeat: pass
transfer: pass
generate: produces previously unseen value
omega_before == omega_after
generated_operations: []
```

Expected:

```text
earned_class: TOOL
disposition: RETAIN
reason_code: DELTA_OMEGA_EMPTY
```

### 13.3 `self-minting-operator.json`

Purpose: prevent self-certification.

Shape:

```text
candidate declares a new operation
new operation's only derivation points to pending PHASELIFT receipt
```

Expected:

```text
disposition: REFUSE
reason_code: CIRCULAR_PROMOTION_PROOF
```

---

## 14. Positive fixture

A positive control is also required: `lawful-new-verb.json`.

It must demonstrate:

```text
repeat: same transformation replays
transfer: same transformation operates in a declared distinct context
generate: explicit PLUS_CO composition with verb and provenance
sigma: non-empty
delta_omega: exactly one new operation
new operation has a replay probe independent of the promotion result
proof graph: acyclic
```

Expected:

```text
earned_class: OPERATOR_CANDIDATE
disposition: PROMOTE
```

This fixture proves only the local kernel contract.

---

## 15. Proposed implementation boundary

The implementation should remain isolated from the public engine dispatch table in its first slice.

Proposed files:

```text
dogram/phaselift.py
tests/test_phaselift.py
tests/fixtures/phaselift/three-echoes.json
tests/fixtures/phaselift/novel-output-no-new-verb.json
tests/fixtures/phaselift/self-minting-operator.json
tests/fixtures/phaselift/lawful-new-verb.json
research/phaselift-3-promotion-kernel.md
```

No CLI route is required in the first slice.

No new third-party dependency is required.

---

## 16. Evaluator interface

The first Python research evaluator should expose one narrow function:

```python
def evaluate_phaselift(specimen: dict) -> tuple[dict, dict]:
    ...
```

The first tuple element is the calculation/promotion result. The second is the canonical receipt, following the repository's existing evaluator convention.

The evaluator should remain pure with respect to ambient state:

```text
NO NETWORK
NO FILE WRITE
NO CLOCK DEPENDENCE
NO RANDOMNESS
NO DYNAMIC IMPORT
NO EVAL / EXEC
```

Fixture loading belongs to tests, not the evaluator.

---

## 17. Reason code floor

The first implementation requires stable reason codes:

```text
MISSING_TRIAL
DUPLICATE_TRIAL_RECEIPT
CANDIDATE_IDENTITY_CHANGED
TRANSFORMATION_IDENTITY_CHANGED
TRANSFER_CONTEXT_NOT_DISTINCT
PLUS_CO_MISSING_VERB
COMPOSITION_ATTRIBUTION_INCOMPLETE
DELTA_OMEGA_EMPTY
GENERATED_OPERATION_INVALID
COMPOSITIONAL_SURPLUS_EMPTY
CIRCULAR_PROMOTION_PROOF
PROVENANCE_INCOMPLETE
SCHEMA_INVALID
```

Reason ordering must be deterministic.

---

## 18. Explicit non-goals

This slice does not:

- automatically discover candidates in the Daily Slice;
- decide which research idea is important;
- crawl external repositories;
- admit generated operations into the public Dogram registry;
- mutate Dogram's host kernel;
- perform semantic theorem proving;
- assign truth/evidence/support/authority;
- create unrestricted self-modifying code;
- implement general graph rewriting;
- infer hidden semantic context distinctions.

Those may become later bounded slices only after PHASELIFT-3 itself survives replay, transfer, and generative use.

---

## 19. Future mADDMaximachinal relation

PHASELIFT-3 is the promotion kernel required by the broader mADDMaximachinal architecture.

Conceptually:

```text
COMPOST
  -> WITNESS
  -> PRESSURE
  -> BRAID
  -> COMPOSE
  -> PROBE
  -> LAND
  -> RECEIPT
  -> PHASELIFT-3
```

The broader machine may eventually search for candidates and compositions, but PHASELIFT-3 remains intentionally narrower:

> It judges whether a caller-declared candidate survived a caller-declared bounded promotion contract. It does not decide what to search for or what reality means.

This separation keeps search creativity outside the constitutional gate.

---

## 20. Acceptance floor

The first slice is acceptable when all of the following are true:

1. the four public Dogram operators remain unchanged;
2. `evaluate_phaselift` is deterministic and pure;
3. all four frozen fixtures produce their exact declared dispositions;
4. three aliases of one receipt cannot satisfy three roles;
5. a novel output without `DeltaOmega` cannot promote;
6. a context rename without declared changed dimensions cannot satisfy transfer;
7. a `PLUS_CO` witness without a verb cannot satisfy composition;
8. a self-referential promotion proof is refused;
9. the positive fixture promotes with exactly one attributable new operation;
10. the result explicitly states that local promotion is not public operator admission;
11. the full existing test suite still passes.

The design deliberately keeps the first executable slice small enough to pressure hard.
