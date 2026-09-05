# MATHBAND-INCUBATOR-001 — Architectural Design

**Date:** 2026-09-05  
**Status:** EXPERIMENTAL ARCHITECTURAL INCUBATOR · NO PUBLIC OPERATOR ADMITTED  
**Repository:** `the-static-collective/Dogram`

## 0. Purpose

MathBand is an experimental Dogram research subsystem for pressure-testing **declared mathematical bridges** between distinct mathematical formulations, disciplines, or representational systems without flattening their assumptions, silently deleting unmatched structure, or promoting structural resemblance into semantic or evidentiary equivalence.

The design is intentionally narrower than a universal translator, theorem prover, ontology merger, or automatic discovery engine.

Its first job is:

> **Given two intact mathematical voices and an explicitly declared bridge into one common comparison stage, calculate what survives, what changes, what is lost, what remains extra, and where the first decisive mismatch occurs.**

Dogram's constitutional rule remains unchanged:

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

MathBand adds no public Dogram operator in this slice.

---

## 1. Why Dogram owns the incubator

MathBand composes three already-established Dogram research lines rather than inventing a new constitution.

### 1.1 Common carrier

Existing common-carrier work separates shared scale from primitive transition shape and preserves both rather than conflating them.

MathBand generalizes that posture:

```text
shared presentation carrier
!=
shared mathematical object
```

and:

```text
common normalization
!=
proof of equivalence
```

### 1.2 Binocular disparity

Existing binocular work preserves loss, surplus, unresolved material, contradiction, and trajectory delta as distinct residual classes rather than collapsing them into one scalar score.

MathBand adopts the same refusal:

```text
one similarity score
!=
adequate bridge receipt
```

### 1.3 Target-relative quotient/probe

Existing quotient/probe work defines equivalence relative to a declared target family rather than globally.

MathBand therefore treats every bridge claim as scoped:

```text
preserved under declared probes
!=
globally equivalent
```

The subscript is load-bearing.

---

## 2. Constitutional non-collapses

MathBand must preserve these distinctions:

```text
VOICE_A != VOICE_B
BRIDGE != IDENTITY
COMMON STAGE != COMMON WORLD
NORMALIZATION != EQUIVALENCE
UNMAPPED != FALSE
EXTRA != ERROR
APPROXIMATE != EXACT
LOW RESIDUAL != PROOF
KNOWN BRIDGE != HISTORICAL INFLUENCE
STRUCTURAL HOMOLOGY != COMMON ORIGIN
PRESERVED UNDER P != GLOBALLY EQUIVALENT
FAILED BRIDGE != FAILED THEORY
```

A successful MathBand result establishes only that the declared bridge preserved the declared structure under the declared probes.

It does not establish truth, historical priority, explanatory superiority, physical identity, semantic identity, causal influence, or authority.

---

## 3. Core objects

### 3.1 Voice

A `Voice` is one mathematical formulation kept intact enough to preserve the distinctions required by the comparison.

Conceptually:

```text
Voice = (
  id,
  objects,
  relations,
  operations,
  assumptions,
  domain,
  normalization,
  declared_invariants
)
```

The first implementation need not support arbitrary symbolic mathematics. Fixtures may use finite typed structures sufficient to exercise the bridge contract.

A voice may not be rewritten merely to make the bridge succeed.

### 3.2 Declared bridge

A bridge consists of explicitly supplied maps from each voice into a declared common stage:

```math
V_A \xrightarrow{\phi_A} B \xleftarrow{\phi_B} V_B
```

A bridge declaration must state:

```text
source voice
source domain
map definition
common-stage target type
known lossy fields
required assumptions
probe family
```

MathBand does not infer historical intent or conceptual identity from a bridge declaration.

### 3.3 Common stage

The common stage `B` is the smallest comparison surface needed for the declared probes.

It may be, for example:

- a finite relation table;
- an integer/rational tuple space;
- a graph;
- a matrix action on a finite specimen set;
- a partition or quotient witness;
- an exact symbolic record chosen by the fixture.

