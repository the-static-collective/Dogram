# MARKOV-RESIDUAL-PROPAGATION-001

Status: bounded research specimen. Authority: none. Public operator: none.

## Question

Does a small one-step total-variation discrepancy between two declared finite Markov kernels guarantee a small discrepancy after many steps?

No, not without additional contraction/mixing structure.

## Frozen hostile specimen

Reference kernel `P` is the two-state identity. Perturbed kernel `Q` leaks `epsilon=1/10` from state 0 to absorbing state 1 each step. The maximum rowwise TV discrepancy is exactly `1/10`. Starting from state 0, after `t` steps the exact TV discrepancy is

`1 - (9/10)^t`.

At `t=10` this is `6513215599/10000000000 > 3/5`, despite the one-step residual being only `1/10`. The Dobrushin coefficient of `P` is exactly 1, so there is no strict contraction to suppress accumulated perturbation.

## Computable envelope

For rowwise perturbation `epsilon = max_x TV(P(x,.),Q(x,.))` and Dobrushin coefficient `kappa(P)`, the elementary recurrence

`e_(t+1) <= epsilon + kappa e_t`

gives

`e_t <= epsilon * sum_{j=0}^{t-1} kappa^j`.

The kernel computes this envelope exactly with `Fraction`. A hostile noncontractive control has `kappa=1` and linear envelope `t*epsilon`. A contractive control with `kappa=0` stays at `epsilon`; an intermediate `kappa=1/2` specimen verifies the geometric envelope.

## Seal

**SMALL ONE-STEP RESIDUAL != UNIFORMLY SMALL MULTI-STEP RESIDUAL WITHOUT A CONTRACTION HYPOTHESIS.**

Secondary: **A LOCAL ERROR RECEIPT AND A PROPAGATION RECEIPT ARE DIFFERENT THINGS.**

## Documented mathematics

The Dobrushin contraction coefficient bounds total-variation contraction under a Markov kernel. A recent treatment states `TV(mu P, nu P) <= kappa TV(mu,nu)` and notes that ergodic chains may still have one-step coefficient `kappa=1`: DOI `10.1111/sjos.12686`. Markov perturbation literature studies how rowwise transition perturbations relate to distributional/stationary errors and emphasizes dependence on mixing/ergodicity structure: DOI `10.1002/rsa.70007`. Non-exact aggregation work supplies matrix bounds when ordinary lumpability fails: DOI `10.1002/nla.824`.

## Dogram inference

The prior one-step lumpability residual can be preserved as a local delta, but it must not be silently promoted into a finite-horizon behavioral guarantee. If a caller wants a horizon claim, receipt the horizon and the contraction/mixing assumption or compute the exact finite model.

## Refusals

- positive probability != occurrence
- transition probability != evidentiary confidence
- small residual != semantic equivalence
- finite-horizon bound != causal guarantee
- Dobrushin contraction != historical convergence
- bound != observed trajectory
- this finite declared model != a claim that Dogram's world is Markovian
