# MATROID-RANK-COHERENCE-001

**Date:** 2026-09-01  
**Status:** RESEARCH KERNEL · EXACT FINITE SET-FUNCTION CHECKS · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this seam survived

Dogram now has an exact vector-matroid circuit kernel (`HIGHER-ORDER-DEPENDENCE-001`). That kernel starts from a concrete rational representation, so its subset ranks are automatically coherent as a matroid rank function.

A different problem appears when a rank/dependence surface is *declared* or arrives from another system:

> **Can a finite table look locally plausible while failing the global axioms required of a matroid rank function?**

Yes. The smallest useful hostile control needs only three labels.

## 1 — Documented mathematics

For a finite ground set `E`, a matroid rank function `r : 2^E -> N` is characterized by conventional rank axioms including:

```text
r(empty) = 0
0 <= r(X) <= |X|
X subset Y -> r(X) <= r(Y)
r(X) + r(Y) >= r(X intersect Y) + r(X union Y)
```

The final inequality is submodularity.

Useful references:

- Fortier, Király, Szigeti & Tanigawa, *On packing spanning arborescences with matroid constraint*, Journal of Graph Theory 93(2), 2019, DOI `10.1002/jgt.22484` — states finite matroid rank via normalization, monotonicity, subcardinality, and submodularity.
- de Vries, Raach & Vohra, *On inner independence systems*, Naval Research Logistics 72(1), 2025, DOI `10.1002/nav.22210` — gives equivalent rank/submodular characterizations of matroids.
- Huang, Zhu & Kuang, *Geometric Lattice Structure of Covering and Its Application to Attribute Reduction through Matroids*, Journal of Applied Mathematics 2014, DOI `10.1155/2014/183621` — states the rank-function characterization directly.

The mathematics here is classical; Dogram contributes only a deterministic finite receipt surface.

## 2 — Frozen valid control

Ground set:

```text
E = {a,b,c}
```

Use the uniform matroid `U_{1,3}`:

```text
r(empty) = 0
r(X) = 1 for every nonempty X
```

Thus:

```text
singletons = 1
pairs      = 1
triple     = 1
```

The table passes all checked rank axioms.

## 3 — Hostile top-order lift

Now hold every subset of size at most two fixed and change exactly one entry:

```text
r(empty) = 0
singletons = 1
pairs      = 1
r({a,b,c}) = 2
```

The hostile table remains:

```text
normalized
integer-valued
nonnegative
subcardinal
monotone
```

Yet for

```text
X = {a,b}
Y = {a,c}
```

we obtain

```text
r(X) + r(Y) = 1 + 1 = 2
r(X intersect Y) + r(X union Y) = 1 + 2 = 3
```

so

```text
2 >= 3
```

fails with exact residual

```text
3 - 2 = 1.
```

The same obstruction appears symmetrically for the other two overlapping pair pairs.

Exact compression:

```text
SAME RANK SURFACE THROUGH ORDER 2
!=
SAME GLOBAL MATROID COHERENCE
```

Candidate mathal:

> **LOCAL RANK PLAUSIBILITY != GLOBAL MATROID COHERENCE.**

## 4 — Dogram inference

This gives Dogram a useful pressure step *before* downstream interpretation:

```text
declared rank/dependence table
  -> finite axiom check
  -> attributable violating subsets if incoherent
  -> no semantic promotion
```

A coherent rank table may deserve further mathematical analysis. An incoherent one has failed its own declared grammar before questions of meaning, evidence, causality, or authority even arise.

This is not an inference engine. It is a refusal to calculate matroid consequences from a set-function that has not earned the name `matroid rank`.

## 5 — Information-theory neighbor — HOLD

Submodularity is also central in information theory and polymatroid theory. Entropy-like set functions can satisfy polymatroidal inequalities without being matroid rank functions; conversely, matroid rank functions are a much more restricted integer/subcardinal class.

Relevant neighbor:

- Madiman, Marcus & Tetali, *Entropy and set cardinality inequalities for partition-determined functions*, Random Structures & Algorithms 40(4), 2012, DOI `10.1002/rsa.20385` — develops submodularity-based entropy inequalities.

Possible future research question:

```text
Can Dogram distinguish:
  arbitrary set-function
  -> submodular / polymatroid-like
  -> matroid-rank coherent
  -> representable matroid
without collapsing those classes?
```

That is a mathematical classification ladder only. It must not be read as:

```text
submodular -> informative
matroidal -> causal
representable -> true
```

## 6 — Runtime boundary

This slice introduces only the research module:

```text
dogram.matroid_rank_coherence
```

It checks a complete finite integer rank table and returns deterministic violations of:

```text
NORMALIZATION
SUBCARDINALITY
MONOTONICITY
SUBMODULARITY
```

It does **not**:

- infer a rank table from evidence;
- infer independence from observations;
- decide causal/statistical/semantic independence;
- prove representability over a field;
- prove an oriented-matroid realization;
- grant evidence, support, authority, or truth;
- add a public Dogram operator.

Explicit HOLD:

```text
rank_coherence@1
submodular@1
polymatroid@1
representability@1
```

## 7 — Verification receipt

TDD order:

```text
RED:
focused test committed before production module
failure reason: dogram.matroid_rank_coherence did not exist

GREEN:
fresh focused harness
Ran 3 tests
OK
```

Frozen fixture:

```text
tests/fixtures/matroid_rank_coherence_001.json
```

The hostile specimen returns three `SUBMODULARITY` witnesses, each with residual `1`.

Wolfram semantic computation was also asked to evaluate the set-function inequality but returned no direct result, so no Wolfram-derived claim is made. The arithmetic above is exact integer arithmetic and independently reproduced by the focused kernel.

## 8 — Seals

> **A TABLE CAN LOOK LAWFUL ONE FACE AT A TIME AND STILL FAIL TO BE ONE OBJECT.**

> **THE AXIOMS ARE NOT MEANING. THEY ARE THE PRICE OF USING THE MATHEMATICAL NAME.**

> **CHECK THE GRAMMAR BEFORE YOU INTERPRET THE STORY.**
