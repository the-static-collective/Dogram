# Dogram Ω — Metaoscillatory Mathal Runtime

**Date:** 2026-08-28  
**Status:** APPROVED ARCHITECTURAL DESIGN · IMPLEMENTATION NOT YET ADMITTED  
**Repository:** `the-static-collective/Dogram`  
**Supersedes:** none  
**Amends:** `docs/superpowers/specs/2026-08-28-dogram-v0-design.md`

## 0. Decision

Dogram will not stop at a direct Python operator lab, and it will not begin as a fully metacircular or unrestricted graph-rewrite machine.

The selected architecture is a **metaoscillatory Mathal VM**:

> **A small deterministic host kernel executes typed mathal programs; each execution is reified into attributable data; bounded meta-mathals may inspect that data and propose the next program state; proposals cross an explicit phase gate before they can become executable.**

The runtime therefore alternates between two distinct modes:

```text
EXECUTE
   ↓
RECEIPT / REIFY
   ↓
META-PASS
   ↓
PROGRAM PROPOSAL
   ↓
PHASE GATE
   ↓
EXECUTE AGAIN
```

This is intentionally **not** full metacircularity.

Dogram does not require its interpreter to be written entirely in Dogram. Instead, Dogram is designed so that increasingly large portions of its behavior may be expressed as mathals and pressure-tested against the remaining host floor.

The governing compression is:

> **DO → WITNESS → PEEL → VARY → DO AGAIN.**

---

## 1. Why this middle architecture exists

Three implementation shapes were considered.

### 1.1 Direct Python operators

Python directly implements `delta`, `rectangle`, `ablate`, and `reach`.

Advantages:

- smallest implementation effort;
- straightforward tests;
- the existing v0 implementation plan already describes this shape.

Limitation:

- Dogram uses mathals as subject matter but does not meaningfully run on mathals.

### 1.2 Tiny Mathal VM

Python implements a small evaluator while Dogram's public operators are expressed as mathal programs.

Advantages:

- deterministic;
- testable;
- Dogram begins executing its own native representations;
- the host floor can shrink later.

Limitation:

- execution remains largely one-way: program → result.

### 1.3 Full graph-rewrite / metacircular runtime

Interpreter and runtime behavior are themselves substantially expressed through the language they interpret.

Advantages:

- maximum self-description and rewrite power.

Costs:

- difficult termination analysis;
- much larger trusted computing base in practice;
- harder debugging and replay;
- reflection can silently become authority or arbitrary code execution;
- v0 becomes architecture research rather than a usable calculation instrument.

### 1.4 Selected middle: metaoscillation

The selected architecture preserves the small VM but adds a lawful reflective cycle:

```text
RUN ↔ REFLECT
```

The reflective side operates on **reified execution artifacts**, not on the live interpreter.

This gives Dogram enough self-contact to inspect, compare, pressure, and propose changes to its own mathal programs without requiring full interpreter self-hosting.

---

## 2. Core distinction: metacircularity vs metaoscillation

### Metacircularity

A language can describe or implement the machine that interprets the language.

### Metaoscillation

A language can repeatedly encounter attributable descriptions of its own execution and use them to propose its next bounded computation.

The difference is temporal and constitutional.

```text
METACIRCULAR
program
  ↓
interpreter expressed in program language
  ↓
self-interpretation

METAOSCILLATORY
program
  ↓ execute
receipt
  ↓ reify
program-as-data + receipt-as-data
  ↓ meta-pass
proposal
  ↓ gate
next executable program
```

Metaoscillation does not require an interpreter to stare recursively into itself. It requires a trustworthy succession of attributable machine states.

---

## 3. Runtime state

A Dogram Ω machine cut is modeled conceptually as:

```math
Ω_t = (W_t, P_t, ρ_t, φ_t, F_t)
```

where:

- `W_t` — current bounded working state;
- `P_t` — current executable mathal program;
- `ρ_t` — accumulated attributable receipts available to this run;
- `φ_t` — current runtime phase;
- `F_t` — remaining explicit fuel / resource budget.