The common stage is not a master ontology.

### 3.4 Probe family

A probe family `P` is declared before bridge scoring.

For each `p in P`, both sides must produce comparable typed outputs on the common stage or explicitly return `UNMAPPED`/`UNDEFINED`.

The first decisive disagreement is retained rather than hidden by aggregate scoring.

### 3.5 Receipt

The receipt is the primary MathBand product.

Conceptually:

```text
MathBandReceipt = (
  bridge_ref,
  voice_a_ref,
  voice_b_ref,
  common_stage_ref,
  declared_assumptions,
  declared_probe_family,
  preserved,
  changed,
  broken,
  unmapped,
  extra,
  residual,
  first_decisive_probe,
  lossy_steps,
  exactness,
  refusals
)
```

No single `match_score` is admitted in v0.

---

## 4. Comparison semantics

Given two voices `V_A`, `V_B`, declared maps `phi_A`, `phi_B`, common stage `B`, and probe family `P`, MathBand evaluates each probe separately.

For a probe `p`, define:

```math
r_A(p) = p(\phi_A(V_A))
```

```math
r_B(p) = p(\phi_B(V_B))
```

The finite receipt classifies outcomes without semantic promotion.

### 4.1 `PRESERVED`

The two mapped outputs are exactly equal under the fixture's declared equality relation.

### 4.2 `CHANGED`

Both sides map and remain comparable, but a typed delta is present.

### 4.3 `BROKEN`

A probe expected by the declared bridge to commute or preserve structure does not.

### 4.4 `UNMAPPED`

One side contains an object/relation/operation for which no map was declared.

This is not failure unless the bridge claimed coverage of that object.

### 4.5 `EXTRA`

One voice contains a degree of freedom or structure outside the declared image of the other.

Extra structure must survive the receipt. It may not be projected away merely to increase apparent similarity.

### 4.6 `RESIDUAL`

A numeric or typed disagreement remains after all declared common transformations have been applied.

Residuals are retained exactly where fixture arithmetic permits, otherwise with declared tolerance and representation.

### 4.7 `REFUSE`

The bridge is not evaluable because a required assumption, domain restriction, or comparison relation is missing or contradictory.

Refusal is a successful constitutional outcome.

---

## 5. The Five Bats

No unfamiliar or speculative bridge may be treated as a meaningful MathBand result until the bridge contract survives the five hostile classes below on known fixtures.

### BAT-1 — Rename Bat

Change only presentation:

- rename symbols;
- reorder declarations;
- permute labels;
- change harmless notation;
- scramble fixture serialization.

Expected:

```text
true structural receipt invariant
```

Incorrect:

```text
bridge depends on familiar names or ordering
```

### BAT-2 — Gauge Bat

Apply a declared representation-preserving transformation:

- common rescaling;
- coordinate change;
- basis change;
- harmless orientation convention when explicitly accounted for;
- equivalent normalization.

Expected:

```text
invariants preserved
carrier/calibration delta receipted separately
```

Incorrect:

```text
normalization delta silently treated as mathematical disagreement
```

or:

```text
non-invariant structure silently erased
```

### BAT-3 — Domain Bat

Construct a bridge that is valid only on a proper subdomain.

Expected:

```text
bridge valid on declared restricted domain
bridge refused or broken outside it
```

Incorrect:

```text
local identity promoted to global equivalence
```

### BAT-4 — Extra-Voice Bat

Give one voice an additional parameter, operation, dimension, branch, or relation not represented by the other.

Expected:

```text
EXTRA / UNMAPPED survives
```

Incorrect:

```text
extra structure discarded to force bridge success
```

### BAT-5 — False-Friend Bat

Construct two superficially similar formulations with one decisive structural incompatibility.

Expected:

```text
first discriminating probe kills the declared bridge
```

Incorrect:

```text
surface resemblance or low aggregate residue overrides decisive mismatch
```

---

## 6. Calibration specimen: complex rotation vs 2x2 linear algebra

The first frozen bridge must be mathematically known in advance.

### Voice A — complex multiplication

