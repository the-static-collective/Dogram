# DECODER-SPACE CALCULUS — Differentiate the Key

**Date:** 2026-08-28  
**Status:** RESEARCH SLICE / NO RUNTIME CONFORMANCE CLAIM  
**Scope:** finite variation over declared decoder constitutions  
**Promotion:** HOLD

> **DOGRAM CAN DIFFERENTIATE NOT ONLY WORLDS, BUT DECODERS.**

## 0. Decision

The recent `022100` work exposed a new calculational target.

Dogram has so far treated a decoder as context supplied around a specimen. The new question is narrower:

> If the source is held fixed and one declared decoder coordinate changes, what changes in the projection?

This note models the decoder itself as a bounded variation field.

It does **not** add a Dogram operator, alter a schema, or claim that any decoder is semantically correct.

The calculational object is only:

```text
same source
+
declared decoder variation
->
typed projection difference
```

---

## 1. Typed setup

Let `x` be a held source object.

Let a decoder constitution be a finite tuple:

```math
D = (d_1,d_2,\dots,d_m)
```

with candidate coordinates such as:

```text
segmentation
orientation
radix
symbol map
observer cut
projection rule
aggregation rule
relation vocabulary
probe order
```

These coordinates are not assumed commensurable.

A decoder may produce a projection:

```math
M_x(D).
```

The output may be numeric, symbolic, structured, graph-valued, or opaque.

Therefore:

```text
decoder comparison
!=
subtraction by default
```

Dogram must retain its existing typed-value discipline.

---

## 2. `SEGMENTATION-BIFURCATION-001`

A boundary is part of the decoder constitution.

For a token string of length `n`, there are `n-1` internal gaps. If each gap is independently declared CUT / NO-CUT, the segmentation-mask family has size:

```math
2^{n-1}.
```

For `022100`, `n=6`:

```math
2^5 = 32.
```

There are five one-cut decoders and thirty-one nontrivial cut masks relative to the uncut form.

The important result is not the count itself.

Different segmentations may change the **type** of the decoded object.

Example:

```text
022 | 100
```

under a declared `2 -> *` question decoder may be typed as:

```text
(question, target)
```

while:

```text
022100
```

may be typed as one six-coordinate partial question:

```text
0**100
```

Thus:

> **SEGMENTATION MAY CHANGE OBJECT TYPE, NOT MERELY OBJECT VALUE.**

### Required refusal

If two decoder outputs are not admitted into a common comparison type, Dogram must not manufacture a numeric delta between them.

Possible outcomes include:

```text
SAME
DIFFERENT
TYPE_CHANGED
INSUFFICIENT_TO_COMPARE
```

No semantic interpretation is implied.

---

## 3. `DECODER-DELTA-001`

Choose a baseline decoder `D` and a decoder variant `D'` differing in exactly one declared coordinate.

For numeric outputs:

```math
\Delta_D M_x = M_x(D') - M_x(D).
```

For opaque or structured outputs, use the existing typed comparison discipline rather than illicit subtraction.

Conceptually:

```text
SOURCE x held fixed
DECODER D0
  -> projection P0

change exactly one declared decoder coordinate

DECODER D1
  -> projection P1

COMPARE(P0,P1)
  -> decoder-delta receipt
```

### Candidate lowerer

If the two projections can be represented as an ordered two-state trace, this mathal should first be pressured through existing `delta@1` behavior rather than earning a dedicated decoder operator.

### Boundary

`DECODER-DELTA-001` measures sensitivity to a declared decoder change.

It does not establish:

```text
which decoder is true
which reading is historically intended
which reading has evidentiary support
which reading has authority
```

---

## 4. `DECODER-INTERACTION-001`

Let two decoder coordinates be independently perturbable:

```text
A = segmentation variant
B = orientation variant
```

Construct the four projections:

```text
M00 = M_x(A0,B0)
M10 = M_x(A1,B0)
M01 = M_x(A0,B1)
M11 = M_x(A1,B1)
```

For compatible numeric outputs, define the mixed decoder difference:

```math
I_{AB}(x) = M_{11} - M_{10} - M_{01} + M_{00}.
```

This asks:

> Does the joint decoder change alter the projection beyond the two first-order decoder changes considered separately?

For non-numeric outputs, an equivalence-mode rectangle may ask whether parallel decoder-change effects agree under a declared comparison relation.

### Candidate lowerer

Pressure first through `rectangle@1` composition.

### Important non-collapse

```text
nonzero decoder interaction
!=
causality
!=
hidden intent
!=
correct reading
```

It establishes only non-additive or non-parallel sensitivity under the declared decoder family.

---

## 5. Higher-order decoder differences

For three independently declared decoder coordinates `A,B,C`, a full `2^3` decoder table permits a third mixed difference.

The same bounded hierarchy appears:

```text
decoder state
  -> first decoder difference
  -> pair decoder interaction
  -> third-order decoder interaction residual
```

This is mathematically ordinary finite-difference structure applied to a different domain.

The novelty claim is therefore intentionally small:

