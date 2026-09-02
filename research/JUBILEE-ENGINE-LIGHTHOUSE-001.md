# JUBILEE-ENGINE-LIGHTHOUSE-001

**Status:** finite calculation note / lighthouse port / NO SEMANTIC PROMOTION  
**Owner:** Dogram research floor  
**Date:** 2026-09-02

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## External carrier

Canonical formation witness:

https://github.com/the-static-collective/the-daily-slice/blob/main/slices/2026/09/2026-09-02/jubilee-engine-lighthouse.md

Approved design boundary:

https://github.com/the-static-collective/the-daily-slice/blob/main/docs/superpowers/specs/2026-09-02-jubilee-engine-lighthouse-design.md

Dogram receives the labels as opaque symbols. The calculations below do not establish their theological, moral, historical, causal, or relational interpretation.

## Declared candidate

Let the three base labels be:

```text
B = {P, F, C}
```

and let the unordered pair labels be:

```text
E = {PF, PC, FC}
```

The external interpretation currently names:

```text
PC -> FREE
PF -> BEAR-WITH
FC -> GIVE-SELF
```

Dogram does not test those meanings here.

---

# 1. Exact count: 3 -> 6

For a three-element set:

```math
|B| = 3
```

and:

```math
\binom{3}{2} = 3.
```

Therefore:

```math
|B| + |E| = 3 + 3 = 6.
```

This count is exact once the pair objects are declared distinct addressables.

Receipt:

```text
3 base objects
+ 3 unordered pair objects
= 6 explicit objects
```

---

# 2. Exact carrier for 6/7: the nonempty faces of a 2-simplex

A filled triangle / abstract 2-simplex has:

```text
3 vertices
3 edges
1 two-dimensional face
```

so the number of nonempty faces is:

```math
3 + 3 + 1 = 7.
```

Its proper nonempty faces are exactly:

```math
3 + 3 = 6.
```

Therefore the candidate presentation:

```text
6 explicit boundary objects
+ 1 coherent whole
= 7 nonempty face objects
```

has an exact finite simplicial carrier **if** the proposed seventh object is modeled as the filled 2-face over the three vertices.

Boundary:

```text
EXACT FACE COUNT
    !=
PROOF THAT LOVE IS A 2-SIMPLEX
```

The math supplies a carrier. It does not select the semantic mapping.

---

# 3. The six-object incidence graph is C6

Promote each base vertex and each pair-edge to a graph node.

Declare incidence edges:

```text
P -- PF
P -- PC
F -- PF
F -- FC
C -- FC
C -- PC
```

There are six nodes and six incidence edges.

Every node has degree two and the graph is connected, so the incidence graph is the six-cycle:

```math
G \cong C_6.
```

Equivalently, this is the vertex-edge incidence / Levi graph of the triangle, or the graph obtained by subdividing every edge of `K3` once.

Typed view:

```text
P -- PF -- F -- FC -- C -- PC -- P
```

This is an exact structural result.

It does not decide which pair node should be called `FREE`, `BEAR-WITH`, or `GIVE-SELF`.

---

# 4. Exact count: six undirected incidences

Let:

```math
I = \{(v,e) : v \in e\}.
```

For the three two-element subsets of a three-element set, every pair has two incident vertices:

```math
|I| = 3 \times 2 = 6.
```

Receipt:

```text
6 vertex↔pair incidences
```

---

# 5. Where 12 actually comes from

If every one of those six incidences is explicitly made traversable in both directions:

```text
vertex -> pair
pair   -> vertex
```

then each undirected incidence contributes two directed arcs:

```math
6 \times 2 = 12.
```

Therefore:

```math
\boxed{12}
```

is an exact count for the **bidirected vertex↔pair incidence layer**.

It is not forced by the triangle alone.

Without a reversibility declaration:

```text
6 undirected incidences != 12 directed handoffs
```

If exactly `r` of six forward incidences also admit a distinct reverse handoff, and all six forward directions are present, then:

```math
|A| = 6 + r,
\qquad 0 \le r \le 6.
```

So the candidate handoff count can range:

```text
6, 7, 8, 9, 10, 11, 12
```