Let:

```math
z = a + bi
```

Multiplication by `i` gives:

```math
i(a+bi) = -b + ai
```

### Voice B — matrix action

Let:

```math
R = \begin{pmatrix}0 & -1\\1 & 0\end{pmatrix}
```

Then:

```math
R\begin{pmatrix}a\\b\end{pmatrix}
=
\begin{pmatrix}-b\\a\end{pmatrix}
```

### Declared bridge

```math
\phi(a+bi) = (a,b)
```

The calibration common stage is a finite integer-pair specimen set under one declared quarter-turn action.

### Initial probes

For frozen integer pairs, compare:

- mapped output pair;
- fourfold return;
- norm preservation `a^2+b^2`;
- composition of two quarter turns;
- identity after four turns.

All arithmetic can remain exact integer arithmetic.

### Hostile siblings

The calibration family must include at least:

1. symbol/coordinate renaming;
2. scrambled fixture order;
3. a declared basis change with corresponding bridge update;
4. complex conjugation/orientation reversal with correctly receipted delta;
5. false friend matrix `[[0,1],[1,0]]` or another reflection-like action that looks similar but fails the quarter-turn probes.

The point is not to rediscover the known isomorphism. The point is to verify that the receipt remains stable under harmless presentation changes and fails under genuine structural change.

---

## 7. Specimen ladder

MathBand must progress through increasing epistemic risk.

### Level 0 — exact known bridge

Known equivalence/isomorphism expressed in distinct surfaces.

Purpose: calibrate the receipt.

### Level 1 — known partial bridge

A declared embedding, correspondence, or approximation valid only on a restricted domain or probe family.

Purpose: verify domain and `UNMAPPED` behavior.

### Level 2 — known non-bridge

A deliberately seductive false friend.

Purpose: verify refusal and decisive-probe behavior.

### Level 3 — unfamiliar but documented bridge

Two established mathematical disciplines with a known literature bridge not encoded into the fixture's expected outputs.

Purpose: test whether the representation can faithfully express a real cross-disciplinary correspondence.

### Level 4 — novel candidate bridge

A user/researcher-proposed bridge whose status is genuinely unknown.

Purpose: pressure-test, not promote.

At Level 4, MathBand may report only the declared calculations and residuals. Any claim of mathematical novelty, significance, or literature priority belongs to downstream scholarly/human review.

---

## 8. Discovery is out of scope for v0

The first incubator does **not** search arbitrary mathematical corpora for bridges.

```text
MATHBAND-V0 = pressure declared bridges
```

not:

```text
MATHBAND-V0 = invent bridge candidates automatically
```

This is deliberate.

A discovery layer can only be considered after the receipt system has demonstrated low false-positive behavior on hostile known fixtures.

Potential future flow:

```text
candidate generator
  -> declared bridge proposal
  -> MathBand pressure
  -> HOLD / SURVIVED DECLARED PROBES
  -> scholarly/human review
```

The candidate generator must never be allowed to grade its own bridge.

---

## 9. Relationship to ALEX, LOADOUT, and 3rdi

This incubator remains Dogram-local in v0, but its future ownership boundaries are explicit.

### ALEX

ALEX owns source provenance, historical formulations, transcription/normalization layers, literature claims, priority, and scholarly evidence.

MathBand may consume already-constituted mathematical fixture material, but:

```text
source provenance != bridge success
bridge success != historical influence
```

### LOADOUT

LOADOUT may later own which mathematical adapters/capabilities are admitted into a bounded comparison run.

```text
available adapter != relevant adapter
bound adapter != mathematical authority
```

### 3rdi

3rdi may later own observer-local presentation and decoder constitution when the same bridge appears differently under different representations.

MathBand itself owns only the deterministic comparison receipt.

---

## 10. Proposed implementation boundary after design approval

This section is a design target only. No implementation is authorized by this document alone.

The smallest durable runtime should remain internal research code, standard-library only, and outside the public operator registry.

Candidate files:

