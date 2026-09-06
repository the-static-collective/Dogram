# JOINT-DEGREE-INCIDENCE-001

Status: bounded research specimen; no public operator promotion.

## Seal

**SAME COMPLETE LAPLACIAN SPECTRUM + SAME DEGREE MULTISET != SAME DEGREE-DEGREE INCIDENCE.**

Operational form:

**THE DEGREE LIST DOES NOT SAY WHICH DEGREES TOUCH. KEEP THE INCIDENCE RECEIPT IF THE QUESTION CONSUMES IT.**

## Frozen pair

Two connected simple graphs on vertices `0..6`:

- control edges: `(0,1) (0,5) (0,6) (1,2) (1,5) (2,3) (3,4) (4,5)`
- hostile edges: `(0,1) (0,5) (0,6) (1,2) (2,3) (2,4) (3,4) (4,5)`

Both have degree sequence:

`(3,3,3,2,2,2,1)`

Both have exact combinatorial-Laplacian characteristic polynomial:

`lambda^7 - 16 lambda^6 + 100 lambda^5 - 308 lambda^4 + 485 lambda^3 - 364 lambda^2 + 98 lambda`.

But if `J(k,l)` counts edges whose endpoint degrees are `{k,l}`, then:

control:
- `J(3,3)=3`
- `J(3,2)=2`
- `J(3,1)=1`
- `J(2,2)=2`

hostile:
- `J(3,3)=1`
- `J(3,2)=6`
- `J(3,1)=1`
- `J(2,2)=0`

Thus the complete Laplacian spectrum and complete degree multiset agree while the edge-level incidence of those degrees differs.

## Why this matters relative to nearby Dogram work

`LAPLACIAN-COSPECTRAL-STRUCTURE-001` (#76, reviewable) showed that complete Laplacian spectra can collide while degree sequences differ. `LAPLACIAN-CODEGREE-STRUCTURE-001` (#77, reviewable) closed that escape by freezing the degree multiset while cut geometry changed.

The pair later used by `LOCALIZED-SPECTRAL-DECK-001` (#78, reviewable) was initially framed as requiring an explicitly localized deletion probe to separate after several coarse invariants were frozen. This specimen finds a strictly earlier separator on that same pair: no vertex deletion and no localized spectrum are required. The ordinary unlabeled degree list agrees, but its incidence refinement does not.

This corrects the minimality story without invalidating #78's mathematical statement that its vertex-deleted spectral decks differ.

## Computation

The bounded stdlib kernel:

1. validates a connected simple graph on consecutive nonnegative integer vertices;
2. computes the exact degree sequence;
3. computes the exact combinatorial Laplacian characteristic polynomial using integer Faddeev-LeVerrier recurrence;
4. counts each undirected edge by the unordered pair of endpoint degrees.

No floating point, eigensolver, graph library, random search, or public runtime operator is used.

## Literature neighborhood

The joint degree matrix is a standard refinement used when a degree sequence alone does not retain how edges are distributed between degree classes. Cooper, Dyer & Greenhill, *Random Structures & Algorithms* 66 (2025), DOI `10.1002/rsa.70019`, explicitly describe specifying the numbers of edges between sets of vertices of given degrees, in addition to the degree sequence, via a joint degree matrix. Related network literature distinguishes degree distribution from degree-degree correlation / assortative mixing for the same reason.

No claim is made that the cited work contains this exact seven-vertex cospectral pair.

## Dogram boundary

Documented mathematics:
- a degree sequence records vertex degrees but not the complete adjacency relation;
- joint degree data records how many edges join specified degree classes;
- Laplacian cospectrality is weaker than graph isomorphism in general.

Exact specimen inference:
- for this frozen pair, complete Laplacian spectral data plus the complete degree multiset still does not determine degree-degree edge incidence;
- therefore the degree-incidence surface is information not recoverable from those two frozen receipts on this pair.

Speculative HOLD:
- whether Dogram should ever expose a generic incidence-refinement or assortativity receipt.

## Explicit refusals

- `DEGREE-DEGREE INCIDENCE != CAUSAL INTERACTION`.
- `ASSORTATIVE MIXING != SOCIAL OR HISTORICAL AFFINITY`.
- `JOINT DEGREE MATRIX != GRAPH IDENTITY`.
- `SPECTRAL COLLISION != HIDDEN EQUIVALENCE`.
- `INCIDENCE DELTA != EVIDENCE DELTA`.
- `MORE DISCRIMINATING != MORE TRUE`.

## HOLD

No `joint_degree@1`, `assortativity@1`, `degree_correlation@1`, `incidence_refinement@1`, or `graph_identity@1` promotion.

## Strongest next frontier

Freeze the complete Laplacian spectrum, degree multiset, **and joint degree matrix**, then ask for the smallest exact pair whose local incidence geometry still differs.

Candidate probes include triangle participation by degree class, two-step degree transition counts, or another permutation-blind finite invariant. The target is not to reconstruct the graph by accumulation; it is to locate the next precise information boundary and receipt which question created the delta.
