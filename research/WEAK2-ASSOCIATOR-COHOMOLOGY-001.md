# WEAK2-ASSOCIATOR-COHOMOLOGY-001 — Same Object Product, Nonzero Associator Receipt

**Date:** 2026-09-04  
**Status:** EXACT FINITE COHERENCE SPECIMEN · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## Question

The preceding strict-2-group research asks whether typed higher compositions close when their required action/whiskering data are retained. This slice asks a genuinely different question:

> What survives when associativity itself is weakened from literal equality to coherent equivalence with an explicit associator witness?

The bounded specimen is a skeletal coherent 2-group encoded by finite group-cohomology data.

## Documented mathematics

For a special/skeletal coherent 2-group, the object group is a group `G`, automorphisms of the unit form an abelian group `H`, `G` acts on `H`, and the associator is encoded by a normalized `H`-valued 3-cocycle. The pentagon identity is exactly the corresponding cocycle condition. Coherent 2-groups are classified up to equivalence by this data, including the cohomology class of the associator.

Primary source:

- John C. Baez and Aaron D. Lauda, *Higher-Dimensional Algebra V: 2-Groups*, Theory and Applications of Categories 12 (2004), 423–491. arXiv:math/0307200.

Supporting peer-reviewed source:

- Eric Sharpe, *Notes on generalized global symmetries in QFT*, Fortschritte der Physik 63 (2015), 659–682. DOI: `10.1002/prop.201500048`. The review explicitly describes a 3-cocycle as the associator data and cocycle closure as the pentagon condition.

## Frozen exact specimen

Take

```text
G = Z/2Z
H = Z/2Z
G-action on H = trivial
```

and define the normalized 3-cochain

```math
a(g,h,k)=ghk \pmod 2.
```

It is normalized because if any input is zero then `a=0`.

For trivial action, the additive 3-cocycle residual is

```math
(\delta a)(g,h,k,\ell)
=
a(h,k,\ell)
-a(g+h,k,\ell)
+a(g,h+k,\ell)
-a(g,h,k+\ell)
+a(g,h,k).
```

Complete enumeration of all `16` quadruples in `(Z/2)^4` gives

```text
pentagon residual set = {0}
```

so the associator is coherent.

## The local delta

For the triple `(1,1,1)`, the object-level product is strictly associative in `G`:

```math
(1+1)+1 = 1+(1+1) = 1 \pmod 2.
```

But the associator receipt is

```math
a(1,1,1)=1.
```

Therefore the two bracketings land on the same skeletal object while retaining a nonidentity coherence witness.

Candidate seal:

> **SAME OBJECT-LEVEL PRODUCT DOES NOT FORCE A ZERO ASSOCIATOR RECEIPT.**

Stronger form:

> **COHERENT EQUIVALENCE CAN REQUIRE A WITNESS EVEN WHEN THE END OBJECT IS LITERALLY THE SAME.**

## Cohomology pressure: can the witness be normalized away?

A normalized 2-cochain `beta:G^2->H` on this specimen is determined entirely by the single bit `beta(1,1)`. There are exactly two normalized 2-cochains.

For each one, compute

```math
(\delta\beta)(g,h,k)
=
\beta(h,k)
-\beta(g+h,k)
+\beta(g,h+k)
-\beta(g,h).
```

Complete enumeration gives the zero 3-cochain for both normalized choices. Neither coboundary equals `a`, since `a(1,1,1)=1`.

Thus this frozen associator represents a nonzero class in the declared finite cohomology calculation.

The Dogram-relevant point is not the abstract name `H^3`; it is the exact finite receipt:

```text
same object group
same binary object multiplication
same endpoint object for 111
pentagon residual = 0
associator witness at 111 = 1
no normalized 2-cochain removes that witness
```

Candidate seal:

> **KEEP THE ASSOCIATOR; DO NOT FLATTEN WEAK COHERENCE INTO STRICT EQUALITY.**

## Contract pressure

This specimen licenses only mathematical statements about the declared finite weak-2-group model.

Explicit refusals:

```text
ASSOCIATOR WITNESS != HISTORICAL EVENT
COHOMOLOGY CLASS != CAUSAL CLASS
PENTAGON COHERENCE != TRUTH
NONTRIVIAL H3 != PHYSICAL OBSTRUCTION
COHERENT EQUIVALENCE != EVIDENCE EQUIVALENCE
```

The fact that two expressions are coherently related does not say that two real-world histories are the same, that either history occurred, or that the witness carries semantic authority.

## Why this is materially new relative to STRICT2-INTERCHANGE-WHISKERING-001

The strict-2-group specimen requires the correct action/whiskering law so that two lawful pasting routes become literally equal.

This specimen occupies the next layer:

```text
STRICT 2-GROUP:
correct composition data -> literal equality

WEAK / COHERENT 2-GROUP:
correct composition data -> explicit isomorphism witness
                       -> witness obeys a higher coherence law
```

So Dogram gains a precise mathematical distinction between

```text
EQUAL
```

and

```text
NOT IDENTIFIED BY STRICTNESS, BUT LAWFULLY RELATED BY A RECEIPTED COHERENCE WITNESS.
```

No public operator is justified yet.

## Executable boundary

`dogram/weak2_associator_cohomology.py` is stdlib-only and bounded to this `Z/2` specimen. It computes:

- the frozen associator;
- all pentagon/3-cocycle residuals;
- the object-level bracketing receipt;
- all normalized 2-cochains and their coboundaries;
- whether any such coboundary removes the associator.

It does **not** implement arbitrary group cohomology, arbitrary bicategories, strictification, semantic equivalence, causal equivalence, evidence aggregation, or historical inference.

Explicit HOLD:

```text
associator@1
coherence@1
weak2@1
cocycle@1
strictify@1
```

## Strongest next frontier

Do not merely enlarge the group. The next worthwhile specimen should test **cohomologous but pointwise different associators**: two associator tables that differ by an explicit 2-cochain coboundary and therefore represent the same cohomology class.

That would pressure the next distinction:

```text
RAW ASSOCIATOR TABLE != COHERENCE CLASS
```

and ask Dogram to receipt the exact change-of-gauge/cochain witness without concluding that cohomologous mathematical presentations are semantically, causally, or historically identical.

## Verification note

The exact finite arithmetic was independently enumerated during the research pass. Wolfram was also invoked for an independent check, but its connector returned an upstream `502` error; therefore this slice makes no Wolfram-verification claim.
