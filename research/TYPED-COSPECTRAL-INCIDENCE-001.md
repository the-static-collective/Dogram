# TYPED-COSPECTRAL-INCIDENCE-001

## Question
Can coarse global invariants still collide after requiring connectedness, matching loads on both incidence sides, and matching adjacency spectrum?

## Frozen specimen
Treat rows as representatives and columns as successor classes; these are distinct declared types.

A = [[1,1,0,1],[0,1,1,0],[1,0,0,0],[1,0,0,0]]

B = [[1,0,1,1],[1,1,0,0],[0,1,0,0],[1,0,0,0]]

Both connected bipartite graphs have seven edges, row-degree multiset (1,1,2,3), column-degree multiset (1,1,2,3), and exact adjacency characteristic polynomial

x^2 (x^2 - 2) (x^4 - 5 x^2 + 3).

Yet exhaustive row-permutation x column-permutation search finds no type-preserving isomorphism. If the two bipartition roles are allowed to swap, the underlying untyped graphs are isomorphic. The delta therefore lives specifically in typed incidence orientation, not in untyped graph shape or spectrum.

## Documented mathematics
Bipartite incidence can be represented by binary matrices; row and column permutations encode type-preserving relabeling. Graph spectra are generally incomplete isomorphism invariants: cospectral nonisomorphic structures exist. The present specimen is narrower because its underlying untyped graphs are isomorphic; the failure appears only after preserving the declared two-sorted roles.

## Dogram inference
If representative and successor are semantically distinct carrier types, an abstraction must not silently permit a side-switching isomorphism merely because the untyped graph and spectral receipts agree. Preserve type labels in the receipt whenever the operator contract distinguishes the two sides.

Seal: SAME CONNECTED SHAPE + SAME LOCAL LOADS + SAME SPECTRUM CAN STILL LOSE THE DIRECTION OF TYPED INCIDENCE.

## Boundary
INCIDENCE EDGE != OCCURRENCE. COSPECTRAL != SAME TYPED WIRING. UNTYPED ISOMORPHISM != TYPE-PRESERVING ISOMORPHISM. ROW/COLUMN ROLE != INTERCHANGEABLE WITHOUT DECLARATION. STRUCTURAL COLLISION != SEMANTIC OR HISTORICAL COLLISION.

## Reproduction
Run `python research/typed_cospectral_incidence_001.py` and `pytest tests/test_typed_cospectral_incidence_001.py`.
