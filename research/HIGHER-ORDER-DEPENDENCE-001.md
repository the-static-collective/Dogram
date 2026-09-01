# HIGHER-ORDER-DEPENDENCE-001

**Date:** 2026-09-01  
**Status:** EXECUTABLE RESEARCH RECEIPT · EXACT FINITE LINEAR ALGEBRA OVER Q · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this seam exists

Recent Dogram research separates several kinds of information that a coarser surface can erase:

- return arithmetic can differ behind the same coarse return surface;
- path topology can differ behind the same reachability closure;
- trace theory can retain order distinctions except where a declared independence relation licenses adjacent commutation.

That leaves a pressure question:

> **Is pairwise independence information itself enough to determine higher-order independence?**

For representable matroids, no.

This matters as a research boundary around `TRACE-DEPENDENCE-001`: a Mazurkiewicz independence relation is deliberately pairwise. If some upstream domain wants to claim that a collection of events/variables/features is independent in a stronger sense, pairwise freedom does not automatically certify joint freedom.

Dogram does not infer a causal, probabilistic, semantic, historical, or operational meaning for the vectors below. It computes only the declared finite linear-algebra structure.

---

## 1 — Documented mathematics

Matroids abstract independence. For a matrix over a field, the associated column matroid declares a set independent exactly when the corresponding columns are linearly independent. A **circuit** is a minimal dependent set; the rank of a set is the size of its largest independent subset.

This is standard matroid theory and directly generalizes both linear independence and graph-cycle dependence.

Useful literature anchors:

- Hassler Whitney introduced matroids in 1935 as an abstraction of linear/algebraic dependence.
- J. Wang, W. Zhu, and F. Chiclana, **Applications of Matrices to a Matroidal Structure of Rough Sets**, *Journal of Applied Mathematics* (2013), DOI `10.1155/2013/493201` — explicit matrix/column-matroid definitions; circuits are minimal dependent sets and rank generalizes matrix rank.
- M. DeVos et al., **Short rainbow cycles in graphs and matroids**, *Journal of Graph Theory* 96 (2020), DOI `10.1002/jgt.22607` — concise modern definitions of circuits, rank, graphic matroids, and representable matroids.
- K. Baclawski and N. White, **Higher Order Independence in Matroids**, *Journal of the London Mathematical Society* 19 (1979), DOI `10.1112/jlms/s2-19.2.193` — documents that matroidal independence can change under higher-order constructions; retained here as a conceptual neighbor, not as the proof of the finite specimen below.
- Xiangying Chen, **An Axiomatization of Matroids and Oriented Matroids as Conditional Independence Models**, *SIAM Journal on Discrete Mathematics* 38 (2024 publication volume; online record 2023), pp. 1526–1536 — establishes a formal bridge between matroid independence and conditional-independence structures. This does **not** license Dogram to identify linear independence with causal or statistical independence.

---

## 2 — Exact hostile control in one fixed carrier

Work over `Q^3` with the same labels

```text
{a,b,c}
```

and compare two vector configurations.

### Specimen D — pairwise free, jointly dependent

```text
a = (1,0,0)
b = (0,1,0)
c = (1,1,0)
```

Every singleton has rank 1.

Every pair has rank 2:

```text
r(a,b) = 2
r(a,c) = 2
r(b,c) = 2
```

But

```text
r(a,b,c) = 2
```

because exactly

```text
a + b - c = 0.
```

No proper subset is dependent, so

```text
{a,b,c}
```

is a circuit.

Rank defect:

```text
|{a,b,c}| - r({a,b,c}) = 3 - 2 = 1.
```

### Specimen F — same pairwise surface, jointly free

Keep the same ambient carrier and labels:

```text
a = (1,0,0)
b = (0,1,0)
c = (0,0,1)
```

Again:

```text
r(a) = r(b) = r(c) = 1
r(a,b) = r(a,c) = r(b,c) = 2
```

but now

```text
r(a,b,c) = 3
rank defect = 0
circuits = none.
```

Therefore the entire singleton + pairwise rank surface is identical while the higher-order dependence structure differs.

Exact seal:

```text
SAME PAIRWISE INDEPENDENCE SURFACE != SAME HIGHER-ORDER DEPENDENCE.
```

