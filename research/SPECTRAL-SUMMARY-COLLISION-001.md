# SPECTRAL-SUMMARY-COLLISION-001

Status: bounded research slice; no public operator promotion.

## Question

After `SHEAF-LAPLACIAN-ENERGY-001`, how much of the nonzero spectrum is still lost if a receipt preserves not only the global-section kernel but also the Laplacian trace?

## Fixed carrier

Use the already-landed three-vertex path scalar-sheaf kernel

```text
0 -- 1 -- 2
```

with positive integer edge scales `(p,q)` and

```text
delta(x0,x1,x2) = (p(x1-x0), q(x2-x1)).
```

The Laplacian is

```text
L = delta^T delta
  = [[ p^2,          -p^2,      0],
     [-p^2, p^2 + q^2,   -q^2],
     [   0,          -q^2,    q^2]].
```

For every positive `p,q`,

```text
ker(delta) = span{(1,1,1)}
nullity    = 1
```

and

```text
det(lambda I - L)
= lambda [lambda^2 - 2(p^2+q^2)lambda + 3p^2q^2].
```

Therefore the trace sees only `2(p^2+q^2)`, while the product of the two nonzero eigenvalues sees `3p^2q^2`.

## Exact collision

Choose

```text
A: (p,q) = (1,8)
B: (p,q) = (4,7)
```

because

```text
1^2 + 8^2 = 4^2 + 7^2 = 65.
```

Both specimens therefore have

```text
same host graph
same global-section basis = (1,1,1)
same nullity = 1
same trace = 130
```

but their characteristic polynomials are

```text
A: lambda(lambda^2 - 130 lambda + 192)
B: lambda(lambda^2 - 130 lambda + 2352)
```

because

```text
3(1^2)(8^2) = 192
3(4^2)(7^2) = 2352.
```

The exact nonzero eigenvalues are therefore

```text
A: 65 +/- sqrt(4033)
B: 65 +/- sqrt(1873).
```

Thus:

> SAME KERNEL + SAME TRACE != SAME SPECTRUM.

and, more generally for this declared family:

> A LOW-ORDER SPECTRAL SUMMARY CAN COLLIDE WHILE A HIGHER SPECTRAL INVARIANT STILL MOVES.

## Documented mathematics

This is ordinary finite weighted-Laplacian algebra. The distinction between harmonic/kernel information and non-harmonic spectral information is standard. Wang, Nguyen & Wei (2020), *Persistent spectral graph*, DOI `10.1002/cnm.3376`, explicitly separate zero/harmonic spectral information from additional non-harmonic spectral information. Izmestiev & Lam (2025), *Discrete Laplacians — Spherical and hyperbolic*, DOI `10.1112/jlms.70235`, note that choices of weights can leave harmonic functions unchanged while affecting nonzero eigenvalues and eigenspaces.

No claim is made that either paper contains this exact `(1,8)` versus `(4,7)` specimen; the specimen is a deterministic finite construction from the already-landed Dogram kernel.

## Dogram inference

A receipt that preserves only

```text
kernel/nullity + trace
```

cannot reconstruct the full nonzero spectrum even in this smallest weighted-path family. If a downstream calculation consumes a spectral summary, the summary chosen is part of the decoder contract.

This does **not** imply that every downstream task needs the full spectrum. It implies only that discarded invariants cannot later be treated as though they were preserved.

## Refusals

```text
SAME TRACE != SAME SPECTRUM
SPECTRAL COLLISION != HISTORICAL EQUIVALENCE
NONZERO EIGENVALUE PRODUCT != CAUSAL STRENGTH
SPECTRAL GAP != CONFIDENCE
LAPLACIAN ENERGY != EVIDENCE
WEIGHT CHOICE != OCCURRENCE
ALGEBRAIC DISTINCTION != TRUTH
```

## Verification

The frozen fixture and focused tests reuse the already-landed `dogram.sheaf_laplacian_energy` kernel. No new production module is added.

Independent exact symbolic arithmetic during the research pass reproduced:

```text
trace(A) = trace(B) = 130
chi_A = lambda(lambda^2 - 130 lambda + 192)
chi_B = lambda(lambda^2 - 130 lambda + 2352)
```

A Wolfram connector check was attempted during the pass but returned an upstream 404. No Wolfram verification claim is made.

## HOLD

Do not promote:

```text
spectral_summary@1
pseudodeterminant@1
spectral_gap@1
isospectral@1
spectral_equivalence@1
```

The next meaningful frontier is stronger: hold the complete eigenvalue multiset fixed and ask whether different weighted/sheaf structures can still carry different localized eigenvectors or restriction-map geometry. That would test the inverse-spectral boundary rather than another scalar summary.
