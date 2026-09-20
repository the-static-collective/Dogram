# MARKOV-LUMPABILITY-001

Status: bounded research specimen. Authority: none. Public operator: none.

## Question

Dogram now has exact quotient-successor and operation-descent work. What changes when a declared transition system carries probability mass, not only support?

## Exact specimen

States `a,b` share quotient block `A`; `c` is block `B`.

- from `a`: mass `1/2` to `A`, `1/2` to `B`
- from `b`: mass `1/4` to `A`, `3/4` to `B`

Both states have exactly the same positive quotient successor support `{A,B}`. Nevertheless their total probability mass into target block `A` differs, so the partition is not strongly lumpable and no state-independent quotient transition row for `A` is emitted.

Hostile control: change `b` to send `1/2` inside `A` and `1/2` to `B` (even to a different concrete representative inside `A`). Raw rows can differ while block totals agree; then the quotient transition is well-defined.

## Seal

**SAME QUOTIENT SUCCESSOR SUPPORT != SAME QUOTIENT TRANSITION LAW.**

For a finite Markov chain with partition blocks, strong lumpability requires states in one source block to have equal total transition probability into every target block. This is the probabilistic analogue of a descent condition, but it is strictly finer than support-level successor descent.

## Documented mathematics

Finite-state Markov aggregation/lumpability is standard. Bušić & Fourneau (2011), DOI `10.1002/nla.824`, discuss aggregation under partitions and block transition mass through collector/distributor matrices. Kim & Smith (1995), DOI `10.1002/1520-6750(199510)42:7<1115::AID-NAV3220420710>3.0.CO;2-W`, treat exact aggregation/disaggregation of finite Markov chains.

Scholar Gateway pass on 2026-09-20 returned 8 passages / 8 articles (1995–2022). The repository kernel uses only the elementary finite block-sum criterion and exact rational arithmetic; it does not claim a novel lumpability theorem.

## Dogram delta

`SUCCESSOR-DESCENT-001` can establish that two representatives expose the same quotient successor *classes*. That does not authorize treating a stochastic transition law as descended. The new receipt retains:

1. quotient support per concrete state;
2. exact aggregate probability mass per target block;
3. first same-source-block mass mismatch;
4. induced quotient transition only after the complete finite check passes.

## Refusals

- POSITIVE SUPPORT != OCCURRENCE.
- SAME QUOTIENT SUPPORT != LUMPABILITY.
- TRANSITION PROBABILITY != EVIDENTIARY CONFIDENCE.
- LUMPABILITY != CAUSAL EQUIVALENCE.
- MARKOV MODEL != HISTORICAL PROCESS.
- A WELL-DEFINED QUOTIENT LAW != AUTHORITY TO EXECUTE OR PREDICT THE WORLD.

## Reproduce

`pytest -q tests/test_markov_lumpability_001.py`

No public operator, schema, runtime action, stochastic inference pipeline, evidence status, or authority promotion is introduced.