Required primary phases:

```text
EXEC
META
```

The implementation may include internal adapter states, but no external behavior may collapse the distinction between executing a program and inspecting a representation of execution.

---

## 4. EXEC phase

The EXEC phase performs a deterministic bounded interpretation of one mathal program against one explicit working state.

Conceptually:

```math
E(W, P, F) → (W', r, F')
```

where `r` is an execution receipt.

EXEC may:

- resolve typed addresses;
- load typed values;
- apply admitted bootstrap intrinsics;
- compose mathal steps in explicit order;
- emit deterministic intermediate step receipts when required;
- terminate successfully;
- return `REFUSE`;
- return `INSUFFICIENT_TO_TEST`;
- return `FUEL_EXHAUSTED`.

EXEC may not:

- dynamically import code;
- use `eval`/`exec` or equivalent dynamic code execution;
- mutate its active program definition in place;
- inspect hidden Python interpreter state;
- access the network;
- expand capability or authority;
- silently carry non-receipted state into the next cycle.

At the end of EXEC, the active execution is over before META begins.

---

## 5. Reification membrane

The central safety boundary is **reify before reflect**.

Execution is converted into inert typed data before any meta-level operation can inspect it.

Required first-class data families:

```text
Value
Graph
Program
Receipt
Proposal
Patch
```

A running `Program` and a serialized/reified `Program` are not the same runtime kind.

Hard non-collapse:

```text
PROGRAM != PROGRAM-AS-DATA
PROGRAM-AS-DATA != EXECUTABLE CAPABILITY
RECEIPT != AUTHORITY
REFLECTION != MUTATION
```

The reified form must be canonicalizable and digestible.

At minimum, reification preserves:

- program digest;
- program version/schema;
- operator/mathal identities traversed;
- input digest;
- consumed inputs;
- ordered step results or a deterministic digest chain sufficient for replay verification;
- final result/status;
- refusals/residuals;
- remaining fuel;
- branch identity when applicable.

Reification must not expose implementation-private Python objects, closures, callables, file handles, module references, memory addresses, or ambient capabilities.

---

## 6. META phase

META consumes reified artifacts and may perform bounded mathal computation over them.

Conceptually:

```math
M(P_data, W_data, r, F) → (q, F')
```

where `q` is a typed proposal.

Initial proposal family:

```text
NextProgram
ProgramPatch
AblationProposal
CompositionProposal
BranchProposal
NoChange
Stop
Refuse
```

META may:

- compare receipts;
- calculate deltas between program outputs;
- inspect declared consumed-input sets;
- compare program graphs;
- ablate a reified step or relation in a candidate program;
- compose existing admitted mathal fragments into a candidate program;
- propose replacement of a host intrinsic by a mathal implementation;
- propose multiple explicit candidate next programs;
- decide that no further computation is earned.

META may not:

- directly mutate the active EXEC program;
- manufacture new host capabilities;
- convert arbitrary data into executable code;
- add Python functions or imports;
- bypass fuel accounting;
- admit its own proposal into execution;
- grant evidence, support, truth, historical identity, world authority, or external side effects.

---

## 7. Phase gate

A META result is only a **proposal**.

```text
META OUTPUT != NEXT EXECUTION
```

The phase gate validates whether a proposal may become the next executable program.

Conceptually:

```math
G(q, P_current, F) → P_next | REFUSE
```

The v0 phase gate is deterministic and structural, not semantic authority.

It checks at least:

- proposal schema/version;
- base program digest when patching;
- all referenced mathals exist in the admitted local registry;
- all referenced intrinsics are already admitted host-floor operations;
- no dynamic code payload is present;
- bounded program size;
- bounded branch width;
- bounded step count;
- declared type compatibility where statically checkable;
- canonical ordering for otherwise unordered program structures.

The gate does **not** decide whether a result is true, evidentiary, authoritative, morally correct, or admitted into an external world.

