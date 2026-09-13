# FINITE-GAUGE-HOLONOMY-001

Status: research kernel only. No public Dogram operator.

## Question

Can Dogram distinguish a raw loop-transport delta from a delta that survives an explicitly declared local gauge freedom?

This slice uses one oriented triangle and the finite non-Abelian permutation group S3. It does not model a physical gauge field. The group, graph, edge transports, cycle, composition convention, and vertex-gauge rule are all declared inputs to the mathematical specimen.

## Contract

DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.

In particular:

- HOLONOMY != OCCURRENCE.
- GAUGE EQUIVALENCE != PHYSICAL EQUIVALENCE.
- CONJUGACY CLASS != CAUSAL CLASS.
- NONTRIVIAL LOOP PRODUCT != PHYSICAL CURVATURE.
- A MATHEMATICAL QUOTIENT ONLY FORGETS THE FREEDOM THAT WAS EXPLICITLY DECLARED.

## Representation

A permutation is stored as a 1-indexed image tuple. For example:

- identity: `(1,2,3)`
- transposition `(12)`: `(2,1,3)`
- 3-cycle `(123)`: `(2,3,1)`

Dogram freezes the product convention

`compose(left, right) = left after right = left o right`.

For an oriented edge `u -> v` with transport `g_uv` and declared vertex gauges `h_u`, the transformed edge is

`g'_uv = h_u g_uv h_v^-1`.

For the declared oriented triangle `0 -> 1 -> 2 -> 0`, the based loop product is

`H = g_01 g_12 g_20`.

The edge-gauge factors telescope, so

`H' = h_0 H h_0^-1`.

Therefore the raw based holonomy may change, while its conjugacy orbit under the declared group is invariant.

## Frozen exact specimen

Base connection:

- `g_01 = (12)`
- `g_12 = e`
- `g_20 = e`

so

`H = (12)`.

Declared vertex gauges:

- `h_0 = (123)`
- `h_1 = (12)`
- `h_2 = (23)`

The transformed edge transports are exactly:

- `g'_01 = (123)`
- `g'_12 = (123)`
- `g'_20 = (12)`

and the new based loop product is

`H' = (23)`.

Thus

`H != H'`

but both are transpositions, and exact group closure from generators `(12)` and `(123)` produces all six elements of S3. The conjugacy orbit of a transposition contains exactly three elements:

`{(12), (13), (23)}`.

Therefore the raw loop receipt changed while the declared gauge quotient did not.

## Hostile control

Hold fixed:

- the triangle,
- the base vertex,
- the group S3,
- the composition convention,
- two identity edge transports.

Change only `g_01` from the transposition `(12)` to the 3-cycle `(123)`.

The hostile loop product is then

`H_hostile = (123)`.

Its conjugacy orbit in S3 contains the two 3-cycles

`{(123), (132)}`.

It is disjoint from the transposition orbit. Therefore this delta survives the declared vertex-gauge quotient.

## Exact delta

The specimen establishes two distinct comparison levels:

1. raw based holonomy equality;
2. equality modulo the declared conjugation action.

The durable relation is:

`SAME DECLARED GAUGE CLASS != SAME RAW EDGE LABELS OR SAME RAW BASED HOLONOMY.`

The hostile complement is:

`DIFFERENT CONJUGACY ORBIT -> DELTA SURVIVES THIS DECLARED GAUGE QUOTIENT.`

The implication is deliberately one-way and specimen-scoped. For this single-cycle S3 graph, the conjugacy orbit is the relevant quotient witness. This slice does not claim a complete classifier for arbitrary graphs, arbitrary gauge groups, higher cells, bundles, or continuum connections.

## Why this is new relative to nearby Dogram work

`HOME-MOTION-COMMUTATOR-001` and `HEISENBERG-BILINEAR-ORDER-RESIDUE-001` ask whether composition order leaves an exact residue.

This slice asks a different question after a residue or transport has been calculated:

> Which raw differences disappear under a freedom that the representation explicitly licenses us to quotient?

That places finite gauge transformation next to, but not inside, the earlier reorientation work:

