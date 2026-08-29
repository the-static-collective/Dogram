# ALCHEMATHOLOGY Ninefold Mathals — Dogram Companion Design

**Date:** 2026-08-28  
**Status:** research/specimen design only  
**Runtime status:** does not add or admit a new Dogram v0 operator

Dogram's standing law remains:

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

This document extracts nine exact calculation families from the ALCHEMATHOLOGY thread. They are pressure specimens for the existing `delta`, `rectangle`, `ablate`, and `reach` grammar and candidates for later composition helpers. None of these outputs are evidence, support, historical authority, or symbolic truth.

## 0. Shared typed floor

Every specimen must declare:

```text
carrier
state_space
boundary
decoder
mutation_or_operator
observable
receipt
```

Never compare values across incompatible carriers/decoders without an explicit translation.

---

# 1 — RECEIPT-RANK

## Seed

Formation histories `f` map to terminal state change:

\[
\Delta x=Nf.
\]

Hidden endpoint-invisible histories are:

\[
H=\ker N.
\]

Add receipt map `R`.

Remaining ambiguity:

\[
\ker N\cap\ker R
=
\ker\begin{pmatrix}N\\R\end{pmatrix}.
\]

## Exact criterion

\[
\boxed{
\ker N\cap\ker R=\{0\}
}
\]

iff the receipt separates every hidden linear history direction.

## Dogram pressure

- `delta`: compare terminal-state equality while receipt differs.
- `ablate`: remove one receipt coordinate and recompute hidden dimension.
- `rectangle`: topology intact/broken × receipt absent/present.

## Output

```text
hidden_dim_before
receipt_rank_on_hidden_space
hidden_dim_after
separating: true|false
```

## Refusal

`same terminal state -> same formation` is invalid.

---

# 2 — CYCLE-RANK-DUALITY

For a graph incidence matrix `B`:

\[
\ker B
\]

is cycle/circulation space.

A local additive edge relation `a` comes from a global potential iff it annihilates every cycle:

\[
a^Th=0
\quad\forall h\in\ker B.
\]

For a connected graph:

\[
k=m-n+1.
\]

The same `k` counts:

1. independent hidden circulations;
2. independent cycle-closure questions needed for integrability.

## Dogram pressure

- `reach`: establish topology.
- `ablate`: remove a chord and recompute `k`.
- `delta`: compare cycle rank.
- companion closure test: sum relation around each basis cycle.

## Output

```text
cycle_rank
hidden_history_basis[]
closure_residue[]
integrable: true|false
```

## Refusal

A zero endpoint delta does not imply zero path activity.

---

# 3 — 4ONtheFLOOR / FIVE-KILLS-HOLE

## 4D grade ladder

\[
\dim\Lambda^kV=\binom4k
\]

gives:

\[
\boxed{1,4,6,4,1}.
\]

## Tetrahedral boundary

A tetrahedron boundary has:

```text
4 vertices
6 edges
4 faces
```

and:

\[
H_2(\partial\Delta^3)\cong\mathbb Z.
\]

Attach the interior 3-cell `c`:

\[
z=\partial_3c,
\]

so the prior 2-cycle becomes exact and:

\[
H_2(\Delta^3)=0.
\]

## Dogram pressure

Compare two explicit chain complexes:

```text
A = tetrahedron boundary
B = boundary + interior cell
```

Required delta:

```text
H2_rank: 1 -> 0
cell_count_grade3: 0 -> 1
```

## Mathal IDs

- `4ONTHEFLOOR`
- `FIVE-KILLS-HOLE`

## Refusal

Do not generalize this simplex specimen into a universal property of the numerals 4 or 5.

---

# 4 — Q-4ONtheFLOOR

Let:

\[
V=\mathbb F_3^4.
\]

Gaussian-binomial subspace counts are:

\[
\boxed{1,40,130,40,1}.
\]

This is a finite-field relation-space analogue of:

\[
1,4,6,4,1.
\]

## Dogram pressure

Input:

```text
field_order: 3
vector_dimension: 4
```

Expected:

```text
subspace_counts_by_dimension:
0: 1
1: 40
2: 130
3: 40
4: 1
total_subspaces: 212
```

## Mathal ID

`Q-4ONTHEFLOOR`

## Refusal

Coordinate subspaces are not all subspaces. The six coordinate 2-planes are only six representatives among 130 actual 2D subspaces.

---

# 5 — ORIENTATION-DEBT / TENET-81

The 81 ternary vectors decompose under inversion:

\[
J(v)=-v.
\]

Only zero is fixed because characteristic is 3:

\[
v=-v\Rightarrow2v=0\Rightarrow v=0.
\]

Therefore:

\[
\boxed{
81=40+1+40
}
\]

or:

\[
81=1+40\cdot2.
\]

Projectivizing identifies:

\[
v\sim-v
\]

and collapses 80 oriented nonzero states to 40 unoriented direction classes.

## Dogram pressure

Compare:

```text
oriented_state_count = 81
projective_nonzero_direction_count = 40
fixed_states_under_negation = 1
```

Receipt loss:

```text
axis retained
orientation erased
```

## Mathal IDs

- `ORIENTATION-DEBT`
- `TENET-81`

## Refusal

A projective axis cannot by itself distinguish `INTO` from `OUT-OF`.

---

# 6 — GATE-TRANSVERSAL

Choose a nonzero linear functional:

\[
\lambda:\mathbb F_3^4\to\mathbb F_3.
\]

It partitions the 81 states into:

\[
\boxed{27+27+27}.
\]

For translation:

\[
T_v(x)=x+v,
\]

the gate value changes by:

\[
\lambda(T_vx)=\lambda(x)+\lambda(v).
\]

