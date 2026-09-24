# AMBIGUITY-PROFILE-001 — same coarse invariants, different local ambiguity

Status: bounded research specimen; no public operator/runtime promotion.

## Question
Does fixing code length, cardinality, minimum Hamming distance, covering radius, and worst-case radius-1 list size determine how ambiguity is distributed across the ambient observation space?

No.

## Frozen specimen
In binary Hamming space of length 4, declare

- `A = {0000,0011,0101,0110}`
- `B = {0000,0011,0101,1010}`

For both codes, exhaustive enumeration gives:

- length `n = 4`
- cardinality `|C| = 4`
- minimum distance `d_min = 2`
- covering radius `rho = 2`
- maximum radius-1 list size `L_max = 3`

But their complete radius-1 list-size histograms differ:

- `A`: `{0:4, 1:8, 3:4}`
- `B`: `{0:4, 1:6, 2:4, 3:2}`

Thus equal worst-case ambiguity and equal coarse coding invariants do not determine the distribution of local ambiguity.

## Seals

**SAME WORST-CASE AMBIGUITY != SAME AMBIGUITY PROFILE.**

**SAME COARSE CODE PARAMETERS != SAME LOCAL COMPATIBILITY GEOMETRY.**

**HISTOGRAM AGREEMENT, IF PRESENT, WOULD STILL != POINTWISE LIST AGREEMENT.**

## Documented mathematics
This specimen lives in standard coding/covering geometry. Krotov (2024), DOI `10.1002/jcd.21947`, defines multifold 1-perfect codes by an exact constant number of code elements in every radius-1 ball, making local ball multiplicity an explicit mathematical object. Gillespie & Praeger (2017), DOI `10.1112/blms.12016`, distinguish minimum distance, covering radius, distance partitions, and distance distributions. Barg (2020), DOI `10.1112/mtk.12066`, relates finite Hamming-space discrepancy to distance distributions.

The particular pair above and its exhaustive profile comparison are project-local finite deductions, not claims of a new coding theorem.

## Dogram boundary
The kernel receipts every ambient word's radius-1 candidate list and only then derives the histogram and worst-case scalar. This preserves the witness underneath the summary.

Refusals:

- list size != probability
- candidate multiplicity != evidentiary weight
- local ambiguity != occurrence
- worst-case equality != local equivalence
- histogram != pointwise provenance
- covering radius != semantic coverage
- code equivalence has not been asserted or inferred
- mathematical symmetry != historical interchangeability

## Reproduce

`pytest -q tests/test_ambiguity_profile_001.py`
