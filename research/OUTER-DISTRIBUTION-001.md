# OUTER-DISTRIBUTION-001

## Question
Does equality of coarse radius-1 ambiguity statistics determine the full pointwise Hamming-space compatibility geometry?

No.

## Frozen finite specimen
Let

- `A={0000,0001,0010,0101}`
- `B={0000,0001,0010,0111}`.

Exhaustive enumeration of all 16 ambient binary words gives both codes:

- cardinality 4;
- minimum distance 1;
- covering radius 2;
- radius-1 list-size histogram `{0:4, 1:6, 2:4, 3:2}`.

But their outer distributions differ. For ambient word `0000`, counting codewords at exact distances `0,1,2,3,4` gives:

- A: `(1,2,1,0,0)`
- B: `(1,2,0,1,0)`.

The complete histograms of outer rows also differ. The kernel retains every ambient-word row rather than only the histogram.

## Seal

**SAME RADIUS-1 AMBIGUITY HISTOGRAM != SAME OUTER DISTRIBUTION.**

**SAME COARSE COVERING PARAMETERS != SAME POINTWISE DISTANCE GEOMETRY.**

## Documented mathematical substrate
In coding theory, the outer distribution records, for each ambient vertex, counts of codewords in each distance relation. Association schemes retain intersection numbers and relation-specific structure. Completely regular codes are characterized by an equitable distance partition, a stronger condition than sharing a few aggregate parameters.

Research orientation: Hyun (2014), DOI `10.1002/jcd.21412`, develops harmonic/weight/distance distributions for equitable hypercube partitions and defines complete regularity through equitable distance partitions. Vanhove (2010), DOI `10.1002/jcd.20275`, reviews association-scheme intersection numbers plus inner and outer distributions. Gillespie & Praeger (2017), DOI `10.1112/blms.12016`, distinguishes minimum distance, covering radius, distance partitions/distributions, complete regularity and complete transitivity.

The particular A/B collision above is a project-local exhaustive finite deduction, not attributed to those papers.

## Dogram boundary
- distance count != occurrence
- outer distribution != evidence
- same histogram != same pointwise witness
- same covering radius != same local geometry
- equitable partition != semantic equivalence
- complete regularity != historical regularity
- mathematical symmetry != authority to identify sources

This is research only. It creates no public operator, evidence status, causal inference, or execution authority.

## Reproduce

`pytest -q tests/test_outer_distribution_001.py`
