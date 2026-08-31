# Dogram Ω-CYCLE-001 — Result-Equivalence Amendment

**Date:** 2026-08-30  
**Status:** APPROVED IN CHAT · IMPLEMENTATION-BINDING AMENDMENT  
**Amends:** `docs/superpowers/specs/2026-08-30-dogram-omega-cycle-001-design.md`

## Decision

Replace the original required hostile fixture `OMEGA-RESULT-CHANGED-001` with `OMEGA-EXECUTION-CHANGED-001`.

Under the current pure acyclic Mathal VM and the Ω-CYCLE-001 gate, a `remove_step` proposal is admissible only when the removed step has no surviving reference from any later step or the final result. Therefore an admitted `remove_step` cannot lawfully change the declared final result unless the runtime contains hidden side effects or undeclared state.

The corrected hostile control is:

```text
OMEGA-EXECUTION-CHANGED-001

GATE: ADMIT
FINAL RESULT: IDENTICAL
PROGRAM DIGEST: DIFFERENT
EXECUTION RECEIPT: DIFFERENT
```

At least one execution-history surface must differ, such as:

- step trace;
- fuel remaining;
- consumed-input provenance;
- execution digest.

Hard laws:

```text
RESULT EQUIVALENCE != EXECUTION EQUIVALENCE
GATE ADMIT != RECEIPT IDENTITY
```

The gate remains structural only. This amendment does not broaden the proposal grammar and does not add side effects, hidden state, semantic judgment, or a new public operator.

All other Ω-CYCLE-001 requirements remain unchanged.
