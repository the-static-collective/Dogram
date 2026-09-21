# TRANSPORT-GEOMETRY-001

Research-only bounded specimen following COUPLING-WITNESS-001.

## Question
Can two coupling witnesses with the same marginals and the same scalar disagreement probability carry different geometry-dependent transport cost?

## Frozen specimen
Carrier `{0,1,2}` with uniform marginals. `pi01` swaps 0/1 and fixes 2; `pi12` fixes 0 and swaps 1/2. Both have disagreement probability `2/3`.

Declare the path metric with edge lengths `d(0,1)=1`, `d(1,2)=2`, hence `d(0,2)=3`. Exact expected costs are:

- `E_pi01[d(X,Y)] = 2/3`
- `E_pi12[d(X,Y)] = 4/3`

Under the discrete/Hamming metric (`d(x,y)=1` for `x!=y`) both costs collapse back to `2/3`.

## Seal
**SAME MARGINALS + SAME DISAGREEMENT MASS != SAME GEOMETRY OF DISAGREEMENT.**

Secondary: **TRANSPORT COST DEPENDS ON A DECLARED GROUND METRIC; THE METRIC IS NOT RECOVERED FROM THE COUPLING.**

## Provenance
Standard finite optimal-transport mathematics. Wasserstein cost is an infimum over couplings of expected declared ground-metric cost; see Sommerfeld & Munk (2017), DOI `10.1111/rssb.12236`, and Zhang et al. (2020), DOI `10.1155/2020/9870620`. A 2026 Environmetrics treatment explicitly forms the finite cost matrix as `D_ij=d(x_i,y_j)` for a chosen metric, DOI `10.1002/env.70091`.

Wolfram independently evaluated the two frozen coupling matrices and declared metric: both marginals uniform, both disagreement `2/3`, costs `2/3` and `4/3` respectively.

## Boundary / refusals
- coupling != occurrence
- expected transport cost != observed movement
- ground metric != ontology
- small cost != semantic similarity unless separately declared
- optimal plan != causal mechanism
- Wasserstein geometry != evidentiary confidence

No public operator, runtime action, evidence status, or authority promotion is proposed.
