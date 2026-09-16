# FRACTIONAL-ISOMORPHISM-COUPLING-001

Status: bounded research specimen; no public operator promotion.

## Seal

**FRACTIONAL ISOMORPHISM != GRAPH ISOMORPHISM.**

Operational form:

**A DOUBLY-STOCHASTIC INTERTWINER IS A RELAXED COUPLING WITNESS, NOT A VERTEX BIJECTION. KEEP THE WITNESS CLASS IN THE RECEIPT.**

## Frozen carrier pair

- `C6`, the 6-cycle;
- `2K3`, the disjoint union of two triangles.

Both graphs have 6 vertices, 6 edges, and constant degree 2. They are not isomorphic because `C6` has one connected component while `2K3` has two. Their triangle counts also differ: 0 versus 2.

Wolfram independently returns 6 vertices / 6 edges / 1 component for `C6`, and 6 vertices / 6 edges / 2 components for `2K3`.

## Exact fractional witness

Let `A` and `B` be the adjacency matrices of `C6` and `2K3`. Let

`X = J/6`,

where `J` is the `6 x 6` all-ones matrix.

`X` is doubly stochastic: every entry is nonnegative and every row and column sums to 1.

Because both graphs are 2-regular,

`A J = 2 J` and `J B = 2 J`.

Therefore

`A X = A(J/6) = (2/6)J = (J/6)B = X B`.

Thus the pair is fractionally isomorphic under the standard matrix relaxation even though the carriers are not graph-isomorphic.

The kernel replays this with exact `Fraction` arithmetic and receipts the surviving structural residuals:

- component delta: `2 - 1 = 1`;
- triangle delta: `2 - 0 = 2`.

## Why this matters after WL-ARITY-SEPARATION-001

The prior open WL slice says decoder dimension is part of the receipt. This slice exposes an orthogonal axis: **witness class is part of the receipt**.

Ordinary graph isomorphism asks for a permutation matrix `P` satisfying `AP = PB`. Fractional isomorphism relaxes `P` to an arbitrary doubly stochastic matrix `X`. The relaxed feasible set is convex and can contain witnesses that are mixtures rather than bijections.

For this frozen pair, the uniform coupling `J/6` erases every vertex-specific correspondence while retaining only the shared regular degree through the intertwining equation.

That is a Dogram-grade quotient warning: a successful witness inside a relaxed category certifies exactly the relaxed relation and nothing stronger.

## Documented mathematics

- Fractional graph isomorphism is defined by a doubly stochastic matrix `X` satisfying the adjacency intertwining equation. Permutation-matrix witnesses recover ordinary isomorphism.
- Tinhofer's results, and later work by Ramana, Scheinerman, and Ullman, identify fractional isomorphism with indistinguishability by color refinement / existence of a common coarsest equitable partition.
- Dell, Grohe, and Rattan connect the same equivalence to equality of all tree homomorphism counts and place it in the Weisfeiler-Leman hierarchy. See `Lovasz Meets Weisfeiler and Leman`, ICALP 2018, DOI `10.4230/LIPIcs.ICALP.2018.40`.
- Atserias and Maneva relate fractional-isomorphism LP relaxations, Sherali-Adams levels, Weisfeiler-Leman refinement, and bounded-variable counting logic. DOI `10.1137/120867834`.

Scholar Gateway returned supporting literature on equitable partitions and degree refinement; the direct fractional-isomorphism equivalences were cross-checked against the ICALP 2018 paper and later hierarchy literature.

## Exact specimen inference

From the frozen matrices only:

- the pair admits the exact uniform doubly stochastic intertwiner `J/6`;
- the pair has different component counts and triangle counts;
- therefore the relaxed witness does not imply graph identity, connectivity agreement, triangle agreement, or a hidden bijection.

## Speculative HOLD

Do not yet promote:

- a generic fractional-isomorphism operator;
- a generic transport/coupling abstraction;
- a claim that every useful Dogram quotient should be formulated as a convex relaxation;
- any semantic interpretation of coupling mass.

A future slice may compare permutation, doubly stochastic, signed-real, and higher Sherali-Adams witness classes on one frozen pair family.

## Dogram boundary

- `FRACTIONAL ISOMORPHISM != GRAPH ISOMORPHISM`.
- `DOUBLY STOCHASTIC != BIJECTIVE`.
- `COUPLING MASS != OCCURRENCE MASS`.
- `LP FEASIBILITY != EVIDENCE`.
- `COMMON EQUITABLE PARTITION != COMMON HISTORY`.
- `COLOR-REFINEMENT COLLISION != CARRIER IDENTITY`.
- `TREE-HOM COUNT AGREEMENT != HISTORICAL AGREEMENT`.
- `RELAXED WITNESS != AUTHORITY`.
- `CONVEX COMBINATION != CAUSAL MIXTURE`.

## Promotion boundary

No `fractional_isomorphism@1`, `doubly_stochastic_witness@1`, `transport_coupling@1`, `equitable_partition@1`, or LP-relaxation operator is promoted by this specimen.
