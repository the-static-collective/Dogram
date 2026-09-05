# LAPLACIAN-COSPECTRAL-STRUCTURE-001

Status: bounded research specimen; no public operator promotion.

## Question

Does the complete combinatorial-Laplacian eigenvalue multiset determine the underlying finite graph structure?

## Frozen specimen

Two connected simple graphs on six labeled vertices:

- Graph A edges: `(0,2) (1,2) (1,3) (1,4) (2,5) (3,5) (4,5)`.
- Graph B edges: `(0,2) (0,5) (1,3) (1,4) (2,3) (3,4) (3,5)`.

Exact Newton-identity evaluation of `det(lambda I - L)` gives the same polynomial for both:

`lambda^6 - 14 lambda^5 + 73 lambda^4 - 176 lambda^3 + 192 lambda^2 - 72 lambda`.

Therefore the complete Laplacian eigenvalue multisets agree, including multiplicities.

The structural receipts do not agree:

- Graph A degree sequence: `(3,3,3,2,2,1)`; triangles: `0`.
- Graph B degree sequence: `(4,2,2,2,2,2)`; triangles: `1`.

Both are connected, both have seven edges, and the Matrix-Tree spectrum receipt gives twelve spanning trees for each.

## Delta

`SAME COMPLETE LAPLACIAN SPECTRUM != SAME GRAPH STRUCTURE.`

The spectrum preserves some exact invariants in this specimen (vertex count, edge count via trace, connectedness via zero multiplicity, spanning-tree count via the Matrix-Tree theorem) while failing to preserve the degree sequence or triangle count.

This is stronger than `SPECTRAL-SUMMARY-COLLISION-001`: no low-order spectral statistic was discarded. The entire Laplacian characteristic polynomial collides.

## Documented mathematics

Laplacian cospectrality is standard spectral graph theory: two graphs are L-cospectral when their Laplacian eigenvalue multisets agree. The broader literature distinguishes graphs determined by their Laplacian spectra from graphs with non-isomorphic L-cospectral mates. Relevant background includes:

- Liu, Yuan, You & Chen, *Discrete Mathematics* 341 (2018), `Which cospectral graphs have same degree sequences`, DOI `10.1016/j.disc.2018.07.017`.
- Lorenzen, *Special Matrices* 10 (2021), `Cospectral constructions for several graph matrices using cousin vertices`, DOI `10.1515/spma-2020-0143`.
- Yu, Wang, Zhou & Zhang, *Journal of Applied Mathematics* (2014), `Laplacian Spectral Characterization of Some Unicyclic Graphs`, DOI `10.1155/2014/268464`.

No claim is made that those papers contain this exact six-vertex pair. The pair was independently located and exactly verified for this bounded Dogram specimen.

## Dogram inference

A complete eigenvalue multiset is still a projection. If a downstream decoder needs local combinatorial structure, equality of spectra cannot silently supply it.

Candidate seal:

`EVEN THE WHOLE SPECTRUM MAY BE A PROJECTION.`

## Explicit refusals

- `LAPLACIAN COSPECTRAL != ISOMORPHIC`.
- `SAME SPECTRUM != SAME LOCAL STRUCTURE`.
- `SPECTRAL EQUIVALENCE != HISTORICAL EQUIVALENCE`.
- `TRIANGLE COUNT != CAUSAL MOTIF`.
- `DEGREE SEQUENCE != AUTHORITY`.
- `SPECTRAL COLLISION != EVIDENCE OF HIDDEN IDENTITY`.
- `ALGEBRAIC INDISTINGUISHABILITY UNDER ONE PROBE != TRUTH`.

## Implementation boundary

The research kernel is stdlib-only and bounded to exact finite simple-graph receipts. It computes:

- combinatorial Laplacian;
- exact characteristic coefficients via Newton identities;
- connectedness;
- degree sequence;
- triangle count;
- spectrum-derived spanning-tree count.

No `spectrum@1`, `cospectral@1`, `graph_isomorphism@1`, `spectral_identity@1`, or `inverse_spectrum@1` is promoted.

## Verification

The frozen arithmetic was independently reproduced exactly outside the repository implementation before landing:

- shared characteristic coefficients: `(1,-14,73,-176,192,-72,0)`;
- degree sequences differ as frozen;
- triangle counts are `0` and `1`;
- shared spectrum-derived spanning-tree count is `12`.

Wolfram was attempted as an independent verifier, but its connector returned an upstream 404, so no Wolfram-verification claim is made.

## Next frontier

The next useful question is not another graph pair with the same eigenvalues. It is whether **eigenvectors / spectral projectors together with eigenvalues** still admit a bounded representation ambiguity after labels or basis choices are quotiented. That should be pressure-tested only if a finite exact specimen distinguishes what the eigenvalue-only projection lost without smuggling vertex labels back into the answer.
