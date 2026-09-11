# FACET-SCALING-MULTIPLIER-001

Status: bounded research slice; no public operator promotion.

## Question

If one inequality row is multiplied by a positive scalar, the feasible halfspace is unchanged. Does a raw optimal dual multiplier remain numerically invariant under that presentation change?

## Frozen specimen

Primal objective:

`max x`

Base H-presentation:

- `-x <= 0`
- `-y <= 0`
- `x + y <= 2`

Scaled H-presentation:

- `-x <= 0`
- `-y <= 0`
- `7x + 7y <= 14`

The third rows define the same halfspace because the scaled row is exactly `7` times the base row. Both presentations therefore define the same triangle and have the same primal optimum `(2,0)` with value `2`.

Using the dual convention `min b^T lambda` subject to `A^T lambda = (1,0)` and `lambda >= 0`, the base presentation has certificate

`lambda = (0,1,1)`.

The scaled presentation has certificate

`lambda' = (0,1,1/7)`.

Both have dual value `2` and zero exact stationarity residual.

The raw multiplier attached to the rescaled facet changes inversely with the row scale:

`1 = 7 * (1/7)`.

But its multiplier-weighted facet contribution does not:

- base: `1 * (1,1) = (1,1)` and `1 * 2 = 2`;
- scaled: `(1/7) * (7,7) = (1,1)` and `(1/7) * 14 = 2`.

## Exact delta

`SAME FEASIBLE HALFSPACE + SAME PRIMAL GEOMETRY + SAME PRIMAL OPTIMUM != SAME RAW DUAL MULTIPLIER COORDINATE UNDER POSITIVE ROW SCALING.`

For this frozen nondegenerate specimen, the multiplier-weighted normal/bound contribution is invariant under the declared positive rescaling.

## Mathals

- `CONSTRAINT IDENTITY != FACET IDENTITY.`
- `RAW MULTIPLIER MAGNITUDE IS A COORDINATE OF THE CONSTRAINT PRESENTATION.`
- `RECEIPT THE CONSTRAINT NORMALIZATION BEFORE COMPARING MULTIPLIER MAGNITUDES.`
- `IN THIS FROZEN SPECIMEN, lambda_i a_i AND lambda_i b_i SURVIVE POSITIVE ROW RESCALING EVEN THOUGH lambda_i DOES NOT.`

## Literature basis

This is standard KKT/duality geometry, not a novel theorem.

- Capobianco, Harsch, Eugster & Leine (2021), *International Journal for Numerical Methods in Engineering*, DOI `10.1002/nme.6801` — convex cones and normal-cone scaling properties; useful geometric background for separating a cone/facet object from a particular coordinate scaling.
- Cui, Luo, Qi & Yan (2022), *Numerical Linear Algebra with Applications*, DOI `10.1002/nla.2468` — explicit finite-dimensional KKT conditions, Lagrange multipliers, complementary slackness, and duality conventions.
- Preckel, Featherstone & Baker (1987), *American Journal of Agricultural Economics*, DOI `10.2307/1242197` — dual-variable interpretation depends on the units in which the constrained resource is expressed, consistent with treating raw shadow-price magnitude as coordinate/unit sensitive.
- Buerger, Cannon & Kouvaritakis (2016), *International Journal of Robust and Nonlinear Control*, DOI `10.1002/rnc.3501` — nearby warning that multiplier objects can also become multivalued under active-set degeneracy; therefore this slice does not generalize individual weighted-normal invariance into degenerate presentations without a separate proof.

No claim is made that these sources contain this exact frozen triangle.

Wolfram was attempted as an independent verifier for the row-scaling calculation but returned a network error, so no Wolfram-verification claim is made.

## Boundary / refusals

- `DUAL MULTIPLIER != AUTHORITY WEIGHT`.
- `DUAL MULTIPLIER != EVIDENCE WEIGHT`.
- `FACET NORMAL != CAUSAL DIRECTION`.
- `ROW SCALING != OCCURRENCE CHANGE`.
- `LARGER MULTIPLIER != MORE IMPORTANT` without a declared normalization and interpretation contract.
- `PRESENTATION-INVARIANT CERTIFICATE CONTRIBUTION != PRESENTATION-INVARIANT MEANING`.
- `SAME FEASIBLE GEOMETRY != SAME HISTORICAL WORLD`.

## Scope / HOLD

This slice adds only:

- one bounded stdlib exact kernel;
- one frozen fixture;
- one focused test file;
- this research receipt.

No general LP solver, canonical facet normalizer, redundancy engine, KKT engine, shadow-price semantics, evidence semantics, authority semantics, or public schema is added.

Explicit HOLD: `facet@1`, `normalize_constraint@1`, `dual_multiplier@1`, `shadow_price@1`, `normal_cone@1`, `certificate@1`.

## Next frontier

The next useful pressure is not another arbitrary scale factor. It is to compare **different coordinate systems on the primal variables themselves**. Variable rescaling changes both objective and constraint coefficients and induces a corresponding transformation of dual/normal coordinates. A bounded specimen could ask which quantities are covariant under a declared invertible change of basis, and which apparent deltas are merely coordinates.

Candidate seal:

`A COORDINATE CHANGE CAN MOVE EVERY NUMBER IN THE RECEIPT WITHOUT MOVING THE UNDERLYING FEASIBLE GEOMETRY. KEEP THE CHANGE-OF-BASIS MAP.`