Hard boundary:

```text
PHASE GATE != WORLD CONSTITUTION
PROGRAM ADMISSION != EXTERNAL AUTHORITY
```

Dogram's phase gate only decides whether a candidate is a valid next Dogram computation under the local runtime contract.

---

## 8. Bootstrap floor

The first executable runtime keeps a small, explicit, boring host floor.

Candidate initial intrinsic families:

```text
ADDRESS / LOAD
TYPE
SAME
ADD / SUB
SEQUENCE / SELECT
GRAPH ADD / REMOVE
REACH
TRACE
REFUSE
```

This list is deliberately provisional at the implementation boundary.

The implementation plan must pressure whether some of these can be expressed from a smaller primitive set without obscuring behavior or increasing the trusted computing base.

Every bootstrap intrinsic must have:

- a stable identifier;
- a version;
- declared input/output kinds;
- deterministic behavior;
- explicit refusal conditions;
- direct tests;
- a reference/oracle surface when a mathal replacement is attempted.

No bootstrap intrinsic receives blanket exemption from later peeling.

---

## 9. Mathal program representation

Dogram Ω requires a portable, inert program representation.

Conceptual shape:

```json
{
  "schema": "dogram.program/v0",
  "program_id": "stdlib/delta",
  "program_version": 1,
  "entry": "step-001",
  "steps": [
    {
      "id": "step-001",
      "op": "intrinsic:type",
      "inputs": ["$input.left"],
      "next": "step-002"
    }
  ]
}
```

The exact schema may change during implementation, but the following laws are fixed:

- program order/reachability is explicit;
- step identity is stable within a program version;
- arguments are data, never source code;
- operations resolve only to admitted intrinsics or admitted mathal programs;
- recursion is forbidden in the first implementation unless a later amendment defines bounded recursion semantics;
- cyclic program graphs are rejected initially;
- a program may call another mathal program only through explicit static identity/version;
- all program structures canonicalize deterministically.

The first implementation should prefer a DAG or linear step graph over a general graph-rewrite language.

---

## 10. Dogram standard library

The public Dogram operators should become mathal-defined programs over the bootstrap floor.

Target standard library:

```text
stdlib/delta.mathal.json
stdlib/rectangle.mathal.json
stdlib/ablate.mathal.json
stdlib/reach.mathal.json
```

The existing direct Python implementations from the original v0 plan should be retained during transition as **reference oracles**.

Therefore, each public operator has two paths during bootstrap:

```text
SPECIMEN
  ├── Python oracle ── result A
  └── Mathal VM ───── result B

              A ↔ B
                ↓
          hostile DELTA
```

An operator graduates to mathal-defined runtime status only after oracle and VM behavior agree across its required corpus under the declared equivalence lens.

The oracle is then non-authoritative reference/test material and may later be removed or retained as a conformance witness.

---

## 11. First standard-library lowering: DELTA

`delta` is the first operator to lower into the Mathal VM because it exercises the essential runtime floor without requiring broad graph semantics.

Conceptual lowering:

```text
DISTINGUISH boundary order
    ↓
RELATE left/right values
    ↓
SAME / DIFFERENT under declared value kind
    ↓
SUB compatible numeric values where lawful
    ↓
SELECT first difference
    ↓
TRACE consumed inputs + result
```

The first strong self-reference is intentional but bounded:

> **DELTA helps prove the mathal implementation of DELTA.**

This is not metacircular interpretation. It is cross-implementation conformance pressure.

Required initial proof:

```text
oracle delta(specimen) == vm delta(specimen)
```

under an explicitly named receipt/result equivalence lens that ignores only fields whose difference is intentionally non-operative.

---

## 12. Metaoscillation cycle

A complete Dogram Ω cycle is:

```text
1. EXEC(P_t, W_t)
2. emit receipt r_t
3. REIFY(P_t, W_t', r_t)
4. META(reified artifacts)
5. emit proposal q_t
6. PHASE-GATE(q_t)
7. if admitted, obtain P_(t+1)
8. EXEC again
```

