# CO-PHASE-WALK-BRAID-SPRING-001

**Date:** 2026-08-31  
**Status:** RESEARCH LEDGER · EXACT MATH + MODEL MATH + HOSTILE CONTROLS · NO NEW RUNTIME OPERATOR

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

This ledger freezes two connected mathematical constructions:

1. an eight-state verb/co-phase walk with path receipts;
2. an N-imaginal spring / mapping-torus model with twisted resonance.

The spring material here is math-only. Calendar, theological, and symbolic interpretations are intentionally excluded.

---

# A. CO-PHASE WALK BRAID

## `CO-IS-PHASE-NOT-VERB-001` — EXACT STATE PRODUCT

Let

```math
V=\{P,C,K,R\}
```

for predict, compose, construct, create.

Let

```math
\mathbb Z_2=\{0,1\}
```

encode `not-co` / `co`.

Then the visible state surface is

```math
S=V\times\mathbb Z_2.
```

There are exactly

```math
|S|=4\cdot2=8
```

states.

Seal:

```text
CO IS NOT A FIFTH VERB.
CO IS A BINARY PHASE COORDINATE ON THE VERB.
```

## `ENDPOINT-NE-WALK-001` — PATH CATEGORY FLOOR

Let `G` be the directed graph whose vertices are the eight states and whose edges are declared verb-advance and co-toggle moves.

A walk is an edge word

```math
p=e_1e_2\cdots e_n.
```

Two walks may have the same source and target while remaining distinct paths:

```math
s(p)=s(q),\qquad t(p)=t(q),\qquad p\ne q.
```

Therefore

```text
SAME ENDPOINT != SAME WALK HISTORY.
```

This is exact in the free path category before any quotient relation is imposed.

## `BARE-LADDER-COMMUTES-001` — HOSTILE CONTROL

Define a partial verb lift `L` by

```math
L(v,c)=(v+1,c)
```

where the next verb exists, and define the co-toggle

```math
C_o(v,c)=(v,c+1\bmod2).
```

If the operators are independent, then wherever both composites are defined,

```math
L\circ C_o=C_o\circ L.
```

So the eight-state Cartesian product alone does **not** create noncommutative braid algebra.

Seal:

```text
GRID != BRAID.
PATH RETENTION OR CO-SENSITIVE TRANSITION LAW IS REQUIRED.
```

## `COMMUTING-SQUARE-QUOTIENT-001` — EXACT CONTROL

If we impose the relation

```math
LC_o\sim C_oL
```

for every commuting square, path order is erased at that square.

If we do not impose it, the two edge words remain distinguishable formation histories even though their endpoint states coincide.

Therefore:

```text
ENDPOINT QUOTIENT MAY ERASE FORMATION ORDER.
```

## `CO-SENSITIVE-LIFT-001` — MODEL EXTENSION

A stronger model may declare phase-sensitive lifts

```math
L_0(v),\qquad L_1(v)
```

with

```math
L_0\ne L_1.
```

Then changing co-phase before a verb transition may alter the resulting state or transition receipt.

This is a model extension only. It is not implied by `V x Z_2`.

---

# B. N-IMAGINAL SPRING GEOMETRY

## `N-HELIX-PHASE-RING-001` — EXACT GEOMETRIC MODEL

For `N` phase-offset helical centerlines, let

```math
\phi_j=\frac{2\pi j}{N},\qquad j=0,\ldots,N-1.
```

A simple shared-axis family is

```math
\mathbf C_j(t)=
\begin{pmatrix}
R\cos(t+\phi_j)\\
R\sin(t+\phi_j)\\
ht
\end{pmatrix}.
```

For a circular helix with radius `R` and axial rise parameter `h`,

```math
\kappa=\frac{R}{R^2+h^2},
\qquad
\tau=\frac{h}{R^2+h^2}.
```

Hence

```math
\frac{\tau}{\kappa}=\frac{h}{R}.
```

