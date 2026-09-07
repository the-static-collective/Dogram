# PROBE-PARTITION-REFINEMENT-001

Status: bounded research specimen. No public operator promotion.

## Question

When several deterministic probes are available on the same finite carrier set, can Dogram receipt **which declared question first creates a delta** without silently turning “stronger probe” into “truer result”?

## Documented mathematics

A deterministic probe `f : X -> Y` induces an equivalence relation on `X` by

`x ~_f x'  iff  f(x) = f(x')`.

Equivalence relations correspond to partitions. Partitions of a finite set form a lattice under refinement. If partition `pi_q` refines `pi_p`, then `q` retains at least the distinctions retained by `p`. In the deterministic finite case this is equivalent to a factorization witness: there exists a map `h` on observed outputs with

`p = h o q`.

The implementation checks that criterion exactly: equal `q` outputs must always imply equal `p` outputs, and when they do it returns the finite output map `h`.

Peer-reviewed background:

- Kaldmae, Kotta, Shumsky & Zhirabok, *International Journal of Robust and Nonlinear Control* 25 (2014), DOI `10.1002/rnc.3265` — uses the partial order/lattice of state partitions, explicitly interprets refinement as containing the same or more state information, and gives incomparable partition examples.
- Eberhard, Manners & Mrazovic, *Proceedings of the London Mathematical Society* 127 (2023), DOI `10.1112/plms.12538` — records standard partition-lattice language: refinement/coarsening, meet/join, discrete and indiscrete partitions.
- Tatsuoka & Ferguson, *Journal of the Royal Statistical Society B* 65 (2003), DOI `10.1111/1467-9868.00377` — treats finite experiments as inducing partitions of a finite state set and studies experiment selection on a poset.

No claim is made that these papers contain this exact four-state fixture or Dogram interpretation.

## Frozen exact specimen

Carrier set:

`X = {a,b,c,d}`.

Declared probes:

- `coarse = (all, all, all, all)`;
- `vertical = (L, L, R, R)`;
- `diagonal = (U, D, U, D)`;
- `joint = (LU, LD, RU, RD)`.

Induced partitions:

- `coarse : {abcd}`;
- `vertical : {ab | cd}`;
- `diagonal : {ac | bd}`;
- `joint : {a | b | c | d}`.

Exact cover relations, written `stronger -> weaker`, are:

- `vertical -> coarse`;
- `diagonal -> coarse`;
- `joint -> vertical`;
- `joint -> diagonal`.

`vertical` and `diagonal` are incomparable: neither factors through the other.

For target pair `(a,d)`:

- `coarse` does not separate;
- `vertical` separates;
- `diagonal` separates;
- `joint` separates.

The minimal separating probes in the declared family are therefore

`{vertical, diagonal}`.

They are both minimal and mutually incomparable.

Exact factorization witnesses include:

- `joint -> vertical`: `LU,LD -> L` and `RU,RD -> R`;
- `joint -> diagonal`: `LU,RU -> U` and `LD,RD -> D`.

No factorization witness exists between `vertical` and `diagonal` in either direction.

## Dogram inference

`INFORMATION ORDER IS PARTIAL, NOT TOTAL.`

`A MINIMAL QUESTION THAT CREATES A DELTA NEED NOT BE UNIQUE.`

`SHOW WHICH QUESTION MADE THE DELTA VISIBLE, AND KEEP INCOMPARABLE MINIMAL QUESTIONS IN THE RECEIPT.`

The carrier and target pair remain fixed. Only the declared probe changes. Separation is therefore a decoder/probe fact inside this finite family, not an occurrence delta.

## Explicit refusals

- `REFINES != MORE TRUE`;
- `SEPARATES != PROVES`;
- `MINIMAL PROBE != CHEAPEST PROBE` unless a cost model is separately declared;
- `INCOMPARABLE PROBES != CONTRADICTORY PROBES`;
- `PARTITION CELL != CAUSAL CLASS`;
- `FACTORING THROUGH != EVIDENCE DERIVATION`;
- `PROBE DELTA != OCCURRENCE DELTA`;
- `MORE INFORMATION != MORE AUTHORITY`.

## Speculation / HOLD

A later Dogram layer could attach **declared costs** or capability requirements to probe nodes and search for Pareto-minimal separators. That would create a product order between information and cost, but this specimen does not earn such an operator and does not assume that computational expense, relational arity, evidence strength, or truth are monotone with refinement.

No `probe@1`, `information_order@1`, `partition@1`, `minimal_separator@1`, `experiment@1`, or authority/evidence operator is promoted.

## Verification contract

The frozen fixture and focused tests recompute:

1. all induced partitions;
2. exact cover relations in the declared finite probe family;
3. incomparable `vertical` / `diagonal` refinement failures;
4. explicit factorization witnesses for lawful refinements;
5. the separating probes for `(a,d)`;
6. the two incomparable minimal separators.

The kernel is stdlib-only and bounded to deterministic finite probes with hashable outputs. Duplicate induced partitions are rejected so probe names remain distinct nodes of the analyzed poset.

## Seal

**SHOW THE DELTA — AND SHOW WHICH DECLARED QUESTION MADE IT VISIBLE.**
