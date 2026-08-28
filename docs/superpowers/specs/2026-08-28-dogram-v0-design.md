# Dogram v0 — Deterministic Operations for Graph / Relation / Mathal Pressure

**Date:** 2026-08-28  
**Status:** ARCHITECTURAL SPEC · IMPLEMENTATION NOT YET ADMITTED  
**Repository:** `the-static-collective/Dogram`

## 0. Purpose

Dogram is a small deterministic calculation lab for pressure-testing mathals, provenance pipelines, and graph/relation hypotheses.

Its job is deliberately narrow:

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

Dogram is not:

- an evidence authority;
- a semantic relation kernel;
- a truth engine;
- a symbolic-physics oracle;
- a replacement for Wolfram or another CAS;
- an ALEX runtime dependency;
- a master ontology for Static Collective projects.

Dogram consumes explicit small specimens, performs deterministic typed operations, and emits calculation receipts that another system — including ALEX — may inspect, cite, compare, or pressure.

The first implementation target is a pure offline Python 3.12 tool with a JSON input/output boundary and no network dependency.

---

## 1. Architectural ancestry

Dogram grows from a recent ALEX / MutatedMathalModel research run that converged on several non-collapses:

```text
PRESENT != AVAILABLE != LOADED != CONSUMED
FORMATION BASIS != SUPPORT BASIS
TRUST != EVIDENCE
TRUST != SUPPORT
TRUST != AUTHORITY
SAME SURFACE != SAME CAUSAL STATE
RECURRENCE != SHARED MECHANISM
```

The practical research problem is not merely to describe those distinctions but to pressure them experimentally:

> **If one declared relation or coordinate changes, what changes — and where does the first lawful difference appear?**

Dogram supplies deterministic operators for that question without claiming semantic interpretation of the result.

### 1.1 Trust as traversal

Wild associations may legitimately motivate bounded investigation.

Working distinction:

```text
WILD ASSOCIATION
      ↓
TRUSTED TRAVERSAL
      ↓
PRESSURE
      ↓
SHARED PRIMITIVE CANDIDATE OR DEAD EDGE
```

Trust may keep an unresolved edge traversable long enough to test it. Trust does not certify the edge.

A useful hostile test is therefore **trust withdrawal**: remove the motivating association/trust edge and ask whether the candidate primitive can still be independently reconstructed from domain receipts.

Dogram may calculate that reachability change. It does not decide whether the surviving structure counts as evidence or support.

---

## 2. Boundary with ALEX

ALEX owns provenance-first research semantics, evidence-path pressure, refusal, and attributable derivation.

Dogram owns only deterministic calculation over explicitly typed specimens.

```text
SPECIMEN
   ↓
DOGRAM OPERATOR
   ↓
CALCULATION RECEIPT
   ↓
ALEX / HUMAN / OTHER OWNER MAY INTERPRET
```

Hard boundary:

```text
DOGRAM OUTPUT != SUPPORT
DOGRAM OUTPUT != EVIDENCE BY ITSELF
DOGRAM OUTPUT != AUTHORITY
DOGRAM ACCEPT != ALEX ACCEPT
DOGRAM REACHABLE != TRUE
DOGRAM EQUIVALENT != IDENTICAL
```

Dogram must not import ALEX semantic predicates such as `SUPPORTS` into its own operation semantics.

ALEX must not be required for Dogram to execute a valid v0 specimen.

---

## 3. Design principles

### 3.1 Pure first

Each v0 operator is a pure function over decoded specimen data.

No:

- network access;
- filesystem mutation inside operator logic;
- hidden time dependence;
- random behavior;
- model calls;
- environmental discovery;
- dynamic code execution.

The CLI may read one JSON document from a file or stdin and write one JSON receipt to stdout.

### 3.2 Typed difference

Dogram must not pretend every state lives in a numeric vector space.

For numeric values, a finite difference may be meaningful:

```text
Δ = right - left
```

For opaque strings, digests, labels, graph identities, and categorical values, v0 supports equality/equivalence comparison only:

```text
SAME | DIFFERENT
```

No subtraction, distance, ordering, or interpolation of opaque digests is permitted.

### 3.3 Exact arithmetic before floating point

Where specimens use bounded integers or rational values, v0 should preserve exact arithmetic.

Implementation target:

```text
int
fractions.Fraction
```

Floating point is permitted only when the specimen explicitly declares a floating numeric value.

The receipt must preserve numeric kind so exact and approximate outputs cannot silently collapse.

### 3.4 Operation as receipt

Every result must preserve:

