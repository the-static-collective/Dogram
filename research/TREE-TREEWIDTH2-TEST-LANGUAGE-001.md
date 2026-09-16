# TREE-TREEWIDTH2-TEST-LANGUAGE-001

## Status

Research-only bounded specimen. No public Dogram operator is promoted.

## Carrier

Freeze two simple undirected targets on six vertices:

- `G = C6`, one six-cycle;
- `H = 2K3`, two disjoint triangles.

Both are 2-regular on six vertices. They are not isomorphic: `G` has one connected component while `H` has two.

## Exact tree-language collision

For any finite tree `T` with `m >= 1` vertices and any `d`-regular target graph `Q` on `n` vertices,

`hom(T,Q) = n * d^(m-1)`.

Reason: root `T` arbitrarily. There are `n` choices for the root image. Each of the remaining `m-1` tree vertices has exactly one parent edge and therefore exactly `d` choices once its parent image is fixed. No cycles impose additional consistency constraints.

Therefore for every finite tree `T`,

`hom(T,C6) = hom(T,2K3) = 6 * 2^(|V(T)|-1)`.

This is an all-tree certificate, not a finite sample extrapolation. The frozen fixture includes only replay samples.

## First bounded-treewidth separation

Use the source `K3`. Its treewidth is 2. In a simple loopless target, every homomorphism `K3 -> Q` maps onto a triangle, and each target triangle contributes `3! = 6` homomorphisms.

- `C6` has no triangles, hence `hom(K3,C6)=0`.
- `2K3` has two triangles, hence `hom(K3,2K3)=12`.

Exact delta: `12`.

The executable kernel also enumerates all ordered triples directly, so the frozen `K3` counts do not depend only on the triangle-count argument.

## Documented mathematics

Dell, Grohe & Rattan, *Lovász Meets Weisfeiler and Leman*, ICALP 2018, DOI `10.4230/LIPIcs.ICALP.2018.40`, prove that equality of homomorphism counts from all trees is equivalent to indistinguishability by color refinement/fractional isomorphism, and lift the result to homomorphism counts from graphs of bounded treewidth and higher-dimensional Weisfeiler-Leman/Sherali-Adams levels.

Grohe, Rattan & Seppelt, *Homomorphism Tensors and Linear Equations*, ICALP 2022, DOI `10.4230/LIPIcs.ICALP.2022.70`, develop a unified algebraic framework for homomorphism indistinguishability over restricted source classes including bounded treewidth, pathwidth, and treedepth.

Wolfram independently confirmed that `C6` and `2K3` each have six vertices and six edges, with connected-component counts one and two respectively. Its semantic interface did not directly return the requested homomorphism counts, so no Wolfram claim is made for the all-tree or `K3` calculations.

Consensus was attempted during this pass but the connected account's monthly search quota was exhausted; no Consensus literature claim is made.

## Dogram inference

The carrier pair is unchanged while the declared source/test language is enlarged from all trees (treewidth 1) to permit one treewidth-2 graph. The resulting delta is attributable to the language change.

Candidate seals:

**SAME ALL-TREE RECEIPTS != SAME TREEWIDTH-2 RECEIPTS.**

**A CYCLE IN THE TEST LANGUAGE CAN REVEAL A DELTA THAT EVERY TREE MISSES.**

**THE SOURCE CLASS IS PART OF THE DECODER RECEIPT.**

## Refusals

- `TREE-HOM COLLISION != GRAPH IDENTITY`
- `TREEWIDTH-2 DELTA != OCCURRENCE DELTA`
- `STRONGER TEST LANGUAGE != MORE TRUE`
- `HOMOMORPHISM COUNT != EVIDENCE COUNT`
- `SOURCE CYCLE != CAUSAL CYCLE`
- `WL DIMENSION != AUTHORITY LEVEL`
- `FRACTIONAL ISOMORPHISM != HISTORICAL EQUIVALENCE`

## HOLD

Do not promote `hom_test_language@1`, `treewidth_probe@1`, `tree_hom@1`, `bounded_treewidth@1`, `wl_dimension@1`, graph identity, evidence, occurrence, causal, semantic, or authority machinery from this specimen.

## Strongest next frontier

The useful question is no longer merely `treewidth 1 -> treewidth 2`. The next pressure point is whether the hierarchy can be factored by *specific source grammar* inside a fixed treewidth bound: cycles, series-parallel sources, bounded pathwidth, and bounded treedepth need not carry the same distinguishing power even when they share coarse width bounds.

Candidate next seal:

**WIDTH BOUNDS THE QUESTION LANGUAGE; IT DOES NOT UNIQUELY SPECIFY IT. RECEIPT THE SOURCE CLASS, NOT ONLY THE WIDTH.**