```text
dogram/mathband.py
tests/test_mathband.py
tests/fixtures/mathband_incubator_001.json
research/MATHBAND-INCUBATOR-001.md
```

No CLI route, schema promotion, generic symbolic parser, theorem prover, CAS dependency, external network dependency, or public `mathband@1` operator is included in the first implementation.

The fixture should encode finite exact data rather than arbitrary prose mathematics.

---

## 11. Testing strategy

Implementation must be test-driven.

The first red tests should establish:

1. exact complex/matrix calibration passes all declared probes;
2. Rename Bat leaves receipt semantics unchanged;
3. Gauge Bat preserves declared invariants while retaining the gauge delta;
4. Domain Bat reports restricted validity rather than global equivalence;
5. Extra-Voice Bat preserves unmatched structure;
6. False-Friend Bat records a decisive failure even if several other probes pass;
7. lossy mapping is explicitly represented;
8. absent required assumptions produce `REFUSE` rather than guessed normalization;
9. fixture and receipt ordering are deterministic;
10. public Dogram operator floor remains unchanged.

At least one hostile fixture must be constructed so that a naïve aggregate similarity score would incorrectly prefer the false bridge. MathBand must still reject it because the decisive probe is load-bearing.

---

## 12. Success criteria for the incubator

MATHBAND-INCUBATOR-001 succeeds only if:

- exact known bridges survive all harmless representation attacks;
- partial bridges remain explicitly partial;
- false friends fail under decisive probes;
- extra dimensions/operations survive as `EXTRA` or `UNMAPPED`;
- residuals remain visible;
- every successful comparison is scoped to a declared probe family and assumptions;
- no result claims truth, priority, influence, semantic identity, or authority;
- the public Dogram operator floor remains unchanged.

A high number of bridge successes is not a success criterion.

Low false-positive pressure is more important than recall at this stage.

---

## 13. Extraction trigger

MathBand should remain a Dogram incubator until at least all of the following are true:

1. the Five Bats have stable reusable fixtures;
2. at least one exact known bridge, one partial bridge, and one known non-bridge are correctly receipted;
3. at least one documented cross-disciplinary bridge can be represented without special-case code for that discipline pair;
4. the same core receipt shape works across those specimens;
5. no additional public Dogram operator is required merely to host the experiment;
6. a concrete downstream user need exists that would benefit from a reusable standalone interface.

Only then should a standalone MathBand repository or public protocol be considered.

Extraction must preserve Dogram receipts as ancestry rather than rewriting the incubator as though it had always been an independent system.

---

## 14. Terry / novel mathematics gate

A personally or historically important mathematical formulation must not be the calibration target.

Such a specimen enters only after the known ladder above has passed.

The lawful question is:

> **Given an explicit formalization of formulation A and formulation B, and explicit candidate maps, which declared structures are preserved, which fail, which require extra assumptions, and where is the first decisive mismatch?**

The unlawful questions are:

```text
Is Terry right?
Did Terry anticipate field X?
Does this prove two disciplines are secretly the same?
Did one field cause or derive from the other historically?
```

Those questions require different evidence and different authorities.

---

## 15. Candidate seals

```text
MAKE THE MATH PLAY TOGETHER. DO NOT MAKE IT AGREE.
```

```text
THE COMMON STAGE DOES NOT OWN THE VOICES.
```

```text
A BRIDGE MAY PRESERVE RELATION WITHOUT PRESERVING LANGUAGE.
```

```text
WHAT FAILS TO MAP MUST NOT BE SILENTLY ERASED.
```

```text
THE FIRST DECISIVE PROBE OUTRANKS A THOUSAND COSMETIC SIMILARITIES.
```

```text
EXTRA VOICE != WRONG NOTE.
```

---

## 16. HOLD

This design does not authorize implementation until human review approves the written specification.

No runtime code, tests, fixture, CLI, schema, dependency, public operator, automatic bridge discovery, ALEX integration, LOADOUT integration, 3rdi integration, or Terry-specific specimen is admitted yet.

The next lawful step after approval of this written specification is a dedicated implementation plan under the Superpowers workflow.
