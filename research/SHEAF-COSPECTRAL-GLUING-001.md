# SHEAF-COSPECTRAL-GLUING-001

Status: bounded research specimen; no public operator promotion.

## Question

Does degree-zero global-section dimension together with the full signed/sheaf Laplacian spectrum determine rank-one gluing data on a fixed base graph?

No, even in a six-vertex exact finite specimen.

## Frozen base graph

Vertices: `0..5`.

Edges:

`01, 04, 05, 14, 15, 24, 25, 34, 35, 45`.

Every vertex and edge stalk is rank one. Every edge transport has magnitude one. Two signings differ only in the declared ±1 transport data.

- A: negative edges `25,35`.
- B: negative edges `25,35,45`.

Their signed connection/sheaf Laplacians are formed as `L = D - A_sigma`.

## Exact collision

Both characteristic polynomials are

`x^6 - 20 x^5 + 152 x^4 - 552 x^3 + 992 x^2 - 832 x + 256`

with exact factorization

`(x-4)(x-2)(x^2-8x+8)(x^2-6x+4)`.

Thus both have determinant `256`, rank `6`, and degree-zero global-section dimension `0`.

Wolfram independently reproduced the shared characteristic polynomial, spectrum, and determinant. The shared spectrum is

`{2, 4, 4-2 sqrt(2), 4+2 sqrt(2), 3-sqrt(5), 3+sqrt(5)}`.

## Gluing-class separation

Switching preserves the sign/product around every cycle. A base-graph automorphism preserves vertex degree.

The two negative triangles in signing A have degree profile

`(2,5,5), (2,5,5)`.

The two negative triangles in signing B have degree profile

`(3,5,5), (3,5,5)`.

Therefore no switching plus base-graph automorphism can map A to B. The signings are not switching-isomorphic even though the entire signed Laplacian spectrum and `H^0` dimension agree.

## Delta

**SAME BASE GRAPH + SAME STALK DIMENSIONS + SAME LOCAL MAP MAGNITUDES + SAME H0 DIMENSION + SAME SHEAF-LAPLACIAN SPECTRUM != SAME GLUING CLASS.**

**SPECTRUM IS A QUOTIENT OF GLUING DATA, NOT A RECONSTRUCTION OF IT.**

**KEEP A CYCLE/GAUGE RECEIPT WHEN THE GLUING CLASS MATTERS.**

## Documented mathematics

Signed-graph switching acts by diagonal signature similarity and preserves signed Laplacian spectra; switching also preserves cycle signs. See Tao, Tao & Fu, *On Laplacian Equienergetic Signed Graphs* (2021), DOI `10.1155/2021/5029807`, and Yu, Qu & Brodka, *More on Spectral Analysis of Signed Networks* (2018), DOI `10.1155/2018/3467158`.

This specimen is an exact finite inference built inside that documented framework. It does not claim that the pair is a previously published smallest example.

## Refusals

- LAPLACIAN COSPECTRAL != SAME SHEAF
- SAME H0 != SAME GLUING
- SWITCHING CLASS != HISTORICAL CLASS
- CYCLE SIGN != EVIDENCE SIGN
- HOLONOMY DELTA != OCCURRENCE DELTA
- SPECTRAL COLLISION != SEMANTIC EQUIVALENCE
- GAUGE INEQUIVALENCE != CAUSAL INEQUIVALENCE
- MATHEMATICAL OBSTRUCTION != TRUTH

## HOLD

No `sheaf@1`, `signed_laplacian@1`, `switching_class@1`, `cospectral@1`, `holonomy@1`, `global_section@1`, evidence, causal, semantic, or authority operator is promoted.

## Next frontier

Pressure whether even richer low-order spectral/local receipts can collide: same Laplacian spectrum plus the same distribution of signed cycle counts by length, while switching class still differs. That would isolate exactly how much cycle-local information must be retained before a declared gluing quotient becomes faithful on a bounded family.
