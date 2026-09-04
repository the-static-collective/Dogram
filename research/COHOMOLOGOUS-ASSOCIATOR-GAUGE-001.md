# COHOMOLOGOUS-ASSOCIATOR-GAUGE-001 — Raw Table Change, Same Cohomology Class

**Date:** 2026-09-04  
**Status:** EXACT FINITE COHOMOLOGY SPECIMEN · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## Question

`WEAK2-ASSOCIATOR-COHOMOLOGY-001` established that a coherent associator can be nonzero and represent a nontrivial finite cohomology class. The next pressure question is different:

> Can two pointwise different associator tables represent the same coherence class, and can Dogram retain the exact change-of-presentation witness rather than confusing raw table difference with class difference?

This slice answers that question with one bounded `Z/3` specimen.

## Documented mathematics

For a skeletal/special coherent 2-group, the associator is encoded by a normalized 3-cocycle `a:G^3 -> H`, where `H` is an abelian `G`-module. The pentagon identity is the 3-cocycle condition. Equivalence classes depend on the cohomology class `[a]`, not on one pointwise representative table: changing `a` by a 3-coboundary produced from a 2-cochain leaves the class unchanged.

Primary reference:

- John C. Baez and Aaron D. Lauda, *Higher-Dimensional Algebra V: 2-Groups*, Theory and Applications of Categories 12 (2004), 423–491, arXiv:math/0307200. Their classification uses quadruples `(G,H,action,[a])` with `[a] in H^3(G,H)`.

For cyclic groups, carry-type cocycle formulas are standard in explicit bar-resolution calculations. This slice does not rely on the formula being privileged: every relevant cocycle and coboundary identity is exhaustively checked on the finite declared carrier.

## Frozen carrier

Take

```text
G = Z/3Z
H = Z/3Z
G-action on H = trivial
```

using representatives `{0,1,2}`.

Define

```math
a(g,h,k)=g\left\lfloor\frac{h+k}{3}\right\rfloor \pmod 3.
```

This is normalized because any zero input makes the value zero. Exhaustive evaluation of the additive 3-coboundary on all `3^4 = 81` quadruples gives only zero:

```text
{ delta(a)(g,h,k,l) } = {0}
```

so `a` is a normalized 3-cocycle in the declared finite model.

Its nonzero entries are:

```text
(1,1,2) -> 1
(1,2,1) -> 1
(1,2,2) -> 1
(2,1,2) -> 2
(2,2,1) -> 2
(2,2,2) -> 2
```

## Base-class pressure

A normalized 2-cochain `beta:G^2->H` is forced to vanish whenever either input is `0`, so it is determined by the four values on

```text
(1,1), (1,2), (2,1), (2,2).
```

There are exactly

```text
3^4 = 81
```

normalized 2-cochains. Exhaustive enumeration shows that none has coboundary equal to `a`.

Therefore, within this exact finite normalized-cochain calculation, `a` is not itself a coboundary.

This fact is useful only to keep the hostile specimen away from the trivial zero class; no semantic or physical interpretation is attached.

## Explicit change-of-presentation witness

Now freeze one normalized 2-cochain

```text
beta(1,1) = 1
beta(g,h) = 0 otherwise.
```

For trivial action,

```math
(\delta\beta)(g,h,k)
=
\beta(h,k)
-\beta(g+h,k)
+\beta(g,h+k)
-\beta(g,h)
\pmod 3.
```

The coboundary is nonzero on exactly four triples:

```text
(1,1,2) -> 2
(1,2,2) -> 1
(2,1,1) -> 1
(2,2,1) -> 2
```

Define the shifted associator

```math
a' = a + \delta\beta \pmod 3.
```

Then:

```text
a != a' pointwise
```

but, by construction and direct replay,

```text
a' - a = delta(beta)
```

on every one of the `27` triples.

A second exhaustive `81`-quadruple check gives

