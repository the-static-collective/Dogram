# HOME-MOTION-COMMUTATOR-001 — Mutual Shears, Order Residue, and a Ternary 3x3 Face

**Date:** 2026-09-02  
**Status:** EXACT FINITE ALGEBRA + MODEL SPECIMEN · NO NEW RUNTIME OPERATOR  
**Runtime authority:** NONE  
**Owner boundary:** Dogram computes declared differences and preserves receipts. The names `HOME`, `MOTION`, `NuOmetry`, `Protection`, `Faithfulness`, `Connection`, and `Y` are interpretation-layer labels supplied by the surrounding research conversation. The exact mathematics below does not establish those interpretations.

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

---

## 0. Why this packet exists

A conversation-level architecture compressed into two complementary faces:

```text
HOME
= constitutional / invariant-bearing local field

MOTION
= traversal / transformation / nextness
```

The proposed intuition is mutual nesting:

```text
HOME in MOTION
MOTION in HOME
```

This packet asks only the bounded mathematical question:

> **Can a small exact model distinguish passive coexistence from genuinely order-sensitive mutual action, and can the order residue be retained as an explicit receipt?**

Answer for the declared toy model below:

```text
YES.
```

That answer is about the toy algebra only.

---

## 1. Receipt classes

```text
EXACT
  ordinary finite algebra / combinatorics calculated exactly

MODEL
  a declared assignment of conversation labels onto exact mathematics

ANALOGY
  a suggestive neighboring mathematical picture not proved to be the owning structure

HOLD
  an interpretation or extension not established by this packet
```

Nothing in this file creates a public Dogram operator.

---

## 2. `HOME-MOTION-3X3-001` — EXACT COMBINATORICS

Declare two three-element label sets:

```text
H = {P, F, C}

M = {possibility, crossing, realization}
```

No semantics are inferred from the names.

The Cartesian interaction surface is:

```math
H \times M
```

with exact cardinality:

```math
|H \times M| = 3 \cdot 3 = 9.
```

If the three outer HOME labels remain addressable in addition to the nine paired cells, the visible one-level count is:

```math
3 + 9 = 12.
```

Ternary recursive counts by depth are:

```text
depth 1:   3
depth 2:   9
depth 3:  27
depth 4:  81
depth 5: 243
depth 6: 729
```

Mathal:

> **THREE OUTER FIELDS PLUS THEIR 3x3 INTERACTION FACE YIELDS TWELVE ADDRESSABLE SLOTS WITHOUT DECLARING TWELVE INDEPENDENT PRIMITIVES.**

Boundary:

```text
3 + 9 = 12
!=
proof that any existing 12-field architecture is generated this way
```

---

## 3. `SEPARATE-FACTOR-CONTROL-001` — EXACT

First establish the boring control case.

Let `H` and `M` now denote arbitrary `3 x 3` linear operators. Lift them to the tensor-product space by:

```math
A = H \otimes I_3
```

and

```math
B = I_3 \otimes M.
```

Then the standard Kronecker-product identity gives:

```math
(H \otimes I_3)(I_3 \otimes M)
= H \otimes M
= (I_3 \otimes M)(H \otimes I_3).
```

Therefore:

```math
[A,B] = AB - BA = 0.
```

Exact receipt:

```text
lifted dimension: 9 x 9
commutator rank: 0
order-sensitive delta: none
```

Mathal:

> **SEPARATE FACTORS CAN COEXIST WITHOUT PRODUCING BRAID HISTORY.**

Interpretive boundary:

```text
commuting actions
!=
absence of all possible relational structure
```

It only says this declared pair of lifted actions is order-insensitive.

---

## 4. `MUTUAL-SHEAR-F3-001` — EXACT MODEL

To obtain the smallest nontrivial mutual-action specimen, work over the finite field:

```math
\mathbb F_3 = \{0,1,2\}.
```

Use a two-coordinate column state:

```math
x = \begin{pmatrix} h \\ m \end{pmatrix}
```

with arithmetic modulo `3`.

Interpretation-layer labels:

```text
h = HOME coordinate
m = MOTION coordinate
```

Define two determinant-one shears.

### A — HOME acts on MOTION

```math
A = \begin{pmatrix}
1 & 0 \\
1 & 1
\end{pmatrix}
```

so:

```math
A\begin{pmatrix}h\\m\end{pmatrix}
=
\begin{pmatrix}h\\h+m\end{pmatrix}.
```

The HOME coordinate is retained while the MOTION coordinate is updated by HOME.

### B — MOTION acts on HOME

```math
B = \begin{pmatrix}
1 & 1 \\
0 & 1
\end{pmatrix}
```

so:

