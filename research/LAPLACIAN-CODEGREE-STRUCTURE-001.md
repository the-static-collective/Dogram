# LAPLACIAN-CODEGREE-STRUCTURE-001

## Question

Does the complete combinatorial-Laplacian spectrum together with the complete degree multiset determine the graph's cut geometry?

## Frozen specimen

Two connected simple graphs on seven vertices:

- A: `(0,1) (0,4) (1,2) (1,4) (2,3) (3,6) (4,5)`
- B: `(0,1) (0,3) (0,4) (1,2) (2,5) (2,6) (5,6)`

Both have degree sequence

`(3,3,2,2,2,1,1)`

and exact Laplacian characteristic polynomial

`lambda^7 - 14 lambda^6 + 75 lambda^5 - 192 lambda^4 + 239 lambda^3 - 130 lambda^2 + 21 lambda`.

Therefore they have the same complete Laplacian eigenvalue multiset with multiplicity and the same degree multiset.

Their cut geometry nevertheless differs:

- A articulation vertices: `(1,2,3,4)`; diameter `5`.
- B articulation vertices: `(0,1,2)`; diameter `4`.

The differing articulation counts alone certify non-isomorphism.

## Exact receipt

The research kernel uses only standard-library integer arithmetic. Laplacian characteristic coefficients are computed by the Faddeev-LeVerrier trace recurrence; articulation vertices and diameter are obtained by exhaustive finite graph traversal.

Core seal:

`SAME COMPLETE LAPLACIAN SPECTRUM + SAME DEGREE MULTISET != SAME CUT GEOMETRY.`

## Literature neighborhood

The spectral-graph literature distinguishes Laplacian cospectrality from determination by the Laplacian spectrum. Liu, Yuan, You & Chen, *Discrete Mathematics* 341 (2018), DOI `10.1016/j.disc.2018.07.017`, study when Laplacian-cospectral graphs are forced to share degree sequences; that question is strictly weaker than graph isomorphism. Li & Sun, *Journal of Combinatorial Designs* 28 (2020), DOI `10.1002/jcd.21743`, record the standard relation between graph diameter and the number of distinct Laplacian eigenvalues, illustrating that spectra constrain diameter without generally encoding the full carrier.

No claim is made that these papers contain this exact seven-vertex pair. The specimen was located independently and frozen only after exact verification.

## Dogram inference

A decoder that retains the complete Laplacian eigenvalue multiset and degree multiset has still projected away incidence information required to reconstruct cut structure.

This licenses only a receipt-level statement about information loss under the declared projection.

## Refusals

- `LAPLACIAN COSPECTRAL != ISOMORPHIC`.
- `SAME DEGREE MULTISET != SAME INCIDENCE`.
- `ARTICULATION VERTEX != CAUSAL BOTTLENECK`.
- `DIAMETER != HISTORICAL DISTANCE`.
- `CUT GEOMETRY != EVIDENCE`.
- `SPECTRAL AGREEMENT != SEMANTIC AGREEMENT`.
- `ALGEBRAIC INDISTINGUISHABILITY UNDER DECLARED PROBES != TRUTH`.

## HOLD

No `codegree@1`, `articulation@1`, `diameter@1`, `inverse_spectrum@1`, or `structural_identity@1` promotion.

## Frontier

The next useful pressure is not another global invariant. Hold complete Laplacian spectrum, degree multiset, and coarse cut summaries fixed, then test whether a localized spectral measure or vertex-deleted spectral deck can distinguish the carrier. Any such move must receipt the additional localization/basis information it consumes rather than smuggling labels back into the inverse problem.
