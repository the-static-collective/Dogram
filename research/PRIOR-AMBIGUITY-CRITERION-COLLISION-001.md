# PRIOR-AMBIGUITY-CRITERION-COLLISION-001

Status: research-only / HOLD

Base: `main@f09a1702c3904b8f91635b5a84e0c763a7967d88`

## Question

Can one frozen finite policy-cost table produce different unique winners under (1) Bayes expected cost for one declared prior, (2) robust minimax expected cost over a declared ambiguity set of priors, and (3) minimax regret over that same ambiguity set?

Yes.

## Frozen specimen

States: `s1,s2,s3`.

Policy state-cost vectors:

- `A=(2,2,7)`
- `B=(1,7,1)`
- `C=(5,5,1)`

Declared Bayes prior:

`pi0=(1/2,1/3,1/6)`.

Exact Bayes expected costs:

- `A=17/6`
- `B=3`
- `C=13/3`

Therefore the unique Bayes winner under `pi0` is `A`.

Declared ambiguity-prior set:

- `p1=(3/5,1/5,1/5)`
- `p2=(1/5,3/5,1/5)`
- `p3=(1/5,1/5,3/5)`

Exact maximum expected costs across that declared set:

- `A=5`
- `B=23/5`
- `C=21/5`

Therefore the unique robust minimax-expected-cost winner is `C`.

For minimax regret, regret at each declared prior is computed relative to the cheapest policy at that same prior. Exact maximum regrets are:

- `A=14/5`
- `B=8/5`
- `C=2`

Therefore the unique minimax-regret winner is `B`.

The state set, policies, and cost table never move. The criterion/prior object does.

## Exact distinction

`SAME STATES + SAME POLICIES + SAME COST TABLE != SAME WINNER AFTER CRITERION CHANGE.`

`BAYES(pi0) -> A`

`ROBUST MINIMAX EXPECTED(P) -> C`

`MINIMAX REGRET(P) -> B`

## Documented mathematics

Bayes risk/expected loss consumes a specified probability distribution. Robust Bayes/minimax formulations evaluate rules against classes or sets of priors. Minimax regret instead evaluates loss relative to the state- or distribution-specific best achievable rule, then minimizes the worst such regret. These are distinct decision criteria and need not agree.

Relevant literature:

- Andrews & Shapiro (2021), *Econometrica*, DOI `10.3982/ECTA18155` — robust Bayes/minimax evaluation over a class of priors and explicit contrast between weighted-average and maximum-risk criteria.
- Manski (2021), *Econometrica*, DOI `10.3982/ECTA17985` — maximin and minimax-regret criteria under uncertainty; they agree only in special cases and differ generally.
- Chen & Xie (2021), *Production and Operations Management*, DOI `10.1111/poms.13515` — ambiguity sets combined with distinct robust decision criteria, including worst-case expectation and minimax regret.
- Hansen & Sargent (2023), *Journal of Applied Econometrics*, DOI `10.1002/jae.3010` — decision theory under ambiguity about priors/models.

No claim is made that these papers contain this exact three-state fixture or the Dogram interpretation below.

## Dogram inference

The decision criterion and every prior object it consumes belong in the calculation receipt. A winner produced under one criterion is conditional on that criterion and its declared inputs. Replacing Bayes expectation by robust minimax expectation or minimax regret is a decoder/decision-rule delta, not an evidence delta.

Candidate seals:

- `UNCERTAINTY ABOUT THE PRIOR IS A NEW INPUT, NOT PERMISSION TO INVENT ONE.`
- `THE DECISION CRITERION IS PART OF THE RECEIPT.`
- `A CRITERION WINNER IS CONDITIONAL ON THE CRITERION; IT IS NOT A UNIVERSAL PREFERENCE.`
- `BAYES, ROBUST MINIMAX, AND MINIMAX REGRET CAN DISAGREE WITHOUT ANY ARITHMETIC ERROR.`

## Explicit refusals

- `BAYES WINNER != TRUE`
- `ROBUST WINNER != TRUE`
- `MINIMAX REGRET WINNER != PREFERRED`
- `PRIOR SET != EVIDENCE`
- `PRIOR MASS != OCCURRENCE FREQUENCY` unless independently sourced and declared
- `ROBUSTNESS != AUTHORITY`
- `REGRET != HISTORICAL REMORSE`
- `CRITERION DELTA != EVIDENCE DELTA`

## Verification / provenance

Fixture and focused tests precede the production kernel.

- test-only head `78a037b15530c2beef1a3226767ab150b39a5a02`: Dogram CI #537 RED at Unit tests with the expected `ModuleNotFoundError: No module named 'dogram.prior_ambiguity_criterion_collision'`;
- kernel head `7e950651fd28be75b03b8220db52295f8b38f070`: Dogram CI #538 GREEN.

The kernel uses only exact `fractions.Fraction` arithmetic and finite enumeration over the supplied prior set. It does not estimate a prior, choose a criterion, or infer semantics.

Wolfram was attempted as an independent check but its connector returned an upstream 404, so no Wolfram-verification claim is made.

## HOLD

No `prior_set@1`, `robust_bayes@1`, `minimax@1`, `regret@1`, `criterion@1`, `policy_choice@1`, utility semantics, evidence semantics, or authority semantics are promoted.

## Next frontier

Move from a finite list of priors to an explicitly declared convex ambiguity polytope and receipt its decision geometry. Expected cost is affine in the prior, so pairwise policy ties cut the probability simplex by affine hyperplanes. The bounded question is whether the Bayes-optimality cells, least-favorable-prior witnesses, and regret-optimality cells expose a useful new distinction without promoting any cell to a real-world probability claim.

Candidate next seal:

`A WINNER IS A CELL OF A DECLARED DECISION GEOMETRY, NOT A PROPERTY OF THE POLICY ALONE.`
