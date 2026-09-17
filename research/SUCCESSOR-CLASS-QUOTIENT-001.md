# SUCCESSOR-CLASS-QUOTIENT-001

Status: bounded research specimen. Authority: none. Public operator: none.

## Question

Can a state quotient preserve exactly which declared operations are enabled while failing to preserve where those operations can lead?

## Frozen specimen

Collapse `ready` and `blocked` into quotient class `pending`. Keep `green` and `hold` distinct.

- `ready --advance--> green`
- `blocked --advance--> hold`

Both members of `pending` enable exactly `{advance}`, so enabled-label membership factors through the quotient.

Their `advance` successor-class sets differ:

- `ready`: `{green}`
- `blocked`: `{hold}`

Therefore the one-step successor relation does not factor exactly through the same collapse.

## Delta

`enabled_factors = true`

`successor_factors(advance) = false`

`exact_one_step_factors = false`

Seal:

> SAME ENABLED OPERATIONS != SAME EXECUTABLE FUTURES.

> PRESERVING THE VERB DOES NOT NECESSARILY PRESERVE WHERE THE VERB CAN TAKE YOU. KEEP THE SUCCESSOR RECEIPT.

## Mathematics / provenance

For a labeled transition system, transition behavior is carried by the labeled transition relation, not merely the set of labels enabled at a state. Simulation/bisimulation conditions compare successor behavior under matching labels. See Yu, Yang, Wu & Song (2015), *Approximate Analyzing of Labeled Transition Systems*, DOI `10.1155/2015/963597`, and Pola, Pepe & Di Benedetto (2014), *Symbolic models for time-varying time-delay systems via alternating approximate bisimulation*, DOI `10.1002/rnc.3204`.

Fu, Fan, An & Qiao (2026), DOI `10.1002/asjc.70082`, gives an explicit existential quotient transition construction: a quotient transition exists when some representative transition connects the two classes. That is a lawful declared quotient semantics, but it is not the same claim as exact representative-independent successor behavior.

Wolfram Language independently checked the finite hostile control: the two collapsed states have equal enabled-label sets `{a}` and unequal successor-class sets `{G}` and `{H}`.

## Boundary / refusals

- ENABLED != OCCURRED.
- EXECUTABLE != EXECUTED.
- SUCCESSOR CLASS != HISTORICAL DESTINATION.
- EXACT ONE-STEP FACTORIZATION != BISIMULATION.
- EXISTENTIAL QUOTIENT EDGE != UNIVERSAL QUOTIENT EDGE.
- STRUCTURAL PRESERVATION != EVIDENCE, TRUTH, OR AUTHORITY.

## Next frontier

Freeze a nondeterministic carrier where all representatives have the same enabled labels and the same *union* of quotient successors, while representative-wise successor sets differ. Compare existential/may, universal/must, and bisimulation-style matching explicitly. This should locate the next information-loss boundary between aggregate successor surfaces and representative-stable transition structure.
