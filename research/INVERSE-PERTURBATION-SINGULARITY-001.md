# INVERSE-PERTURBATION-SINGULARITY-001

Status: bounded research only. No public operator promotion.

## Frozen family

For every integer `n>=2`, with Euclidean operator norm, declare

`A_n = diag(1,1/n)` and `B_n = diag(1,2/n)`.

Both are invertible and both have operator norm exactly `1`.

Exact forward delta:

`||A_n-B_n||_2 = 1/n -> 0`.

Exact inverses:

`A_n^-1 = diag(1,n)` and `B_n^-1 = diag(1,n/2)`.

Exact inverse delta:

`||A_n^-1-B_n^-1||_2 = n/2 -> infinity`.

Therefore the amplification ratio is

`||A_n^-1-B_n^-1||_2 / ||A_n-B_n||_2 = n^2/2`.

The smallest singular values, hence the spectral-norm distances to the singular set, are respectively `1/n` and `2/n`. The forward maps approach each other while both approach rank loss.

The exact inverse-difference identity closes:

`B^-1-A^-1 = B^-1(A-B)A^-1`.

## Earned seals

- `SMALL FORWARD-OPERATOR DELTA != SMALL INVERSE DELTA NEAR RANK LOSS.`
- `KEEP THE DISTANCE TO SINGULARITY IN THE RECEIPT.`
- `NORMALIZED FORWARD NORM != UNIFORM PERTURBATION STABILITY.`
- `LOCAL CONTINUITY ON GL(n) != UNIFORM CONTINUITY UP TO THE SINGULAR BOUNDARY.`

## Documented mathematics

- Jain, Sah & Sawhney (2022), DOI `10.1112/blms.12561`, recall `sigma_min(A)=||A^-1||^-1` for invertible matrices and the condition-number role of the extreme singular values.
- Clotet, Magret & Su (2013), DOI `10.1155/2013/948147`, explicitly invoke the Eckart-Young-Mirsky theorem: in spectral norm the minimum distance from a full-rank matrix to a lower-rank matrix equals its smallest singular value.
- Auras et al. (2024), DOI `10.1002/gamm.202470003`, describe finite-dimensional inverse ill-conditioning through the ratio of largest to smallest singular value and reciprocal singular-value amplification.
- Petkov (2024), DOI `10.1002/nla.2582`, situates small-data perturbations and condition-dependent output perturbations within standard matrix perturbation analysis.

No source is claimed to contain this exact diagonal Dogram fixture.

## Dogram inference

The stability margin consumed by an inverse/reconstruction calculation is part of the receipt. A small delta in the forward representation does not by itself license a small delta claim downstream when the admissible family approaches a singular boundary.

## Refusals

- `SMALL OPERATOR DELTA != SMALL OCCURRENCE DELTA`.
- `LARGE INVERSE DELTA != LARGE EVIDENCE DELTA`.
- `NEAR SINGULAR != FALSE`.
- `DISTANCE TO SINGULARITY != DISTANCE TO TRUTH`.
- `CONDITION NUMBER != AUTHORITY WEIGHT`.
- `NUMERICAL SENSITIVITY != CAUSAL SENSITIVITY`.
- `RANK LOSS != HISTORICAL LOSS`.
- `PERTURBATION BOUND != SEMANTIC BOUND`.

## Scope / HOLD

This slice adds only a stdlib exact diagonal kernel, frozen fixture, focused tests, and this receipt. It does not add a general SVD engine, matrix inverse API, perturbation solver, regularizer, evidence semantics, causal semantics, or authority semantics.

HOLD: `distance_to_singularity@1`, `inverse_stability@1`, `condition_number@1`, `perturbation@1`, `regularize@1`, `rank_loss@1`.

## Next frontier

The strongest next pressure is discontinuity of the Moore-Penrose pseudoinverse across rank change. A family can converge exactly to a rank-deficient matrix while pseudoinverses diverge, yet if rank is locally fixed the pseudoinverse is continuous. Candidate seal:

`PSEUDOINVERSE CONTINUITY REQUIRES A RANK-STRATUM RECEIPT.`
