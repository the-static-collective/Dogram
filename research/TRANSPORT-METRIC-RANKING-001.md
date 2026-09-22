# TRANSPORT-METRIC-RANKING-001

Status: bounded research specimen only. No public operator or semantic promotion.

## Question
Can two fixed coupling witnesses reverse their cost ranking when only the declared ground metric changes?

## Frozen exact specimen
Use the uniform distribution on four states. A permutation defines a deterministic coupling of the uniform law with itself.

- `pi = (0,1,3,2)`: fixes 0,1 and swaps 2,3.
- `rho = (0,2,1,3)`: fixes 0,3 and swaps 1,2.

Declare two metrics by embedding the same four named states injectively into the real line:

- `d_left`: coordinates `(0,1,7,3)`.
- `d_right`: coordinates `(0,1,3,7)`.

Both are ordinary line metrics and the kernel checks symmetry, positivity, zero diagonal, and every triangle inequality.

Exact expected costs under uniform coupling mass are:

| geometry | C(pi) | C(rho) | cheaper witness |
|---|---:|---:|---|
| d_left | 2 | 3 | pi |
| d_right | 2 | 1 | rho |

Therefore

**SAME COUPLINGS + SAME MARGINALS != SAME COST RANKING UNDER DIFFERENT DECLARED GEOMETRIES.**

The coupling receipts are held fixed. Only the declared metric changes.

## Documented mathematics
Kantorovich optimal transport minimizes an expected declared cost over couplings. Wasserstein transport specializes that cost using a ground metric. Thus an optimizer/ranking is conditional on the cost geometry supplied to the problem, not intrinsic to a coupling in isolation.

Relevant background: finite-state optimal transport explicitly depends on the ground metric; Celik, Jamneshan, Montufar, Sturmfels & Venturello, *Optimal Transport to a Variety*, arXiv:1909.11716. Lee, Li, Lin & Monod, *Tropical Optimal Transport and Wasserstein Distances*, arXiv:1911.05401, likewise explicitly specifies a ground metric before constructing Wasserstein distances.

Consensus search was quota-blocked during this pass; no Consensus-derived claim is used. Wolfram semantic search returned no direct finite specimen, so the exact arithmetic is independently frozen here rather than attributed to Wolfram.

## Dogram inference
An `optimal`, `cheaper`, or `closer` transport claim must receipt the cost/metric declaration that licensed the comparison. A scalar transport score cannot silently promote its geometry into ontology.

## Refusals
- ground metric != ontology
- lower transport cost != semantic similarity
- optimal coupling != causal mechanism
- coupling != occurrence
- metric choice != evidence
- ranking reversal != contradiction: the optimization problems differ
- mathematical optimality != authority

## Reproduce

`python research/transport_metric_ranking_001.py`

`pytest -q tests/test_transport_metric_ranking_001.py`
