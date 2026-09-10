# SMOOTH-FLAT-GERM-001

## Question

Can complete Taylor data at one point distinguish smooth germs without an additional regularity assumption?

## Frozen specimen

Let

```text
h(x) = exp(-1/x^2), x != 0
h(0) = 0
```

and compare it with the zero function germ at `0`.

On the punctured line every derivative has the exact form

```text
h^(n)(x) = P_n(1/x) exp(-1/x^2)
```

with integer polynomial recurrence

```text
P_0(y) = 1
P_{n+1}(y) = -y^2 P_n'(y) + 2 y^3 P_n(y).
```

For every polynomial `P`, the standard limit theorem gives

```text
P(1/x) exp(-1/x^2) -> 0 as x -> 0.
```

Therefore every derivative of the smooth extension exists at zero and equals zero. Its complete Taylor series is the zero formal power series.

But `h(x) > 0` for every `x != 0`, so the smooth germ is not the zero germ.

Hence

```text
SAME INFINITE TAYLOR SERIES != SAME SMOOTH GERM.
```

This statement is category-sensitive. In a quasianalytic class, including the real-analytic class, zero Taylor expansion forces the function to vanish locally. Bierstone & Milman define quasianalyticity exactly this way: a function in the class whose Taylor expansion vanishes at a point is identically zero near that point (Journal of the London Mathematical Society 95 (2017), DOI 10.1112/jlms.12032). Rolin & Servi likewise formulate quasianalyticity as injectivity of the map from a germ to its asymptotic/Taylor-type expansion (Proceedings of the London Mathematical Society 110 (2015), DOI 10.1112/plms/pdv010).

Smooth singularity theory therefore treats flat perturbations as a distinct issue rather than silently identifying infinite jet equality with germ equality. Shi, Pei & Hencl describe infinite determinacy of smooth map-germs as stability under flat perturbations (Journal of Function Spaces 2013, DOI 10.1155/2013/549845).

No source is claimed to contain this exact frozen Dogram fixture.

## Executable receipt

The kernel intentionally does **not** claim to prove an infinite theorem by finite enumeration.

It does two bounded things:

1. generates `P_n` exactly over integer coefficients from the derivative recurrence;
2. emits a zero Taylor jet only when the flatness limit theorem is explicitly declared as a proof obligation.

The test surface freezes orders `0..8`, checks the exact initial recurrence, checks nonzero values away from the base point, and checks refusal when the limit theorem is withheld.

## Dogram delta

Prior slices established that increasing finite jet order can expose hidden higher-order structure. This specimen shows a strict ceiling on that strategy in the smooth category:

```text
FOR EVERY FINITE k:
    j^k h(0) = j^k 0(0)
AND EVEN THE FULL FORMAL TAYLOR SERIES AGREES,
YET THE SMOOTH GERMS DIFFER.
```

The missing input is not "more derivative depth". It is the **regularity category / reconstruction theorem** under which Taylor data is being interpreted.

## Seals

```text
RECEIPT THE REGULARITY CATEGORY.
FLAT RESIDUE != ZERO GERM.
FORMAL EQUALITY != SMOOTH-GERM IDENTITY.
AN INFINITE JET IS STILL A PROBE WITH A DOMAIN OF VALID RECONSTRUCTION.
```

## Refusals

```text
TAYLOR COLLISION != OCCURRENCE IDENTITY
FLAT != ABSENT
SMOOTH != ANALYTIC
ANALYTIC RIGIDITY != EVIDENCE STRENGTH
NONZERO NEARBY != CAUSAL EFFECT
GERM DIFFERENCE != HISTORICAL DIFFERENCE
FORMAL SERIES != OBSERVATION HISTORY
QUASIANALYTIC != TRUE
```

## HOLD

No `jet@1`, `germ@1`, `flat@1`, `analytic@1`, `quasianalytic@1`, `reconstruct@1`, or equivalence/classification operator is promoted.

## Next frontier

The natural next pressure is Borel's theorem: in the full smooth category, arbitrary formal Taylor data can be realized by a smooth germ. That separates two directions that are easy to conflate:

```text
JET -> GERMS may be highly non-unique,
while
GERM -> JET is perfectly well-defined.
```

A bounded quotient specimen could model the kernel of the Taylor map as "flat residue" without pretending the quotient selects a canonical representative.

Candidate seal:

```text
THE TAYLOR MAP CAN BE SURJECTIVE WITHOUT BEING INJECTIVE. RECONSTRUCTION NEEDS A SECTION, AND A SECTION IS EXTRA STRUCTURE.
```
