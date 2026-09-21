# MARKOV-LUMPABILITY-RESIDUAL-001

Status: research-only, stacked on open `MARKOV-LUMPABILITY-001` (#161).

## Question

When exact strong lumpability fails, can Dogram show the stochastic delta without converting a numerical tolerance into semantic equivalence?

## Frozen specimen

Partition `{a,b}->A`, `{c}->B`. Projected transition rows are

- `a: (A,B)=(1/2,1/2)`
- `b: (A,B)=(1/4,3/4)`

They have the same positive quotient support but differ by signed block delta `(1/4,-1/4)`. Therefore

`max_B |P(a,B)-P(b,B)| = 1/4`

and

`TV(P_A(a,.), P_A(b,.)) = (1/2) sum_B |P(a,B)-P(b,B)| = 1/4`.

The kernel retains the concrete pair, source block, signed block deltas, target block attaining the largest discrepancy, maximum block discrepancy, and total-variation residual. Exact rational arithmetic is used throughout.

## Declared tolerance control

A caller may supply a tolerance `epsilon`. For the frozen specimen, `epsilon=1/4` returns `within_declared_tolerance=True`, while exact `strong_lumpable` remains `False`. At `epsilon=1/5`, the tolerance check fails. The threshold is declaration data, not an inferred semantic boundary.

## Seal

**SMALL STOCHASTIC RESIDUAL != EXACT LUMPABILITY; DECLARED TOLERANCE != SEMANTIC EQUIVALENCE.**

## Documented mathematics

Strong lumpability requires equal total transition probability from representatives in one source block into each target block. Regnier & Shechter (2013), DOI `10.1002/sim.5808`, states this blockwise criterion. Bušić & Fourneau (2011), DOI `10.1002/nla.824`, treats non-ordinary-lumpable aggregation with componentwise lower/upper bounds. Total variation is a standard row-discrepancy metric; recent Markov perturbation work explicitly bounds row perturbations in total variation (Vial & Subramanian 2025, DOI `10.1002/rsa.70007`).

Wolfram independently evaluated the frozen projected rows and returned signed difference `{1/4,-1/4}`, maximum block discrepancy `1/4`, and total variation `1/4`.

## Dogram inference

The residual is useful as a receipt of *how exact descent fails*. It is not a permission to identify representatives. A tolerance only answers the explicitly declared numerical predicate `residual <= epsilon`.

## Refusals

- positive probability != occurrence
- small residual != exact lumpability
- within tolerance != semantic equivalence
- transition probability != evidentiary confidence
- residual magnitude != causal distance
- approximate stochastic agreement != historical identity

No public operator, runtime action, evidence pipeline, automatic threshold, or authority promotion is introduced.
