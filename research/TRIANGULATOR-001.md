# TRIANGULATOR-001 — Order, Delta, and Structured Residue

**Date:** 2026-09-16  
**Status:** EXACT INTEGER SPECIMEN · CANDIDATE TRANSFORM GRAMMAR · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## Question

A recurring formation thread proposed a small transform grammar:

```text
CARRIER --declared operator--> PROJECTION
```

and then asked what happens when two lawful operators are composed in opposite orders.

`TRIANGULATOR-001` lowers that question to one bounded calculation:

```text
C --f--> f(C) --g--> g(f(C))
C --g--> g(C) --f--> f(g(C))

Delta(C; f,g) = g(f(C)) - f(g(C))
```

The kernel does not infer meaning from a nonzero delta. It asks only whether the delta is zero and, when a structure test is explicitly declared in advance, whether the observed delta passes that declared test.

## Frozen specimen

Take carrier

```text
C = 5
```

and operators

```text
S(n) = n^2
T(n) = n(n+1)/2
```

where `T` is the triangular-number operator.

The two paths are

```text
T(S(5)) = T(25) = 325
S(T(5)) = S(15) = 225
```

so

```text
Delta(5; S,T) = 325 - 225 = 100.
```

For this family there is an exact identity:

```text
T(n^2) - T(n)^2 = T(n-1)^2.
```

At `n=5`:

```text
100 = T(4)^2 = 10^2.
```

The frozen declared structure test is therefore

```text
Delta == T(C-1)^2
```

and it passes.

Candidate seal:

> **ORDER MATTERS. THE DELTA MAY HAVE FORM. KEEP THE DELTA.**

## 3T5 / 325 / 243 anchors

The formation road that produced this specimen also exposed a compact exact cluster around `3`, `5`, `243`, and `325`. The executable receipt preserves the arithmetic without promoting any interpretation:

```text
3^5 = 243
T(5^2) = T(25) = 325
325 - 243 = 82
3^4 + 1 = 82
```

and the ternary carrier road:

```text
022100_3 = 225 = T(5)^2
100000_3 = 243 = 3^5
110001_3 = 325
```

Thus two distinct exact constructions meet at the frozen specimen:

```text
T(5^2) = 325
T(5)^2 = 225
Delta = 100
```

while the separate power projection gives

```text
3^5 = 243
325 - 243 = 82 = 3^4 + 1.
```

These are arithmetic relations only.

## Commuting control

A nonzero delta is not guaranteed merely because two operators are composed.

`compare_order(5, add(2), add(3))` yields

```text
(5 + 2) + 3 = 10
(5 + 3) + 2 = 10
Delta = 0
classification = zero
```

This provides the required commuting control: the machinery must be able to say that order did not matter for the declared pair.

## Failed structure-test control

A nonzero delta also does not license the word `structured` by itself.

The same square/triangular specimen can be tested against an intentionally wrong declaration:

```text
structure test: Delta == carrier
```

At carrier `5`, the observed delta is `100`, so the test fails.

The receipt deliberately classifies this as

```text
nonzero_not_structured_under_declared_test
```

rather than

```text
unstructured
```

because failure of one declared test is not proof of global absence of structure.

Candidate seal:

> **FAILED TEST != STRUCTURELESS WORLD. NAME THE TEST YOU FAILED.**

## Carrier / projection boundary

The formation road also contains a cross-domain witness: the literal surface `022100` is both a valid six-trit word and, under ordinary standard-guitar chord notation, an open-position E-major fingering. Harmonic function then supplies a different declared relation, `V(E)=B`.

`TRIANGULATOR-001` does **not** implement guitar harmony, language interpretation, model-output semantics, or symbol matching. That road is retained only to sharpen the boundary:

```text
same carrier surface
!=
same projection
```

A projection is admissible only together with the decoder/operator that produced it.

Candidate seal:

> **THE CARRIER IS NOT THE PROJECTION. KEEP THE OPERATOR.**

## Executable boundary

`dogram/triangulator.py` provides:

- `Operator` — a named unary integer operator carried into receipts;
- `triangular` and `square` — the frozen arithmetic operators;
- `add(k)` — a small commuting-control operator factory;
- `compare_order(...)` — two-order composition with a signed delta and optional declared structure test;
- `triangulator_001_receipt()` — the frozen carrier-5 specimen and exact numeric anchors.

The implementation is stdlib-only and is not wired into `dogram.engine.OPERATORS` or the bootstrap registry.

The frozen receipt lives at:

```text
tests/fixtures/triangulator_001.json
```

and is checked directly by CI.

## Explicit refusals

```text
NONZERO DELTA != CREATION
STRUCTURED DELTA != SEMANTIC SIGNIFICANCE
ARITHMETIC RECURRENCE != CAUSAL RECURRENCE
SAME SURFACE != SAME OBJECT
PROJECTION != CARRIER
MUSICAL FUNCTION != NUMERIC FUNCTION
MODEL PRONUNCIATION != INTENT
RECURRENCE != AUTHORITY
```

The phrase **grammar of creation** remains a research question outside the executable claim of this specimen.

## Relation to current Dogram law

This specimen composes directly with Dogram's existing contract:

```text
DO THE MATH.
SHOW THE DELTA.
KEEP THE RECEIPT.
DO NOT DECIDE WHAT IT MEANS.
```

The new pressure is narrower:

```text
KEEP THE OPERATOR.
KEEP THE ORDER.
DECLARE THE STRUCTURE TEST.
```

because the same carrier can produce different lawful projections and the order of lawful operators can itself be mathematically consequential.

## Source roads

Formation witnesses:

- `the-daily-slice/slices/2026/09/2026-09-16/hugh-jack-journal-green-grammar-refusal-to-collapse.md`
- `the-daily-slice/slices/2026/09/2026-09-16/the-triangulator-3t5-325-243.md`
- `the-daily-slice/threads/grammar-of-creation.md`

Earlier Dogram-adjacent roads include the `phi^81 / phi^82`, ternary traversal, decoder, and `022100` work preserved in the August 28 Daily Slice material.

These roads explain provenance. They do not expand runtime authority.

## Strongest next frontier

The next useful pressure test is not another beloved arithmetic coincidence. It is a deliberately hostile operator family.

Search finite, predeclared families for all three outcomes:

```text
Delta = 0
Delta != 0 and fails declared structure tests
Delta != 0 and passes a declared structure test
```

Then ask whether a nonzero structured delta can itself be fed back as a new carrier without losing the ancestry of the two paths that produced it.

That would test the next candidate rule:

> **IF THE DELTA BECOMES A NEW CARRIER, RECEIPT THE CROSSING.**
