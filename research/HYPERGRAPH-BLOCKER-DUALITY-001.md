# HYPERGRAPH-BLOCKER-DUALITY-001

Status: research-only; no public operator promotion.

## Question

Given a finite declared carrier of views and a clutter of pair-distinction supports, can Dogram compute the inclusion-minimal retained-view sets sufficient to hit every declared distinction obligation, while retaining an exact receipt of what was dualized?

## Specimen

Views: `0,1,2,3`.

Distinction-support clutter:

- `{0,1}`
- `{1,2}`
- `{2,3}`

Exact enumeration of minimal transversals gives the blocker:

- `{0,2}`
- `{1,2}`
- `{1,3}`

Blocking that clutter again reconstructs the original support clutter exactly.

## Documented mathematics

For a finite hypergraph, the blocker (dual/transversal hypergraph) consists of its inclusion-minimal transversals. For a Sperner hypergraph/clutter, blocker duality is involutive: `b(b(H)) = H`. See Boros, Gurvich, Milanič & Uno (2025), *Journal of Graph Theory*, DOI 10.1002/jgt.23238, which states both definitions and the involution result while tracing them to Berge/Schrijver.

## Dogram inference

If distinction supports are declared as hyperedges, the blocker computes every inclusion-minimal retained-view set that intersects every support. This gives an exact finite receipt of alternative minimal separating-view bundles. The double-blocker check is a useful round-trip invariant: after clutter normalization, the original support obligations can be reconstructed from the family of minimal hitting sets.

This is stronger than storing only a minimum cardinality. Three different minimal retained bundles exist here, all size two, and the actual membership is part of the receipt.

## Refusals

- `TRANSVERSAL != COMPLETE HISTORY`
- `HYPEREDGE != CAUSAL GROUP`
- `MINIMAL HITTING SET != MINIMUM TRUTH`
- `BLOCKER DUALITY != EVIDENCE DUALITY`
- `DISTINCTION SUPPORT != INDEPENDENT WITNESS SET`

No occurrence, evidence, causal, semantic, or authority surface is promoted.

## Reproduce

Run:

```bash
pytest -q tests/test_hypergraph_blocker_duality.py
```

The implementation is exhaustive finite enumeration, intentionally bounded and dependency-free.

## Frontier

The next hostile question is whether two support clutters with the same transversal number and the same multiset of edge cardinalities can nevertheless have different blocker structure. If so, cardinality summaries on both the obligation and repair sides can collide while the exact dual receipt differs.