```math
B\begin{pmatrix}h\\m\end{pmatrix}
=
\begin{pmatrix}h+m\\m\end{pmatrix}.
```

The MOTION coordinate is retained while the HOME coordinate is updated by MOTION.

Both satisfy:

```math
\det(A)=\det(B)=1 \pmod 3.
```

So both are invertible elements of `SL(2,3)`.

This is a declared toy assignment, not a discovered ontology.

---

## 5. `ORDER-DELTA-001` — EXACT

Compute the two compositions:

```math
AB
=
\begin{pmatrix}
1 & 1 \\
1 & 2
\end{pmatrix}
```

and

```math
BA
=
\begin{pmatrix}
2 & 1 \\
1 & 1
\end{pmatrix}
```

modulo `3`.

Therefore:

```math
AB \ne BA.
```

Exact receipt:

```text
same two generators: A and B
same finite field: F3
same state dimension: 2
composition AB != composition BA
```

Mathal:

> **THE SAME GENERATORS CAN LEAVE A DIFFERENT RESULT WHEN THEIR CROSSING ORDER CHANGES.**

This is the exact algebraic seam relevant to existing Dogram work on trace dependence.

See:

- `research/TRACE-DEPENDENCE-001.md`
- `research/ORIENTATION-SIGNATURE-001.md`
- `research/HIGHER-ORDER-DEPENDENCE-001.md`
- `research/CO-PHASE-WALK-BRAID-SPRING-001.md`

No claim is made that these papers/operators are equivalent constructions.

---

## 6. `BRAID-COMMUTATOR-RECEIPT-001` — EXACT

To isolate the group-theoretic residue of noncommutation, compute the group commutator:

```math
K = ABA^{-1}B^{-1}.
```

Over `F3`:

```math
A^{-1}
=
\begin{pmatrix}
1 & 0 \\
2 & 1
\end{pmatrix}
```

and

```math
B^{-1}
=
\begin{pmatrix}
1 & 2 \\
0 & 1
\end{pmatrix}.
```

The exact commutator is:

```math
K
=
\begin{pmatrix}
0 & 1 \\
2 & 0
\end{pmatrix}.
```

Since:

```math
K \ne I,
```

the two transformations do not commute.

The commutator powers are:

```math
K^1 =
\begin{pmatrix}0&1\\2&0\end{pmatrix}
```

```math
K^2 =
\begin{pmatrix}2&0\\0&2\end{pmatrix}
= -I
```

```math
K^3 =
\begin{pmatrix}0&2\\1&0\end{pmatrix}
```

```math
K^4 = I.
```

Therefore the commutator has exact order:

```math
\operatorname{ord}(K)=4.
```

Mathal:

> **ORDER DIFFERENCE CAN ITSELF BE RETAINED AS AN ALGEBRAIC CARRIER.**

Boundary:

```text
nonidentity group commutator
!=
proof of physical braid, causal history, moral difference, or semantic meaning
```

It is an exact receipt of noncommutation in this declared model.

---

## 7. `SL23-CLOSURE-001` — EXACT

Generate the subgroup of `GL(2,3)` from:

```math
\langle A,B \rangle.
```

Exact finite enumeration gives:

```text
closure size = 24
```

Every generated matrix has determinant `1 mod 3`.

Independently enumerate all `2 x 2` matrices over `F3` with determinant `1`.

Exact count:

```math
|SL(2,3)| = 3(3^2-1) = 24.
```

Therefore:

```math
\langle A,B \rangle = SL(2,3).
```

Mathal:

> **TWO MUTUAL TERNARY SHEARS GENERATE THE FULL 24-ELEMENT SPECIAL LINEAR GROUP `SL(2,3)`.**

Interpretive boundary:

`det = 1` means the exact linear transformations preserve the standard alternating area form over `F3` and are invertible. It does not automatically mean preservation of user-defined Protection, Faithfulness, Connection, truth, value, or authority.

---

## 8. Why `SL(2,3)` is interesting but not yet promoted

The finite group is mathematically real and exact.

The surrounding labels are a model.

The suggestive seam is:

```text
A:
retain HOME coordinate
shear MOTION by HOME

B:
retain MOTION coordinate
shear HOME by MOTION

A and B:
mutually change one another
without losing invertibility

AB != BA:
order leaves a delta

commutator K:
explicit receipt of that delta
```

This resembles the conversation-level NuOmetry intuition:

```text
one in the other
in one another
same ingredients
order-sensitive crossing
new retained residue
```

But resemblance remains interpretation-layer material.

---

## 9. Fiber / skew-product neighboring mathematics — ANALOGY / HOLD

A standard fiber bundle is a map:

```math
\pi:E\to B
```

whose total space is locally product-like:

