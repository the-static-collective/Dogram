# FIELD-REDUCTION-DEPENDENCE-001

**Date:** 2026-09-02  
**Status:** RESEARCH + EXACT PRIME-FIELD ARITHMETIC · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Research question

Previous Dogram work separates:

```text
matroid coherence
!=
linear representability
```

The next boundary is narrower than deciding representability over an arbitrary field:

> **If one integer matrix is held fixed, can changing only the declared coefficient field change its induced dependence matroid?**

Yes.

This packet computes only that finite reduction effect. It does not decide whether an abstract matroid is representable over a field, and it does not treat coefficient-field behavior as causal, semantic, historical, physical, or evidentiary meaning.

## 1 — Documented mathematical substrate

For a field `F`, a matrix with labeled columns induces a representable matroid whose independent sets are the linearly independent column subsets over `F`.

Useful literature anchors:

- C. Merino, M. Ramírez-Ibáñez, G. Rodríguez-Sánchez, C. H. Li, **The Tutte Polynomial of Some Matroids**, *International Journal of Combinatorics* (2012), DOI `10.1155/2012/430859`. The paper records the standard rank-3 seven-column Fano matrix and states that the Fano matroid is representable over fields of characteristic 2.
- Peter Nelson, **Almost all matroids are nonrepresentable**, *Bulletin of the London Mathematical Society* 50(2) (2018), DOI `10.1112/blms.12141`. The paper explicitly distinguishes `F`-representability from representability over at least one field.

The finite arithmetic below does not rely on a general representability decision theorem.

## 2 — Frozen carrier

Hold the integer matrix fixed:

```text
A =
[1 0 0 1 1 0 1]
[0 1 0 1 0 1 1]
[0 0 1 0 1 1 1]
```

with column labels:

```text
1 2 3 4 5 6 7
```

Only the coefficient field changes.

The kernel enumerates every 3-column subset and computes exact rank after reducing entries modulo a declared prime.

## 3 — Exact delta

For `GF(2)`:

```text
rank-3 basis count = 28
```

For `GF(3)`:

```text
rank-3 basis count = 29
```

The symmetric difference of the complete rank-3 basis supports is exactly:

```text
{4,5,6}
```

No other 3-subset changes status.

### Smallest attributable witness

Columns `4,5,6` form

```text
[1 1 0]
[1 0 1]
[0 1 1]
```

with exact integer determinant

```math
\det = -2.
```

WolframAlpha independently returned `-2` for this determinant on 2026-09-02.

Therefore:

```text
mod 2: -2 = 0 -> dependent
mod 3: -2 = 1 -> independent
```

So the entire field-sensitive delta can be receipted to one minor.

## 4 — What is documented, inferred, and speculative

### Documented mathematics

```text
matrix + field -> column matroid
```

and the standard Fano matrix is a characteristic-2 representation.

### Dogram inference

The exact finite specimen supports:

```text
SAME INTEGER MATRIX
!=
SAME DEPENDENCE SURFACE AFTER FIELD REDUCTION
```

and therefore:

> **THE COEFFICIENT DOMAIN IS PART OF THE DECODER RECEIPT.**

### Speculation / HOLD

This may eventually inform ALEX/3rdi handshakes where a source object is projected through different declared calculational domains. That architectural connection is not promoted here.

Dogram does not infer that one field is more truthful, more physical, more historical, or more causally appropriate than another.

## 5 — Hostile boundaries

```text
REPRESENTABLE OVER GF(2) != REPRESENTABLE OVER EVERY FIELD

SAME INTEGER ENTRIES != SAME LINEAR DEPENDENCE AFTER REDUCTION

FIELD-SENSITIVE DELTA != SOURCE CHANGE

DEPENDENCE IN A DECLARED FIELD != CAUSAL DEPENDENCE

A WORKING REPRESENTATION != A TRUE MODEL OF THE SOURCE
```

Also:

```text
THIS KERNEL COMPARES ONE FIXED INTEGER MATRIX UNDER PRIME REDUCTION.
IT DOES NOT DECIDE ABSTRACT MATROID REPRESENTABILITY.
```

That distinction prevents this research slice from overclaiming what the Fano example proves computationally.

## 6 — Executable research surface

`dogram.field_reduction.compare_prime_field_basis_support(...)`:

1. validates a finite integer matrix and unique column labels;
2. requires declared prime characteristics;
3. enumerates rank-sized column subsets;
4. computes exact Gaussian rank in `GF(p)`;
5. returns basis counts and the exact support symmetric difference.

The frozen fixture is:

```text
tests/fixtures/field_reduction_dependence_001.json
```

Focused test:

```text
tests/test_field_reduction_dependence.py
```

No external dependency is introduced.

## 7 — TDD receipt

RED was observed before production implementation:

```text
ModuleNotFoundError: No module named 'dogram.field_reduction'
```

After the minimal kernel was added, the focused harness returned:

```text
Ran 2 tests in 0.001s
OK
```

The focused module and test also compile with Python.

The fixture was then bound to the test without changing the researched behavior.

## 8 — Runtime verdict

**NO PUBLIC OPERATOR.**

Explicit HOLD:

```text
field_reduction@1
field_representability@1
binary_matroid@1
regular_matroid@1
characteristic_set@1
```

The current kernel is research-only exact arithmetic.

## 9 — Seals

> **SAME CARRIER, DIFFERENT DECLARED FIELD, DIFFERENT DEPENDENCE SURFACE.**

> **THE DOMAIN IS NOT DECORATION. IT PARTICIPATES IN THE CALCULATION.**

> **CHANGE THE DECODER, RECEIPT THE DELTA; DO NOT PRETEND THE SOURCE CHANGED.**
