# STRONGLY-REGULAR-CLIQUE-COLLISION-001

Status: bounded research specimen; no public operator promotion.

## Seal

**SAME COMPLETE LAPLACIAN SPECTRUM + SAME DEGREE MULTISET + SAME JOINT DEGREE MATRIX + SAME STRONGLY REGULAR PARAMETERS + SAME TRIANGLE COUNT != SAME 4-CLIQUE STRUCTURE.**

Operational form:

**TWO-POINT REGULARITY DOES NOT DETERMINE FOUR-POINT INCIDENCE. KEEP THE ORDER OF THE PROBE IN THE RECEIPT.**

## Frozen classical pair

The specimen uses the two non-isomorphic strongly regular graphs with parameters `(16,6,2,2)`:

- the `4 x 4` rook graph / Hamming graph `H(2,4)`;
- the Shrikhande graph.

Vertices are encoded as `0..15`; the fixture freezes the complete edge sets.

Both graphs have:

- 16 vertices;
- 48 edges;
- degree sequence `(6,6,...,6)`;
- joint degree counts `J(6,6)=48`;
- strongly regular parameters `(16,6,2,2)`;
- adjacency spectrum `6^1, 2^6, (-2)^9`;
- combinatorial-Laplacian spectrum `0^1, 4^6, 8^9`;
- 32 triangles.

But their 4-clique structure differs:

- rook graph: `8` copies of `K4`, clique number `4`;
- Shrikhande graph: `0` copies of `K4`, clique number `3`.

The rook `K4`s are the four rows and four columns of the `4 x 4` grid.

## Why this matters relative to nearby Dogram work

`JOINT-DEGREE-INCIDENCE-001` (#79, reviewable) established that complete Laplacian spectrum plus degree multiset can still discard which degree classes touch. Its strongest frontier was to freeze the joint degree matrix too and seek a finer incidence separator.

This specimen closes that frontier with a much stronger classical control. Because both graphs are 6-regular, their joint degree matrix is identical automatically. More importantly, they share the same strongly regular parameters `(v,k,lambda,mu)=(16,6,2,2)`, so every vertex has the same degree, every adjacent pair has exactly two common neighbors, and every nonadjacent pair has exactly two common neighbors in both carriers.

Even that complete two-point regularity does not determine four-point clique incidence.

The delta therefore appears only when the declared probe asks a genuinely higher-order question.

## Computation

The bounded stdlib kernel:

1. validates a connected simple graph on consecutive nonnegative integer vertices, capped at 16 vertices;
2. computes exact degree sequence and joint degree counts;
3. computes the exact integer combinatorial-Laplacian characteristic polynomial with Faddeev-LeVerrier recurrence and factors its integral roots by exact synthetic division;
4. enumerates triangles and 4-cliques exactly;
5. computes clique number by finite exhaustive subset search.

No floating point, eigensolver, graph library, random search, or public runtime operator is used in the landed calculation.

The pair was independently reconstructed during research from its standard definitions: the rook graph by row/column incidence on `Z4 x Z4`, and the Shrikhande graph as the Cayley graph on `Z4 x Z4` with connection set `±(1,0), ±(0,1), ±(1,1)`. Independent exact checks reproduced the frozen counts.

Wolfram was attempted for an independent verification route, but the connector returned an upstream 404; no Wolfram-verification claim is made.

## Literature neighborhood

Nowak, Olmez & Song, *Journal of Combinatorial Designs* 24 (2016), DOI `10.1002/jcd.21518`, explicitly note that the Hamming graph `H(2,4)` and the Shrikhande graph are non-isomorphic strongly regular graphs with the same `(16,6,2)` design data. Standard strongly regular graph theory gives that the spectrum is determined by `(v,k,lambda,mu)`; see also Evans, Goryainov & Shalaginov, *Journal of Combinatorial Designs* 33 (2025), DOI `10.1002/jcd.22001`, for the parameter-to-eigenvalue relation.

The exact `K4` counts in this fixture are independently computed from the frozen edge lists; no claim is made that the cited papers supply those exact enumerations.

## Dogram boundary

Documented mathematics:

- strongly regular parameters constrain all one-vertex degrees and all two-vertex common-neighbor counts;
- those parameters determine the adjacency spectrum and therefore, for regular graphs, the Laplacian spectrum;
- non-isomorphic strongly regular graphs with the same parameters exist.

Exact specimen inference:

- for this classical pair, complete Laplacian spectral data, the degree multiset, the joint degree matrix, all `(16,6,2,2)` two-point regularity data, and total triangle count still do not determine 4-clique incidence;
- therefore higher-order motif information is not recoverable from those frozen lower-order receipts on this pair.

Speculative HOLD:

- whether Dogram should expose any generic motif hierarchy, Weisfeiler-Leman refinement, coherent-configuration, or higher-order incidence operator.

## Explicit refusals

- `K4 != FOUR-WAY CAUSAL COALITION`.
- `CLIQUE NUMBER != AUTHORITY`.
- `STRONGLY REGULAR != HISTORICALLY REGULAR`.
- `COMMON-NEIGHBOR COUNT != EVIDENCE AGREEMENT`.
- `HIGHER-ORDER INCIDENCE != OCCURRENCE`.
- `MORE DISCRIMINATING != MORE TRUE`.
- `SPECTRAL / ASSOCIATION-SCHEME AGREEMENT != GRAPH IDENTITY`.

## HOLD

No `clique@1`, `motif@1`, `strongly_regular@1`, `association_scheme@1`, `higher_order_incidence@1`, or graph-identity promotion.

## Strongest next frontier

This specimen suggests a broader and more mathematically native frontier than accumulating ad hoc graph invariants:

**WHAT LEVEL OF RELATIONAL ARITY DOES A DECLARED RECEIPT ACTUALLY SEE?**

The strongly regular parameters capture one- and two-point incidence constraints, while the `K4` delta lives at four-point incidence. A useful next pass should investigate coherent configurations, association schemes, and Weisfeiler-Leman / finite-model-theory refinement as explicit bounded hierarchies of distinguishability.

The target law is:

**IF A DELTA APPEARS ONLY AFTER RAISING THE ARITY OF THE QUESTION, RECEIPT THAT ARITY CHANGE AS PART OF THE DECODER DELTA.**