```math
\pi^{-1}(U) \cong U \times F.
```

This gives a useful neighboring picture for:

```text
MOTION = base
HOME = local fiber carried along the road
```

However, no topological spaces, transition functions, local trivializations, or bundle axioms have been declared for the current architecture.

Therefore:

```text
HOME-in-MOTION resembles a fibered picture
!=
HOME-in-MOTION has been proved to be a fiber bundle
```

If future work allows MOTION to update HOME fibers, a skew-product, cocycle, connection, transport, or bundle-with-dynamics formulation may become more precise.

HOLD.

---

## 10. Multiway / rewrite neighboring mathematics — ANALOGY / HOLD

A second neighboring formalism is a multiway rewrite system.

There:

- one state may admit multiple rewrites;
- branch pairs record bifurcating evolutions;
- resolved/unresolved critical pairs can test confluence;
- causal invariance asks whether different update histories yield isomorphic causal networks.

This is suggestive for:

```text
Y      -> branch
HOLD   -> unresolved crossing
REFUSE -> pruned / inadmissible local continuation
receipt -> retained path history
```

But this packet does not define a rewrite system for PFC(D), JOY?, YES, or NOW!.

HOLD.

---

## 11. Smallest next proving specimens

### A. `COMMUTING-CONTROL`

Choose mutually independent operators.

Expected:

```text
AB = BA
commutator = I
```

Purpose: prove the method can distinguish no order residue.

### B. `MUTUAL-SHEAR-F3`

Reuse this packet's `A` and `B`.

Expected:

```text
AB != BA
commutator != I
order(commutator) = 4
generated group size = 24
```

Purpose: frozen exact fixture candidate.

### C. `SAME-ENDPOINT-DIFFERENT-WORD`

Find two execution words that land on the same visible state but differ as trace words under declared dependence.

Purpose: connect this algebraic seam to `TRACE-DEPENDENCE-001` without silently collapsing endpoint equality into history equality.

### D. `TARGET-RELATIVE-QUOTIENT`

Declare a target that ignores the order residue and another that inspects it.

Purpose:

```text
same two histories
EQUIVALENT_UNDER_T1
DIFFERENT_UNDER_T2
```

This would connect naturally to `OMEGA-QUOTIENT-001-RECEIPT.md`.

### E. `HOME-MOTION-3X3-FACE`

Keep the 3x3 interaction table as labels only and test whether any proposed 12-field downstream architecture actually needs all twelve addressable slots.

Purpose: prevent numerological promotion from a matching count.

---

## 12. Candidate mathals

```text
HOME = WHAT MUST SURVIVE.                 [MODEL LABEL]

MOTION = WHAT MAY CHANGE.                 [MODEL LABEL]

SEPARATE FACTORS NEED NOT LEAVE
ORDER-SENSITIVE RESIDUE.                  [EXACT IN CONTROL MODEL]

MUTUAL ACTION CAN MAKE ORDER MATTER.       [EXACT IN DECLARED MODEL]

THE GROUP COMMUTATOR CAN RETAIN
THE NONCOMMUTATION AS A RECEIPT.           [EXACT]

TWO DECLARED F3 SHEARS GENERATE SL(2,3).  [EXACT]

SAME GENERATORS != SAME COMPOSITION WORD. [EXACT WHEN AB != BA]

SAME PARENT SET != SAME PARENTAL BRAID.   [INTERPRETIVE COMPRESSION]
```

---

## 13. Boundary

This packet does **not** establish:

- that P/F/C are universal primitives;
- that HOME and MOTION are mathematical objects of one unique type;
- that NuOmetry is equivalent to `SL(2,3)`;
- that the number `24` carries semantic, theological, or architectural authority;
- that every order difference matters to every target;
- that every noncommuting system should be interpreted as a braid;
- that a 12-field architecture is validated by `3+9=12`;
- that a fiber-bundle interpretation has been proved;
- any new Dogram public operator.

It preserves one exact finite proving specimen:

```text
separate actions can commute
mutual actions can fail to commute
failure to commute has an exact receipt
that receipt can be peeled further
```

---

## 14. Exit receipt

```text
DECLARED FIELD:
F3

DECLARED GENERATORS:
A = [[1,0],[1,1]]
B = [[1,1],[0,1]]

EXACT:
det(A) = det(B) = 1 mod 3
AB != BA
ABA^-1B^-1 = [[0,1],[2,0]]
order(commutator) = 4
< A,B > = SL(2,3)
|SL(2,3)| = 24

MODEL INTERPRETATION:
A = HOME acts on MOTION
B = MOTION acts on HOME
commutator = order-sensitive residue

AUTHORITY:
NONE
```

**DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**
