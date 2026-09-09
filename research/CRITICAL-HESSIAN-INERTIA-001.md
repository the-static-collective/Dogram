# CRITICAL-HESSIAN-INERTIA-001

## Question

At a declared nondegenerate critical point, what second-order information survives an arbitrary smooth invertible local reparameterization, and what is merely coordinate presentation?

This slice is downstream of reviewable `NONLINEAR-HESSIAN-CHAIN-001` (#91). It does not promote a public operator.

## Frozen exact specimen

Take

`f(x,y)=x^2-y^2`

at the critical point `(0,0)`. Then

`grad f=(0,0)`

and

`H_x=[[2,0],[0,-2]]`.

Declare the nonlinear local coordinate map

`phi(u,v)=(u+v+u^2, u+3v+v^2)`.

At `(0,0)`,

`J=D phi=[[1,1],[1,3]]`, with `det J=2`,

while the component Hessians of `phi` are nonzero:

`H(phi_1)=[[2,0],[0,0]]`,

`H(phi_2)=[[0,0],[0,2]]`.

The multivariate second-order chain rule is

`H_z(f o phi)=J^T H_x(f) J + sum_a (partial_a f) H_z(phi_a)`.

Because the declared point is critical, `grad f=0`, so the nonlinear correction is exactly zero even though `phi` has nonzero second derivatives. Therefore

`H_z=J^T H_x J=[[0,-4],[-4,-16]]`.

## Delta

The raw Hessian presentation changes.

Base characteristic polynomial:

`lambda^2 - 4`.

Transformed characteristic polynomial:

`lambda^2 + 16 lambda - 16`.

Base determinant is `-4`; transformed determinant is `-16`, satisfying the exact congruence law

`det(H_z)=det(J)^2 det(H_x)=4(-4)=-16`.

Thus raw entries, characteristic polynomial, determinant magnitude, and individual eigenvalues are not invariant under this general coordinate change.

But both symmetric Hessians have exact inertia

`(positive, negative, zero)=(1,1,0)`.

Hence the Morse index remains exactly `1`.

## Documented mathematics

At a critical point, the Hessian of a scalar function is an intrinsic symmetric bilinear form; chart matrices represent that form in coordinates. Rivera (2018), *Journal of the London Mathematical Society*, DOI `10.1112/jlms.12190`, explicitly gives the critical-point Hessian as a connection-independent bilinear form and writes the local-coordinate second-order chain rule, including the first-derivative-weighted correction that vanishes at a critical point.

For a real symmetric matrix, nonsingular congruence `A -> B^T A B` preserves inertia by Sylvester's law. Wilmes & Pinho (2014), *International Journal for Numerical Methods in Engineering*, DOI `10.1002/nme.4706`, state this law explicitly and contrast it with the more restrictive orthogonal case where eigenvalue behavior is stronger.

Morse-theory usage identifies nondegeneracy with nonsingularity of the Hessian and the index with the number of negative Hessian eigenvalues; see Bhatia et al. (2018), *Journal of Computational Chemistry*, DOI `10.1002/jcc.25181`.

Fox (2016), *Mathematische Nachrichten*, DOI `10.1002/mana.201500128`, provides a neighboring coordinate-normalization warning: Hessian determinant values can depend on the affine coordinate/volume normalization, while sign-level information can retain invariant significance.

No claim is made that these papers contain this exact frozen polynomial specimen.

## Dogram inference

The mathematically durable receipt is not the raw Hessian matrix or its ordinary eigenvalue list. Under a declared invertible coordinate change at a critical point, the coordinate Hessians are related by congruence, and inertia is the exact second-order type preserved by that congruence.

Candidate seals:

- `RAW HESSIAN SPECTRUM IS NOT A COORDINATE-INVARIANT CRITICAL-POINT RECEIPT.`
- `HESSIAN INERTIA AT A CRITICAL POINT SURVIVES INVERTIBLE REPARAMETERIZATION.`
- `KEEP THE JACOBIAN; CONGRUENCE IS NOT SIMILARITY.`
- `THE MORSE INDEX IS A PROPERTY OF THE DECLARED CRITICAL-POINT QUADRATIC FORM, NOT OF ONE NUMERIC HESSIAN PRESENTATION.`

## Constitutional boundary

- `HESSIAN ENTRY DELTA != OCCURRENCE DELTA`
- `EIGENVALUE DELTA != HISTORICAL CHANGE`
- `MORSE INDEX != IMPORTANCE`
- `CRITICAL POINT != HISTORICAL EVENT`
- `INERTIA CLASS != CAUSAL CLASS`
- `NONDEGENERATE != TRUE`
- `CONGRUENCE != IDENTITY`
- `SIGNATURE != EVIDENCE STRENGTH`
- `COORDINATE-INVARIANT SECOND-ORDER TYPE != SEMANTIC INVARIANCE`

Explicit HOLD: no `hessian@1`, `morse_index@1`, `inertia@1`, `critical_type@1`, `congruence@1`, or `coordinate_invariant@1` promotion.

## Verification receipt

Fixture and tests were committed before the production kernel.

Test-only head `1e1157b73b86416ef6177d765ba523f70a77aae4` produced Dogram CI #582 RED at Unit tests with the expected missing-module error: `ModuleNotFoundError: No module named 'dogram.critical_hessian_inertia'`.

Minimal kernel head `7e0b378e4177109ec6532863e2e9f780f6db36cf` produced Dogram CI #583 GREEN.

All landed calculations use exact `fractions.Fraction` arithmetic. No numeric eigensolver or external math dependency is required.

Wolfram was attempted as an independent verifier after the exact specimen was frozen, but the connector returned an upstream 502. No Wolfram verification claim is made.

## Strongest next frontier

Move from nondegenerate critical points to degenerate singularities, where the Hessian may vanish or lose rank and therefore fail to retain the first nonzero local structure.

A smallest hostile pair is already visible in one variable:

`f(x)=x^3`, `g(x)=x^4` at `x=0`.

Both have the same critical gradient and zero Hessian, but their first nonzero jets occur at different orders. The next slice should pressure whether the order of vanishing is preserved under a declared local diffeomorphism and then connect that bounded fact to finite determinacy / singularity theory without promoting catastrophe semantics.

Candidate seal:

`SAME CRITICAL HESSIAN CAN HIDE DIFFERENT HIGHER-ORDER JETS. KEEP THE ORDER AT WHICH THE FIRST NONZERO TERM APPEARS.`
