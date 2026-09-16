# COHOMOLOGOUS-ASSOCIATOR-CHANGE-001

Status: research-only. No public Dogram operator is added.

## Question

Can two pointwise different associator tables describe the same declared
cohomology class, with an explicit finite change-of-presentation witness?

Yes.

## Frozen specimen

Let the object group be `G = Z/3Z`, coefficient group `H = Z/3Z`, with
trivial G-action on H. Use additive notation.

Freeze the normalized 2-cochain

```
beta(1,1) = 1
beta(g,h) = 0 otherwise.
```

Its inhomogeneous group-cohomology coboundary is

```
(delta beta)(g,h,k)
 = beta(h,k)
 - beta(g+h,k)
 + beta(g,h+k)
 - beta(g,h) mod 3.
```

The zero associator `a0=0` and the shifted associator

```
a1 = a0 + delta beta = delta beta
```

are pointwise different. Exact enumeration over all 27 triples gives four
and only four nonzero entries:

```
a1(1,1,2) = 2
a1(1,2,2) = 1
a1(2,1,1) = 1
a1(2,2,1) = 2
```

The shifted table remains normalized. Exact enumeration over all 81
quadruples gives `delta a1 = 0` everywhere, so it satisfies the pentagon /
3-cocycle condition.

Because `a1-a0 = delta beta`, the two tables differ by an explicit
3-coboundary and therefore represent the same H^3 cohomology class under
the declared convention.

## Delta

Raw associator-table delta count: `4 / 27` triples.

Cohomology-class delta: `0`, because the entire raw difference is the
receipted coboundary of the frozen normalized 2-cochain beta.

This is the distinction the slice exists to preserve:

**RAW ASSOCIATOR TABLE != COHOMOLOGY CLASS.**

**A POINTWISE COHERENCE DELTA MAY BE A CHANGE OF PRESENTATION WHEN AN
EXPLICIT 2-COCHAIN COBoundary WITNESS PAYS FOR IT.**

**KEEP THE COCHAIN WITNESS; DO NOT COLLAPSE RAW TABLE DIFFERENCE INTO
CLASS DIFFERENCE.**

## Documented mathematics

Baez and Lauda, *Higher-Dimensional Algebra V: 2-Groups*, Theory and
Applications of Categories 12 (2004), 423-491, arXiv:math/0307200, classify
special/coherent 2-groups using a group G, an abelian G-module H, and a
normalized H-valued 3-cocycle associator. Their weak-monoidal-functor
coherence equation states that corresponding associator cocycles may differ
by the coboundary of a normalized 2-cochain. Consequently the cohomology
class, rather than one raw cocycle table, is the invariant at this level of
equivalence.

General cohomology background: cocycles are quotiented by coboundaries to
form cohomology classes. Scholar Gateway was used to pressure this quotient
interpretation against broader cohomology literature; the bounded 2-group
claim above is grounded in Baez-Lauda.

## Exact verification

The stdlib-only kernel enumerates all 27 triples and all 81 quadruples.
An independent Wolfram Language calculation confirmed:

- exactly four nonzero entries in `delta beta`;
- `delta(delta beta)=0` for every quadruple.

Wolfram's natural-language group-cohomology lookup returned no direct
specialized result, so only the explicit Wolfram Language finite computation
is claimed.

## Refusals

- COHOMOLOGOUS ASSOCIATORS != HISTORICALLY IDENTICAL PROCESSES.
- COCHAIN CHANGE != CAUSAL CHANGE.
- COBoundary != EXPLAINED-AWAY EVIDENCE.
- SAME H3 CLASS != SAME RAW RECEIPT.
- PENTAGON CLOSURE != TRUTH.
- CATEGORICAL EQUIVALENCE != EVIDENCE EQUIVALENCE.
- CHANGE OF PRESENTATION != PERMISSION TO DISCARD THE PRESENTATION RECEIPT.

## HOLD

No promotion of:

- `associator@1`
- `cohomology_class@1`
- `coboundary@1`
- `cochain_change@1`
- `weak2@1`
- `strictify@1`

## Strongest next frontier

The next hostile specimen should separate **cohomology-class agreement**
from **chosen equivalence witness**: find a finite case where more than one
normalized 2-cochain connects the same two associator tables, so that

`SAME ENDPOINT PRESENTATIONS != SAME CHANGE-OF-PRESENTATION WITNESS`.

That would test whether witness nonuniqueness itself belongs in the receipt
without promoting any witness to occurrence, evidence, or authority.