- operator identity and version;
- exact input digest;
- declared coordinate/value types;
- operation performed;
- output;
- first relevant delta when applicable;
- residual or unresolved conditions;
- warnings/refusals.

A result without enough information to reconstruct what operation ran is invalid.

### 3.5 Refusal is a valid result

Malformed, under-typed, or mathematically invalid specimens should return a structured refusal rather than guess.

Examples:

```text
TYPE_MISMATCH
UNSUPPORTED_VALUE_KIND
MISSING_COORDINATE
NON_NUMERIC_FINITE_DIFFERENCE
INVALID_GRAPH_REFERENCE
AMBIGUOUS_BOUNDARY_ORDER
MALFORMED_SPECIMEN
```

---

## 4. Public v0 specimen envelope

The public JSON boundary should be versioned from the first implementation.

Conceptual shape:

```json
{
  "schema": "dogram.specimen/v0",
  "specimen_id": "example-001",
  "operator": "delta",
  "operator_version": 1,
  "inputs": {},
  "assumptions": [],
  "metadata": {}
}
```

`metadata` is non-operative in v0. Operator logic must not change because arbitrary metadata is present.

This protects:

```text
RECEIPT PRESENT != RECEIPT CONSUMED
```

If an operator uses an input to calculate its result, that input must appear in the operator-specific consumed-input receipt.

---

## 5. Public v0 calculation receipt

Conceptual output:

```json
{
  "schema": "dogram.receipt/v0",
  "specimen_id": "example-001",
  "operator": "delta",
  "operator_version": 1,
  "input_digest": "sha256:...",
  "status": "OK",
  "consumed_inputs": [],
  "result": {},
  "residuals": [],
  "warnings": []
}
```

Required status family:

```text
OK
REFUSE
INSUFFICIENT_TO_TEST
```

`OK` means only that Dogram lawfully executed the declared operator over the supplied specimen.

It conveys no evidentiary or semantic promotion.

---

# 6. Operator 1 — `delta`

## 6.1 Purpose

Compare two ordered boundary traces and identify the first boundary at which they differ.

This is the executable nucleus of `DELTA-PEEL-001`.

Input concept:

```json
{
  "boundary_order": ["LOADOUT", "PROJECTION", "DERIVATION"],
  "left": {
    "LOADOUT": {"kind": "opaque", "value": "ctx-a"},
    "PROJECTION": {"kind": "opaque", "value": "proj-a"},
    "DERIVATION": {"kind": "number", "value": 4}
  },
  "right": {
    "LOADOUT": {"kind": "opaque", "value": "ctx-a"},
    "PROJECTION": {"kind": "opaque", "value": "proj-b"},
    "DERIVATION": {"kind": "number", "value": 7}
  }
}
```

Output concept:

```json
{
  "first_difference": "PROJECTION",
  "comparisons": [
    {"boundary": "LOADOUT", "relation": "SAME"},
    {"boundary": "PROJECTION", "relation": "DIFFERENT"},
    {"boundary": "DERIVATION", "relation": "DIFFERENT", "delta": 3}
  ]
}
```

### 6.2 Laws

- boundary order must be explicit;
- both sides must define the same ordered boundary set;
- opaque values receive only `SAME` / `DIFFERENT`;
- numeric values of compatible kinds may additionally emit finite difference;
- `first_difference = null` is valid when the traces are equivalent under the declared comparison rules;
- Dogram does not label a difference lawful or forbidden unless that classification is explicitly supplied as non-operative annotation for downstream interpretation.

Dogram reports where the difference occurred. Another owner decides what the difference means.

---

# 7. Operator 2 — `rectangle`

## 7.1 Purpose

Pressure interaction between two binary coordinates using four declared outcomes.

Conceptual arrangement:

```text
             i=0       i=1

world=0      F00       F01
world=1      F10       F11
```

### 7.2 Numeric mode

For compatible numeric values:

```text
mixed_delta = F11 - F10 - F01 + F00
```

Dogram must preserve exact arithmetic when all four values are exact.

### 7.3 Equivalence mode

For opaque/categorical values, Dogram does not calculate a fake numeric interaction.

Instead report whether the equivalence pattern changes across the second coordinate.

Example:

```text
F00 == F10 : true
F01 == F11 : false
```

Result:

```text
interaction_detected: true
```

Interpretation such as "interest activates hidden state" belongs downstream.

### 7.4 Laws

- all four cells must share a compatible declared value kind;
- numeric and opaque modes must not silently mix;
- output must name the tested axes and cell identities;
- `interaction_detected` does not establish causality outside the constructed specimen.

---

# 8. Operator 3 — `ablate`

## 8.1 Purpose

