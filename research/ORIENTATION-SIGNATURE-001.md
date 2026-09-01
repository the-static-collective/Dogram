# ORIENTATION-SIGNATURE-001

**Date:** 2026-09-01  
**Status:** RESEARCH KERNEL · EXACT RATIONAL DETERMINANTS · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this survived DrMADDD pressure

`HIGHER-ORDER-DEPENDENCE-001` asks whether ordinary pairwise/rank information hides a larger dependence circuit. This packet asks the next distinct question:

> **Can the entire ordinary basis-support surface remain the same while a mathematically real orientation layer changes?**

Yes, for realizable oriented matroids. A chirotope records the signs of maximal minors (up to the conventional global sign), while forgetting those signs recovers the underlying ordinary matroid basis support.

This packet implements only the finite rational realization arithmetic needed to receipt that distinction. It does not promote an abstract oriented-matroid engine.

## 1 — Documented mathematics

For a rank-`r` real vector configuration, the sign of each `r x r` determinant defines the realizable chirotope on ordered bases. Nonzero determinant support gives the bases of the underlying ordinary matroid; the signs retain orientation information that ordinary basis support forgets.

Useful sources:

- Marcel Celaya, **Patchworking oriented matroids**, *Journal of the London Mathematical Society* (2022), DOI `10.1112/jlms.12667`. Section 2 recalls chirotopes as alternating `{+, -, 0}`-valued maps satisfying Grassmann–Plücker relations.
- Jürgen Bokowski, António Guedes de Oliveira, Jürgen Richter-Gebert, **Algebraic varieties characterizing matroids and oriented matroids**, *Advances in Mathematics* 87(2), 160–185 (1991), DOI `10.1016/0001-8708(91)90070-N`.

## 2 — Frozen hostile control

Use homogeneous rational coordinates in `Q^3` with fixed labels `A < B < C < D`.

Configuration S:

```text
A = (0,0,1)
B = (2,0,1)
C = (2,2,1)
D = (0,2,1)
```

Exact determinants on increasing triples:

```text
ABC =  4
ABD =  4
ACD =  4
BCD =  4
```

So every 3-subset is a basis and the sign tuple is

```text
(+,+,+,+)
```

Configuration I:

```text
A = (0,0,1)
B = (2,0,1)
C = (2,2,1)
D = (2,1,2)
```

Exact determinants:

```text
ABC =  4
ABD =  2
ACD = -2
BCD =  4
```

Again every 3-subset is a basis, so the underlying ordinary rank-3 matroid basis support is identical:

```text
{ABC, ABD, ACD, BCD}
```

But the sign tuple is

```text
(+,+,-,+)
```

Therefore the exact bounded receipt is:

```text
SAME LABELS
SAME RANK
SAME NONZERO BASIS SUPPORT
SAME ORDINARY UNIFORM MATROID U(3,4)
DIFFERENT DECLARED DETERMINANT-SIGN SURFACE
```

Candidate mathal:

> **SAME DEPENDENCE SUPPORT != SAME ORIENTATION SIGNATURE.**

## 3 — What Dogram may infer

Only this:

```text
A declared rational realization can contain sign/orientation information
that disappears when reduced to ordinary rank and circuit support.
```

This is a calculational distinction, not an interpretive one.

## 4 — Required refusals

```text
DIFFERENT CHIROTOPE SIGN != DIFFERENT HISTORICAL EVENT
DIFFERENT ORIENTATION != CAUSAL DIRECTION
ORIENTATION SIGNATURE != HANDEDNESS CLAIM ABOUT THE WORLD
REALIZABLE CONFIGURATION != TRUE MODEL OF THE SOURCE DOMAIN
SAME ORDINARY MATROID != SAME FORMATION HISTORY
MATHEMATICAL ELEGANCE != EVIDENCE
```

A global multiplication of every chirotope sign by `-1` is also a representation convention, so future comparison logic must not silently treat global sign reversal as a substantive difference without a declared normalization.

## 5 — Executable boundary

`dogram.orientation_signature`:

- accepts a finite declared integer-vector realization;
- performs exact `Fraction` Gaussian determinant arithmetic;
- enumerates rank-sized subsets in deterministic label order;
- returns only nonzero bases, exact determinants, and their signs;
- refuses dimension mismatch and invalid rank;
- does not validate arbitrary abstract chirotopes or Grassmann–Plücker tables;
- does not infer orientation semantics.

No public operator is added.

Explicit HOLD:

```text
chirotope@1
oriented_matroid@1
signed_circuit@1
order_type@1
```

## 6 — Verification receipt

TDD was exercised before repository write:

```text
RED:
ModuleNotFoundError: dogram.orientation_signature

GREEN after minimal kernel:
Ran 1 test
OK
```

The committed branch adds a second zero-determinant boundary test and a frozen JSON fixture. Remote CI status must be checked on the PR head before any merge claim.

## 7 — Still-live frontier

The next pressure seam is not “more orientation.” It is **normalization and representation provenance**:

- which transformations preserve the signed invariant;
- which merely globally reverse convention;
- which constitute ground-element reorientation;
- whether two different rational realizations encode the same oriented matroid;
- and who upstream is allowed to assert that this realization is the relevant one.

That boundary belongs beside ALEX/3rdi provenance rather than inside Dogram interpretation.

## Seal

> **A SUPPORT SET CAN TELL YOU WHICH RELATIONS EXIST WHILE FORGETTING WHICH SIDE OF ZERO THEY LIE ON.**

> **KEEP THE SIGN ONLY WHEN THE INPUT GRAMMAR EARNS THE SIGN.**
