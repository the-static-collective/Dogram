# REACHABILITY-PATH-HOMOLOGY-001

**Date:** 2026-08-31  
**Status:** EXECUTABLE RESEARCH KERNEL · EXACT RATIONAL LINEAR ALGEBRA · NO PUBLIC OPERATOR PROMOTION  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Question

Can two directed carriers have the same reachability closure while retaining different directed path topology?

Yes.

This packet freezes the smallest clean hostile control found in the DrMADDDogram hunt. It does **not** claim that path homology reconstructs historical occurrence, causal history, semantic meaning, evidence, or truth.

## 1 — Documented mathematical substrate

Path homology is a homology theory for directed graphs built from allowed directed paths and exact boundary maps. For a loopless digraph `D=(V,A)`, let `A_p(D)` be the allowed directed p-paths. The invariant subspace

```math
\Omega_p=\{\omega\in\mathbb{Q}^{A_p}:\partial\omega\in\mathbb{Q}^{A_{p-1}}\}
```

forms a chain complex. The first Betti number is

```math
\beta_1=\dim\ker\partial_1-\dim\operatorname{im}\partial_2.
```

Primary reference:

- Samir Chowdhury, Steve Huntsman, Matvey Yutin, **Path homologies of motifs and temporal network representations**, *Applied Network Science* 7, 4 (2022), DOI `10.1007/s41109-021-00441-z`.

The paper gives an explicit four-node example with `beta_1=1` versus `beta_1=0` and describes an exact linear-algebra algorithm for arbitrary finite digraphs. The implementation in this branch reproduces that published example as an external sanity check.

## 2 — Frozen hostile control

Let

```text
V = {0,1,2}
```

and compare two loopless digraphs.

### Carrier A — directed 3-cycle

```text
0 -> 1
1 -> 2
2 -> 0
```

### Carrier B — complete bidirected triangle

```text
0 <-> 1
1 <-> 2
2 <-> 0
```

Both are strongly connected. Therefore their reflexive reachability closures are identical:

```math
R_A=R_B=V\times V.
```

Exact closure size:

```text
|R_A| = |R_B| = 9
```

So a decoder that retains only `can source reach target?` cannot distinguish them.

## 3 — Exact beta_1 receipt over Q

The internal research kernel computes non-regular path homology in degree one using exact rational rank calculations.

For the directed cycle:

```text
|A_1| = 3
|A_2| = 3
rank(d1) = 2
rank(nonallowed projection of d2) = 3
rank(full d2 on allowed 2-paths) = 3
rank(B1) = 3 - 3 = 0

dim(Z1) = 3 - 2 = 1
beta1 = 1 - 0 = 1
```

For the complete bidirected triangle:

```text
|A_1| = 6
|A_2| = 12
rank(d1) = 2
rank(nonallowed projection of d2) = 3
rank(full d2 on allowed 2-paths) = 7
rank(B1) = 7 - 3 = 4

dim(Z1) = 6 - 2 = 4
beta1 = 4 - 4 = 0
```

Hence

```math
R_A=R_B
\qquad\text{but}\qquad
\beta_1(A)=1\ne0=\beta_1(B).
```

## 4 — Dogram mathal

The surviving statement is narrow:

> **REACHABILITY CLOSURE IS A LOSSY QUOTIENT OF DIRECTED PATH STRUCTURE.**

Equivalent compression:

```text
SAME REACHABLE SURFACE
!=
SAME DIRECTED PATH TOPOLOGY
```

This directly reinforces an existing Dogram constitutional refusal:

```text
GRAPH REACHABILITY != HISTORICAL OCCURRENCE.
```

but does not prove historical occurrence from path homology either.

## 5 — Why this is stronger than another graph metric

Reachability closure deliberately forgets how reachability is constituted. Once both graphs become all-to-all reachable, ordinary reachability has saturated.

Path homology still distinguishes the two carriers because it retains compatibility relations among allowed directed paths before that saturation quotient.

This gives Dogram an exact finite specimen of:

```text
FINE CARRIER -> COARSE REACHABILITY DECODER
```

where the coarse decoder becomes identical while a declared fine invariant remains different.

## 6 — Implementation boundary

Branch module:

```text
dogram/path_homology.py
```

exports only:

```text
reachability_closure(vertices, edges)
first_betti_number(vertices, edges)
```

Properties:

- Python standard library only;
- exact rational Gaussian elimination via `fractions.Fraction`;
- loopless finite digraphs;
- computes only `beta_1`;
- no persistent path homology;
- no temporal-network inference;
- no public Dogram dispatch;
- no automatic promotion into PHASELIFT or OMEGA.

Focused fixture:

```text
tests/test_reachability_path_homology.py
```

The test was written and observed failing before the module existed. The focused local harness then passed after the minimal module was added.

Direct full-repository clone/test execution was unavailable in the tool runtime because outbound GitHub DNS resolution failed. The authoritative branch writes were performed through the connected GitHub tool. No full-suite claim is made.

## 7 — External sanity control

The 2022 paper gives a four-node example where one digraph has `beta_1=1` and a second has `beta_1=0`.

Using the edge sets described by the paper's explicit boundary formulas:

```text
D1 = {i->j, i->k, l->j, l->k}
D2 = {w->x, w->y, x->z, y->z}
```

the bounded kernel reproduces:

```text
beta1(D1) = 1
beta1(D2) = 0
```

This sanity check is not part of the public API and does not establish completeness of the implementation in higher dimensions.

## 8 — Required refusals

```text
SAME REACHABILITY != SAME PATH STRUCTURE
DIFFERENT PATH HOMOLOGY != DIFFERENT HISTORICAL EVENT RECORD
PATH HOMOLOGY != CAUSAL PROOF
PATH HOMOLOGY != EVIDENCE
PATH HOMOLOGY != SEMANTIC MEANING
STRONGLY CONNECTED != IDENTICAL CARRIER
BETA NUMBER != AUTHORITY
```

## 9 — Still-live temporal frontier

This packet uses static directed reachability closure. It does **not** yet establish the stronger claim:

> two temporal histories with the same temporal reachability relation can be separated by path homology of a canonically declared temporal representation.

That stronger statement remains a live research frontier. It needs the temporal representation itself to be frozen first so that representation choice does not silently manufacture the distinction.

Candidate next probe:

```text
TEMPORAL HISTORY
  -> declared event/time-expanded/path-complex representation
  -> temporal reachability quotient
  -> path-homology receipt
```

with hostile controls over representation choice.

## Seal

> **WHEN REACHABILITY SATURATES, HISTORY MAY STILL HAVE SHAPE — BUT DOGRAM MUST NAME THE REPRESENTATION BEFORE IT CALCULATES THE SHAPE.**