Remove exactly one declared component from a small graph/specimen and report what declared outputs or reachability relations change.

This supports:

```text
NO DELTA -> NO EARNED STATE DIMENSION
```

as a research pressure operation without making that principle a Dogram truth claim.

### 8.2 Graph model

v0 graph representation is deliberately small and explicit:

```json
{
  "nodes": ["A", "B", "P"],
  "edges": [
    ["A", "P"],
    ["B", "P"]
  ]
}
```

Edges are directed in v0.

No weights, labels, hyperedges, probabilities, capacities, or semantic predicates in the first implementation.

### 8.3 Ablation targets

v0 supports exactly:

```text
node
edge
```

For an ablation, Dogram emits:

- removed component;
- graph before/after digests;
- reachability pairs lost;
- reachability pairs gained, normally none for deletion-only ablation;
- requested target reachability before/after when supplied.

### 8.4 Laws

- a missing target returns `INSUFFICIENT_TO_TEST` rather than pretending removal occurred;
- deleting a node removes its incident edges;
- original graph is not mutated in-place;
- graph identity and graph reachability remain separate concepts.

---

# 9. Operator 4 — `reach`

## 9.1 Purpose

Compare directed reachability before and after an explicit graph mutation.

Primary specimens:

- trust withdrawal;
- formation-history reachability;
- graph mutation after receipt consumption;
- adaptive state/topology toy models.

### 9.2 v0 mutation vocabulary

Keep the first version narrow:

```text
ADD_NODE
REMOVE_NODE
ADD_EDGE
REMOVE_EDGE
```

No arbitrary callback, dynamic rule, or executable mutation language.

### 9.3 Output

For declared source/target pairs, emit:

```text
reachable_before
reachable_after
changed
```

Optionally emit shortest unweighted path before/after when one exists.

The path is a graph-theoretic witness only. It is not historical ancestry, evidence, or mechanism.

Hard non-collapse:

```text
GRAPH PATH != CAUSAL PATH
GRAPH REACHABILITY != HISTORICAL OCCURRENCE
```

---

# 10. First hostile specimens

The initial test corpus should be synthetic and domain-neutral.

## 10.1 `interest-mediated-support`

Two variants:

### A. lawful mediation surface

```text
interest changes
→ selected evidence changes
→ downstream score changes
```

Dogram only calculates the differences.

### B. frozen evidence control

```text
interest changes
same evidence
same declared scoring function
→ score must remain the same
```

This is the calculational control for `MEDIATED-SUPPORT-001`; ALEX supplies the semantic refusal if interest is later promoted as support.

## 10.2 `hidden-world-policy-rectangle`

World difference is inert under policy 0 and produces a declared output difference under policy 1.

`rectangle` should detect the interaction pattern without explaining it.

## 10.3 `trust-withdrawal`

Graph contains an association/trust edge that makes a candidate primitive reachable.

Remove that edge.

Question:

> Can the primitive still be reached through independently declared domain paths?

The result is a reachability receipt, not a promotion decision.

## 10.4 `same-surface-different-history`

Two states expose the same surface label but have different hidden graph structure. Apply the same mutation and compare reachability.

This is a synthetic control for `STATE-SUFFICIENCY-001`.

---

# 11. Suggested implementation shape

The design intentionally does not require a framework.

Proposed initial tree:

```text
Dogram/
  docs/
    superpowers/
      specs/
      plans/
  dogram/
    __init__.py
    digest.py
    types.py
    delta.py
    rectangle.py
    graph.py
    ablate.py
    reach.py
    receipt.py
    cli.py
  tests/
    fixtures/
      delta/
      rectangle/
      ablate/
      reach/
    test_delta.py
    test_rectangle.py
    test_ablate.py
    test_reach.py
    test_receipt.py
    test_cli.py
  pyproject.toml
  README.md
```

Responsibility boundaries:

- `types.py` — decode/validate typed scalar values used by multiple operators;
- `digest.py` — canonical JSON serialization and SHA-256 input/graph digests;
- `delta.py` — ordered trace comparison only;
- `rectangle.py` — four-cell interaction calculations only;
- `graph.py` — immutable normalized directed graph and traversal helpers;
- `ablate.py` — deletion pressure over `graph.py`;
- `reach.py` — explicit graph mutation + reachability comparison;
- `receipt.py` — common receipt envelope construction;
- `cli.py` — JSON adapter only; no domain semantics.

The implementation plan may split or combine files if TDD proves a smaller structure sufficient, but public operator boundaries and semantic refusals in this spec remain authoritative unless the design is amended first.

---

# 12. Dependency policy

v0 target:

```text
Python >= 3.12
standard library only
```

