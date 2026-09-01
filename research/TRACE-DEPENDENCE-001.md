# TRACE-DEPENDENCE-001 — partial commutation / history quotient

**Date:** 2026-08-31  
**Status:** EXECUTABLE RESEARCH KERNEL · FINITE EXACT COMBINATORICS · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this seam exists

Recent Dogram research now distinguishes:

- finite return arithmetic from interpretation;
- same graph surface from different local-to-global gluing capacity;
- same reachability closure from different directed path topology.

A different question remains:

> **When two execution words differ only by ordering, which order differences are merely alternative interleavings of declared-independent events, and which differences survive as history?**

Mazurkiewicz trace theory gives a bounded answer without asking Dogram to infer causality.

## 1 — Documented mathematics

Let `A` be a finite alphabet of event labels and let

```math
I \subseteq A \times A
```

be a declared **independence relation**, required to be symmetric and irreflexive. Its complement is the dependence relation.

Trace theory identifies words modulo adjacent commutations of independent letters. In the conventional presentation,

```math
uabv \equiv ubav \quad\text{when }(a,b)\in I.
```

The resulting equivalence classes are Mazurkiewicz traces. They model non-sequential/concurrent behavior through sequential observations while preserving declared dependence constraints.

References:

- A. Mazurkiewicz, **Basic notions of trace theory** (1988), pp. 285–363. The work presents traces as representations of non-sequential concurrent processes and develops their algebraic properties.
- H. P. León, S. Haar, D. Longuet, **Model-based testing for concurrent systems with labelled event structures**, *Software Testing, Verification and Reliability* 24(7), 558–590 (2014), DOI `10.1002/stvr.1543`. Section 6 explicitly recalls partial commutation: words are equivalent when successive swaps exchange neighboring independent letters.
- X. Gao et al., **Unified Mathematical Framework for Slicing and Symmetry Reduction over Event Structures**, *Journal of Applied Mathematics* 2014, DOI `10.1155/2014/352152`. Event structures are represented with partial-order/configuration semantics rather than only interleaved words.

The literature also supplies the key boundary: partial-order semantics contains information that a purely interleaved or state-only view may discard. This does **not** make the partial order an observed causal history unless the independence/dependence data are actually warranted upstream.

## 2 — Exact finite kernel

For a word

```text
w = e0 e1 ... e(n-1)
```

build its finite dependence DAG on event occurrences. For positions `i < j`, add

```text
i -> j
```

when either:

- the two labels are equal; or
- the ordered label pair is **not** in the declared independence relation.

Every topological ordering of this DAG is a linearization compatible with the same declared dependence constraints. The research kernel chooses one deterministic representative by repeatedly taking the lexicographically smallest currently available event label.

This is a calculational normalization only. It does not say which events really were independent.

## 3 — Frozen specimens

### A. Independent interleaving

```text
I = {(a,b),(b,a)}
left  = ab
right = ba
```

Exact result:

```text
canonical(left)  = ab
canonical(right) = ab
trace_equivalent = true
```

Candidate mathal:

> **ORDER DIFFERENCE CAN DISAPPEAR WHEN THE DECLARED DEPENDENCE FIELD DOES NOT REQUIRE IT.**

### B. Same frozen endpoint, dependent order

Freeze an external coarse endpoint as identical for both histories:

```text
left.endpoint  = SAME
right.endpoint = SAME
```

but declare no independence between `a` and `c`:

```text
I = {}
left  = ac
right = ca
```

Exact trace result:

```text
canonical(left)  = ac
canonical(right) = ca
trace_equivalent = false
```

The endpoint is fixture context, not consumed by the trace calculation.

Candidate mathal:

> **SAME ENDPOINT DOES NOT ERASE DEPENDENT ORDER.**

Required refusal:

```text
trace-inequivalent -> different real-world occurrence
```

is invalid. The kernel proves only that the two supplied words occupy different classes under the supplied independence grammar.

### C. Hostile control against naive sorting

Let

```text
I = {(a,b),(b,a),(b,c),(c,b)}
```

so `b` commutes with both `a` and `c`, while `a` and `c` remain dependent.

Then:

```text
cba ~ cab
```

because the `b` occurrence can move around the fixed `c < a` dependence.

The deterministic dependence-poset representative is

```text
bca
```

for both words.

This control matters because a one-pass or locally greedy adjacent swap rule can stop at different irreducible words even when the words are trace-equivalent. Dogram therefore receipts the dependence DAG logic, not a metaphorical “sorting” story.

## 4 — Dogram inference

**Documented mathematics:** trace classes quotient sequential words by swaps of declared-independent neighboring events; partial-order/event-structure models preserve concurrency information beyond plain interleavings.

**Dogram inference:** a tiny trace-class kernel is useful beside `reach` and path homology because it answers a different question:

```text
reachability asks: can a state/node be reached?
path homology asks: what directed path topology survives the chosen graph representation?
trace dependence asks: which ordering differences survive after quotienting only declared-independent swaps?
```

These are not interchangeable.

**Speculation / HOLD:** ALEX or another provenance-bearing layer could eventually supply event identities and warranted independence/dependence claims; 3rdi could compare observer cuts over the same trace class. This packet does not define that handshake and does not grant Dogram authority to infer the relation.

## 5 — Runtime disposition

Research-only module:

```text
dogram.trace_dependence
```

Executable surface:

```text
canonical_trace(word, independence)
analyze_trace_pair(left, right, independence)
```

No public operator is admitted.

Explicitly refused:

```text
trace@1
concurrency@1
causal_order@1
history@1
```

A public operator would need a demonstrated cross-repo consumer, a stable schema for event identity and independence provenance, and hostile controls showing that composition with existing operators is inadequate.

## 6 — TDD receipt

RED was observed after committing the focused test first:

```text
ModuleNotFoundError: No module named 'dogram.trace_dependence'
```

The first GREEN attempt exposed an invalid hostile-control declaration: the fixture mentioned independence for labels not consumed by that pair. The contract was kept strict and the fixture corrected.

Fresh focused verification after the correction:

```text
Ran 4 tests in 0.001s
OK
```

No full-repository test claim is made from this environment.

## 7 — Seals

> **INTERLEAVING IS NOT AUTOMATICALLY HISTORY.**

> **COMMUTATION MUST BE DECLARED OR EARNED; DOGRAM DOES NOT GUESS IT FROM A SHARED ENDPOINT.**

> **SAME ENDPOINT != SAME TRACE CLASS. SAME TRACE CLASS != SAME OCCURRENCE.**

> **QUOTIENT ONLY THE ORDER DIFFERENCES THE GRAMMAR ACTUALLY LICENSES YOU TO FORGET.**
