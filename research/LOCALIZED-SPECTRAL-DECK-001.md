# LOCALIZED-SPECTRAL-DECK-001

Status: bounded research specimen; no public operator promotion.

## Seal

**SAME COMPLETE LAPLACIAN SPECTRUM + SAME DEGREE MULTISET + SAME COARSE CUT/DISTANCE SUMMARIES != SAME VERTEX-DELETED LAPLACIAN DECK.**

A stronger operational form is:

**LOCALIZATION IS EXTRA INFORMATION. RECEIPT WHERE IT CAME FROM.**

## Frozen pair

Two connected simple graphs on vertices `0..6`:

- control edges: `(0,1) (0,5) (0,6) (1,2) (1,5) (2,3) (3,4) (4,5)`
- hostile edges: `(0,1) (0,5) (0,6) (1,2) (2,3) (2,4) (3,4) (4,5)`

Both have:

- degree sequence `(3,3,3,2,2,2,1)`;
- Laplacian characteristic polynomial `lambda^7 - 16 lambda^6 + 100 lambda^5 - 308 lambda^4 + 485 lambda^3 - 364 lambda^2 + 98 lambda`;
- exactly one articulation vertex;
- exactly one bridge;
- diameter `4`;
- distance histogram `{1:8, 2:9, 3:3, 4:1}`;
- exactly one triangle.

But the unlabeled multiset of Laplacian characteristic polynomials of the seven vertex-deleted subgraphs differs. The fixture freezes both complete decks.

The differing deck does not depend on retaining original vertex names: the comparison sorts the seven deletion polynomials and compares only the resulting multiset.

## Why this is new relative to nearby Dogram work

- `SHEAF-LAPLACIAN-ENERGY-001` shows fixed kernel does not fix off-kernel spectral geometry.
- `SPECTRAL-SUMMARY-COLLISION-001` (#75, reviewable) shows fixed kernel + trace does not fix spectrum.
- `LAPLACIAN-COSPECTRAL-STRUCTURE-001` (#76, reviewable) shows the complete spectrum does not fix local structure.
- `LAPLACIAN-CODEGREE-STRUCTURE-001` (#77, reviewable) additionally freezes the degree multiset while coarse cut geometry still changes.
- this specimen freezes those degree data and also articulation count, bridge count, diameter, distance histogram, and triangle count, then separates the carriers only after adding an explicitly localized deletion probe.

It therefore pressure-tests the provenance cost of localization rather than merely adding another global invariant.

## Computation

The bounded stdlib kernel computes exactly:

1. combinatorial Laplacian matrices;
2. integer characteristic-polynomial coefficients using Faddeev-LeVerrier recurrence;
3. degree sequence;
4. articulation and bridge counts by finite deletion tests;
5. all-pairs shortest-path distance histogram and diameter;
6. triangle count;
7. the sorted multiset of Laplacian characteristic polynomials after deleting each vertex.

No floating-point eigensolver is used.

The pair was discovered by finite search over non-isomorphic connected graphs on at most seven vertices using the standard Graph Atlas implementation in NetworkX as a discovery aid. NetworkX is not a Dogram dependency and is not required to replay the frozen specimen. The landed kernel independently recomputes the frozen receipts from edge lists alone.

## Literature neighborhood

- Liu, Yuan, You & Chen, *Discrete Mathematics* 341 (2018), DOI `10.1016/j.disc.2018.07.017`, explicitly separates Laplacian cospectrality from co-degree structure and studies when degree sequences are forced by the spectrum.
- Wang, Wen & Guo, *Electronic Journal of Combinatorics* (2025; preprint arXiv:2408.02488), studies generalized cospectrality of rooted graphs together with vertex-deleted subgraphs and applies that localized spectral information to graph reconstruction.

These sources establish the relevant inverse-spectral/reconstruction neighborhood. No claim is made that either contains this exact seven-vertex pair.

## Dogram boundary

Documented mathematics:
- Laplacian cospectrality is weaker than graph isomorphism in general.
- vertex-deleted spectral information is a recognized stronger/localized reconstruction probe.

Exact specimen inference:
- for this pair, the complete global Laplacian spectrum plus the frozen coarse structural summaries still does not determine the vertex-deleted Laplacian polynomial deck.
- therefore adding localization changes the information available to the inverse problem.

Speculative HOLD:
- whether a future Dogram operator should expose a generalized notion of localized spectral receipt, reconstruction strength, or probe hierarchy.

## Explicit refusals

- `LOCAL SPECTRUM != LOCAL TRUTH`.
- `VERTEX DELETION != HISTORICAL ABLATION`.
- `RECONSTRUCTION POWER != EVIDENCE STRENGTH`.
- `SAME DELETION DECK != GRAPH IDENTITY` unless separately proved for the declared class.
- `LOCALIZATION != OCCURRENCE`.
- `PROBE REFINEMENT != AUTHORITY EXPANSION`.

## HOLD

No `localized_spectrum@1`, `spectral_deck@1`, `reconstruct@1`, `vertex_probe@1`, or `inverse_graph@1` promotion.

## Strongest next frontier

Do not immediately add more localized data. First ask a quotient/provenance question:

**WHEN TWO UNLABELED PROBE FAMILIES HAVE DIFFERENT DISCRIMINATING POWER, WHAT IS THE MINIMAL EXTRA RECEIPT THAT ACCOUNTS FOR THE DELTA?**

A good next finite specimen would compare two explicitly declared probe families on the same carrier pair and measure the smallest refinement that separates them, while preserving that probe choice itself is decoder information rather than evidence or meaning.
