# PHASELIFT-3 Execution Law — Independent Pressure, Sequential Earning

This note is normative for `docs/superpowers/plans/2026-08-31-phaselift-3-promotion-kernel.md` and resolves one implementation-order ambiguity found during plan self-review.

## Law

After schema, attribution, candidate identity, transformation identity, and provenance validation succeed, PHASELIFT-3 evaluates the **transfer** and **generation/composition** pressure surfaces independently.

It must not skip generation pressure merely because transfer failed.

```text
VALID STRUCTURE
   |-- REPEAT pressure
   |-- TRANSFER pressure
   `-- GENERATE + COMPOSE pressure

then

SEQUENTIAL EARNED CLASS
REMNANT -> PATTERN -> TOOL -> OPERATOR_CANDIDATE
```

The checks are evidence-bearing local calculations. The earned class is sequential.

Therefore `three-echoes.json` deterministically returns both:

```text
TRANSFER_CONTEXT_NOT_DISTINCT
DELTA_OMEGA_EMPTY
```

while still earning only:

```text
PATTERN
```

because transfer did not pass.

The final class calculation remains:

```python
def _earned_class(checks: dict[str, bool]) -> str:
    if not checks["recurs"]:
        return "REMNANT"
    if not checks["transfers"]:
        return "PATTERN"
    if not (checks["generates"] and checks["composes"]):
        return "TOOL"
    return "OPERATOR_CANDIDATE"
```

## Required evaluator order

```text
1. Decode + structural validation.
2. Identity + provenance validation.
3. Evaluate repeat.
4. Evaluate transfer.
5. Evaluate finite grammar growth.
6. If delta_omega is non-empty, evaluate PLUS_CO composition/surplus.
7. Evaluate proof circularity.
8. Calculate sequential earned class from the completed check vector.
9. Apply disposition precedence.
10. Canonicalize result and receipt.
```

This preserves two distinct truths:

```text
FAILED EARLIER PROMOTION GATE != DO NOT MEASURE LATER PRESSURE
LATER PRESSURE SUCCESS != EARLIER GATE WAS EARNED
```

No later check can raise the earned class across a failed earlier gate.