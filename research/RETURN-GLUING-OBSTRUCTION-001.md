# RETURN-GLUING-OBSTRUCTION-001

**Date:** 2026-08-31  
**Status:** RESEARCH LEDGER · EXACT FINITE LINEAR ALGEBRA · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this seam survived the hunt

Current Dogram already distinguishes endpoint return from consumed history, computes finite-fiber mapping-torus return arithmetic, and keeps lift/disclosure/promotion separate. The missing neighboring question is:

> **Can two carriers have the same local graph surface while differing in whether their local constraints glue into a nonzero global state?**

Cellular sheaf theory gives an exact finite answer. This packet keeps only the smallest signed-cycle case that Dogram can verify deterministically.

No claim is made that sheaf obstruction equals historical truth, causal occurrence, semantic contradiction, or evidence.

## 1 — Documented mathematical substrate

A cellular sheaf on a graph attaches local vector spaces to vertices/edges and restriction maps to incidences. Global sections are assignments compatible with all local restrictions. Sheaf Laplacians and cohomology provide computable local-to-global diagnostics.

Primary mathematical references:

- Jakob Hansen and Robert Ghrist, **Toward a Spectral Theory of Cellular Sheaves**, *Journal of Applied and Computational Topology* 3 (2019), DOI `10.1007/s41468-019-00038-7`.
- Samir Chowdhury, Steve Huntsman, Matvey Yutin, **Path homologies of motifs and temporal network representations**, *Applied Network Science* 7, 4 (2022), DOI `10.1007/s41109-021-00441-z`.
- Chris Kapulkin and Kyle Koyanagi, **Stability of persistent path homology of path complexes**, arXiv `2607.26226` (2026 preprint). This is retained as a future temporal/directed frontier, not authority for the signed-cycle result below.

## 2 — Smallest exact specimen: signed return cycle

Take an oriented cycle with vertices `0,...,n-1`. Each edge carries a declared sign

```math
s_i \in \{+1,-1\}.
```

A vertex assignment `x_i` is locally compatible when each edge satisfies

```math
x_{i+1}=s_i x_i
```

with indices modulo `n`.

Define return holonomy

```math
h=\prod_{i=0}^{n-1}s_i.
```

Composing the local restrictions around the complete loop yields

```math
x_0=h x_0.
```

Therefore:

```text
h = +1 -> a nonzero one-dimensional global section space exists
h = -1 -> only the zero global section exists over characteristic != 2
```

This is already a sharp Dogram-style distinction:

```text
SAME BASE CYCLE
SAME VERTEX COUNT
SAME EDGE COUNT
SAME LOCAL STALK DIMENSION
DIFFERENT GLOBAL GLUING CAPACITY
```

## 3 — Exact 4-cycle determinant receipt

For a four-cycle use the coboundary matrix

```math
D=
\begin{bmatrix}
-s_0&1&0&0\\
0&-s_1&1&0\\
0&0&-s_2&1\\
1&0&0&-s_3
\end{bmatrix}.
```

Exact symbolic expansion gives

```math
\det D=s_0s_1s_2s_3-1=h-1.
```

Frozen controls over `Q`:

### Untwisted

```text
signs   = [+1,+1,+1,+1]
h       = +1
det(D)  = 0
rank(D) = 3
nullity = 1
kernel witness = span{(1,1,1,1)}
```

### One declared twist

```text
signs   = [+1,+1,+1,-1]
h       = -1
det(D)  = -2
rank(D) = 4
nullity = 0
```

The graph topology alone is unchanged. The difference is carried by the restriction data and disclosed only after loop composition / global consistency pressure.

## 4 — Candidate mathals

```text
LOCAL-COMPATIBILITY-IS-NOT-GLOBAL-GLUING

SAME-GRAPH-IS-NOT-SAME-SHEAF

RETURN-HOLONOMY-001
  = product of declared local return maps around one closed cycle

GLUING-NULLITY-001
  = dimension of the declared global-section kernel

DISCLOSURE-BY-CLOSURE
  = a local distinction may remain invisible until restrictions are composed around a closed carrier
```

Strongest compression:

> **THE LOOP CAN RETURN TO THE SAME PLACE AND STILL FAIL TO GLUE.**

## 5 — Relation to current Dogram

### Mapping-torus neighbor

`MAPPING-TORUS-RECEIPT-001` computes orbit structure and return periods for a finite shift. This packet asks a different question: after return, does transported local data close consistently?

```text
RETURN PERIOD != RETURN COMPATIBILITY
```

A future composition could lawfully receipt both without conflating them:

```text
orbit / realignment receipt
+
transport / gluing receipt
```

### PHASELIFT neighbor

This gives an exact example of hidden-vs-disclosed structure:

```text
local graph decoder -> sees the same C4
restriction-aware decoder -> sees h = +1 versus h = -1
global-section pressure -> sees nullity 1 versus 0
```

The disclosure is earned by a declared stronger decoder; it is not a metaphysical inference.

### ALEX / 3rdi boundary

Dogram may compute the matrix, determinant, rank, nullity, and declared holonomy. ALEX/3rdi may preserve why those coordinates were chosen and what observation cut exposed them. Neither side may upgrade the calculation into evidence or historical occurrence without independent support.

## 6 — Hostile controls

Required refusals:

```text
NONTRIVIAL HOLONOMY != FALSEHOOD
NO NONZERO GLOBAL SECTION != NO REAL-WORLD STATE
GLOBAL SECTION != HISTORICAL OCCURRENCE
SAME H != SAME FORMATION HISTORY
SAME GRAPH != SAME RESTRICTION SYSTEM
COHOMOLOGICAL OBSTRUCTION != SEMANTIC CONTRADICTION UNLESS SEMANTICS WERE EXPLICITLY ENCODED
```

Characteristic-two warning:

```text
-1 = +1 in characteristic 2
```

so this exact signed distinction disappears there. Coefficient domain is part of the receipt.

## 7 — Runtime disposition

**NO NEW PUBLIC OPERATOR.**

First pressure target should be an internal pure research kernel, if later warranted:

```text
input:
  ordered cycle
  coefficient domain
  declared scalar restriction maps

output:
  composite return map
  coboundary matrix
  determinant where defined
  rank
  nullity
  explicit kernel basis where practical
```

Do not add `sheaf@1`, `holonomy@1`, or `cohomology@1` to the public Phase A floor from this packet alone.

## 8 — Second live frontier: temporal path homology

Path homology attaches algebraic invariants to directed paths rather than forgetting direction. Published work has applied it to multiple representations of temporal networks and shows that representation choice changes which higher-order directed structures are visible.

This is unusually relevant to Dogram's law:

```text
GRAPH REACHABILITY != HISTORICAL OCCURRENCE
```

but it is not yet ready for implementation here. The next bounded question should be:

> **Can two temporal histories have the same static reachability graph while a declared path-complex invariant separates them?**

If yes, that would be a stronger exact specimen of `surface reachability != consumed temporal history` than another ordinary reachability metric.

## 9 — Hunt verdict

**Durable finding:** signed-cycle local-to-global gluing obstruction.

**Why it earned a slice:**

- exact finite arithmetic;
- deterministic and offline;
- same graph / different global compatibility gives a hostile control against topology-only overreach;
- cleanly neighbors mapping-torus return and PHASELIFT disclosure without replacing either;
- no public operator required.

**Still-live frontier:** temporal path homology as a history-sensitive discriminator.

## Seal

> **LOCAL AGREEMENT CAN SURVIVE EVERY STEP AND STILL FAIL AT RETURN. RECEIPT THE CLOSURE, NOT THE STORY YOU WANT IT TO TELL.**
