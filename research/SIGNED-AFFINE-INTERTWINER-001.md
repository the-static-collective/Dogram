# SIGNED-AFFINE-INTERTWINER-001

Status: research-only; no public operator promotion.

## Question

What changes if Dogram keeps the graph-intertwining equations fixed but changes only the admissible coefficient domain of the witness matrix?

We compare three witness classes for adjacency matrices `A` and `B`:

1. permutation matrices: graph isomorphism;
2. nonnegative real matrices with row/column sums 1: fractional isomorphism;
3. arbitrary real matrices with row/column sums 1: signed affine intertwiners.

The equations are

`A X = X B`, `X 1 = 1`, and `1^T X = 1^T`.

## Frozen carrier

Left graph `G = C6 + K1`:

- a 6-cycle on vertices 0..5;
- isolated vertex 6;
- degree vector `(2,2,2,2,2,2,0)`;
- two connected components.

Right graph `H` is the 7-vertex subdivided claw with three arms of length two:

- edges `(0,1),(1,2),(0,3),(3,6),(0,4),(4,5)`;
- degree vector `(3,2,1,2,2,1,1)`;
- one connected component.

Thus the graphs are not isomorphic before any relaxed witness is considered.

This carrier is the same shape exhibited by Dell, Grohe, and Rattan as two fractionally non-isomorphic graphs with identical path-homomorphism counts; see *Lovász Meets Weisfeiler and Leman*, ICALP 2018, DOI `10.4230/LIPIcs.ICALP.2018.40`, Figure 1 and Theorem 2.

## Exact signed witness

The frozen rational witness is

```
1/2   0    1/2   0    0    0    0
0     0    0     1/2  1/2  0    0
1/2   0   -1/2   0    0    1/2  1/2
0     0    0     1/2  1/2  0    0
1/2   0    1/2   0    0    0    0
0     1    0     0    0    0    0
-1/2  0    1/2   0    0    1/2  1/2
```

Exact `Fraction` arithmetic verifies:

- every row sum is 1;
- every column sum is 1;
- `A X = X B`;
- two entries are negative.

Therefore the same affine intertwining equations are feasible over `R`, but this particular witness is not doubly stochastic.

## Why no nonnegative witness can exist

From `A X = X B` and `X 1 = 1`,

`d_G = A 1 = A X 1 = X B 1 = X d_H`.

Look at the isolated vertex of `G`. Its degree is zero. If the corresponding row of `X` were nonnegative and summed to one, then `(X d_H)_i` would be a convex combination of the degrees of `H`.

Every vertex of `H` has positive degree, with minimum degree 1. Hence every such convex combination is at least 1, contradicting the required value 0.

So **no nonnegative row-stochastic adjacency intertwiner exists**, and therefore no fractional isomorphism exists. A negative coefficient is not an implementation accident; it is mathematically required by this carrier under the affine equations.

## Path/walk collision

The executable fixture freezes total walk counts through length 8:

`7, 12, 24, 48, 96, 192, 384, 768, 1536`.

The stronger all-length statement is documented mathematics: Dell, Grohe, and Rattan prove that two graphs have equal homomorphism counts from every path iff the affine system above has an arbitrary real solution. Since path homomorphism counts equal total walk counts, this signed witness places the pair in that equivalence class.

The same paper proves the stricter distinction: requiring the real solution to be nonnegative gives fractional isomorphism / color-refinement equivalence, which this pair does not satisfy.

## Delta

Held fixed:

- the two graph carriers;
- adjacency-intertwining equation `AX=XB`;
- row sums = 1;
- column sums = 1.

Changed:

- admissible coefficient domain / cone.

Result:

- arbitrary real coefficients: FEASIBLE;
- nonnegative real coefficients: REFUSES;
- permutation witness: REFUSES already from component/degree structure.

## Candidate seals

**SAME EQUATIONS + DIFFERENT COEFFICIENT DOMAIN = DIFFERENT NOTION OF SAMENESS. RECEIPT THE DOMAIN.**

**A SIGNED AFFINE INTERTWINER CAN PRESERVE EVERY PATH COUNT WHILE FAILING FRACTIONAL ISOMORPHISM.**

**NONNEGATIVITY IS MATHEMATICAL STRUCTURE, NOT DECORATION.**

## Dogram refusals

- SIGNED COEFFICIENT != NEGATIVE EVIDENCE.
- AFFINE INTERTWINER != OCCURRENCE CORRESPONDENCE.
- WALK-COUNT AGREEMENT != GRAPH IDENTITY.
- PATH-HOMOMORPHISM AGREEMENT != COMMON HISTORY.
- NONNEGATIVITY FAILURE != FALSEHOOD.
- FRACTIONAL ISOMORPHISM FAILURE != CAUSAL DIFFERENCE.
- REAL-LINEAR FEASIBILITY != AUTHORITY.
- COEFFICIENT CANCELLATION != PHYSICAL CANCELLATION.

## Literature

Primary source:

- Holger Dell, Martin Grohe, Gaurav Rattan, *Lovász Meets Weisfeiler and Leman*, ICALP 2018, DOI `10.4230/LIPIcs.ICALP.2018.40`. The paper defines the affine system `F_iso(G,H)`, identifies nonnegative real solutions with fractional isomorphism, and proves that dropping nonnegativity makes feasibility equivalent to equality of all path-homomorphism / total-walk counts. Figure 1 is this exact seven-vertex separation shape.

Supporting matrix boundary:

- Standard definitions of doubly stochastic matrices require entrywise nonnegativity in addition to row and column sums of one. The distinction matters here because the frozen affine witness satisfies the sum constraints but necessarily uses negative entries.

## HOLD

Do not promote:

- `signed_intertwiner@1`
- `fractional_isomorphism@1`
- `walk_equivalence@1`
- `affine_graph_match@1`
- any graph identity or semantic equivalence operator.

## Strongest next frontier

The next useful move is not another coefficient relaxation. It is to ask how the **test-language hierarchy** changes when moving from paths to trees to bounded-treewidth source graphs:

`paths -> trees -> treewidth-k`.

This would put the signed affine witness, fractional isomorphism/color refinement, and higher WL/Sherali-Adams receipts into one explicit expressive hierarchy while preserving the rule that decoder strength is not evidence strength.
