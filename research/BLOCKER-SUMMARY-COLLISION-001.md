# BLOCKER-SUMMARY-COLLISION-001

Status: research-only / HOLD. No public operator is proposed.

## Question

Can two finite distinction-obligation clutters agree on the coarse summaries most likely to be retained after HYPERGRAPH-BLOCKER-DUALITY-001, while differing in the actual obligation/repair geometry?

Yes.

## Frozen specimen

Use vertex set `V={0,1,2,3}`.

Left clutter (triangle plus isolated vertex):

`H_L={{0,1},{0,2},{1,2}}`.

Right clutter (a four-vertex path):

`H_R={{0,1},{0,3},{1,2}}`.

Both have edge-size multiset `(2,2,2)`.

Exact exhaustive blocker enumeration gives

`b(H_L)={{0,1},{0,2},{1,2}}`

and

`b(H_R)={{0,1},{0,2},{1,3}}`.

Both have transversal number `2`, and both blocker edge-size multisets are `(2,2,2)`.

So the following entire coarse receipt collides:

- obligation edge-size multiset `(2,2,2)`;
- minimum repair size / transversal number `2`;
- repair edge-size multiset `(2,2,2)`.

But the exact geometry does not collide. The original degree sequences are respectively

`(2,2,2,0)` and `(2,2,1,1)`,

and the blocker degree sequences have the same respective difference. Since degree sequence is preserved by vertex relabeling, these clutters are not isomorphic. Exact double blocking also returns each original clutter separately.

## Documented mathematics

For a finite hypergraph, the blocker is the hypergraph of inclusion-minimal transversals. For a Sperner hypergraph/clutter, blocker dualization is an involution: `b(b(H))=H`. See Boros, Gurvich, Milanič & Uno, *Journal of Graph Theory* 109 (2025), DOI `10.1002/jgt.23238`. The definitions of transversal number and minimal transversal are standard; the same source emphasizes that the dual hypergraph carries the full family of minimal transversals rather than only their minimum cardinality.

The collision above is a bounded exact computation built from those definitions; it is not asserted as a new theorem.

## Dogram inference

A scalar or cardinality-profile receipt can agree on both sides of blocker duality while the actual incidence geometry differs. Therefore blocker involution does not license replacing either exact family by its size summaries when reconstruction or attribution matters.

Seal:

**SAME OBLIGATION-SIZE SUMMARY + SAME MINIMUM REPAIR SIZE + SAME REPAIR-SIZE SUMMARY != SAME OBLIGATION/REPAIR GEOMETRY.**

Secondary seal:

**COUNTING THE OBLIGATIONS AND COUNTING THE REPAIRS STILL DOES NOT TELL YOU WHICH REPAIRS PAY WHICH OBLIGATIONS.**

## Refusals

- HYPEREDGE != REAL-WORLD OBLIGATION.
- TRANSVERSAL != EVIDENCE BUNDLE.
- DEGREE SEQUENCE != COMPLETE STRUCTURE.
- BLOCKER DUALITY != CAUSAL OR EVIDENTIAL DUALITY.
- NONISOMORPHIC CLUTTERS != DIFFERENT HISTORICAL REALITIES.
- COARSE-SUMMARY COLLISION != SEMANTIC COLLISION.

## Reproduce

`pytest -q tests/test_blocker_summary_collision.py`

The kernel is dependency-free and exhaustively enumerates all candidate transversals on the four-vertex carrier.
