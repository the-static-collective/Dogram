# COORDINATE-COVARIANCE-001

Status: bounded research slice; no public operator promotion.

## Question

Can a declared invertible change of primal coordinates move every visible primal coordinate and every linear objective/constraint coefficient while preserving the underlying optimization problem? If so, which parts of the receipt are coordinates, which equalities survive, and what map must be kept to replay the equivalence?

## Frozen specimen

Base linear program:

- objective: `max x`;
- constraints: `-x <= 0`, `-y <= 0`, `x+y <= 2`;
- primal optimum: `x* = (2,0)`;
- dual certificate under `min b^T lambda` subject to `A^T lambda = c`, `lambda >= 0`: `lambda = (0,1,1)`.

Declare the invertible coordinate relation

`x = T z`

with

`T = [[1,1],[1,2]]`

and exact inverse

`T^-1 = [[2,-1],[-1,1]]`.

The transformed problem is obtained by composition, not by interpretation:

- a primal point moves by `z = T^-1 x`;
- a constraint row/covector `a^T x <= b` becomes `(a^T T) z <= b`;
- the objective covector `c^T x` becomes `(c^T T) z`.

Therefore the transformed coordinates are:

- objective: `(1,1)`;
- constraints: `(-1,-1) z <= 0`, `(-1,-2) z <= 0`, `(2,3) z <= 2`;
- carried optimum: `z* = (4,-2)`.

Every coordinate of the chosen optimum changes, and every objective/constraint covector has different coefficients from the base presentation.

Yet replay is exact:

`T z* = (2,0) = x*`,

and the objective value is unchanged:

`(1,0)·(2,0) = 2 = (1,1)·(4,-2)`.

The same dual multiplier tuple also satisfies transformed stationarity because

`(A T)^T lambda = T^T A^T lambda = T^T c`.

The exact residual is zero in both presentations.

## Exact delta

`SAME DECLARED OPTIMIZATION PROBLEM UNDER AN INVERTIBLE COORDINATE MAP != SAME NUMERICAL COORDINATES OR LINEAR COEFFICIENTS.`

The map is not optional metadata. Without `T` and `T^-1`, the two coordinate receipts cannot be replayed as the same transported problem.

## Mathals

- `POINT COORDINATES ARE NOT THE POINT.`
- `COVECTOR COEFFICIENTS ARE NOT THE LINEAR FUNCTIONAL APART FROM A DECLARED BASIS.`
- `A COORDINATE CHANGE CAN MOVE EVERY NUMBER IN THE PRIMAL/COVECTOR PRESENTATION WHILE PRESERVING FEASIBILITY AND OBJECTIVE VALUE.`
- `KEEP THE CHANGE-OF-BASIS MAP.`
- `TRANSFORMATION LAW IS PART OF THE RECEIPT.`

## Documented mathematics

This slice uses standard finite-dimensional linear algebra and linear/convex optimization rather than proposing a new theorem.

- Villalba & Oliveira (2026), *Numerical Linear Algebra with Applications*, DOI `10.1002/nla.70063` — standard matrix-form primal/dual linear programming and the stationarity/duality relation `A^T y + z = c`, providing the algebraic surface transported by a coordinate substitution.
- Said & Wegman (2009), *WIREs Computational Statistics*, DOI `10.1002/wics.16` — reviews equivalent transformations used to put linear programs into alternate standard forms; useful background for treating mathematical-program representations as transformable descriptions rather than intrinsic coordinate strings.
- Ribes-Mallada et al. (2011), *Mathematical Problems in Engineering*, DOI `10.1155/2011/458083` — gives a concrete optimization setting where a change of variables transforms a problem into an equivalent convex formulation, supporting the general distinction between representation and represented optimization problem.
- Charnes, Cooper & Kortanek (1969), *Naval Research Logistics Quarterly*, DOI `10.1002/nav.3800160104` — classical convex duality framed through finite-dimensional vector-space pairing, useful background for the primal/covector distinction.

No claim is made that these sources contain this exact frozen triangle or matrix `T`.

Scholar Gateway was used for literature orientation. Wolfram was attempted as an independent symbolic verifier but returned an upstream 502, so no Wolfram-verification claim is made.

## Inference for Dogram

The durable Dogram inference is provenance-oriented, not semantic:

If two calculations are compared across coordinate systems, a raw numeric delta in point coordinates, objective coefficients, constraint normals, gradients, or other covectors is not by itself an intrinsic geometric delta. A lawful comparison needs the declared transport map and the transformation law for each object type.

This is especially important because points/vectors and linear functionals do not transform by the same matrix under `x = T z`: primal coordinates use `T^-1` to move from `x`-coordinates to `z`-coordinates, while covector coefficients pull back by `T^T` (equivalently row covectors multiply by `T`).

## Boundary / refusals

- `COORDINATE DELTA != OCCURRENCE DELTA`.
- `BASIS CHANGE != HISTORICAL CHANGE`.
- `COVARIANCE != CAUSATION`.
- `INVARIANT OBJECTIVE VALUE != SAME EVIDENCE`.
- `ISOMORPHIC FEASIBLE GEOMETRY != IDENTICAL REAL-WORLD SYSTEM`.
- `TRANSFORMED NORMAL != CAUSAL DIRECTION`.
- `DUAL CERTIFICATE != AUTHORITY`.
- `ALGEBRAIC EQUIVALENCE != SEMANTIC EQUIVALENCE` outside the declared mathematical scope.

## Scope / HOLD

This slice adds only:

- one bounded stdlib exact kernel;
- one frozen fixture;
- one focused test file;
- this research receipt.

No general matrix package, LP solver, coordinate registry, tensor system, automatic basis inference, geometric canonicalizer, evidence semantics, or public schema is added.

Explicit HOLD: `coordinate_map@1`, `basis@1`, `covector@1`, `transport@1`, `equivalence@1`, `canonical_coordinates@1`.

## Next frontier

The next pressure should leave linear coordinate changes and ask which objects survive **nonlinear reparameterization**. For a smooth bijection `x = phi(z)`, first-order covectors transform through the Jacobian transpose, but Hessians do not transform as ordinary rank-2 tensors without an additional connection/critical-point condition because second derivatives of `phi` appear.

That creates a sharper hostile boundary:

`FIRST-ORDER COVARIANCE DOES NOT LICENSE SECOND-ORDER TENSOR LANGUAGE UNDER NONLINEAR REPARAMETERIZATION.`

A bounded next specimen could freeze a one-dimensional nonlinear coordinate map and show an identical scalar function whose first derivative obeys the chain rule while the naive Hessian-transformation rule fails away from a critical point.
