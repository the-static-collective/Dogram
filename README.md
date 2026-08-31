# Dogram

Dogram is a deterministic, offline calculation lab for pressure-testing graph, relation, and mathal specimens while preserving explicit receipts.

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

Dogram does not mint evidence, support, truth, historical identity, causal meaning, or authority.

```text
TRUST MAY OPEN THE BRIDGE. IT MAY NOT CERTIFY THE BRIDGE.
PRESENCE IS NOT CONSUMPTION.
GRAPH PATH != CAUSAL PATH.
GRAPH REACHABILITY != HISTORICAL OCCURRENCE.
```

## Phase A operator floor

Dogram v0 exposes four versioned calculation operators:

- `delta@1` — compare an ordered typed boundary trace and report the first difference.
- `rectangle@1` — compute a 2×2 mixed difference for numeric cells or an equivalence interaction for opaque cells.
- `ablate@1` — remove exactly one graph node/edge and report reachability changes.
- `reach@1` — apply exactly one explicit graph mutation and report before/after path witnesses.

All public specimens use `dogram.specimen/v0`. Calculation receipts use `dogram.receipt/v0`.

## MutatedMathal lowering

```text
MUTATED MATHAL
    -> choose one discriminator
    -> choose the smallest Dogram operator
    -> declare typed specimen
    -> run calculation
    -> retain calculation receipt
    -> send receipt to ALEX / human pressure
```

One mathal may lower to several Dogram specimens. A Dogram `OK` means the declared calculation executed successfully; it is not promotion of the mathal or its interpretation.

Runnable examples:

```bash
python -m dogram.cli examples/mutated_mathals/interest-mediated-support.json
python -m dogram.cli examples/mutated_mathals/hidden-world-policy-rectangle.json
python -m dogram.cli examples/mutated_mathals/trust-withdrawal.json
python -m dogram.cli examples/mutated_mathals/same-surface-different-history.json
```

## Destination architecture

Phase A is the independent oracle floor for **Dogram Ω**, the approved metaoscillatory runtime. Later reviewed slices add an inert Mathal VM, reified execution, bounded META proposals, a phase gate, explicit branching, and bootstrap peeling. The direct Python operators remain independent conformance witnesses during that migration.

The first bounded Ω cycle is implemented as an explicit `EXEC -> REIFY -> META -> PROPOSAL -> PHASE GATE -> EXEC` path. Its META surface can only construct a caller-declared `remove_step` proposal from inert execution data; structural admission remains separate from behavioral comparison, and the public four-operator calculation floor is unchanged.

Dogram also contains an internal finite research kernel for `PRODUCTIVE-DESYNC-001 / TRANSVERSE-GENERATORS-001`. It receipts synchronized quotient sheets, declared bounded cut history, and generated reachability closure while preserving `ONE CROSSING != GENERATOR CLOSURE` and `POTENTIAL REACHABILITY != ACTUAL HISTORY`. This kernel adds no public operator, truth/evidence semantics, or automatic experiment selection.

See `docs/superpowers/specs/2026-08-28-dogram-metaoscillatory-runtime-design.md`.
