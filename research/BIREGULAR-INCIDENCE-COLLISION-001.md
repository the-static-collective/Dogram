# BIREGULAR-INCIDENCE-COLLISION-001

Status: bounded research specimen. Authority: none. Public operator: none.

## Question

After a collapsed representative family has already been summarized by MAY/union, MUST/intersection, representative loads, and successor loads, can the exact representative×successor wiring still differ?

Yes.

## Frozen specimen

Treat a successor family as a bipartite incidence graph between four representatives `r0..r3` and four successors `a..d`.

Left:

- r0 -> {a,b}
- r1 -> {b,c}
- r2 -> {c,d}
- r3 -> {d,a}

This incidence graph is one connected 8-cycle.

Right:

- r0 -> {a,b}
- r1 -> {a,b}
- r2 -> {c,d}
- r3 -> {c,d}

This incidence graph is two disconnected K2,2 components.

Both receipts have exactly:

- MAY/union = {a,b,c,d}
- MUST/intersection = empty
- representative degree multiset = (2,2,2,2)
- successor degree multiset = (2,2,2,2)
- edge count = 8

But their component-size receipts are `(8)` versus `(4,4)`. Connectivity is invariant under graph isomorphism, so no relabeling of representatives and successors can identify these incidence structures.

## Delta

`SAME MODAL EXTREMA + SAME LOADS ON BOTH SIDES != SAME INCIDENCE WIRING.`

The residual is not a scalar load. It lives in the incidence geometry.

## Documented mathematics

A bipartite graph is equivalently a binary incidence matrix. Prescribed degrees on the two parts are prescribed row and column sums. The literature studies whole spaces of bipartite graphs / binary matrices with fixed degree sequences rather than treating those margins as a unique realization; see Greenhill & McKay (2009), DOI 10.1002/rsa.20273, and Liebenau & Wormald (2022), DOI 10.1002/rsa.21105. Brualdi, Harary & Miller (1980), DOI 10.1002/jgt.3190040107, explicitly relates bipartite graph structure to matrix decomposability and connectivity.

Wolfram documentation independently confirms the relevant graph primitives: even cycles are bipartite, incidence matrices encode graph incidence, and graph isomorphism preserves graph structure. The exact finite arithmetic here is also directly reproducible from the fixture.

## Dogram inference

The previous modal-extrema receipt established that union and intersection do not reconstruct the member family. This specimen survives a stronger compression attack: even both partite degree multisets fail to reconstruct the wiring.

Therefore a future Dogram receipt that needs representative-to-future attribution should retain exact incidence (or a declared invariant strong enough for its question), rather than infer wiring from modal extrema and local loads.

## Refusals

- INCIDENCE EDGE != OCCURRENCE
- SUCCESSOR POSSIBILITY != HISTORICAL DESTINATION
- GRAPH CONNECTIVITY != CAUSAL CONNECTIVITY
- BIREGULARITY != EQUAL RELIABILITY
- SAME DEGREE SEQUENCE != SAME SYSTEM
- STRUCTURAL NONISOMORPHISM != SEMANTIC DIFFERENCE
- EXACT INCIDENCE != EVIDENCE OR AUTHORITY

## HOLD frontier

The next hostile target is a pair of connected bipartite incidence graphs with the same bipartite degree sequences and stronger shared invariants (for example component profile, short-cycle counts, or spectrum) but different exact wiring. Prefer the smallest computable collision and receipt the invariant that finally separates it. Do not promote graph isomorphism or Weisfeiler-Leman refinement as a public operator without an earned Dogram use-case.