> **The decoder constitution may itself be a lawful finite-difference specimen.**

No generalized `decoder-cube@1` operator is proposed.

---

## 6. `DECODER-ORBIT-001`

Given a finite, predeclared decoder family:

```math
\mathcal D = \{D_1,\dots,D_k\}
```

define the projection orbit:

```math
\mathcal O_x(\mathcal D)
=
\{M_x(D): D\in\mathcal D\}.
```

Depending on the question, retain either:

```text
set of distinct projections
multiset with recurrence counts
ordered traversal trace
full decoder -> projection map
```

These are different objects.

### Why the map matters

The set:

```text
{P1,P2,P3}
```

forgets which decoder produced which projection.

The map:

```text
D1 -> P1
D2 -> P1
D3 -> P2
D4 -> P3
```

preserves decoder ancestry.

Dogram should prefer the richer receipt when the distinction is material.

### Neighbor

This overlaps the existing `FINITE-ORBIT-001` frontier idea. That is evidence to pressure composition before admitting a new decoder-specific orbit primitive.

---

## 7. `INVARIANT-ASH-001`

A decoder ensemble can pressure a candidate property `P`.

Let `P` be a declared predicate over projections.

Define:

```math
ASH_P(x,\mathcal D)
=
\{D\in\mathcal D : P(M_x(D))\}.
```

A strict family-invariant candidate satisfies:

```math
\forall D\in\mathcal D,\quad P(M_x(D)).
```

This can be compressed as:

```text
burn the decoder variants
keep the declared property that survives all of them
```

Hence the research name:

`INVARIANT-ASH-001`.

### Critical control

Survival across many decoders is not automatically strong if the decoder family is redundant.

For example, ten variants that all preserve the same load-bearing segmentation rule do not independently pressure segmentation sensitivity.

A receipt should therefore record:

```text
decoder axes varied
decoder axes held fixed
known shared construction / ancestry
family generation rule
```

Dogram computes the survival pattern.

ALEX decides what evidentiary or research weight, if any, that recurrence deserves.

---

## 8. Decoder bifurcation map

For a finite decoder adjacency graph `G_D`, label edges by projection change.

```text
D_i ---- D_j
   decoder change
```

with edge receipt:

```text
changed decoder coordinates
projection comparison
output type change, if any
magnitude / relation if lawful
```

A decoder-space boundary is then visible where small declared decoder changes repeatedly yield large or type-changing projection differences.

This is a structural sensitivity map.

It does not decide which side is correct.

Potential calculations can already lower into:

```text
delta@1      first edge change
rectangle@1  pair interaction
reach@1      if a decoder mutation is represented as an explicit graph mutation
ablate@1     if removing one decoder capability and recomputing reachability is the actual question
```

No new operator is earned merely because the graph is called decoder-space.

---

## 9. `BROKEN-DECODER-PROBE-001`

A deliberately malformed or semantically implausible decoder may still be useful as a **controlled perturbation** if its transformation is defined exactly.

The valid inference is narrow:

```text
wrong / hostile decoder
!=
evidence for its projection
```

but:

```text
wrong / hostile decoder
+
controlled comparison to baseline
=
potential evidence about dependence on the altered decoder feature
```

Example:

If an intentionally reversed symbol order destroys a property while several non-reversal changes preserve it, reversal-sensitivity has been demonstrated for that property under the tested family.

Nothing about historical truth follows automatically.

This mathal belongs jointly with ALEX PRESSURE, because Dogram can calculate the change but cannot admit the epistemic conclusion.

---

## 10. `RING-HOLONOMY-001` — the null control first

The earlier exploratory language proposed traversing a closed relation path through decoder coordinates and comparing the returning projection with the starting projection.

The first exact result is a **refusal of fake novelty**.

If:

```text
M_x(D)
```

is a pure deterministic stateless function, and a decoder path returns to the exact same source `x` and exact same decoder constitution `D`, then:

```math
M_x(D_{final}) = M_x(D_{initial})
```

whenever:

```math
D_{final}=D_{initial}.
```

Therefore pure decoder-space has zero return residual by construction.

### Null law

> **NO HIDDEN HISTORY, NO NONZERO HOLONOMY.**

A claimed nonzero return difference implies at least one of:

```text
source changed
decoder state did not actually return
hidden context changed
history is part of the state
nondeterminism entered
comparison was not lawful
implementation bug
```

That is useful pressure.

### Stateful extension

Nontrivial path dependence can be modeled only after admitting an explicit history/context state `H`:

```math
M(x,D,H).
```

A traversal may then update:

```math
H_0 -> H_1 -> ... -> H_k
```

while nominal decoder coordinates return:

```math
D_k = D_0.
```

Now compare:

```math
M(x,D_0,H_k)
```

with:

```math
M(x,D_0,H_0).
```

Any residual is a **history/context residual**, not magic curvature in a stateless decoder.

### Promotion verdict

`RING-HOLONOMY-001` remains research vocabulary only.

Before any runtime consideration it must demonstrate a real specimen where path-dependent state is necessary and cannot be represented cleanly with ordinary trace + delta composition.

