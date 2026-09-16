# WL-ARITY-SEPARATION-001

Status: bounded research specimen; no public operator promotion.

## Seal

**SAME 2-WL RECEIPT != SAME 3-WL RECEIPT.**

Operational form:

**IF A DELTA APPEARS ONLY AFTER RAISING TUPLE DIMENSION, RECEIPT THE DIMENSION CHANGE AS PART OF THE DECODER DELTA.**

## Frozen carrier

This slice reuses the exact edge lists already frozen by `STRONGLY-REGULAR-CLIQUE-COLLISION-001`:

- the `4 x 4` rook graph / Hamming graph `H(2,4)`;
- the Shrikhande graph.

Both are non-isomorphic strongly regular graphs with parameters `(16,6,2,2)`. The prior slice already receipts the lower-order collision and the `K4` delta: the rook graph has 8 copies of `K4` and clique number 4; the Shrikhande graph has no `K4` and clique number 3.

## Declared refinement

The kernel implements the standard joint `k`-dimensional Weisfeiler-Leman replacement refinement for `k in {2,3}`.

For each ordered `k`-tuple `v=(v_1,...,v_k)`:

1. initial color is the complete equality/adjacency atomic type of the tuple;
2. for each vertex `w`, form the `k`-vector of colors obtained by replacing coordinate `i` by `w` for every `i`;
3. collect the multiset of those replacement vectors;
4. refine by `(old_color, replacement_multiset)`.

Color identifiers are assigned jointly across both graphs so histogram comparison is meaningful. The kernel is bounded to 16 vertices and dimensions 2 or 3. It uses only exact finite tuple enumeration and integer color IDs.

## Exact receipt

### 2-WL

Both graphs begin with the same three pair classes:

- diagonal: 16 ordered pairs;
- adjacent: 96 ordered pairs;
- nonadjacent distinct: 144 ordered pairs.

After one joint 2-WL round the partition remains exactly those three classes in both graphs. No old color class splits, no new color classes merge, and the two color histograms remain identical.

This is already stable: for a strongly regular graph, the replacement counts for an ordered pair depend only on whether the pair is equal, adjacent, or nonadjacent, and those counts are fixed by `(v,k,lambda,mu)`. Since this pair shares `(16,6,2,2)`, 2-WL cannot separate it.

### 3-WL

Both graphs begin with the same 15 atomic triple-type class sizes:

`16, 96, 96, 96, 144, 144, 144, 192, 288, 288, 288, 576, 576, 576, 576`.

After one joint 3-WL round their histograms differ.

Rook graph class sizes:

`16, 96, 96, 96, 144, 144, 144, 192, 288, 288, 288, 576, 576, 576, 576`.

Shrikhande graph class sizes:

`16, 96, 96, 96, 96, 96, 96, 144, 144, 144, 192, 192, 192, 192, 192, 192, 192, 192, 384, 384, 384, 384`.

Therefore this frozen pair is 2-WL-indistinguishable but 3-WL-distinguishable under the explicitly declared implementation.

## Why this is stronger than another motif

`STRONGLY-REGULAR-CLIQUE-COLLISION-001` established that a 4-point clique delta survives agreement on degree, spectrum, joint degree counts, strongly regular parameters, and triangle count. This slice changes the question from “which next invariant should we add?” to “what tuple dimension does the decoder possess?”

The delta is no longer merely another scalar statistic. It is a change in the expressive resource of the refinement itself.

That gives Dogram a reusable distinction:

**DECODER DIMENSION IS PART OF THE RECEIPT.**

A collision under a 2-tuple decoder is only a collision relative to that decoder. Raising the tuple dimension changes the admissible relational context and can expose a residual that was previously quotient-collapsed.

## Literature neighborhood

Documented mathematics:

- Strongly regular graphs are regular graphs in which common-neighbor counts for adjacent and nonadjacent pairs are constants `lambda` and `mu`; Polhill, Davis, Smith & Swartz (2024), DOI `10.1002/jcd.21938`, review this standard definition and the adjacency identity controlled by `(v,k,lambda,mu)`.
- Nowak, Olmez & Song (2016), DOI `10.1002/jcd.21518`, explicitly identify `H(2,4)` and the Shrikhande graph as non-isomorphic strongly regular graphs with the same `(16,6,2)` design data.
- Higher-dimensional Weisfeiler-Leman algorithms form a genuine hierarchy of distinguishability; Egrot & Hirsch (2021), DOI `10.1002/jgt.22741`, discuss graph families that evade arbitrary fixed `k`-WL dimensions, demonstrating that WL dimension is a real expressivity resource rather than graph identity itself.
- Coherent configurations and association schemes provide an algebraic language for finite relational color classes and intersection numbers; Sankey (2021), DOI `10.1002/jcd.21798`, treats coherent configurations through their intersection parameters.

Exact specimen inference:

- the frozen rook/Shrikhande pair remains collided under the declared 2-WL kernel;
- the same pair separates after one declared 3-WL refinement round;
- therefore the observed delta is attributable to a decoder-dimension change on an unchanged carrier pair.

Speculative HOLD:

- whether Dogram should expose a generic `k`-WL, coherent-configuration, counting-logic, pebble-game, or relational-arity operator;
- whether WL dimension should become a general “probe arity” abstraction outside graph carriers.

## Wolfram cross-check

Wolfram independently returned 16 vertices and 48 edges for both the `(4,4)` rook graph and the Shrikhande graph, and exposes Weisfeiler-Leman dimension as a graph property in `GraphData`. Its semantic interface did not return the rook/Shrikhande 2-WL versus 3-WL distinction directly, so that distinction is claimed only from the exact frozen computation above.

## Dogram boundary

- `WL DISTINGUISHABLE != NONISOMORPHISM PROOF IN GENERAL` unless the declared test actually separates the pair.
- `WL COLLISION != GRAPH IDENTITY`.
- `HIGHER DIMENSION != MORE TRUE`.
- `TUPLE COLOR != OCCURRENCE`.
- `RELATIONAL ARITY != CAUSAL ARITY`.
- `COLOR REFINEMENT != EVIDENCE ACCUMULATION`.
- `COHERENT CONFIGURATION != HISTORICAL CONFIGURATION`.
- `DECODER POWER != AUTHORITY`.

## HOLD

No `weisfeiler_leman@1`, `wl_dimension@1`, `tuple_refinement@1`, `coherent_configuration@1`, `probe_arity@1`, or graph-identity promotion.

## Strongest next frontier

The immediate next frontier is not `4-WL`. It is the logical/algebraic equivalence layer:

**WHAT EXACTLY IS PRESERVED WHEN WE REPLACE A GRAPH BY ITS k-WL QUOTIENT?**

A useful next pass should compare three views of the same bounded specimen:

1. tuple-color refinement (`k`-WL);
2. counting logic / pebble-game indistinguishability;
3. coherent-configuration intersection data.

Candidate law:

**A DECODER QUOTIENT PRESERVES EXACTLY THE QUESTIONS EXPRESSIBLE IN ITS DECLARED LANGUAGE; DO NOT PROMOTE THAT LANGUAGE TO THE CARRIER.**
