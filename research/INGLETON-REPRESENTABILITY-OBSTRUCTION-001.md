# INGLETON-REPRESENTABILITY-OBSTRUCTION-001

**Status:** RESEARCH LEDGER · EXACT FINITE RANK INEQUALITY · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this seam

A valid matroid rank function need not be linearly representable over any field. Dogram therefore needs to keep two questions separate:

```text
DOES THE DECLARED RANK TABLE SATISFY MATROID AXIOMS?
!=
COULD THIS MATROID COME FROM LINEAR DEPENDENCE IN A VECTOR SPACE?
```

`MATROID-RANK-COHERENCE-001` addresses the first question on its own review branch. This slice is intentionally independent of that branch and addresses only one exact necessary condition for the second.

## 1 — Documented mathematics

For subsets `Y1,Y2,Y3,Y4` of a representable matroid, Ingleton's inequality requires

```math
r(Y_1)+r(Y_2)+r(Y_1\cup Y_2\cup Y_3)+r(Y_1\cup Y_2\cup Y_4)+r(Y_3\cup Y_4)
\le
r(Y_1\cup Y_2)+r(Y_1\cup Y_3)+r(Y_1\cup Y_4)+r(Y_2\cup Y_3)+r(Y_2\cup Y_4).
```

A violation therefore certifies that the supplied rank data cannot arise from a linearly representable matroid under that declared grouping.

Primary modern source used for the frozen witness:

- R. Y. Sharp, **Peter Vámos, 1940–2020**, *Bulletin of the London Mathematical Society* 54(3), 2022. DOI `10.1112/blms.12689`. The article reproduces Ingleton's inequality and the standard Vámos-matroid violation.
- Peter Nelson, **Almost all matroids are nonrepresentable**, *Bulletin of the London Mathematical Society* 50(2), 2018. DOI `10.1112/blms.12141`. This is retained as context that matroidhood and representability are materially different classes.

## 2 — Frozen Vámos witness

Use

```text
Y1 = {3,4}
Y2 = {5,6}
Y3 = {1,2}
Y4 = {7,8}
```

with the consumed Vámos ranks:

```text
r(Y1) = 2
r(Y2) = 2
r(Y1∪Y2∪Y3) = 4
r(Y1∪Y2∪Y4) = 4
r(Y3∪Y4) = 4

r(Y1∪Y2) = 3
r(Y1∪Y3) = 3
r(Y1∪Y4) = 3
r(Y2∪Y3) = 3
r(Y2∪Y4) = 3
```

Therefore

```text
left  = 2+2+4+4+4 = 16
right = 3+3+3+3+3 = 15
slack = right-left = -1
```

The necessary representability inequality fails by exactly one rank unit.

Exact keeper:

> **MATROID-COHERENT DOES NOT IMPLY LINEARLY REPRESENTABLE.**

## 3 — Representable hostile control

For the uniform matroid `U(4,8)`, represented for example by sufficiently generic columns over an appropriate field, use `r(S)=min(4,|S|)` on the same ten consumed subsets.

Then

```text
left  = 16
right = 20
slack = 4
```

so the Ingleton condition passes.

Passing is deliberately weak:

```text
INGLETON PASS != REPRESENTABILITY CERTIFICATE
```

The kernel implements a necessary-condition obstruction, not a representability solver.

## 4 — Dogram boundary

The executable surface consumes only the rank entries actually used by the chosen four-set witness and returns:

```text
left
right
slack = right-left
violates = slack < 0
consumed_subsets
```

It does **not**:

- validate the matroid rank axioms;
- prove representability when the inequality passes;
- identify a field of representation;
- infer causal, statistical, semantic, historical, evidentiary, or physical dependence;
- decide that a supplied rank representation is faithful to its source;
- promote `ingleton@1`, `representability@1`, or `linear@1` into public Dogram dispatch.

## 5 — Mathal ladder

```text
ARBITRARY RANK TABLE
    -> matroid coherence
    -> Ingleton-compatible
    -> ? representable over some field
    -> ? represented by this declared matrix
```

Every arrow is a new mathematical question. None licenses a formation or truth claim.

Candidate seals:

> **PASSING THE AXIOMS DOES NOT EARN THE ORIGIN STORY.**

> **A VALID INDEPENDENCE GRAMMAR MAY STILL HAVE NO LINEAR REALIZATION.**

> **OBSTRUCTION IS ONE-WAY: FAILURE CAN REFUTE A REPRESENTATION CLASS; PASSAGE DOES NOT PROVE MEMBERSHIP.**

## 6 — Verification receipt

TDD sequence reproduced in the focused harness:

```text
RED: ModuleNotFoundError: dogram.ingleton
GREEN: 3 tests, 0 failures
compileall: pass
```

The Vámos arithmetic was independently recomputed as `16` versus `15`; a WolframAlpha query was attempted but returned no result, so no Wolfram verification claim is made.
