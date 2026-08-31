# Dogram Ω-CYCLE-001 Implementation Plan Amendment

**Applies to:** `docs/superpowers/plans/2026-08-30-dogram-omega-cycle-001-implementation.md`

Replace every implementation/test requirement for `OMEGA-RESULT-CHANGED-001` with `OMEGA-EXECUTION-CHANGED-001`.

The replacement test must prove that a structurally lawful `remove_step` proposal can be admitted while:

```text
pre_result == post_result
pre_program_digest != post_program_digest
pre_execution_digest != post_execution_digest
```

and must assert at least one concrete execution-history difference such as step trace length, fuel remaining, or consumed-input provenance.

Do not broaden Ω1's proposal grammar to create a result-changing patch merely for a hostile control.

Hard laws:

```text
RESULT EQUIVALENCE != EXECUTION EQUIVALENCE
GATE ADMIT != RECEIPT IDENTITY
```

All other tasks, TDD sequencing, verification requirements, and constitutional boundaries in the original implementation plan remain unchanged.
