# COUPLING-WITNESS-001 — scalar disagreement does not determine the coupling

Status: bounded research specimen; no public operator or runtime promotion.

## Question

After MARKOV-RESIDUAL-PROPAGATION-001, should a scalar total-variation/disagreement receipt be treated as if it identified the pathwise coupling that produced it? No.

A coupling of finite laws `p,q` is a joint law `pi(i,j)` whose row and column marginals are `p,q`. The coupling inequality gives `TV(p,q) <= Pr[X != Y]`; a maximal coupling attains equality. This scalar constraint does not in general determine the joint law.

## Frozen exact specimen

Use the uniform law `u=(1/3,1/3,1/3)` on `{0,1,2}`. Three exact rational couplings of `u` with itself are frozen:

1. identity: mass `1/3` on `(0,0),(1,1),(2,2)`;
2. swap01: mass `1/3` on `(0,1),(1,0),(2,2)`;
3. swap12: mass `1/3` on `(0,0),(1,2),(2,1)`.

All have the same left and right marginals and hence `TV(u,u)=0`. The two swap couplings also have exactly the same disagreement probability `2/3`, but their joint supports and coupling matrices differ. The identity coupling is the maximal control with disagreement `0=TV`.

Therefore:

> **SAME MARGINALS + SAME SCALAR DISAGREEMENT != SAME COUPLING WITNESS.**

The delta lives in the joint transport/correlation structure, not in either marginal or the scalar disagreement probability.

## Documented mathematics

The coupling inequality and maximal-coupling identity are standard: for any coupling, `Pr[X != Y] >= d_TV(p,q)`, with equality for a maximal coupling. Jacob, O'Leary & Atchade, *JRSS B* 82(3), 2020, DOI `10.1111/rssb.12336`, reviews maximal coupling and its use in Markov-chain analysis. Wolfram's distribution documentation independently distinguishes a multivariate joint distribution from its marginals; changing dependence while holding marginals fixed is the basic copula pattern.

## Dogram inference

A scalar error envelope can bound disagreement without receipting which state pairs carry the disagreement mass. If pathwise provenance matters, preserve an explicit coupling matrix/support (or another declared witness), not merely `TV` or `Pr[X != Y]`.

This does **not** imply that one coupling is historically real, causal, evidentiary, or semantically preferred.

## Refusal boundary

- coupling witness != occurrence
- joint mass != observed pair
- disagreement probability != evidentiary conflict
- maximal coupling != uniquely supplied coupling
- same scalar disagreement != same joint structure
- coupling choice != causal mechanism
- TV bound != pathwise history

## Reproduce

```bash
python research/coupling_witness_001.py
pytest -q tests/test_coupling_witness_001.py
```

Exact `Fraction` arithmetic only; no dependency is added.

## Next frontier

Transport geometry. Two couplings can share marginals and disagreement probability while assigning mass across very different geometric distances. A bounded optimal-transport specimen could compare Hamming disagreement with Wasserstein cost and ask what is lost when a coupling witness is collapsed to either scalar alone. Do not promote a metric choice into meaning: the ground cost itself is a declaration that must remain receipted.
