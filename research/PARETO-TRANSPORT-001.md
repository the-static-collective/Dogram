# PARETO-TRANSPORT-001 — vector cost before scalar preference

Status: bounded research slice; no public operator/runtime/authority promotion.

## Frozen specimen

Carry forward two fixed coupling cost vectors from TRANSPORT-METRIC-RANKING-001:

- `pi = (2,2)`
- `rho = (3,1)`

For minimization neither componentwise dominates the other. The mathematically complete answer at this layer is therefore `incomparable`, not a forced winner.

If a caller separately declares normalized nonnegative weights `(w,1-w)`, weighted costs are

- `C_w(pi)=2`
- `C_w(rho)=1+2w`.

Thus `rho` is cheaper for `w<1/2`, they tie at `w=1/2`, and `pi` is cheaper for `w>1/2`. Exact Wolfram evaluation independently reproduced these inequalities.

## Seal

**PARETO INCOMPARABLE != FAILURE TO CALCULATE.**

**SCALAR WINNER != INTRINSIC WINNER; IT IS CONDITIONAL ON THE DECLARED SCALARIZATION.**

## Documented mathematics

Multiobjective optimization naturally uses componentwise/Pareto order on vector-valued objectives. Weighted-sum scalarization introduces weights representing relative objective importance; positive-weight solutions are Pareto optimal under standard hypotheses, while weighted sums have known limitations on nonconvex Pareto fronts.

Provenance:
- Bevilacqua, Bosi, Zuanon & Reich (2018), *Multiobjective Optimization, Scalarization, and Maximal Elements of Preorders*, DOI 10.1155/2018/3804742.
- Rocha et al. (2015), *Entropy-Based Weighting for Multiobjective Optimization*, DOI 10.1155/2015/608325.
- Wei & Niethammer (2021), *The fairness-accuracy Pareto front*, DOI 10.1002/sam.11560.
- Wolfram Language documentation: multiobjective optimization generally need not have a unique optimum; weighted objectives encode relative importance.

## Dogram inference

A vector receipt can expose a genuine tradeoff without authority to collapse it. If a scalarization is later requested, its weights belong in the receipt as supplied calculation parameters. Changing weights may change the scalar winner without changing the feasible couplings or their vector costs.

## Refusals

- Pareto order != semantic preference.
- Incomparable != unknown.
- Weight != evidence.
- Weight != human worth.
- Scalar optimum != intrinsic optimum.
- Cost vector != ontology.
- Coupling != occurrence.
- Mathematical winner != authority to act.

No claim is made here about a universal best scalarization or about the semantics of the two metrics.
