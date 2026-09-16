# PATH-TREE-TEST-LANGUAGE-001

Status: research-only; no public operator promotion.

## Question

Can the same two finite graph carriers collide under every path homomorphism test and still separate as soon as the source-language admits branching?

This slice keeps the targets fixed and changes only the admissible source/test class.

## Frozen carriers

Left target `G = C6 + K1`:

- 7 vertices;
- degree vector `(2,2,2,2,2,2,0)`.

Right target `H` is the subdivided claw with three arms of length two:

- edges `(0,1),(1,2),(0,3),(3,6),(0,4),(4,5)`;
- degree vector `(3,2,1,2,2,1,1)`.

The targets are non-isomorphic before any test language is chosen.

## Exact all-path collision

For any simple target with adjacency matrix `A`, the number of homomorphisms from the path with `t+1` vertices is the total number of length-`t` walks:

`hom(P_{t+1}, G) = 1^T A^t 1`.

Let `d=A1` be the degree vector. For both frozen targets, exact integer arithmetic verifies

`A d = 2 d`.

Therefore, for every `t>=1`,

`A^t 1 = 2^(t-1) d`.

Both targets have 7 vertices and degree sum 12, so their complete path receipts agree for every length:

- `t=0`: 7;
- `t>=1`: `12 * 2^(t-1)`.

The fixture freezes the first nine totals:

`7,12,24,48,96,192,384,768,1536`.

This is an exact recurrence certificate, not extrapolation from a finite prefix.

## Smallest branching witness

The first tree source that is not a path is the four-vertex claw `K1,3`.

For any target graph `Q`, choosing the image of the claw center at vertex `v` leaves `deg(v)` independent choices for each of the three leaves, so

`hom(K1,3,Q) = sum_v deg(v)^3`.

For the left target:

`6 * 2^3 + 0^3 = 48`.

For the right target:

`3^3 + 3 * 2^3 + 3 * 1^3 = 54`.

Hence

`hom(K1,3,G)=48 != 54=hom(K1,3,H)`.

The executable kernel also brute-force enumerates all `7^4=2401` vertex assignments for the claw and reproduces both counts independently of the degree-cube formula.

Wolfram Language independently returned the two degree vectors, the sums of degree cubes `48` and `54`, and `IsomorphicGraphQ -> False`.

## Delta

Held fixed:

- both target graph carriers;
- ordinary graph homomorphism semantics;
- exact integer arithmetic.

Changed:

- source/test language: paths only -> trees with branching.

Result:

- every path test collides;
- the minimal branching tree separates by exact delta `54-48=6`.

## Candidate seals

**SAME ALL-PATH RECEIPTS != SAME TREE RECEIPTS.**

**THE FIRST BRANCH CAN REVEAL A DELTA THAT EVERY LINEAR WALK MISSES.**

**THE TEST LANGUAGE IS PART OF THE RECEIPT.**

## Documented mathematics

Dell, Grohe, and Rattan, *Lovasz Meets Weisfeiler and Leman*, ICALP 2018, DOI `10.4230/LIPIcs.ICALP.2018.40`, prove the general hierarchy relevant here:

- equality of all tree-homomorphism counts is equivalent to indistinguishability by color refinement and to fractional isomorphism;
- dropping nonnegativity from the corresponding affine linear system yields equality of all path/walk counts;
- the framework extends to homomorphism counts from bounded-treewidth graphs and higher-dimensional Weisfeiler-Leman / Sherali-Adams levels.

Grohe, Rattan, and Seppelt, *Homomorphism Tensors and Linear Equations*, ICALP 2022, DOI `10.4230/LIPIcs.ICALP.2022.70`, develop the broader algebraic framework in which restricted source classes induce distinct graph-equivalence relations.

The exact `48 != 54` claw witness and the recurrence certificate are finite calculations performed in this repository; they do not rely on the literature theorem for correctness.

## Relation to nearby Dogram work

This slice links the open graph-relaxation research without importing it:

- `SIGNED-AFFINE-INTERTWINER-001` isolates all-path equivalence under a signed affine witness;
- `FRACTIONAL-ISOMORPHISM-COUPLING-001` isolates the stronger nonnegative coupling class;
- `WL-ARITY-SEPARATION-001` changes tuple dimension.

The present slice changes neither coefficient domain nor tuple dimension. It changes only which source structures are allowed to ask questions of the target.

## Dogram refusals

- PATH-HOM COLLISION != GRAPH IDENTITY.
- TREE-HOM DELTA != OCCURRENCE DELTA.
- BRANCHING TEST != CAUSAL BRANCH.
- HOMOMORPHISM COUNT != EVIDENCE COUNT.
- STRONGER TEST LANGUAGE != MORE TRUE.
- COLOR-REFINEMENT POWER != AUTHORITY.
- SOURCE TREE != HISTORY TREE.
- TEST-LANGUAGE SEPARATION != SEMANTIC SEPARATION.

## HOLD

Do not promote:

- `hom_test_language@1`
- `tree_hom@1`
- `path_hom@1`
- `branching_probe@1`
- `hom_indistinguishable@1`
- any graph identity, evidence, causal, or authority operator.

## Strongest next frontier

The useful continuation is no longer merely `paths -> trees`. The next pressure is whether Dogram can freeze a three-level source-language ladder on fixed targets:

`paths -> trees (treewidth 1) -> treewidth 2 sources`,

with an explicit pair that survives every tree test but is separated by one minimal cyclic/treewidth-2 source. That would make the bounded-treewidth / Weisfeiler-Leman hierarchy executable one rung at a time without confusing decoder expressivity with carrier identity.