## `ROOTS-OF-UNITY-CENTER-001` — EXACT

The phase positions on a circular cross-section are

```math
z_j=Re^{2\pi i j/N}.
```

For `N>1`,

```math
\sum_{j=0}^{N-1}e^{2\pi i j/N}=0.
```

So a symmetric N-phase ring can have zero vector sum at the center while every local phase remains nonzero.

```text
ZERO RESULTANT != ZERO LOCAL ACTIVITY.
```

## `CYCLE-LAPLACIAN-MODES-001` — EXACT

For nearest-neighbor coupling on the cycle graph `C_N`, the discrete Laplacian eigenmodes are

```math
v_k(j)=e^{2\pi i k j/N},\qquad k=0,\ldots,N-1,
```

with eigenvalues

```math
\lambda_k=4\sin^2\left(\frac{\pi k}{N}\right).
```

Thus

```math
\lambda_k=\lambda_{N-k}.
```

Most nontrivial modes occur as conjugate / counter-rotating pairs.

For `N=72`, the uniform mode is `k=0`, the alternating mode is `k=36`, and the remaining nontrivial modes pair as `(k,72-k)`.

---

# C. CLOSED SPRING AS RETURN MAP / MAPPING TORUS

## `MONODROMY-RETURN-001` — EXACT FINITE-FIBER MODEL

Let the visible carrier coordinate be

```math
x\in[0,L]
```

and the imaginal index be

```math
j\in\mathbb Z_N.
```

Close the carrier with a shift `m`:

```math
(L,j)\sim(0,j+m\bmod N).
```

The resulting quotient is the mapping torus of the permutation

```math
P_m:j\mapsto j+m\pmod N.
```

Seal:

```text
VISIBLE RING CLOSURE NEED NOT BE MATERIAL-IDENTITY CLOSURE.
```

## `GCD-COMPONENTS-001` — EXACT

The permutation `P_m` decomposes `Z_N` into

```math
d=\gcd(N,m)
```

orbits.

Each orbit has length

```math
\ell=\frac{N}{\gcd(N,m)}.
```

Hence the mapping torus contains exactly `d` continuous closed components, each requiring `ell` visible rounds to return to its starting imaginal identity.

For `N=72`:

```text
m=3 -> gcd=3  -> 3 components, length 24
m=4 -> gcd=4  -> 4 components, length 18
m=5 -> gcd=1  -> 1 component, length 72
m=7 -> gcd=1  -> 1 component, length 72
```

## `PRIMITIVE-LIFT-001` — EXACT

A shift `m` is a primitive one-orbit traversal iff

```math
\gcd(N,m)=1.
```

For `N=72`, the number of primitive shifts is

```math
\varphi(72)=24.
```

Thus `m=5` and `m=7` are two members of a 24-element primitive class.

## `FIVE-SEVEN-DELTA-001` — EXACT

Let `P_a` denote shift by `a` on `Z_72`.

Then

```math
P_7P_5^{-1}=P_2.
```

After `k` visible rounds, their relative separation is

```math
\Delta_k=2k\pmod{72}.
```

The first positive relative re-alignment solves

```math
2k\equiv0\pmod{72},
```

giving

```math
k=36.
```

Also

```math
5\cdot36\equiv36\pmod{72},
```

```math
7\cdot36\equiv36\pmod{72}.
```

So both primitive walks hit the antipodal imaginal at half their 72-round cycle while retaining different intermediate orderings.

```text
SAME ORIGIN + SAME ANTIPODE + SAME FINAL CLOSURE
!=
SAME TRAVERSAL ORDER.
```

---

# D. WINDING RECEIPT

## `QUOTIENT-PLUS-WINDING-001` — EXACT

Every integer `k` has a unique Euclidean decomposition

```math
k=Nw+r,
\qquad
0\le r<N.
```

Interpret

```text
r = visible phase on C_N
w = completed winding count
```

