# NONLINEAR-HESSIAN-CHAIN-001

Status: bounded research slice; no public operator promotion.

## Question

After `COORDINATE-COVARIANCE-001`, does first-order covariance under a declared coordinate map justify treating the raw coordinate Hessian as if it transformed tensorially under a nonlinear reparameterization?

No.

## Frozen exact specimen

Use the same nonlinear coordinate map and evaluation point in both controls:

- `phi(z) = z + z^2`;
- `z0 = 1`;
- `x0 = phi(1) = 2`;
- `phi'(1) = 3`;
- `phi''(1) = 2`.

For a scalar composite `g(z)=f(phi(z))`, the exact second-order chain rule is

`g'' = f''(phi) * (phi')^2 + f'(phi) * phi''`.

The first term is the scalar analogue of the naive Hessian pullback `J^T H J`. The second is a gradient-weighted correction contributed by the nonlinear coordinate map.

### Noncritical objective

Let `f(x)=x^2+x`.

At `x0=2`:

- `f'(2)=5`;
- `f''(2)=2`;
- first-order chain: `g'(1)=5*3=15`;
- naive second-order pullback: `2*3^2=18`;
- nonlinear correction: `5*2=10`;
- exact transformed second derivative: `18+10=28`.

Direct polynomial composition independently gives the same `g''(1)=28`.

Therefore the naive tensor-style rule misses an exact delta of `10`.

### Critical-point control

Keep `phi`, `z0`, `x0`, `phi'(1)`, and `phi''(1)` fixed. Change only the objective to

`f_c(x)=(x-2)^2`.

At `x0=2`:

- `f_c'(2)=0`;
- `f_c''(2)=2`;
- first-order chain: `0*3=0`;
- naive second-order pullback: `2*3^2=18`;
- nonlinear correction: `0*2=0`;
- exact transformed second derivative: `18`.

The extra term disappears precisely because the declared point is critical for the objective.

## Documented mathematics

This is the ordinary second-order chain rule, not a new theorem. Savaré & Tomarelli, *Advances in Mathematics* 140 (1998), DOI `10.1006/aima.1998.1770`, study second-order chain rules for bounded-Hessian functions. Magnus & Neudecker, *Matrix Differential Calculus with Applications in Statistics and Econometrics*, 3rd ed. (2019), DOI `10.1002/9781119541219.ch6`, explicitly develops the Hessian chain rule for composite functions. A recent finite-element derivation writes the same coordinate-change structure with second-coordinate derivatives multiplied by first derivatives of the scalar field: DOI `10.1016/j.cma.2025.118083`.

The critical-point boundary is classical Morse/differential-geometry territory: the raw coordinate Hessian obtains an intrinsic bilinear-form meaning at a critical point because the first-derivative correction terms vanish. This slice uses only the exact scalar special case needed for the hostile specimen.

Scholar Gateway was attempted for literature retrieval but returned no passages for this query. Wolfram was attempted as an independent symbolic verifier but returned a network error. No claim of verification by either service is made.

## Dogram inference

The exact mathematical result supports only the following provenance law:

`FIRST-ORDER COVARIANCE DOES NOT LICENSE SECOND-ORDER TENSOR LANGUAGE UNDER NONLINEAR REPARAMETERIZATION.`

And:

`KEEP THE JACOBIAN AND THE SECOND DERIVATIVE OF THE COORDINATE MAP IN THE RECEIPT.`

At a declared critical point:

`THE GRADIENT-WEIGHTED SECOND-ORDER CORRECTION VANISHES.`

That is a conditional algebraic statement, not a semantic promotion.

## Explicit refusals

- `NONLINEAR COORDINATE MAP != HISTORICAL TRANSFORMATION`;
- `HESSIAN DELTA != OCCURRENCE DELTA`;
- `CRITICAL POINT != IMPORTANT EVENT`;
- `VANISHING CORRECTION != EVIDENCE OF CANONICAL COORDINATES`;
- `SECOND DERIVATIVE != CURVATURE` without a declared geometric structure;
- `COORDINATE HESSIAN != INTRINSIC HESSIAN` away from the required structure/critical-point conditions;
- `ALGEBRAIC COVARIANCE != CAUSATION`;
- `CHAIN-RULE CLOSURE != TRUTH`.

## Scope / HOLD

The implementation is deliberately scalar and polynomial, using exact `fractions.Fraction` arithmetic. It is not a manifold package, automatic-differentiation engine, tensor library, connection/Christoffel implementation, optimizer, evidence engine, or coordinate canonicalizer.

No `hessian@1`, `jacobian@1`, `reparameterize@1`, `connection@1`, `critical_point@1`, `covariant_hessian@1`, or `curvature@1` promotion.

## Strongest next frontier

The scalar correction is only the one-dimensional shadow of the multivariate formula

`H_z(f∘phi) = J_phi^T H_x(f) J_phi + sum_a (partial_a f) H_z(phi_a)`.

A bounded two-dimensional hostile specimen could separate three objects that are often flattened together:

1. the raw coordinate Hessian;
2. the Hessian at a critical point, where the gradient-weighted correction vanishes;
3. a covariant Hessian defined using an explicitly declared connection.

Candidate seal:

`SECOND-ORDER COORDINATE DATA BECOMES INTRINSIC ONLY AFTER THE MISSING GEOMETRIC STRUCTURE OR THE CRITICAL-POINT CONDITION IS RECEIPTED.`
