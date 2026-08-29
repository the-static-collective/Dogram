# SYZYGY-RING-001 — Exact Relation Decoder

**Status:** frontier mathal slice · no runtime operator admitted

Dogram's standing law remains:

> DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.

## Purpose

Use **syzygy** as a strict decoder for mathal specimens: declare generators, ambient algebra/world, decoder, proposed relation, and residual; then calculate whether the relation closes exactly.

This is not a claim that every pretty equality is a meaningful syzygy of a phenomenon.

## Core record

A syzygy specimen is represented by

\[
\boxed{(A,G,R,\varepsilon,D)}
\]

where:

- `A` — ambient algebra / world;
- `G` — declared generators;
- `R` — proposed relation evaluated on the generators;
- `epsilon` — residual `R(G)`;
- `D` — decoder / projection that produced the quantities.

Classification:

```text
epsilon = 0  -> EXACT_SYZYGY
epsilon != 0 -> BROKEN_SYZYGY / RESIDUAL
relation changes with A -> AMBIENT_DEPENDENT
relation changes with D -> DECODER_DEPENDENT
relation among established relations -> HIGHER_SYZYGY
```

Dogram calculates these classifications. It does not infer historical, physical, symbolic, causal, or metaphysical meaning.

## 1. Pairfield square

For every integer `n`:

\[
\boxed{n+2\binom n2-n^2=0.}
\]

At `n=8`:

\[
8+28+28-64=0.
\]

This decomposes the full ordered pair space `X x X` into:

- `n` diagonal self-pairs;
- one orientation of every unordered distinct pair;
- the reverse orientation of every unordered distinct pair.

Mathal:

```text
PAIRFIELD-SYZYGY(n)
```

## 2. 136 / 137 relation family

Exact receipts:

\[
137-\binom{17}{2}-1=0,
\]

\[
136-17\cdot8=0,
\]

\[
10^4+1-73\cdot137=0.
\]

These are distinct relations over the same numeric neighborhood. Matching numbers do not collapse the relations into one meaning.

## 3. Reciprocal successor

Let

\[
b=\frac{a}{1+a}.
\]

Then:

\[
\boxed{a-b-ab=0}
\]

and equivalently:

\[
\boxed{\frac1b-\frac1a-1=0.}
\]

This gives two exact decoder surfaces for the same transition.

Mathal:

```text
RECIPROCAL-SYZYGY
```

## 4. Common-carrier successor

For integers `a,b` with `g=gcd(|a|,|b|)` and reduced displacement

\[
\rho=\frac{b-a}{g},
\]

we have the defining relation

\[
\boxed{(b-a)-g\rho=0.}
\]

This keeps raw displacement, shared integer carrier, and primitive step distinct.

## 5. TENET / finite-field relations

Existing exact specimens admit syzygy form:

\[
81-40-1-40=0,
\]

\[
40-13-27=0,
\]

\[
81-(10\cdot9-9)=0,
\]

\[
9-4-1-4=0.
\]

These relations are calculations only. Their symbolic interpretations remain outside Dogram.

## 6. Ambient dependence

For

\[
M=
\begin{pmatrix}
1&1&0\\
1&0&1\\
0&1&1
\end{pmatrix},
\]

over `F_2`:

\[
M(1,1,1)^T=0,
\]

so the columns possess a nontrivial syzygy.

Over `F_3`:

\[
\ker M=\{0\}.
\]

Therefore:

\[
\boxed{\text{SYZYGY IS TYPED BY ITS AMBIENT ALGEBRA.}}
\]

The same discipline applies to factorization: irreducibility in one ambient ring must not be silently promoted into another.

## 7. Residual as failed closure

For a proposed relation `R(G)=0`, define

\[
\boxed{\varepsilon=R(G).}
\]

The residual is not noise by default. It is the exact amount by which the proposed syzygy fails at the declared cut.

This composes with variation calculus. For the three-way mixed difference

\[
\Delta_{ABC}
=
F_{111}-F_{110}-F_{101}-F_{011}+F_{100}+F_{010}+F_{001}-F_{000},
\]

`Delta_ABC = 0` means the lower-order decomposition closes at that observable; nonzero `Delta_ABC` is a top-order residual.

Candidate naming:

```text
SYZYGY-DEFECT
WHOLE-RESIDUAL
```

Neither is admitted as a new runtime operator by this slice.

## 8. Higher syzygy / formation lift

A verified relation may itself be reified as an inert next-level carrier and participate in another declared relation:

```text
objects
  -> relations
  -> relations among relations
  -> higher relations
```

This is a conventional mathematical neighbor for `FORMATION-LIFT` and for Dogram Ω's metaoscillatory direction.

Constitutional rule:

```text
VERIFIED RELATION -> MAY BECOME INERT CARRIER
VERIFIED RELATION -> DOES NOT ACQUIRE AUTHORITY OR MEANING
```

## 9. Syzygy pressure questions

For every candidate:

```text
1. What are the generators?
2. What ambient algebra/world are they in?
3. What decoder produced them?
4. What exact relation is proposed?
5. What is the residual?
6. Does the relation survive a change of parser/decoder?
7. Does it survive hostile controls?
8. Is a relation among relations present?
```

## 10. Refusals

```text
PRETTY EQUALITY != PHENOMENAL RELATION
ZERO RESIDUAL != CAUSATION
SAME SYZYGY SHAPE != SAME SEMANTIC PROCESS
RELATION IN ONE AMBIENT != RELATION IN EVERY AMBIENT
DECODER-DEPENDENT CLOSURE != SOURCE INVARIANT
HIGHER SYZYGY != HIGHER AUTHORITY
```

## Seal

\[
\boxed{\textbf{WHAT MUST CANCEL FOR THIS WHOLE TO CLOSE?}}
\]

Dogram computes the cancellation and preserves the receipt. Interpretation travels elsewhere.