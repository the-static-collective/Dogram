# SKySLICEY72 — Dogram lowering

**Status:** research packet · NO NEW OPERATOR  
**Posture:** do the math, show the delta, keep the receipt, do not decide what it means.

## 1. Y orientation is `D3`, not a commuting six-label product

A three-arm Y has three rotational states and two handedness/reflection states. The full symmetry grammar is:

```text
D3 ≅ S3
|D3| = 6
D3 = C3 ⋊ C2
```

Presentation:

```text
r^3 = e
f^2 = e
f r f = r^-1
```

Therefore:

```text
turn then flip != flip then turn
```

in general.

Candidate 72-state field:

```text
F72 = C12 × D3
|F72| = 12 × 6 = 72
```

This is a cardinality/state-space claim. Do not silently replace it with `C72`.

### Candidate specimen: `Y72-ORIENTATION-001`

Freeze a reference Y, enumerate the six `D3` actions, pair each with 12 phase positions, and receipt:

```text
12 phase values
6 distinct orientation actions
72 ordered pairs
```

Use existing `delta@1` to distinguish orientation traces and `rectangle@1` for declared phase × handedness interactions. No `orient@1` is justified.

## 2. Handed crossing retains history that endpoint permutation forgets

Let:

```text
π : B_n -> S_n
```

be the standard map from braid group to endpoint permutation.

For a generator and its inverse:

```text
σ_i != σ_i^-1
π(σ_i) = π(σ_i^-1)
```

Thus a coarse endpoint observer can report the same swap while the braid receipt remains different.

### `HANDED-CROSSING-001`

```text
same endpoint permutation
!=
same crossing history
```

### Candidate specimen: `BRAID-HANDEDNESS-FIBER-001`

Two typed traces:

```text
A = [σ1]
B = [σ1^-1]
```

with equal endpoint permutation but different ordered boundary traces.

Lower to `delta@1`. Dogram reports the first typed difference; interpretation remains external.

## 3. Prediction field is chronology-sensitive

Given observed node set `N` and a frozen relation grammar `R`, define:

```text
P_R(N) = Cl_R(N) \ N
```

where `Cl_R` is a declared closure operation supplied by the specimen, not inferred by Dogram.

Two formations must remain distinct:

```text
A. declare R -> derive p -> inspect world
B. inspect p -> choose R that includes p
```

Even if both end with the same `N ∪ {p}`, their formation traces differ.

### `PREDICTION-v-COINCIDENCE-001`

Use `delta@1` on ordered formation events. Dogram can prove the histories differ; it cannot call one scientifically stronger without an external evidence policy.

## 4. Oriented aperture / cut

A cut can be represented as an explicit typed boundary parameter:

```text
projection = P_n(carrier)
```

where `n` is the declared aperture orientation.

Compare:

```text
P_n0(X)
P_n1(X)
```

without promoting either projection to `X`.

If a graph mutation is used to model a changed cut, lower the reachability delta to `reach@1` or `ablate@1` as appropriate. No optical-physics claim is minted by the lowering.

## 5. Refusals

```text
72 states != sacred 72
D3 orientation != braid group
handedness != complete formation history
same endpoints != same history
prediction trace != truth
projection != source
NO NEW OPERATOR
```

## Far-side compression

> **TURN AND FLIP DO NOT COMMUTE. ENDPOINTS CAN FORGET WHICH CROSSING OCCURRED. DOGRAM KEEPS ONLY THE DIFFERENCE IT CAN CALCULATE.**