```text
{ delta(a') } = {0},
```

so the shifted table is also a normalized 3-cocycle.

The exact Dogram distinction is therefore:

> **RAW ASSOCIATOR TABLE != COHERENCE CLASS.**

And the receipt discipline is:

> **KEEP THE COCHAIN WITNESS; DO NOT CALL POINTWISE DIFFERENCE A CLASS DIFFERENCE.**

## Why this is materially new

The previous weak-2 slice established:

```text
same object product
!=
zero associator witness.
```

This slice adds another quotient layer:

```text
same G, H, action
same nontrivial cohomology class
pointwise different associator tables
explicit beta witnessing the change
```

So there are now three distinct calculational surfaces:

```text
raw associator table
coboundary relating two tables
cohomology class after quotient by coboundaries
```

Collapsing any two loses information.

## Contract pressure

Documented mathematics licenses the statement that cohomologous cocycles represent the same cohomology class under the declared coefficient/action data.

Dogram inference:

> A quotient-level sameness claim is only receiptable when the declared equivalence move is itself retained.

Speculation / HOLD:

This resembles several Static Collective laws about decoder changes, gauge freedom, and same-surface/different-history, but no cross-domain identification is promoted here. The algebra only supplies a pressureable example of `raw representation != quotient class`.

Explicit refusals:

```text
COHOMOLOGOUS != HISTORICALLY IDENTICAL
COHOMOLOGY CLASS != CAUSAL CLASS
PRESENTATION CHANGE != OCCURRENCE
COHERENCE EQUIVALENCE != EVIDENCE EQUIVALENCE
ALGEBRAIC GAUGE != PHYSICAL GAUGE
POINTWISE DIFFERENCE != CLASS DIFFERENCE
CLASS AGREEMENT != SEMANTIC AGREEMENT
```

## Executable boundary

`dogram/cohomologous_associator_gauge.py` is stdlib-only and bounded to this declared `Z/3` specimen. It computes:

- the frozen base associator;
- the declared normalized 2-cochain coboundary;
- the shifted associator;
- all pentagon/3-cocycle residuals;
- the exact pointwise table delta;
- exhaustive comparison against all `81` normalized 2-cochain coboundaries.

It does **not** implement arbitrary group cohomology, arbitrary monoidal equivalence, bicategorical rewriting, semantic equivalence, causal equivalence, evidence aggregation, or historical inference.

Explicit HOLD:

```text
cohomology_class@1
coboundary@1
associator_gauge@1
weak2@1
presentation_equivalence@1
```

## Verification

TDD RED was observed on test-only head `5ca6a89942c8d3edf92fb5efc3470a1d26f4b330`: Dogram CI run `#396` failed specifically because `dogram.cohomologous_associator_gauge` did not exist; the remainder of the suite passed.

After the minimal kernel was added, exact head `5a9e0e0c43f7547285fddc9ab997d5c1dd343062` passed Dogram CI run `#398`.

Independent exact enumeration during the research pass reproduced:

```text
81/81 pentagon residuals for a = 0
81/81 pentagon residuals for a' = 0
4 pointwise table deltas
81 normalized 2-cochains checked
0 normalized 2-cochains with coboundary = a
```

Wolfram was invoked for an independent check but its connector returned an upstream `404` during this run, so no Wolfram-verification claim is made.

## Strongest next frontier

Do not immediately build a general cohomology engine. The next useful pressure is **quotient choice itself**:

```text
SAME RAW DATA
+ DIFFERENT DECLARED EQUIVALENCE RELATION
-> DIFFERENT QUOTIENT CLASSIFICATION
```

A good hostile specimen would hold the raw cocycle table fixed while changing only the licensed cochain/action data used to quotient it, then receipt exactly which identifications become available or disappear.

That would connect this seam back to Dogram's broader law:

> **QUOTIENT ONLY THE FREEDOMS YOU DECLARED.**