No step is optional when its corresponding state transition occurs.

A runtime that modifies the next program without producing an attributable proposal and gate disposition is non-conformant.

---

## 13. Fuel and termination

Reflection must be bounded explicitly.

The public runtime configuration therefore includes finite budgets such as:

```text
max_exec_steps
max_meta_cycles
max_branch_width
max_program_steps
max_call_depth
```

The exact default numbers belong to the implementation plan and hostile tests, not this architecture document.

Required laws:

```text
NO HIDDEN UNBOUNDED LOOP
NO UNBOUNDED REFLECTIVE TOWER
NO UNBOUNDED BRANCH EXPLOSION
```

Fuel exhaustion is a normal structured runtime result:

```text
status: REFUSE
reason_code: FUEL_EXHAUSTED
```

or a more specific typed refusal where appropriate.

Identical program + state + configuration must exhaust at the same deterministic point.

---

## 14. Explicit branching / bounded multiway evolution

META may eventually emit more than one candidate next program.

Conceptually:

```text
        P_t
      /  |  \
    P_a P_b P_c
     ↓   ↓   ↓
    r_a r_b r_c
      \  |  /
       compare
```

Branching is not hidden nondeterminism.

Every branch has:

- deterministic branch identity;
- explicit parent program/receipt digest;
- explicit candidate program digest;
- independent fuel accounting or a declared deterministic split of parent fuel;
- separate receipts.

When multiple rewrite/proposal candidates are possible, the runtime must choose one of exactly three policies declared by the calling program/configuration:

```text
CANONICAL_FIRST
EXPLICIT_PRIORITY
RETURN_ALL_BOUNDED
```

There is no "whichever host iteration order wins" policy.

Full arbitrary multiway graph rewriting is explicitly deferred.

---

## 15. Bootstrap peeling

The major purpose of META is not merely introspection. It enables Dogram to shrink its trusted host floor lawfully.

Suppose `SAME` initially exists as a Python intrinsic.

A mathal implementation is introduced as a candidate:

```text
host:SAME
mathal:stdlib/same
```

Dogram then performs a peel trial:

```text
HOST SAME
   ↓
receipts / outputs

MATHAL SAME
   ↓
receipts / outputs

META
   ↓
DELTA + hostile corpus + ablation
   ↓
PeelProposal
```

A bootstrap intrinsic may be peeled only when all required conformance tests pass.

Conceptual progression:

```text
K0
 ↓ peel intrinsic
K1
 ↓ peel intrinsic
K2
 ↓
...
```

Each kernel version is attributable and replayable.

Hard law:

```text
BOOTSTRAP SHRINKAGE MUST BE PROVEN, NOT ASSUMED
```

A replacement may be more elegant and still fail to earn removal of the host intrinsic.

---

## 16. Required peel proof

A `PeelProposal` must include:

```text
intrinsic_id
intrinsic_version
candidate_program_id
candidate_program_version
candidate_program_digest
conformance_corpus_digest
required_equivalence_lens
oracle_receipt_digests
candidate_receipt_digests
ablation_result
residual_failures
```

Peeling is admitted only if:

1. all declared positive specimens agree under the required equivalence lens;
2. all declared refusal/negative specimens agree on status and reason family unless the design explicitly permits a narrower distinction;
3. deterministic replay agrees;
4. candidate mathal does not invoke the intrinsic being peeled, directly or transitively;
5. candidate does not smuggle equivalent host behavior through an undeclared replacement intrinsic;
6. ablation of the intrinsic from the candidate runtime leaves the corpus executable;
7. no new external dependency or capability is introduced.

If any condition fails, the intrinsic remains.

---

## 17. Equivalence lenses

Dogram must not introduce universal naked equality for complex runtime artifacts.

Named equivalence lenses are required.

Initial candidate lenses:

