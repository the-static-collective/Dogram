# TETRAHEDRAL-BIANCHI-001

Status: RESEARCH ONLY / HOLD PUBLIC OPERATOR

## Question

Can several individually lawful non-Abelian face-holonomy receipts be combined without first putting them at a common basepoint?

No.

This slice freezes the smallest useful three-dimensional control: one oriented tetrahedron with exact edge transports in the finite non-Abelian group S3.

The calculation is deliberately narrower than physical lattice gauge theory. Dogram receives declared finite group-valued edge data, performs exact multiplication, and receipts the difference between naive face multiplication and multiplication after the required basepoint transport.

## Exact tetrahedral identity

For oriented edge transports `g_ij`, with `g_ji = g_ij^-1`, define

```text
F012 = g01 g12 g20          based at 0
F023 = g02 g23 g30          based at 0
F031 = g03 g31 g10          based at 0
F123 = g12 g23 g31          based at 1
```

Then cancellation of the shared oriented edges gives exactly

```text
F012 F023 F031
= g01 g12 g20 g02 g23 g30 g03 g31 g10
= g01 (g12 g23 g31) g10
= g01 F123 g10.
```

Therefore the closure receipt at vertex 0 is

```text
F012 F023 F031 (g01 F123 g10)^-1 = e.
```

The tempting untransported expression

```text
F012 F023 F031 F123^-1
```

is not the same calculation in a non-Abelian group because `F123` is based at vertex 1.

## Frozen hostile specimen

Use S3 as exact permutation image tuples with

```text
a = g01 = (12)
b = g12 = (23)
all other forward tetrahedron edges = e.
```

The four faces are

```text
F012 = a b
F023 = e
F031 = a^-1
F123 = b.
```

Hence

```text
F012 F023 F031 = a b a^-1
                  = g01 F123 g10.
```

The transported closure residual is exactly identity.

But the naive untransported residual is

```text
a b a^-1 b^-1 = [a,b] = (132) != e.
```

This is useful because it joins two already-live Dogram seams without collapsing them:

- HOME-MOTION-COMMUTATOR-001: order can leave a nontrivial commutator residue;
- FINITE-GAUGE-HOLONOMY-001: raw loop holonomy depends on local frame/basepoint up to conjugation;
- this slice: a multi-face closure calculation must transport compared loop data to one declared basepoint before asking whether the boundary closes.

The commutator here is not introduced as a new ontology. It is the exact residual paid by the specific illegal operation "multiply face receipts from different basepoints as though they were already co-located."

## Commuting control

Hold the same tetrahedron and set

```text
g01 = (12)
g12 = (12)
all other forward edges = e.
```

Now `g01` commutes with `F123`, so both the transported and naive residuals are identity.

Therefore:

> NAIVE CLOSURE PASS DOES NOT PROVE THAT BASEPOINT TRANSPORT WAS LAWFUL.

A commuting specimen can hide the bookkeeping error.

## Documented mathematics

This is standard non-Abelian lattice/discrete gauge mathematics, not a Dogram-specific physical claim.

- J. Kiskis, "Bianchi identity for non-Abelian lattice gauge fields," *Physical Review D* 26 (1982), 429-434, DOI: `10.1103/PhysRevD.26.429`. The paper gives a non-Abelian lattice formulation of the Bianchi identity.
- B. Bahr, B. Dittrich, J. P. Ryan, K. Bamba, "Spin Foam Models with Finite Groups," *Journal of Gravity* (2013), DOI: `10.1155/2013/549824`. Their finite-group lattice treatment defines non-Abelian face curvature as an ordered boundary product and notes that plaquette holonomies based at different adjacent vertices differ by conjugation.
- J. Magnot and A. D. Mironov, "A Mathematical Bridge between Discretized Gauge Theories in Quantum Physics and Approximate Reasoning in Pairwise Comparisons," *Advances in Mathematical Physics* (2018), DOI: `10.1155/2018/7496762`. Their simplex/holonomy treatment explicitly tracks path composition and conjugation under change of base data.

The exact tetrahedral formula above is also directly derivable from the declared edge-product definitions by cancellation; the implementation does not require a continuum limit or numerical approximation.

## Dogram inference

The durable calculational distinction is

```text
INDIVIDUAL LOOP RECEIPTS
        !=
JOINTLY COMPOSABLE LOOP RECEIPTS
```

unless the composition contract includes the transport/basepoint map that makes their comparison well typed.

Candidate seals:

> MOVE THE RECEIPTS TO ONE FRAME BEFORE ASKING WHETHER THEY CLOSE.

> SAME FACE DATA + DIFFERENT BASEPOINT HANDLING CAN CHANGE THE APPARENT CLOSURE RESIDUAL.

> A ZERO RESIDUAL CAN BE ACCIDENTAL WHEN THE OMITTED TRANSPORT HAPPENS TO COMMUTE.

This is directly compatible with the Dogram constitution:

- DO THE MATH: exact finite permutation multiplication;
- SHOW THE DELTA: identity after lawful transport versus `(132)` under naive multiplication;
- KEEP THE RECEIPT: face basepoints, edge carrier, composition convention, transported face, and both residuals are explicit;
- DO NOT DECIDE WHAT IT MEANS: no physical, causal, historical, semantic, evidentiary, or theological interpretation is inferred.

## Explicit refusals

```text
DISCRETE BIANCHI CLOSURE != PHYSICAL FIELD EQUATION
NONZERO NAIVE RESIDUAL != PHYSICAL DEFECT
BASEPOINT TRANSPORT != HISTORICAL TRANSPORT
FACE HOLONOMY != OCCURRENCE
COMMUTATOR RESIDUAL != CAUSAL CONFLICT
ALGEBRAIC CLOSURE != TRUTH
```

The kernel does not infer that the supplied tetrahedron represents space, spacetime, a gauge field, evidence, formation history, or reality.

## Implementation boundary

`dogram/tetrahedral_bianchi.py` is stdlib-only and research-scoped. It provides:

- exact finite permutation composition and inverse;
- declared-edge reversal by exact inverse;
- exact based loop holonomy;
- conjugation transport;
- one frozen oriented tetrahedral closure receipt;
- separate transported and naive residuals.

No public dispatch, schema, runtime operator, or dependency changes are introduced.

Explicit HOLD:

```text
bianchi@1
face_holonomy@1
connection@1
curvature@1
higher_gauge@1
```

## Strongest next frontier

This specimen earns one further question but not another operator:

**Can a finite collection of face/2-cell receipts be organized as typed higher-dimensional composition data so that basepoint transport, face orientation, and coherence are enforced structurally rather than by ad hoc convention?**

That points toward crossed modules / 2-groups, higher gauge theory, and non-Abelian cohomological descent. It should only be pursued with a hostile finite specimen where ordinary group-valued face bookkeeping provably loses a distinction that a genuine 2-dimensional composition law preserves.