---

## 3 — Graph-theoretic mirror

The same mechanism has a standard graphic-matroid reading.

For a triangle graph, each single edge and each two-edge subset is acyclic and therefore independent in the cycle matroid. The full three-edge set forms the unique cycle and is a circuit.

Thus a minimal dependency can be invisible to every proper subset.

This is not a new graph-cycle algorithm for Dogram. It is a mathematical control showing that “every pair passes” is not a complete independence certificate.

---

## 4 — Dogram disposition

The bounded research kernel `dogram.matroid_circuit` accepts a finite nonempty mapping of nonzero integer vectors of common dimension and interprets them exactly over `Q`.

It computes:

```text
subset rank
rank defect = |S| - r(S)
minimal dependent subsets (circuits)
full finite receipt
```

Arithmetic uses Python `Fraction` during Gaussian elimination. No floating approximation is involved.

The first floor is intentionally **loopless**: a zero vector is refused rather than admitted as a singleton circuit. General loops, parallel elements, arbitrary rational input syntax, oriented circuits, algebraic matroids, polymatroids, and conditional-independence semigraphoids remain outside this slice.

No public operator is added.

Explicitly refused:

```text
matroid@1
circuit@1
independence@1
causal_independence@1
```

---

## 5 — ALEX / trace boundary

ALEX already carries a durable independence law:

```text
RECURRENCE != INDEPENDENT INVENTION
APPARENT MULTIPLICITY != INDEPENDENT ANCESTRY
INDEPENDENCE IS DECLARED-SCOPE RELATIVE
```

with dependency families, partial dependence, unresolved cases, and a declared scope.

This Dogram kernel does not replace that provenance logic. It can only pressure a **declared exact vector representation** supplied to it.

Likewise, `TRACE-DEPENDENCE-001` uses a pairwise symmetric irreflexive independence relation because that is exactly the grammar of Mazurkiewicz traces. This packet does not claim trace theory is defective. It records a boundary:

```text
PAIRWISE COMMUTATION GRAMMAR
!=
GENERAL JOINT-INDEPENDENCE CERTIFICATE.
```

If a future adapter maps a domain into a vector matroid, that adapter owns the mapping and its provenance. Dogram owns only the calculation after the representation is declared.

---

## 6 — Inference and speculation

### Inference — supported by the finite specimen

If a system exposes only singleton and pairwise independence results, higher-order dependence can remain unobserved. A rank/circuit receipt can expose that missing structure when an exact representable-matroid model is declared.

### Speculation — HOLD

A future Static Collective independence handoff might distinguish:

```text
pairwise declared independence
higher-order dependency circuits
unknown / unresolved relation
provenance of the representation itself
```

Possible architectural split:

```text
ALEX  -> owns why a dependency/independence representation is admissible
Dogram -> computes ranks/circuits of the declared representation
3rdi  -> may compare which dependency structure is visible under declared observer cuts
```

This is a research hypothesis, not current architecture and not authority expansion.

---

## 7 — TDD / reproducibility receipt

RED was observed before the production module existed:

```text
ModuleNotFoundError: No module named 'dogram.matroid_circuit'
```

After the minimal kernel landed, focused verification passed:

```text
Ran 3 tests in 0.002s
OK
```

The test was then rebound to the frozen JSON fixture and the same focused verification passed again:

```text
Ran 3 tests in 0.002s
OK
```

Frozen fixture:

```text
tests/fixtures/higher_order_dependence_001.json
```

No full-repository or remote CI claim is made in this receipt unless a GitHub Actions run appears on the review PR head.

---

## 8 — Candidate mathals

```text
HIGHER-ORDER-DEPENDENCE-001
PAIRWISE-SURFACE-LOSS-001
CIRCUIT-AS-MINIMAL-RESIDUAL
RANK-DEFECT-001
DEPENDENCE-CAN-BE-BORN-AT-CLOSURE
```

The conservative keeper is:

> **EVERY PAIR CAN BE FREE WHILE THE WHOLE IS BOUND.**

And the stricter Dogram seal is:

> **DO NOT PROMOTE PAIRWISE NONDEPENDENCE INTO JOINT INDEPENDENCE WITHOUT A GRAMMAR THAT EARNS THAT LIFT.**