```text
VALUE_EQUIVALENT
RESULT_EQUIVALENT
RECEIPT_EQUIVALENT
PROGRAM_BEHAVIOR_EQUIVALENT
PATH_IDENTICAL
TRACE_IDENTICAL
BYTE_IDENTICAL
```

Examples:

```text
same result != same path
same result != same trace
same endpoint != same program
same behavior under corpus != proof of universal equivalence
```

The lens used by every conformance or peel decision must be named in the receipt.

---

## 18. Relationship to original v0 operators

The original Dogram v0 architecture remains valid as the first semantic/operator contract.

This amendment changes **where operator behavior should ultimately live**.

Original design:

```text
JSON specimen
  ↓
Python operator
  ↓
calculation receipt
```

Ω target:

```text
JSON specimen
  ↓
Mathal program
  ↓
small host VM
  ↓
calculation receipt
```

During bootstrap both paths coexist.

No original v0 semantic boundary is relaxed:

```text
DOGRAM OUTPUT != SUPPORT
DOGRAM OUTPUT != EVIDENCE BY ITSELF
DOGRAM OUTPUT != AUTHORITY
GRAPH PATH != CAUSAL PATH
REACHABLE != TRUE
EQUIVALENT != IDENTICAL
```

---

## 19. Relationship to ALEX

ALEX may inspect, cite, compare, or pressure Dogram receipts.

ALEX does not become a Dogram runtime dependency.

Dogram does not import ALEX semantic predicates into operator semantics.

Metaoscillation must preserve:

```text
CALCULATION RECEIPT != EVIDENCE PROMOTION
META AGREEMENT != SUPPORT
PEEL SUCCESS != TRUTH
```

ALEX remains the owner of provenance-first research semantics, formation/evidence distinctions, derivation pressure, and its own refusal rules.

---

## 20. Relationship to 3rdi

3rdi may project Dogram program/receipt state under observer-local cuts.

Dogram may use 3rdi-produced artifacts as explicit inputs only when supplied through the ordinary specimen boundary.

Hard non-collapse:

```text
3RDI PROJECTION != DOGRAM SOURCE STATE
DOGRAM REIFICATION != OBSERVER OMNISCIENCE
PROJECTION != EXECUTION AUTHORITY
```

3rdi remains the projection organ; Dogram remains the calculation/runtime organ.

---

## 21. Relationship to LOADOUT

LOADOUT may bind Dogram as a bounded capability.

The presence of META does not grant Dogram new external effects.

LOADOUT's existing law remains controlling at the boundary:

```text
Knowledge may load.
Capability may bind.
Authority does not silently expand.
```

A Dogram `ProgramPatch` is internal data until the Dogram phase gate admits it as a next local computation.

A Dogram result or patch that would mutate an external repository, filesystem target, network service, or world must cross the external owner's separate effect/admission boundary.

---

## 22. Relationship to μ0 / constitutive mathematics

Dogram Ω borrows a useful execution ordering from the incubating μ0 coordinate without claiming μ0 as a universal mathematical foundation.

Useful correspondence:

```text
DISTINGUISH
RELATE
VARY
COMPOSE
TRACE
```

Dogram deliberately does **not** absorb external constitution/authority into its internal mathal algebra.

In particular, an external constitutional `H` remains outside Dogram's claim.

Dogram's local phase gate is structurally analogous only in the narrow sense that a proposal does not become active execution automatically.

Hard boundary:

```text
DOGRAM PHASE GATE != UNIVERSAL H
LOCAL PROGRAM ACTIVATION != WORLD CONSTITUTION
```

---

## 23. Runtime layering

The development ladder is now:

```text
LEVEL 0 — Python operator lab

LEVEL 1 — Tiny Mathal VM
          mathal-defined public operators

LEVEL 2 — DOGRAM Ω
          EXEC ↔ META
          reified execution
          bounded program-as-data
          phase-gated program proposals
          bootstrap peeling

LEVEL 3 — bounded graph rewrite / multiway experiments
          only after Ω hostile evidence

LEVEL 4 — substantially metacircular runtime
          research frontier, not roadmap commitment
```

