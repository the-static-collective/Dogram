# OMEGA-QUOTIENT-001 — Implementation Receipt

**Date:** 2026-08-30 / 2026-08-31 UTC  
**Repository:** `the-static-collective/Dogram`  
**Branch:** `impl/execution-cut-omega-quotient-001`  
**Base main:** `4fbff983df060301d7e2310e4ad043aef5ef33e5`  
**Design:** `docs/superpowers/specs/2026-08-30-execution-cut-omega-quotient-design.md`

## What was implemented

This slice adds two internal Dogram modules without changing the public calculation floor or bootstrap registry:

- `dogram/execution_cut.py`
  - derives `dogram.execution-cut/v0` only from existing runtime-reified `dogram.execution-data/v0`;
  - preserves ordered consumed-input addresses and ordered step traces;
  - computes typed/component-wise footprint residuals without set-coercing ordered history.
- `dogram/omega_quotient.py`
  - compares one baseline/candidate pair under a fixed predeclared target family;
  - wraps the existing one-cycle Ω mutation/gate path instead of duplicating it;
  - requires equal input digests for the controlled pair;
  - keeps gate admission separate from target-relative equivalence;
  - returns `HOLD RUNTIME_BODY_UNPINNED` for cross-runtime claims outside the bounded same-invocation proof.

The first supported target probes are deliberately inert execution-cut fields only:

```text
result
status
reason_code
residuals
step_trace
```

`step_trace` is included specifically so a real structurally admitted Ω candidate can witness `GATE ADMIT != TARGET EQUIVALENT` without inventing semantic target machinery.

No semantic probe registry, ambient I/O, public operator, bootstrap intrinsic, automatic target selection, or automatic experiment selection was added.

## TDD receipt — initial RED

Contract-test head:

```text
9446f164d32e1f595c97b5c98baf3f77dc3dc003
```

GitHub Actions:

```text
run: 33354212838
job: 99373160031
```

Observed result:

```text
Ran 133 tests
FAILED (errors=1)
```

The single error was the intended missing-production-surface failure:

```text
ModuleNotFoundError: No module named 'dogram.execution_cut'
```

The existing Dogram tests reached green results before the new contract module import failed. Production modules had not yet been added.

## TDD receipt — initial GREEN implementation checkpoint

Implementation head:

```text
4068727d975178598ec183ad12f75946beadba89
```

GitHub Actions:

```text
run: 33354278549
job: 99373343948
```

Observed verification:

```text
Ran 141 tests in 0.345s
OK
compile: success
constitutional floor: OK
Omega scope scan: OK
```

The constitutional check still asserted the exact public operator floor:

```text
delta@1
rectangle@1
ablate@1
reach@1
```

and the exact pre-existing bootstrap intrinsic registry.

## Review-pressure TDD — real gate/target separation

A later review pass found that the hostile gate/equivalence test used the comparator directly rather than a real admitted Ω candidate. The test was tightened before expanding production behavior.

RED head:

```text
29ca53890198e79272ff30e3ea8306f954c26a7e
```

GitHub Actions:

```text
run: 33354463261
job: 99373836296
Ran 141 tests
FAILED (failures=1)
```

The new end-to-end test predeclared `T_step_trace = [step_trace]` and ran the existing diagnostic ablation. The Ω phase gate admitted the structurally valid candidate, but quotient comparison refused because `step_trace` had not yet been admitted as an inert target probe.

Minimal GREEN head:

```text
45f208ba44ffc27a186a33fc6188a0bfcc9c1081
```

GitHub Actions:

```text
run: 33354501408
job: 99373942290
Ran 141 tests in 0.379s
OK
compile: success
constitutional floor: OK
Omega scope scan: OK
```

The resulting real witness is now:

```text
phase gate = ADMIT
target = T_step_trace
baseline step trace != candidate step trace
target verdict = DIFFERENT_UNDER_T
```

This makes the separation executable rather than rhetorical:

```text
GATE ADMIT != TARGET EQUIVALENT
```

## Positive specimen — `OMEGA-QUOTIENT-POSITIVE-001`

The positive test uses the existing Ω fixture:

```text
P0:
  value step       <- consumes payload
  diagnostic step  <- consumes diagnostic
  result            = value

proposal:
  remove_step(diagnostic)

P1:
  value step only
```

with predeclared target:

```text
T_result = [result]
```

The executable assertions establish, for this exact paired experiment:

```text
same input digest
same declared result
EQUIVALENT_UNDER_T
baseline execution digest != candidate execution digest
baseline contacts = [[payload], [diagnostic]]
candidate contacts = [[payload]]
baseline step trace = [value, diagnostic]
candidate step trace = [value]
fuel initial = 10
baseline fuel remaining = 8
candidate fuel remaining = 9
```

Therefore the preserved statement is:

> The declared result survived this exact admitted ablation while the measured execution contact surface changed.

It is not a claim that the programs or executions are globally equivalent.

## Hostile controls

The focused suite freezes these boundaries:

| Control | Expected disposition |
| --- | --- |
| target declared only after comparison | `REFUSE / TARGET_NOT_PREDECLARED` |
| different baseline/candidate input digest | `REFUSE / INPUT_CUT_MISMATCH` |
| same trace members in different order | typed `step_trace` residual remains non-empty |
| same result but different history | `EQUIVALENT_UNDER_T` only; no global-equivalence promotion |
| real structurally admitted candidate changes predeclared `step_trace` target | Ω gate `ADMIT` + `DIFFERENT_UNDER_T` |
| comparison across unpinned runtime bodies | `HOLD / RUNTIME_BODY_UNPINNED` |
| undeclared semantic/ambient probe | `REFUSE / UNSUPPORTED_TARGET_PROBE` |
| repeated identical paired experiment | canonical receipt bytes are identical |

## Receipt boundary

Every `dogram.omega-quotient/v0` receipt explicitly carries that it does **not** establish:

```text
global_equivalence
causal_irrelevance
evidence
support
truth
authority
cross-runtime replay
```

The baseline and candidate remain separately attributable to their exact program and execution digests. The target quotient lives beside the typed residual; it does not erase it.

## Interpretation boundary

This slice proves a bounded calculational capability only:

```text
EXECUTE
-> WITNESS CONTACT
-> CHANGE ONE DECLARED THING
-> GATE
-> EXECUTE AGAIN
-> COMPARE ONLY THE PREDECLARED TARGET
-> KEEP THE REST OF THE DIFFERENCE
```

A later ALEX / 3rdi / human pass may pressure or project these receipts. Dogram itself does not decide whether the candidate is better, meaningful, evidentiary, causal, or authoritative.

## Seal

> **THE TARGET SURVIVED. THE HISTORY DID NOT DISAPPEAR. KEEP BOTH RECEIPTS.**
