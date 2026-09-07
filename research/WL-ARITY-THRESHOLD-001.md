# WL-ARITY-THRESHOLD-001

## Question

Can a fixed pair of finite carriers remain indistinguishable under a declared 3-point Weisfeiler-Leman probe while becoming distinguishable as soon as the probe arity is raised to four?

## Frozen carriers

Use the classical non-isomorphic strongly regular pair with parameters `(16,6,2,2)`:

- the `4 x 4` rook graph / Hamming graph `H(2,4)`;
- the Shrikhande graph.

The exact edge lists are frozen in `tests/fixtures/wl_arity_threshold_001.json`.

## Exact result

The bounded evaluator runs the standard tuple-color refinement grammar jointly across both carriers so color identifiers remain comparable.

For `k=3`:

- initial atomic tuple types have the same histogram;
- one refinement round introduces no additional joint color classes;
- both graphs have the identical stable color-class-size multiset
  `(16,96,96,96,144,144,144,192,288,288,288,576,576,576,576)`;
- therefore this declared 3-dimensional WL probe does not distinguish the pair.

For `k=4`:

- the initial atomic 4-tuple type histograms already differ;
- no refinement round is required;
- this is consistent with the simpler structural witness that the rook graph contains `K4` subgraphs while the Shrikhande graph does not.

## Earned distinction

`THREE-POINT REFINEMENT CAN COLLIDE WHILE FOUR-POINT ATOMIC TYPE ALREADY SEPARATES.`

`KEEP THE PROBE ARITY IN THE RECEIPT.`

The delta here is produced by a **decoder/probe change** from 3-tuples to 4-tuples. The carriers are held fixed.

## Documented mathematics

- The Shrikhande graph and `4 x 4` rook graph are the two non-isomorphic strongly regular graphs with parameters `(16,6,2,2)`; they share the same standard spectral/two-point data.
- Published graph-learning and simplicial-network literature uses this pair as an example that 3-WL does not distinguish while 4-clique structure does.
- The broader Weisfeiler-Leman hierarchy is a family of increasingly expressive bounded-tuple refinement procedures; increasing dimension changes the information available to the comparison.

Useful references:

- Bailey & Cameron, *Bulletin of the London Mathematical Society* 43 (2011), DOI `10.1112/blms/bdq096` — coherent configurations / graph-isomorphism neighborhood.
- Egrot & Hirsch, *Journal of Graph Theory* 99 (2021), DOI `10.1002/jgt.22741` — explicit treatment of `k`-dimensional Weisfeiler-Leman as a hierarchy and finite non-isomorphic pairs not distinguished at bounded dimension.
- Message-passing simplicial-network literature uses the rook/Shrikhande pair specifically as a 3-WL-equivalent example separated by 4-clique structure.

The exact stable 3-WL histogram and round-0 4-point separation in this slice are independently recomputed from the frozen edge lists; no claim is made that the cited papers contain these exact receipt values.

## Explicit refusals

- `WL INDISTINGUISHABLE != ISOMORPHIC`.
- `HIGHER ARITY != MORE TRUE`.
- `4-CLIQUE != FOUR-WAY CAUSAL COALITION`.
- `REFINEMENT POWER != EVIDENCE STRENGTH`.
- `DECODER DELTA != OCCURRENCE DELTA`.
- `FAILURE TO DISTINGUISH != EVIDENCE OF HIDDEN IDENTITY`.

## Scope / HOLD

This is a bounded research kernel only. It does not promote `wl@1`, `arity@1`, `isomorphism@1`, `coherent_configuration@1`, `association_scheme@1`, or any graph-identity / evidence / authority operator.

## Next frontier

The stronger next question is not simply `k=5`. Build a small finite **probe-poset** whose nodes are declared probe families and whose edges mean strict information refinement. Then receipt the *minimal* probe change that first creates a delta, rather than silently equating computational expense, relational arity, or discrimination with truth.
