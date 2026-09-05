# LOCAL-GLOBAL-CYCLE-COHOMOLOGY-001

Status: bounded research specimen; no public Dogram operator.

## Question

Can every declared local constraint be individually satisfiable while the complete finite system has no global assignment?

Yes. On the oriented 3-cycle `0 -> 1 -> 2 -> 0` over `GF(2)`, give each edge a parity bit `b_uv` and ask for vertex bits satisfying

`x_v - x_u = b_uv (mod 2)`.

Every single edge equation has exactly two local solutions. A global assignment exists iff

`b_01 + b_12 + b_20 = 0 (mod 2)`.

This is the coboundary criterion for the edge 1-cochain on `C3`. Since `H^1(C3; GF(2)) ~= GF(2)`, the cycle parity is the exact class coordinate in this frozen specimen.

## Frozen control

`b = (0,0,0)`.

Cycle parity is `0`. The two global assignments are `(0,0,0)` and `(1,1,1)`.

## Frozen hostile specimen

`b = (0,0,1)`.

Each edge constraint remains individually satisfiable, but the cycle parity is `1`. Exhaustive enumeration of all eight vertex assignments finds no global solution. The edge cochain is not a coboundary and represents the nonzero class in `H^1(C3; GF(2))`.

Across all eight possible edge-bit tables, exactly four have even cycle parity and admit global assignments; exactly four have odd cycle parity and do not.

## Durable distinction

`EVERY LOCAL CONSTRAINT CAN PASS WHILE THE GLOBAL GLUING FAILS.`

`LOCAL SATISFIABLE != GLOBALLY GLUEABLE.`

`KEEP THE CYCLE RESIDUE; DO NOT INVENT ITS MEANING.`

## Dogram contract pressure

- DO THE MATH: exhaustive finite GF(2) enumeration and exact cycle parity.
- SHOW THE DELTA: control parity `0` / hostile parity `1`; two global solutions / none.
- KEEP THE RECEIPT: edge ordering, coefficient field, all local satisfiability counts, global solutions, and class bit are returned.
- DO NOT DECIDE WHAT IT MEANS: no causal, evidentiary, historical, semantic, or physical interpretation is promoted.

Explicit refusals:

- `LOCAL SATISFIABLE != GLOBAL OCCURRENCE`.
- `NONZERO H1 CLASS != CAUSAL CONFLICT`.
- `COHOMOLOGY OBSTRUCTION != HISTORICAL CONTRADICTION`.
- `GLOBAL SECTION != TRUTH`.
- `NO GLOBAL SECTION != PROOF THAT ANY LOCAL REPORT IS FALSE`.

## Literature basis

Cellular sheaves provide a finite, computable language for local data, restriction/compatibility maps, global sections, and cohomological obstructions. Hansen and Ghrist develop cellular sheaf cohomology and Laplacians on cell complexes, including synchronization and consistency applications: Justin Hansen and Robert Ghrist, "Toward a spectral theory of cellular sheaves," *Journal of Applied and Computational Topology* 3 (2019), 315-358.

A recent applied treatment states the same local-to-global architecture explicitly: local data may satisfy local compatibility checks yet fail to arise from a global assignment, with first cohomology measuring the residual obstruction. See Louis Anthony Cox Jr., "Integrating Fragmented Risk Knowledge: Sheaf Theory for Risk Analysts," *Risk Analysis* 46(3) (2026), DOI: 10.1111/risa.70206.

The present kernel is intentionally narrower than a general sheaf engine: it is ordinary cellular cohomology of one fixed 1-dimensional complex with constant `GF(2)` coefficients.

## HOLD

Do not promote `sheaf@1`, `cohomology@1`, `global_section@1`, `glue@1`, or `obstruction@1` from this specimen alone.

Strongest next frontier: distinguish an intrinsic cycle obstruction from one created or removed by changing the declared restriction maps while holding the underlying graph and local stalk dimensions fixed. That would pressure `SAME TOPOLOGY != SAME GLUING LAW` without conflating structure with evidence.
