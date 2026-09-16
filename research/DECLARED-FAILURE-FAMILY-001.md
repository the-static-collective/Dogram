# DECLARED-FAILURE-FAMILY-001

Status: research-only; no public operator promotion.

## Question

Does ordinary minimum Hamming distance determine resilience when the admissible failures are a declared family of coordinate sets rather than all failures up to a given cardinality?

No.

## Frozen exact specimen

Two four-state binary signature systems are frozen:

- resilient: `0000, 0011, 0101, 0110`
- fragile: `0000, 0011, 0101, 1001`

Both have exact minimum Hamming distance `2`.

Declare one admissible correlated erasure: coordinates `{0,1}` fail together.

After deleting coordinates 0 and 1:

- resilient projects to `00, 11, 01, 10`, still four distinct states;
- fragile projects to `00, 11, 01, 01`, collapsing states 0 and 3.

Therefore

`SAME MINIMUM DISTANCE != SAME RESILIENCE TO A DECLARED FAILURE FAMILY.`

The fragile carrier also survives erasure `{2,3}`, proving that the distinction is not the number of erased coordinates alone; placement matters.

## Documented mathematics

Classical coding theory defines Hamming distance by the number of differing coordinates and uses minimum distance to characterize worst-case error/erasure guarantees under cardinality-bounded corruption models. Kokkala & Ostergard (2014), DOI 10.1002/jcd.21400, provides a standard finite-code formulation. Raskhodnikova, Ron-Zewi & Varma (2021), DOI 10.1002/rsa.21031, explicitly distinguishes erasure and error corruption models and studies erasure-resilient decoding/testing. Yang, Yeung & Zhang (2008), DOI 10.1002/ett.1290, emphasizes that decoder guarantees depend on the declared weight/error model; Hamming weight is one particular measure.

## Dogram inference

For a pair of signatures `x,y`, let its distinguishing-coordinate receipt be

`D(x,y) = {i : x_i != y_i}`.

An erased coordinate set `F` collapses that pair exactly when `D(x,y) subseteq F`. Thus a declared failure family `mathcal F` can be checked exactly without assigning semantics to coordinates. Minimum distance keeps only `min |D(x,y)|`; it forgets where each distinguishing set lives.

## Seals

- SAME REDUNDANCY COUNT != SAME FAILURE RESILIENCE.
- RECEIPT WHICH DISTINCTIONS CAN FAIL TOGETHER.
- MINIMUM DISTANCE IS A CARDINALITY SUMMARY; A DECLARED FAILURE FAMILY CAN REQUIRE THE SUPPORT RECEIPT.

## Refusals

- COORDINATE FAILURE != HISTORICAL ABSENCE
- CORRELATED FAILURE SET != COMMON CAUSE
- HAMMING SUPPORT != EVIDENCE SUPPORT
- RESILIENT SIGNATURE != TRUE STATE
- FAILURE-FAMILY SURVIVAL != AUTHORITY
- MATHEMATICAL ROBUSTNESS != REAL-WORLD RELIABILITY

## HOLD

No `failure_family@1`, `support_distance@1`, `correlated_erasure@1`, evidence, occurrence, causal, semantic, or authority surface is promoted.

## Next frontier

Replace a single declared failure set by a finite hypergraph of admissible joint failures and compute minimal transversals of pair-distinguishing supports. This could expose a duality between `failure sets that destroy separation` and `view sets that guarantee separation`, but should remain research-only until a bounded specimen earns it.