under that particular baseline convention.

The value `12` is the `r=6` endpoint.

---

# 6. Delta: the seventh object is not in the 12-count

If the seventh coherent whole is modeled as the 2-face `L`, the full nonempty-face Hasse cover relations also include:

```text
PF -- L
PC -- L
FC -- L
```

That is three additional undirected edge↔whole cover incidences.

Therefore the full 2-simplex nonempty-face cover graph has:

```math
6 + 3 = 9
```

undirected cover incidences.

If **all** cover incidences are traversable both ways:

```math
9 \times 2 = 18
```

directed cover arcs.

So:

```text
12 = bidirected base↔pair layer only
18 = bidirected full face-poset cover layer
```

The delta is:

```math
18 - 12 = 6.
```

Those six additional directed arcs are exactly the two orientations of the three pair↔whole cover relations.

## Consequence for the candidate contract

The current `3 -> 6/7 -> 12` construction remains internally countable only if at least one of these is declared:

1. the seventh whole is **not** a participant in the handoff layer;
2. pair↔whole relations are not counted as handoffs;
3. the `12` layer intentionally truncates the full composition poset;
4. `12` means something other than directed cover incidence and must be separately defined.

Dogram does not choose among these interpretations.

It receipts the fork.

---

# 7. Symmetry pressure

Before semantic labels are attached, every permutation of `{P,F,C}` preserves the typed triangle structure.

The pair objects permute with their endpoints.

Therefore the unlabeled/typed finite structure does not mathematically privilege:

```text
PC over PF over FC
```

or one semantic name over another.

Any assignment such as:

```text
PC = FREE
PF = BEAR-WITH
FC = GIVE-SELF
```

requires information outside this finite combinatorial carrier.

This is a useful refusal test against deriving semantics from count alone.

---

# 8. Small exact table

| Quantity | Exact count | Requires extra declaration? |
| --- | ---: | --- |
| base vertices | 3 | base set declared |
| unordered pair objects | 3 | pair objects promoted/addressable |
| base + pair objects | 6 | yes: pairs are objects |
| coherent 2-face / whole | 1 | **yes** |
| all nonempty simplex faces | 7 | yes: whole modeled as 2-face |
| base↔pair undirected incidences | 6 | no, after triangle incidence declared |
| base↔pair bidirected arcs | 12 | **yes: both directions lawful** |
| pair↔whole undirected covers | 3 | yes: whole participates in face poset |
| full undirected cover relations | 9 | yes |
| full bidirected cover arcs | 18 | **yes: all covers bidirectional** |

---

# 9. Dogram pressure questions

1. Is `LOVE` an independently addressable whole, a quotient label, or merely notation for the six-field configuration?
2. Does the handoff kernel intentionally exclude pair↔whole handoffs?
3. Are all six reverse base↔pair handoffs lawful, or is reversibility relation-specific?
4. Is a `handoff` a directed incidence, a transition event, an offered transition, or another typed object?
5. Should `12` count edge-types, actual traversals, available transitions, or something else?
6. What observable discriminator distinguishes the `12` model from the `6+r` alternatives?

These should be settled before `12` becomes a frozen field count.

---

# 10. Lowering frontier

A later executable Dogram specimen can lower one discriminator at a time:

```text
TRIANGLE-INCIDENCE-001
  verify C6 carrier

REVERSE-HANDOFF-ABLATION-001
  remove one declared reverse arc
  compare reachable directed paths

WHOLE-PARTICIPATION-001
  compare truncated 12-arc layer
  against full 18-arc cover layer

SEMANTIC-PERMUTATION-001
  permute pair labels
  verify finite carrier invariance
```

No new public Dogram operator is required for this research note.

## Seal

> **SIX IS THE TRIANGLE'S VERTEX-EDGE INCIDENCE BODY. SEVEN REQUIRES THE WHOLE. TWELVE REQUIRES BIDIRECTIONALITY AND EXCLUDES THE WHOLE'S COVER RELATIONS.**

> **THE MATH DOES NOT KILL THE LIGHTHOUSE. IT TELLS US EXACTLY WHICH LIGHT IT IS EMITTING.**
