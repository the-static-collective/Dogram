# ROBUST-SEPARATION-MARGIN-001

Status: bounded research specimen; no public operator or authority promotion.

## Question

Ordinary finite separation asks whether every distinct state pair differs under at least one declared probe. What additional information is retained by counting *how many* probe coordinates distinguish the weakest pair?

For probe family `F`, define the signature `sigma_F(x)` and

`delta(F) = min_{x != y} HammingDistance(sigma_F(x), sigma_F(y))`.

Ordinary separation is exactly `delta(F) >= 1` on a completely enumerated finite domain. A larger margin is a separate property.

## Frozen specimen

States are `00, 01, 10, 11`. Probes are `x`, `y`, and `xor`. Their signatures are

- `00 -> 000`
- `01 -> 011`
- `10 -> 101`
- `11 -> 110`

Every pair has Hamming distance exactly 2, so `delta=2`. Delete any one probe and the remaining two probes still separate all four states, but the new margin is exactly 1. Delete down to a singleton probe and separation fails.

Thus the three-probe family and each two-probe family all have complete ordinary distinguishing power, while their distinguishing margins differ.

## Seals

**SAME COMPLETE DISTINGUISHING POWER != SAME DISTINGUISHING MARGIN.**

**SEPARATING != SINGLE-PROBE-LOSS TOLERANT.**

**REDUNDANT FOR ORDINARY SEPARATION != REDUNDANT FOR ROBUSTNESS.**

## Documented mathematics

This is the minimum-distance viewpoint of coding theory applied to declared observation signatures. Hamming distance counts disagreeing coordinates. Fault-tolerant identifying-code work explicitly strengthens ordinary pair distinction by requiring multiple distinguishing detector coordinates; Jean & Seo (2024), DOI 10.1002/net.22254, studies error-detecting identifying codes permitting a detector false negative. Junnila, Laihonen & Parreau (2012/2013), DOI 10.1002/net.21472, studies tolerant identifying codes robust to neighborhood changes. Separating-system background: Lichev & Sanhueza-Matamala (2026), DOI 10.1002/rsa.70091.

Wolfram Language documentation independently defines `HammingDistance[u,v]` as the number of positions at which equal-length vectors disagree.

## Project-local inference

For this exact finite binary specimen, `delta>=2` guarantees that deleting any one probe coordinate leaves every state pair differing somewhere. This is an elementary finite deduction, not a claim that arbitrary Dogram observation processes have independent, binary, or equally reliable probes.

The calculation retains all pairwise distances rather than only the minimum so the scalar margin does not erase which pairs realize it.

## Refusals

- probe output != occurrence
- Hamming distance != semantic distance
- separating != evidentiary truth
- robustness != reliability of a physical sensor
- larger margin != greater human worth / truth / authority
- redundancy for separation != uselessness
- deletion tolerance in a declared finite signature != historical survival of evidence
- finite-domain robustness != global observability

## Reproduce

`pytest -q tests/test_robust_separation_margin_001.py`

`python research/robust_separation_margin_001.py`
