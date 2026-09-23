# ERASURE-CORRUPTION-DISTANCE-001

Status: bounded research specimen; no public operator or semantic promotion.

## Question

Does robustness to loss of one *known* probe coordinate imply robustness to one *unknown corrupted* probe value?

No.

## Frozen specimen

Use the four binary signatures already natural to the `x,y,xor` probe family:

- `00 -> 000`
- `01 -> 011`
- `10 -> 101`
- `11 -> 110`

Every pair of codewords has Hamming distance exactly 2. Deleting any one known coordinate leaves four distinct length-2 signatures, so any one declared erasure location is recoverable on this finite domain.

Every one-bit flip leaves the even-parity code, so a single unknown flip is detectable. But it is not uniquely correctable. For example received word `001` is Hamming distance 1 from each of `000`, `011`, and `101`. The receipt therefore retains all compatible source codewords instead of selecting one.

A distance-3 control `{000,111}` uniquely corrects any one unknown bit flip. A distance-1 control `{00,01}` shows that a one-bit flip can land on another valid codeword and evade detection.

## Exact distinction

For a code with minimum Hamming distance `d`:

- one known erasure is uniquely recoverable when `d >= 2`;
- one unknown substitution is detectable when `d >= 2`;
- one unknown substitution is uniquely correctable when `d >= 3`.

The frozen `d=2` specimen sits exactly on the boundary: erasure recovery + flip detection, but no unique flip correction.

## Seals

**ROBUST TO ONE KNOWN PROBE LOSS != ROBUST TO ONE UNKNOWN PROBE CORRUPTION.**

**DETECTABLE CORRUPTION != UNIQUELY CORRECTABLE CORRUPTION.**

**AMBIGUOUS DECODING RECEIPT != PERMISSION TO CHOOSE A SOURCE.**

## Provenance

Documented coding-theoretic substrate: minimum Hamming distance controls error detection/correction; Marin & Mogilnykh (2025), DOI `10.1002/jcd.22012`, states the standard unique-correction radius `floor((d-1)/2)`. Raskhodnikova, Ron-Zewi & Varma (2021), DOI `10.1002/rsa.21031`, explicitly distinguishes erasures (missing entries) from errors (wrong values) and studies their differing decoding behavior. Jean & Seo (2024), DOI `10.1002/net.22254`, studies fault-tolerant identifying codes with single-detector false-negative transmissions.

Wolfram documentation independently defines Hamming distance as the number of disagreeing coordinates and its Linear Codes repository includes the binary length-3 repetition code with distance 3. Wolfram semantic search returned no direct result for the exact erasure/corruption specimen; no stronger Wolfram claim is made.

Project-local inference: the `x,y,xor` signatures form the even-parity `[3,2,2]` code, and exhaustive finite enumeration supplies the ambiguity witnesses above.

## Refusal boundary

- probe bit != occurrence
- missing coordinate != false coordinate
- code distance != semantic distance
- error detection != evidentiary contradiction
- unique decoding != historical truth
- ambiguous decoding != permission to guess
- robustness under a declared corruption model != physical sensor reliability
- finite-domain correction != global observability
- mathematical recoverability != authority to overwrite a receipt

## Reproduce

```bash
python research/erasure_corruption_distance_001.py
pytest -q tests/test_erasure_corruption_distance_001.py
```