**Target architecture: Level 2.**

Level 3 and Level 4 are explicitly not required for Dogram Ω success.

---

## 24. Implementation sequence

The implementation plan should preserve this order unless TDD exposes a smaller dependency graph.

### Phase A — original deterministic floor

Build and prove:

- canonicalization;
- typed values;
- structured receipts/refusals;
- direct Python oracle implementations for `delta`, `rectangle`, `ablate`, `reach`;
- existing hostile fixtures.

This remains useful independent evidence and prevents the VM from becoming its own only oracle.

### Phase B — inert program representation

Add:

- `dogram.program/v0` parser/validator;
- deterministic program canonicalization/digest;
- acyclic step graph;
- static operation registry;
- explicit fuel accounting.

No META yet.

### Phase C — Mathal VM

Add:

- bounded interpreter;
- intrinsic dispatch;
- nested admitted mathal calls if needed;
- step receipts;
- structured refusal on invalid program behavior.

Lower `delta` first.

### Phase D — standard-library migration

Lower and conformance-test:

```text
delta
rectangle
ablate
reach
```

Only then may the public CLI default to mathal implementations.

### Phase E — reification membrane

Add canonical first-class:

```text
ProgramData
ReceiptData
ExecutionData
```

Prove that no live host capability crosses reification.

### Phase F — META read-only

Allow meta-mathals to:

- inspect receipts/program graphs;
- compute deltas;
- emit `NoChange`, `Stop`, and analytical proposals.

No program patch admission yet.

### Phase G — phase-gated ProgramPatch

Add:

- patch schema;
- base digest check;
- structural validation;
- local registry resolution;
- bounded size/depth checks;
- admitted next-program activation.

### Phase H — explicit branching

Add bounded candidate branching only after single-successor META is proven deterministic.

### Phase I — first bootstrap peel

Attempt one deliberately simple intrinsic replacement.

Preferred first candidates:

```text
SAME
or
SELECT-FIRST
```

Do not begin with graph reachability.

The first peel success is Dogram Ω's strongest graduation witness.

---

## 25. Hostile test corpus

Ω must add hostile tests beyond the original v0 operator corpus.

### `META-LIVE-MUTATION-001`

A meta-mathal attempts to alter the currently executing program.

Expected:

```text
REFUSE
```

No active program mutation occurs.

### `DATA-CAPABILITY-COLLAPSE-001`

A reified program contains a string/value naming a host operation that is not admitted in the registry.

Expected:

```text
value remains inert
execution refused if activation is attempted
```

### `PATCH-STALE-BASE-001`

A patch targets a program digest other than the active base.

Expected:

```text
REFUSE: STALE_PROGRAM_BASE
```

### `META-FUEL-001`

A legal meta cycle attempts to continue past the declared `max_meta_cycles`.

Expected:

```text
REFUSE: FUEL_EXHAUSTED
```

at a deterministic cycle.

### `BRANCH-BOUND-001`

META emits more candidates than `max_branch_width`.

Expected:

```text
REFUSE
```

or deterministic truncation only if a future explicit design amendment permits it. v0 should prefer refusal.

### `PEEL-SELF-SMUGGLE-001`

Candidate replacement for intrinsic `X` calls `X` indirectly through another mathal.

Expected:

```text
REFUSE PEEL
```

### `PEEL-BEHAVIOR-DRIFT-001`

Candidate matches happy-path outputs but changes refusal behavior.

Expected:

```text
PEEL NOT EARNED
```

### `SAME-RESULT-DIFFERENT-TRACE-001`

Oracle and candidate return the same final result but traverse different paths.

Expected:

```text
RESULT_EQUIVALENT = true
TRACE_IDENTICAL = false
```

No naked `equal` conclusion.

### `REPLAY-META-001`

Replay the same EXEC→META cycle from identical canonical input/program/configuration.

Expected:

```text
byte-stable deterministic receipt/proposal payloads
```

excluding only fields explicitly outside deterministic payloads; v0 should avoid such fields.