Then reduction modulo `N` retains `r` but discards `w`.

```text
SAME VISIBLE PHASE != SAME WINDING HISTORY.
```

This is a direct quotient/lift specimen.

---

# E. TWISTED RESONANCE

## `TWISTED-BOUNDARY-MODE-001` — EXACT GIVEN THE MODEL

Let a field on the closed carrier satisfy

```math
q(L,j,t)=q(0,j+m,t).
```

Expand across the imaginal index:

```math
q(x,j,t)=\sum_k a_k(x,t)e^{2\pi i k j/N}.
```

Then the boundary condition becomes

```math
a_k(L,t)=e^{2\pi i km/N}a_k(0,t).
```

For a longitudinal factor

```math
a_k(x,t)\propto e^{i\kappa x},
```

allowed wave numbers satisfy

```math
e^{i\kappa L}=e^{2\pi i km/N},
```

so

```math
\boxed{
\kappa_{n,k}^{(m)}=
\frac{2\pi}{L}
\left(n+\frac{km}{N}\right)
}
```

for integer `n`.

Thus the return-map monodromy enters the resonance condition as a phase twist.

## `FIVE-SEVEN-RESONANCE-DELTA-001` — EXACT GIVEN THE MODEL

For `N=72`, holding the same transverse Fourier index `k`,

```math
\kappa_{n,k}^{(7)}-\kappa_{n,k}^{(5)}
=
\frac{2\pi}{L}\frac{2k}{72}
=
\frac{2\pi}{L}\frac{k}{36}.
```

This is a mode-by-mode longitudinal wave-number shift.

## `SPECTRUM-CAN-HIDE-HISTORY-001` — HOSTILE CONTROL

If all imaginal sites are otherwise indistinguishable and only the unordered set of phase eigenvalues is observed, primitive shifts may produce spectrally equivalent data under relabeling.

Therefore:

```text
DIFFERENT MONODROMY HISTORY
NEED NOT FORCE
DIFFERENT COARSE OBSERVABLE.
```

A probe must be sensitive to adjacency, identity, coupling, orientation, or path history before it may distinguish the traversals.

---

# F. CONTINUUM LIMIT

## `YARN-TO-TUBE-LIMIT-001` — MODEL LIMIT

For cyclic fields `q_j(t)` with angular spacing

```math
\Delta\theta=\frac{2\pi}{N},
```

the nearest-neighbor second difference

```math
\frac{q_{j+1}-2q_j+q_{j-1}}{(\Delta\theta)^2}
```

approaches

```math
\frac{\partial^2q}{\partial\theta^2}
```

under the usual smooth continuum-limit assumptions as `N -> infinity`.

So a dense cyclic yarn bundle can be modeled by a field

```math
q(\theta,t)
```

on `S^1`, or by

```math
q(s,\theta,t)
```

when longitudinal material coordinate `s` is also retained.

Seal:

```text
DISCRETE YARN BUNDLE -> CONTINUOUS TUBE FIELD
IS A LIMIT PROCEDURE, NOT AN IDENTITY CLAIM.
```

---

# G. SURVIVING MATHALS

```text
CO IS A PHASE COORDINATE, NOT A VERB.

GRID != BRAID.
THE PATH MUST BE RETAINED OR THE TRANSITION LAW MUST EARN NONCOMMUTATIVITY.

END STATE != WALK HISTORY.

VISIBLE RING CLOSURE != MATERIAL CLOSURE.

NUMBER OF CLOSED YARNS = gcd(N,m).

COPRIME SHIFT -> ONE ORBIT THROUGH ALL N IMAGINALS.

SAME VISIBLE PHASE != SAME WINDING HISTORY.

RETURN-MAP PHASE CAN ENTER THE RESONANCE CONDITION.

DIFFERENT HISTORY NEED NOT FORCE DIFFERENT COARSE OBSERVABLE.
```

No runtime primitive is proposed by this ledger.
