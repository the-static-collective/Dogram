# REORIENTATION-OBSTRUCTION-001

**Date:** 2026-09-01  
**Status:** RESEARCH KERNEL · EXACT GF(2) REORIENTATION TEST · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this survived the hunt

`ORIENTATION-SIGNATURE-001` proved that identical ordinary basis support can retain different determinant-sign surfaces. It also left an explicit warning: a global reversal of all chirotope signs is conventional, and ground-element reorientation is another lawful sign transformation in oriented-matroid theory.

The next calculational question is therefore narrower:

> **When two sign tables differ, is the delta explainable entirely by a global sign and per-element reorientation, or does a residual sign obstruction remain after those freedoms are quotiented?**

This packet answers only that finite algebraic question.

## 1 — Documented mathematics

For an oriented matroid, reorienting a subset `A` of the ground set changes the signs attached to those elements in the signed-circuit/covector descriptions. In realizable sign-matrix descriptions, reorienting an element corresponds to reversing the sign of the corresponding column. See:

- N. García-Colín, L. P. Montejano, J. L. Ramírez Alfonsín, **On the number of vertices of projective polytopes**, *Mathematika* 69(2), 535–561 (2023), DOI `10.1112/mtk.12193` — Section 3 recalls reorientation and explicitly notes column-sign reversal in the sign-matrix model.
- J. Rau, A. Renaudineau, K. Shaw, **Real phase structures on matroid fans and matroid orientations**, *Journal of the London Mathematical Society* 106(4), 3687–3710 (2022), DOI `10.1112/jlms.12671` — orientations are encoded in `{+,-,0}` sign data and are naturally related to `Z/2Z` phase structure.

For a chirotope sign table on rank-sized bases, represent each element reorientation by a bit `x_e in GF(2)` and the conventional global sign by `g in GF(2)`. For each basis `B`, the observed sign mismatch bit `d_B` must satisfy

```math
d_B = g + \sum_{e\in B} x_e \pmod 2.
```

Thus reorientation comparison is an exact finite linear-system problem over `GF(2)`.

## 2 — Frozen hostile control

Two homogeneous rational point configurations in `Q^3` share labels `A<B<C<D<E` and have every 3-subset nonzero.

Left:

```text
A=(0,0,1)
B=(0,1,1)
C=(1,0,1)
D=(1,1,1)
E=(2,3,1)
```

Increasing-triple determinants:

```text
ABC=-1 ABD=-1 ABE=-2 ACD= 1 ACE= 3
ADE= 1 BCD= 1 BCE= 4 BDE= 2 CDE=-1
```

Right:

```text
A=(0,0,1)
B=(0,1,1)
C=(1,0,1)
D=(1,1,1)
E=(3,2,1)
```

Increasing-triple determinants:

```text
ABC=-1 ABD=-1 ABE=-3 ACD= 1 ACE= 2
ADE=-1 BCD= 1 BCE= 4 BDE= 1 CDE=-2
```

Both therefore have the same complete basis support `U(3,5)`.

Their sign tuples differ only at `ADE`:

```text
left  = (-,-,-,+,+,+,+,+,+,-)
right = (-,-,-,+,+,-,+,+,+,-)
```

A single changed basis sign might look small, but it is **not** realizable by any combination of global sign reversal and ground-element reorientation.

The exact inconsistent-system witness returned by elimination is

```text
{ABC, ABE, ACD, ADE}
```

Each ground element occurs an even number of times across that selected basis family:

```text
A:4  B:2  C:2  D:2  E:2
```

and the number of selected bases is even, so every allowed reorientation factor and the global sign factor cancel in the product. Yet

```text
product(left signs)  = +1
product(right signs) = -1
```

Therefore no allowed reorientation/global-sign assignment can explain the delta.

## 3 — Dogram mathal

```text
SAME BASIS SUPPORT
!= SAME ORIENTATION SIGNATURE
!= SAME REORIENTATION CLASS
```

Sharper seal:

> **A SIGN DELTA IS NOT YET A STRUCTURAL DELTA; QUOTIENT THE LICENSED SIGN FREEDOMS FIRST.**

And after quotienting:

> **AN EVEN-INCIDENCE SIGN PRODUCT CAN WITNESS WHAT REORIENTATION CANNOT ERASE.**

## 4 — Executable boundary

`dogram.reorientation_obstruction`:

- accepts a finite declared basis family and two `{+1,-1}` sign tables;
- solves the reorientation/global-sign equations exactly over `GF(2)`;
- when solvable, returns one deterministic global sign and ground-element reorientation assignment and can replay it against the target sign table;
- when inconsistent, returns a finite parity certificate as a subset of bases;
- validates basis/sign shape and never infers whether the supplied signs are a valid abstract chirotope.

The frozen fixture derives both sign tables from the already-landed exact rational `orientation_signature` kernel before comparison.

No public operator is added.

Explicit HOLD:

```text
reorientation@1
orientation_class@1
chirotope_equivalence@1
projective_equivalence@1
```

## 5 — Required refusals

```text
REORIENTATION EQUIVALENCE != SAME HISTORICAL FORMATION
REORIENTATION OBSTRUCTION != CAUSAL DIFFERENCE
PARITY CERTIFICATE != EVIDENCE ABOUT THE SOURCE DOMAIN
SAME REORIENTATION CLASS != SAME REALIZATION
DIFFERENT REORIENTATION CLASS != DIFFERENT MEANING
REALIZABLE ORIENTED-MATROID ARITHMETIC != WORLD TRUTH
```

The kernel compares only one declared sign representation. It does not establish that the representation is admissible, canonical, causally faithful, or historically attributable.

## 6 — TDD / verification receipt

The focused test was committed before production implementation and RED was observed because `dogram.reorientation_obstruction` did not exist.

After the minimal kernel, the focused test surface passed. The fixture was then bound to two exact rational realizations and the integration test re-ran through `dogram.orientation_signature` before the reorientation comparison.

Remote CI status must be checked on the exact PR head before any repository-wide pass claim.

## 7 — Still-live frontier

The next seam is **representation equivalence beyond reorientation**.

Reorientation is only one allowed transformation family. Distinct rational realizations may encode the same oriented matroid through orientation-preserving linear/projective changes, relabelings, or other declared equivalences. Conversely, an oriented-matroid equivalence does not preserve formation history.

A future pass should ask for the smallest exact quotient ladder:

```text
raw coordinates
-> determinant signs
-> global-sign quotient
-> reorientation quotient
-> relabeling / oriented-matroid isomorphism
-> ??? provenance remains external
```

Do not collapse these layers into one notion of sameness.

## Seal

> **QUOTIENT THE FREEDOMS YOU DECLARED. KEEP THE RESIDUAL YOU COULD NOT EXPLAIN AWAY.**