Preferred standard-library components:

```text
json
hashlib
fractions.Fraction
collections.deque
argparse
```

A third-party dependency requires an explicit design amendment demonstrating why the standard library cannot satisfy the first four operators cleanly.

---

# 13. Determinism and canonicalization

Dogram receipts should be reproducible for identical specimens under the same operator version.

Therefore:

- canonical JSON serialization sorts object keys;
- graph nodes and edges normalize to deterministic order in receipts/digests;
- sets never leak nondeterministic ordering into output;
- no timestamps belong inside deterministic calculation payloads;
- optional runtime wrapper metadata such as execution time must stay outside the calculation digest.

Required property:

```text
same specimen bytes after canonical decoding
+ same operator version
→ same calculation receipt payload
```

excluding any explicitly non-deterministic outer transport metadata, which v0 should avoid entirely.

---

# 14. Error and refusal model

Operators should return data, not raise uncaught exceptions for ordinary invalid specimens.

Conceptual refusal:

```json
{
  "status": "REFUSE",
  "reason_code": "NON_NUMERIC_FINITE_DIFFERENCE",
  "residuals": [
    "boundary DERIVATION declared opaque; numeric delta unavailable"
  ]
}
```

Programmer errors and impossible internal invariants may still raise exceptions during development, but public CLI behavior must convert specimen errors into structured receipts.

---

# 15. Versioning

Version independently:

```text
specimen schema
receipt schema
operator
```

Example:

```text
dogram.specimen/v0
dogram.receipt/v0
delta@1
rectangle@1
ablate@1
reach@1
```

An operator change that alters mathematical output for an already valid specimen requires a new operator version.

Formatting-only receipt changes may instead require a receipt-schema version change.

---

# 16. Deliberately deferred

The following are not part of v0:

- symbolic algebra;
- calculus / automatic differentiation;
- differential equation solving;
- Hodge decomposition;
- graph spectra / eigenproblems;
- optimization;
- statistics or causal inference estimators;
- probability distributions;
- units library;
- physical constants database;
- Wolfram API integration;
- NumPy / SciPy;
- visualization;
- graph database;
- hypergraphs;
- persistent storage;
- web service;
- plugin system;
- ALEX predicate evaluation;
- LLM interpretation.

Any of these may later be earned by a concrete hostile specimen.

---

# 17. Success criteria for Dogram v0

v0 earns existence when all of the following are demonstrated with executable tests:

1. `delta` identifies the first difference across ordered typed traces and never performs numeric operations on opaque values.
2. `rectangle` performs exact mixed finite differences for rational/integer values and equivalence-pattern interaction tests for opaque values.
3. `ablate` removes one declared node/edge without mutating the input graph and reports lost reachability.
4. `reach` applies one explicit graph mutation and reports before/after reachability deterministically.
5. Every valid execution emits a versioned calculation receipt with canonical input digest and explicit consumed inputs.
6. Malformed or under-typed specimens produce structured refusal/insufficient receipts.
7. All four hostile fixtures are represented in domain-neutral synthetic form.
8. Full test suite passes offline with Python 3.12 and standard library only.
9. Re-running identical fixtures produces byte-stable canonical calculation payloads.
10. Nothing in the implementation can mint evidence, support, truth, authority, or ALEX semantic relations.

---

# 18. Promotion boundary

Dogram v0 is a calculator with receipts.

Its strongest claim after a green implementation should be:

> Given a valid versioned specimen, Dogram deterministically executed one declared v0 operator and emitted the corresponding typed calculation receipt.

It must not claim:

- that the supplied world model is historically true;
- that a graph edge is causal;
- that a recurring structure is universal;
- that a surviving primitive is scientifically established;
- that an ALEX claim is supported;
- that a trusted association was justified.

Those remain separate research and authority questions.

---

# 19. Final seal

Dogram exists to make speculative mathals cheaper to attack.

```text
ASSOCIATION
    ↓
TRUSTED TRAVERSAL
    ↓
DECLARED SPECIMEN
    ↓
DOGRAM
    ↓
DELTA / INTERACTION / ABLATION / REACHABILITY RECEIPT
    ↓
ALEX PRESSURE OR HUMAN INTERPRETATION
```

Its constitutional lines are:

> **TRUST MAY OPEN THE BRIDGE. IT MAY NOT CERTIFY THE BRIDGE.**

> **PRESENCE IS NOT CONSUMPTION.**

> **PERTURB ONE RELATION; RECEIPT THE FIRST DIFFERENCE.**

> **THE OPERATOR MUST DECLARE WHAT KIND OF THING IT OPERATED ON.**

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**
