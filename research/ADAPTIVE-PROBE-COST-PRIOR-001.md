# ADAPTIVE-PROBE-COST-PRIOR-001

Status: bounded research specimen. No public operator promotion.

## Question

Can the same frozen target, probe costs, and two candidate policies have a stable worst-case cost order while their expected-cost order changes solely because the declared prior changes?

## Frozen carrier and target

Carrier:

`X = {a,b,c,d}`

Target labels:

- `a -> 1`
- `b -> 1`
- `c -> 0`
- `d -> 0`

Both candidate policies compute exactly this same target.

## Policy A: adaptive

Root probe cost: `1`.

- state `a` terminates after the root;
- states `b,c,d` consume a second branch probe of cost `2`.

Exact state-cost vector:

`(a,b,c,d) = (1,3,3,3)`.

Worst-case cost:

`3`.

## Policy B: fixed

One-shot probe cost: `2` on every state.

Exact state-cost vector:

`(a,b,c,d) = (2,2,2,2)`.

Worst-case cost:

`2`.

Thus worst-case comparison needs no prior:

`fixed < adaptive`.

## Prior-sensitive expected cost

Expected cost consumes an explicitly declared normalized distribution on the carrier.

For

`pi_heavy(a,b,c,d) = (3/4,1/12,1/12,1/12)`:

- adaptive: `3/2`;
- fixed: `2`;
- therefore adaptive has lower expected cost.

For the uniform prior

`pi_uniform(a,b,c,d) = (1/4,1/4,1/4,1/4)`:

- adaptive: `5/2`;
- fixed: `2`;
- therefore fixed has lower expected cost.

Nothing about the carrier, target, policies, path costs, or worst-case order changed. Only the declared prior changed.

## Earned distinctions

`EXPECTED COST REQUIRES A DECLARED DISTRIBUTION; WORST-CASE COST DOES NOT.`

`SAME POLICY + SAME COSTS + SAME TARGET != SAME EXPECTED-COST ORDER AFTER PRIOR CHANGE.`

`A PRIOR-WEIGHTED ADVANTAGE IS A CONDITIONAL RECEIPT, NOT A UNIVERSAL PREFERENCE.`

## Literature neighborhood

- Daldal, Gamzu, Segev & Unluyurt (2016), *Naval Research Logistics*, DOI `10.1002/nav.21693`: sequential testing policies minimize expected testing cost given a-priori probabilistic information on component states.
- Bennett (1987), *Applied Stochastic Models and Data Analysis*, DOI `10.1002/asm.3150030407`: weighted decision trees and mean testing cost.
- Magniez et al. (2016), *Random Structures & Algorithms*, DOI `10.1002/rsa.20598`: decision-tree cost is defined per input as queries consumed along its path, providing the finite path-cost basis used here.
- Tatsuoka & Ferguson (2003), *JRSS B*, DOI `10.1111/1467-9868.00377`: sequential experiment selection under a finite Bayesian state space.

No claim is made that these papers contain this exact four-state fixture or Dogram interpretation.

## Dogram boundary

This specimen receipts a decoder/policy-cost distinction only.

Explicit refusals:

- `PRIOR != EVIDENCE`;
- `PRIOR MASS != OCCURRENCE FREQUENCY` unless independently sourced and declared;
- `LOWER EXPECTED COST != MORE TRUE`;
- `LOWER WORST-CASE COST != PREFERRED`;
- `BAYES-AVERAGED ADVANTAGE != UNIVERSAL ADVANTAGE`;
- `ADAPTIVE BRANCH != HISTORICAL BRANCH`;
- `POLICY != AUTHORITY`;
- `COST ORDER != EVIDENCE ORDER`.

## Verification

The exact arithmetic is rational:

- heavy-a adaptive: `(3/4)*1 + (1/4)*3 = 3/2`;
- uniform adaptive: `(1/4)*1 + (3/4)*3 = 5/2`;
- fixed expected cost is always `2` for any normalized prior because every state costs `2`;
- worst-case costs are `3` and `2`, respectively.

Fixture and focused tests were committed before the production kernel. The test-only head failed CI at the unit-test stage before `dogram.adaptive_probe_cost` existed.

## HOLD

No `policy@1`, `prior@1`, `expected_cost@1`, `worst_case@1`, `bayes@1`, `decision_tree@1`, utility semantics, evidence semantics, or automatic policy choice.

## Next frontier

Move from one fixed prior to a declared **set of admissible priors**. Compare Bayes-optimal, minimax, and minimax-regret receipts without silently selecting one decision criterion. Candidate seal:

`UNCERTAINTY ABOUT THE PRIOR IS A NEW INPUT, NOT PERMISSION TO INVENT ONE.`