---

## 26. Observability and receipts

Every oscillation must produce enough information to reconstruct the transition without private reasoning.

Conceptual cycle receipt:

```json
{
  "schema": "dogram.oscillation-receipt/v0",
  "cycle": 3,
  "exec": {
    "program_digest": "sha256:...",
    "receipt_digest": "sha256:..."
  },
  "meta": {
    "program_digest": "sha256:...",
    "proposal_digest": "sha256:..."
  },
  "gate": {
    "status": "ADMIT_LOCAL_PROGRAM",
    "next_program_digest": "sha256:..."
  },
  "fuel": {
    "before": {},
    "after": {}
  }
}
```

The exact schema is implementation-plan material, but the receipt must distinguish:

```text
what executed
what was observed
what was proposed
what was admitted locally
what changed
what did not change
```

---

## 27. Security / containment consequences

The architecture intentionally reduces reflective risk through representation boundaries.

Required containment properties:

- no arbitrary code evaluation;
- static local operation registry;
- canonical program schemas;
- bounded program/call/meta depth;
- no implicit filesystem/network access;
- patches apply only to reified Dogram programs;
- external effects require an external owner/gate;
- all activation happens between phases;
- reified host details contain no callable capabilities.

This does not make arbitrary future mathals safe automatically. Every new intrinsic expands the trusted host floor and therefore requires explicit review.

---

## 28. Non-goals

Dogram Ω does not initially provide:

- a universal programming language;
- arbitrary source-code evaluation;
- general recursion;
- unbounded loops;
- unrestricted graph rewriting;
- unbounded multiway computation;
- distributed execution;
- concurrent mutation;
- JIT/native compilation;
- a theorem prover;
- a CAS replacement;
- evidence/support/truth promotion;
- external world authority;
- a universal ontology;
- proof that μ0 is minimal or universal;
- proof that Dogram is fully self-hosting.

---

## 29. Graduation criteria

Dogram Ω earns its first runtime claim only when all of the following are executable and tested:

1. original v0 direct oracle operators pass their hostile corpus;
2. a deterministic Mathal VM executes an inert versioned program representation;
3. `delta`, `rectangle`, `ablate`, and `reach` execute through mathal standard-library programs and conform to the reference oracles;
4. EXEC output is canonically reified without leaking host capability;
5. at least one read-only META mathal consumes reified execution and emits a deterministic proposal;
6. at least one `ProgramPatch` crosses the local phase gate and becomes the next executable program without live mutation;
7. replay of an EXEC→META→GATE→EXEC sequence is deterministic;
8. all fuel and branch limits refuse deterministically;
9. at least one bootstrap intrinsic passes the full peel proof and is removed from a candidate kernel;
10. the same hostile corpus still passes after that intrinsic is absent.

Only then may the repository claim:

> **DOGRAM Ω METAOSCILLATORY RUNTIME — FIRST PROOF OF LIFE**

A stronger claim such as fully self-hosted, graph-rewrite-native, or metacircular requires a later design and independent evidence.

---

## 30. Architectural seal

```text
PROGRAM
  ↓
DO
  ↓
RECEIPT
  ↓
WITNESS
  ↓
REIFY
  ↓
PEEL / PRESS / VARY
  ↓
PROPOSE
  ↓
GATE
  ↓
DO AGAIN
```

And the non-collapse beneath the entire runtime:

```text
DESCRIPTION != CAPABILITY
REFLECTION != MUTATION
PROPOSAL != EXECUTION
EXECUTION != AUTHORITY
RESULT != HISTORY
EQUIVALENCE != IDENTITY
RECEIPT != CONSTITUTION
```

The roof target is therefore not infinite self-reference.

It is a machine that can lawfully encounter what it just did, pressure that history using its own mathals, propose a bounded next form, and keep shrinking the amount of machinery that must remain outside itself.

> **Dogram does not have to swallow itself whole. It can digest its bootstrap one attributable bite at a time.**