---

## 11. A decoder variation hierarchy

The current candidate hierarchy is:

```text
SOURCE x
  |
  v
DECODER STATE D
  |
  +-- one coordinate changes
  |      -> DECODER-DELTA-001
  |
  +-- two coordinates vary
  |      -> DECODER-INTERACTION-001
  |
  +-- finite family
  |      -> DECODER-ORBIT-001
  |      -> INVARIANT-ASH-001
  |
  +-- decoder graph
  |      -> segmentation / bifurcation map
  |
  +-- closed path
         -> zero-return null control if stateless
         -> history residual only if explicit state evolves
```

This is a calculus of **sensitivity**, not a truth engine.

---

## 12. Hostile controls

### CONTROL A — source drift

Change the source while claiming only the decoder changed.

Expected:

```text
REFUSE / SOURCE_NOT_HELD_FIXED
```

### CONTROL B — multi-coordinate smuggling

Claim a first-order decoder delta while two decoder coordinates changed.

Expected:

```text
REFUSE / UNCONTROLLED_DECODER_CHANGE
```

unless the comparison is explicitly typed as a multi-coordinate perturbation.

### CONTROL C — output-type collapse

Subtract a graph output from a numeric output because both are called projections.

Expected:

```text
REFUSE / INCOMPATIBLE_OUTPUT_TYPES
```

### CONTROL D — correlated ensemble inflation

Generate many cosmetic decoder variants that preserve the same load-bearing rule and claim independent recurrence.

Expected:

Dogram reports recurrence counts and family ancestry only; no independence conclusion.

### CONTROL E — post-hoc family selection

Explore hundreds of decoders, then report only the five that preserve the favored pattern.

Expected:

Receipt must preserve the declared family or label the run exploratory/post-hoc.

### CONTROL F — broken decoder authority laundering

A hostile decoder emits a desired result; analyst treats that result as supported because the perturbation was useful.

Expected:

```text
CALCULATION MAY STAND
SEMANTIC PROMOTION REFUSED OUTSIDE DOGRAM
```

### CONTROL G — fake holonomy

Traverse a pure stateless decoder cycle that returns to exact `D0`, then claim a nonzero return residual.

Expected:

```text
ZERO
```

or refusal due to hidden changed state.

### CONTROL H — history admitted

Use explicit context state `H`, mutate it along the path, return to `D0`, and observe a changed output.

Expected:

Receipt attributes the residual to changed `H` / formation history rather than to decoder closure alone.

---

## 13. Runtime verdict

Do **not** add:

```text
decoder-delta@1
decoder-orbit@1
invariant-ash@1
holonomy@1
```

from this note.

First pressure the mathals through the existing/planned v0 floor:

```text
first decoder difference -> delta@1
pair decoder interaction -> rectangle@1
reachability change       -> reach@1 when structurally appropriate
withdrawal                -> ablate@1 when structurally appropriate
```

`FINITE-ORBIT-001` remains a neighboring research capability, not proof that an orbit operator is needed.

A new operator must earn existence by demonstrating a calculational gap, not a naming gap.

---

## 14. Owner boundary

Dogram may report:

```text
what changed
where it changed
whether first-order changes interact
which declared properties survive a finite decoder family
whether a return residual is zero under a pure decoder
```

Dogram does not report:

```text
which decoder is historically correct
which projection is evidence
which recurrence is independent corroboration
which relation is meaningful
which reading has authority
```

Those are owner-gated questions outside the calculator.

---

## 15. Recommended frozen specimens

### `DECODER-CUT-001`

Source:

```text
022100
```

Decoder A:

```text
022 | 100
```

Decoder B:

```text
022100
```

Assert:

```text
source identical
segmentation differs
result type differs under the declared question grammar
```

### `DECODER-RECTANGLE-001`

Choose two independent decoder coordinates and four frozen outputs.

Assert first-order effects and pair interaction with existing rectangle semantics.

### `DECODER-ENSEMBLE-001`

Use a predeclared finite family containing materially different variants plus redundant controls.

Assert:

```text
raw recurrence count
unique projection count
family ancestry
property-survival mask
```

without semantic promotion.

### `STATELESS-RING-NULL-001`

Traverse a closed decoder path returning exactly to `D0` with source held fixed.

Assert:

```text
final projection == initial projection
```

### `STATEFUL-RING-001`

Repeat with explicit evolving context `H`.

Assert:

```text
nominal decoder returns
context differs
return residual, if any, is attributable to context/history
```

---

## Seal

> **THE KEY CAN ENTER THE DIFFERENCE TABLE.**
>
> **A BROKEN DECODER DOES NOT PROVE ITS READING. IT CAN REVEAL WHAT THE READING DEPENDS ON.**
>
> **BURN THE DECODERS. KEEP THE TYPED INVARIANT ASH.**
>
> **NO HIDDEN HISTORY, NO NONZERO HOLONOMY.**
>
> **DO THE MATH. SHOW THE DECODER DELTA. KEEP THE RECEIPT.**
