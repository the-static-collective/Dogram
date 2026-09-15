# SEPARATING-VIEW-FAMILY-001

Status: research-only; no public operator promotion.

## Question

Given a finite declared carrier and a finite family of lawful local views, which views are actually necessary to distinguish every pair of carrier states?

## Frozen specimen

Carrier `X = {x0,x1,x2,x3}` and binary tests:

- `t1 = {x1,x2,x3}`
- `t2 = {x2,x3}`
- `t3 = {x3}`

The full signatures are:

- `x0 -> 000`
- `x1 -> 100`
- `x2 -> 110`
- `x3 -> 111`

Hence the full family separates all six unordered pairs.

Exhaustive subfamily enumeration shows the unique minimum separating subfamily is the full three-test family. Each omission has a frozen collision:

- omit `t1`: `x0 ~ x1`
- omit `t2`: `x1 ~ x2`
- omit `t3`: `x2 ~ x3`

The information-theoretic lower bound `ceil(log2 |X|) = 2` does not imply that two of the *declared available* tests suffice. The admissible view family matters.

## Documented mathematics

This is the finite Test Cover / separating-family problem. A test separates two items when it contains exactly one; a test cover separates every distinct pair. Minimum Test Cover is NP-hard in general. See de Bontridder et al., *Approximation Algorithms for the Test Cover Problem*, Mathematical Programming 98 (2003), DOI 10.1007/s10107-003-0414-6; Crowston et al., *Parameterized Study of the Test Cover Problem*, MFCS 2012, DOI 10.1007/978-3-642-32589-2_27.

## Dogram delta

The executable receipt computes pair collisions for every subfamily rather than inferring sufficiency from cardinality. In this specimen all three views are individually necessary relative to the declared family.

Seals:

> A VIEW FAMILY CAN BE COLLECTIVELY SEPARATING WHILE EVERY MEMBER IS LOCALLY NECESSARY.

> AN INFORMATION LOWER BOUND DOES NOT GUARANTEE THAT THE DECLARED VIEWS ACHIEVE IT.

> RECEIPT THE ADMISSIBLE VIEW FAMILY AND THE PAIRS EACH VIEW UNIQUELY SEPARATES.

## Refusals

- SEPARATING FAMILY != COMPLETE HISTORY
- DISTINGUISHABLE STATE != OBSERVED OCCURRENCE
- TEST COVER != EVIDENCE COVER
- MINIMUM VIEW FAMILY != MINIMUM TRUTH
- OMITTED VIEW != HIDDEN CAUSE
- PAIR SEPARATION != SEMANTIC DIFFERENCE
- COMPUTATIONAL MINIMALITY != AUTHORITY

## Frontier

For larger finite carriers, compute the pair-universe `C(X,2)` and map each view to the pairs it separates. Minimal sufficient view selection is then a set-cover instance over pair distinctions. Useful next questions are redundancy, multiple incomparable minimum covers, weighted views, and robustness under one-view loss. Keep those as research kernels until a concrete Dogram use earns promotion.
