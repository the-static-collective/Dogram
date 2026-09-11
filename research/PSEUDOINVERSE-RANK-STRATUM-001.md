# PSEUDOINVERSE-RANK-STRATUM-001

Status: bounded research specimen; no public operator promotion.

## Question

Can two matrix families converge to the same limit while their Moore-Penrose pseudoinverses behave differently solely because one family crosses rank strata and the other does not?

## Frozen exact specimen

Let

`L = diag(1,0)`.

For integers `n>=1`, define

`A_n = diag(1,1/n)` and `B_n = diag(1+1/n,0)`.

Both converge to `L`, and in spectral norm both are exactly distance `1/n` from `L`.

For a real diagonal matrix the Moore-Penrose pseudoinverse is obtained by inverting each nonzero diagonal entry and leaving zeros at zero. Therefore

`L^+ = diag(1,0)`,

`A_n^+ = diag(1,n)`,

`B_n^+ = diag(n/(n+1),0)`.

Hence

`||A_n^+-L^+||_2 = n -> infinity`,

while

`||B_n^+-L^+||_2 = 1/(n+1) -> 0`.

The two forward families have the same declared limit and the same exact forward-distance schedule `1/n`, but different rank behavior:

- `rank(A_n)=2` while `rank(L)=1`;
- `rank(B_n)=rank(L)=1`.

Core seal:

`PSEUDOINVERSE CONTINUITY REQUIRES A RANK-STRATUM RECEIPT.`

Stronger finite specimen:

`SAME MATRIX LIMIT + SAME FORWARD DELTA SCHEDULE != SAME PSEUDOINVERSE LIMIT WHEN APPROACH RANK DIFFERS.`

## Documented mathematics

Wolfram Language documents the diagonal rule directly: `PseudoInverse` transposes a diagonal matrix, inverts the nonzero diagonal entries, and leaves zero entries zero. It also computes pseudoinverses from singular-value decomposition and identifies the Moore-Penrose equations.

Zhou & Soleymani (2014), DOI `10.1155/2014/498016`, quote a standard perturbation bound for Moore-Penrose inverses under rank and smallness hypotheses, explicitly retaining rank in the admissibility conditions.

Li, Xu & Wei (2011), DOI `10.1002/nla.838`, study stable perturbations of Moore-Penrose inverses and derive perturbation bounds under stability/acute-perturbation hypotheses.

These sources support the mathematical distinction. No source is claimed to contain this exact Dogram fixture.

Scholar Gateway query: finite-dimensional Moore-Penrose pseudoinverse continuity, constant rank, rank-changing perturbations, and perturbation bounds. Retrieved 10 passages from 10 articles spanning 2001-2025.

Consensus was attempted but the monthly search quota was exhausted; no Consensus citation is claimed.

## Dogram inference

This specimen earns only a receipt boundary:

- matrix convergence does not by itself license pseudoinverse convergence;
- rank stratum is part of the hypotheses required to interpret local perturbation continuity;
- equal forward perturbation size can conceal radically different reconstruction behavior.

It does not promote rank to evidence, truth, occurrence, causation, or authority.

## Refusals

`RANK DELTA != OCCURRENCE DELTA`

`PSEUDOINVERSE DELTA != EVIDENCE DELTA`

`RANK DEFICIENCY != FALSEHOOD`

`CONSTANT RANK != STABLE HISTORY`

`MATRIX LIMIT != HISTORICAL LIMIT`

`MINIMUM-NORM RECONSTRUCTION != TRUE RECONSTRUCTION`

`LEAST-SQUARES CANONICALITY != SEMANTIC CANONICALITY`

`NUMERICAL DISCONTINUITY != CAUSAL DISCONTINUITY`

## Scope / HOLD

This slice adds only:

- one bounded stdlib exact kernel;
- one frozen fixture;
- one focused test file;
- this receipt.

No general SVD engine, pseudoinverse API, rank detector, regularization policy, evidence semantics, causal semantics, or authority semantics.

Explicit HOLD: `pseudoinverse@1`, `rank_stratum@1`, `least_squares@1`, `minimum_norm@1`, `regularize@1`, `continuity@1`.

## Next frontier

The strongest next seam is regularization versus exact pseudoinversion near rank loss. For example, compare

`A_epsilon^+ = diag(1,1/epsilon)`

with a Tikhonov-regularized inverse factor

`R_{epsilon,lambda}=diag(1/(1+lambda), epsilon/(epsilon^2+lambda))`.

For fixed `lambda>0`, the unstable reciprocal channel is suppressed and the family remains bounded as `epsilon->0`, but the result is biased relative to exact inversion.

Candidate seal:

`STABILITY CAN BE PURCHASED BY CHANGING THE OPERATOR. KEEP THE REGULARIZATION PARAMETER AND BIAS IN THE RECEIPT.`
