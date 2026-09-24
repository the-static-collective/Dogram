# LIST-DECODING-AMBIGUITY-001

Status: bounded research specimen; no public operator/runtime promotion.

## Question

When unique correction fails, can Dogram retain the exact compatibility set instead of either guessing a source or collapsing to a generic failure?

## Frozen specimen

Use the binary even-parity code

`C = {000, 011, 101, 110}`

with Hamming radius `r=1`. Exact exhaustive enumeration of all eight received words gives:

- the four codewords themselves have list size 1;
- each of the four odd-parity words has list size 3;
- maximum list size is 3;
- list-size distribution is `{1: 4, 3: 4}`;
- covering radius is 1;
- minimum code distance is 2.

Example:

`L_1(001) = {000, 011, 101}`.

Thus every possible received word is within radius 1 of at least one codeword, but half the observation space has three compatible sources at that radius.

## Seals

**BOUNDED CANDIDATE SET != IDENTIFIED SOURCE.**

**COVERED BY THE CODE != UNIQUELY DECODABLE.**

**FINITE AMBIGUITY != FAILURE TO CALCULATE.**

## Documented mathematics

This is standard finite Hamming/list-decoding mathematics. Raskhodnikova, Ron-Zewi & Varma (2021), DOI `10.1002/rsa.21031`, explicitly treat list decoding as outputting lists rather than a unique decoder/source. Krotov (2024), DOI `10.1002/jcd.21947`, studies multifold 1-perfect codes where every graph vertex lies within distance 1 of exactly a declared number of code elements, directly exposing multiplicity inside radius-one balls.

Scholar Gateway pass: 10 passages / 8 articles / 2011-2024. Wolfram exact evaluation independently enumerated the same eight radius-one lists, distribution `1 -> 4, 3 -> 4`, maximum list size 3, and covering radius 1.

## Dogram inference

The receipt should preserve the complete candidate set and its radius. It should not manufacture a tie-breaker. A bounded list is stronger information than `decoding failed`, but weaker than source identification.

## Refusals

- compatibility != occurrence
- candidate != source
- list membership != evidentiary support
- nearest != historically true
- bounded list != permission to choose
- covering radius != semantic coverage
- list size != probability
- unique mathematical candidate != empirical proof of origin

## Reproduce

`pytest -q tests/test_list_decoding_ambiguity_001.py`