If:

\[
\lambda(v)=0,
\]

the direction is tangent.

If:

\[
\lambda(v)\neq0,
\]

it is transverse.

Among 40 projective directions:

\[
\boxed{
40=13_{\rm tangent}+27_{\rm transverse}.
}
\]

## Dogram pressure

For each gate/direction pair report:

```text
gate_class
direction_class
lambda_v
tangent: true|false
orbit_floor_pattern
```

A transverse direction decomposes the 81 states into 27 three-state gate-crossing orbits.

## Mathal ID

`GATE-TRANSVERSAL`

## Refusal

Endpoint floor alone does not encode whether a trajectory stayed tangent, entered, crossed through, or exited.

---

# 7 — HIDDEN-NINE

Treat the same 81 elements as the finite field:

\[
\mathbb F_{81}.
\]

It contains the unique subfield:

\[
\mathbb F_9.
\]

As an `F_9` vector space:

\[
\boxed{
\mathbb F_{81}\cong\mathbb F_9^2.
}
\]

The map:

\[
x\mapsto x^9
\]

fixes exactly `F_9`.

There are:

\[
\frac{9^2-1}{9-1}=10
\]

one-dimensional `F_9`-subspaces, each with 9 states and common zero:

\[
\boxed{
81=10(9)-9.
}
\]

Inside one 9-line:

\[
9=1+8=4+1+4.
\]

Relative trace:

\[
\operatorname{Tr}_{81/9}(x)=x+x^9
\]

has 9 outputs with 9-element fibers.

Relative norm:

\[
N_{81/9}(x)=x^{10}
\]

maps the 80 nonzero elements onto 8 nonzero `F_9` values with 10-element fibers:

\[
\boxed{
81=1+8(10).
}
\]

## Dogram pressure

Report the same carrier under multiple declared decoders:

```text
decoder: F3^4 vector
decoder: F9^2 vector
decoder: F81 field
decoder: trace_to_F9
decoder: norm_to_F9
```

## Mathal ID

`HIDDEN-NINE`

## Refusal

Do not treat numerically equal decompositions as the same quotient. `10×8` orbit grouping and `8×10` norm-fiber grouping have different formation receipts.

---

# 8 — PHI / FROBENIUS RECEIPT

Real golden ratio:

\[
\phi=\frac{1+\sqrt5}{2}.
\]

For odd `n`:

\[
\phi^n=L_n+\phi^{-n}.
\]

At `n=81`:

\[
\phi^{-81}\approx1.180323733260147\times10^{-17}.
\]

The residual is small but exact.

Now define Frobenius on `F_81`:

\[
\sigma(x)=x^3.
\]

Since:

\[
\sigma^4=I,
\]

the selected powers satisfy:

\[
\boxed{x^3=\sigma(x)}
\]

\[
\boxed{x^{27}=\sigma^{-1}(x)}
\]

\[
\boxed{x^{81}=x}
\]

\[
\boxed{x^{82}=x^2}.
\]

Let `alpha` satisfy:

\[
\alpha^2-\alpha-1=0
\]

over `F_3`. Then `alpha` lies in `F_9` and:

\[
\alpha^4=-1,\qquad\alpha^8=1.
\]

## Dogram pressure

Record separately:

```text
real_phi_lane
finite_field_alpha_lane
exponent_receipt
operator_type
```

Never compare them without an explicit analogy relation.

## Mathal IDs

- `PHI-RECEIPT`
- `FROBENIUS-TENET`
- `RETURN-PLUS-ONE`

## Refusal

A mathematically suggestive exponent pattern is not historical or physical evidence.

---

# 9 — COHERENCE-HULL

Let `G` be a constrained carrier framework with configuration space:

\[
\mathcal C.
\]

A realization is:

\[
q\in\mathcal C,
\qquad F(q)\subset\mathbb R^3.
\]

A history:

\[
q:T\to\mathcal C.
\]

A family of histories:

\[
q_s:T\to\mathcal C.
\]

The lawful occupancy hull:

\[
\boxed{
\Omega(G)=
\bigcup_{s,t}F(q_s(t)).
}
\]

## Dogram pressure

No new runtime operator is admitted here. Use existing/composed operations:

### `reach`
Construct a graph approximation of reachable coherent configurations.

### `ablate`
Remove one carrier or one constraint and recompute reachability.

### `delta`
Compare occupancy sets, reachable-set summaries, or topological invariants.

Candidate set delta:

\[
\Delta_\Omega
=
\Omega(G)\setminus\Omega(G-\text{carrier}).
\]

Question:

> How much lawful possible world does one constituent support?

## Mathal IDs

- `COHERENCE-HULL`
- `FORMATION-OF-FORMATION`

## Refusal

The existence of an unmodeled configuration parameter does not establish literal higher-dimensional physical agency.

---

# Ninefold output contract

A Dogram companion run over these specimens should return only:

```text
INPUT DECLARATION
OPERATION
BEFORE
AFTER
DELTA
RECEIPT
REFUSALS / INCOMPATIBILITIES
```

It must not return:

```text
therefore historical ancestry
therefore mystical truth
therefore physical fifth dimension
therefore evidence support
```

## Candidate implementation ordering

If any of these become runtime work later:

1. keep `RECEIPT-RANK` as composition over matrix/rank helpers;
2. add chain-complex/homology only behind a new explicit design;
3. treat finite-field/q-binomial calculations as companion math modules, not v0 graph operators;
4. prototype `COHERENCE-HULL` only after a concrete constrained mechanism is supplied;
5. preserve every decoder/boundary declaration in the receipt.

## Seal

> **Dogram counts the structure the decoder exposes. It does not decide why that structure matters.**