`RAW DELTA -> DECLARED FREEDOM -> QUOTIENTED DELTA`.

The mathematical names differ because the group actions differ.

## Documented mathematics

Gauge theory on graphs treats edge data as connection/transport data and vertex actions as local gauge transformations; holonomy along graph paths supplies gauge-sensitive and gauge-invariant observables after the appropriate quotient. Meusburger and Wise develop graph holonomy and gauge-invariant observables in the broader ribbon-Hopf setting, with face holonomies supplying curvature-like observables. Majid and Simao explicitly study finite-group gauge theory on connected graphs and the moduli space of regular connections modulo gauge transformations.

References:

1. C. Meusburger and D. Wise, "Hopf algebra gauge theory on a ribbon graph," Reviews in Mathematical Physics (2015). Consensus record: https://consensus.app/papers/hopf-algebra-gauge-theory-on-a-ribbon-graph-meusburger-wise/790553e1f3f45b1fab39edd8cf2f54cb/
2. Shahn Majid and Francisco Simao, "Finite group gauge theory on graphs and gravity-like modes," Nuclear Physics B (2025). Consensus record: https://consensus.app/papers/finite-group-gauge-theory-on-graphs-and-gravitylike-modes-majid-simao/3474b1f2e5d35683b3f7dcc034306161/

These references support the mathematical neighborhood. The exact S3 triangle fixture and its Dogram boundary are this repository's research construction.

## Independent computation

Wolfram Language was used as an independent permutation-algebra check. Its `PermutationProduct` argument ordering differs from the convention frozen in this kernel. The discrepancy was therefore treated as a representation-convention pressure test, not as a contradiction. The landed fixture is verified against Dogram's declared `left after right` convention.

## Implementation boundary

`dogram/finite_gauge_holonomy.py` is an internal research kernel only. It provides:

- exact tuple-permutation composition and inverse;
- closure of a finite permutation group from declared generators;
- conjugacy-orbit enumeration;
- vertex-gauge transformation of directed edge transports;
- exact based holonomy around a declared directed cycle.

It does not add public dispatch, schemas, semantic interpretation, evidence status, physical units, curvature tensors, bundles, Wilson actions, or gauge-theory ontology.

Explicit HOLD:

- `holonomy@1`
- `gauge@1`
- `connection@1`
- `curvature@1`
- `wilson_loop@1`
- arbitrary-graph gauge-orbit classification
- higher gauge / 2-holonomy

## Verification

TDD RED was observed before the research module existed as `ModuleNotFoundError: dogram.finite_gauge_holonomy`.

Fresh local fixture-bound verification after the minimal kernel:

- generated group order: 6;
- base holonomy: `(12)`;
- gauge-transformed holonomy: `(23)`;
- transformed holonomy lies in the base conjugacy orbit;
- hostile holonomy: `(123)`;
- hostile holonomy does not lie in the transposition conjugacy orbit;
- transposition orbit size: 3;
- 3-cycle orbit size: 2;
- focused tests: 3/3 pass;
- `py_compile` passes for module and focused test.

No full-repository or remote-CI claim is made until the exact PR head is checked.

## Candidate seals

> RAW HOLONOMY CAN MOVE WHILE THE DECLARED GAUGE CLASS STAYS PUT.

> QUOTIENT ONLY THE FRAME FREEDOM YOU ACTUALLY DECLARED.

> A LOOP RESIDUE IS A RECEIPT OF THE REPRESENTATION, NOT A VERDICT ABOUT THE WORLD.

## Strongest next frontier

The next mathematically earned question is not a larger gauge runtime. It is the relation among:

`LOCAL EDGE TRANSPORT -> LOOP HOLONOMY -> GAUGE QUOTIENT -> FACE/2-CELL CONSISTENCY`.

A bounded next specimen could use two adjacent faces sharing an edge and test whether local face-holonomy receipts obey a discrete Bianchi-type closure constraint. That would create a genuine bridge toward cohomology / higher gauge structure while preserving the refusal:

`DISCRETE BIANCHI CONSISTENCY != PHYSICAL FIELD EQUATION`.
