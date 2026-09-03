# HEISENBERG-BILINEAR-ORDER-RESIDUE-001

**Date:** 2026-09-02  
**Status:** EXACT RATIONAL ALGEBRA + EXECUTABLE EXISTING-OPERATOR WITNESS · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0. Why this seam survived

Current `main` already contains `HOME-MOTION-COMMUTATOR-001`, which proves that two declared transformations can be order-sensitive and that a group commutator can retain the residue. The narrower next question is:

> **Can that order residue itself be an exact mixed second-order term that lowers into Dogram's already-existing `rectangle@1` calculation?**

For the smallest Heisenberg matrix specimen below, yes.

No new runtime operator is required.

## 1. Documented mathematical substrate

Let

```math
X=E_{12}=\begin{pmatrix}0&1&0\\0&0&0\\0&0&0\end{pmatrix},
\qquad
Y=E_{23}=\begin{pmatrix}0&0&0\\0&0&1\\0&0&0\end{pmatrix}.
```

Then

```math
X^2=Y^2=0,
\qquad
XY=E_{13},
\qquad
YX=0,
```

so

```math
[X,Y]=XY-YX=E_{13}.
```

The bracket is central in the strictly upper-triangular 3x3 Lie algebra:

```math
[X,E_{13}]=[Y,E_{13}]=0.
```

This is the standard step-2 Heisenberg pattern. For step-2 nilpotent Lie algebras, higher nested commutators vanish, so the Baker-Campbell-Hausdorff expansion truncates after the bracket term. See:

- Sean Li, **Stratified beta-numbers and traveling salesman in Carnot groups**, *Journal of the London Mathematical Society* 106(2), 2022, DOI `10.1112/jlms.12582` — gives BCH polynomial coordinates and the Heisenberg bracket relations `[X,Y]=Z`, `[X,Z]=[Y,Z]=0`.
- V. Ayala, H. Román-Flores, M. Torreblanca Todco, A. Lay-Ekuakille, **Control Sets of Linear Control Systems on Matrix Groups and Applications**, *Mathematical Problems in Engineering*, 2019, DOI `10.1155/2019/2963120` — records the upper-unitriangular 3x3 matrix representation of the Heisenberg group and its nilpotent Lie algebra.

## 2. Exact exponentials

Because `X^2=Y^2=0`, no approximation is involved:

```math
\exp(sX)=I+sX,
\qquad
\exp(tY)=I+tY.
```

Therefore

```math
\exp(sX)\exp(tY)
=I+sX+tY+stE_{13},
```

while

```math
\exp(tY)\exp(sX)
=I+sX+tY.
```

Hence the complete order delta is

```math
\boxed{\exp(sX)\exp(tY)-\exp(tY)\exp(sX)=st[X,Y]=stE_{13}}.
```

This is exact over `Q`; it is not a small-parameter approximation.

## 3. Group-commutator receipt

Since

```math
\exp(-sX)=I-sX,
\qquad
\exp(-tY)=I-tY,
```

the group commutator is exactly

```math
\exp(sX)\exp(tY)\exp(-sX)\exp(-tY)
=I+stE_{13}.
```

Thus the same bilinear scalar `st` appears as both:

```text
forward-order minus reverse-order central residue
and
group-commutator central residue.
```

Required refusal:

```text
nonzero commutator != causal mechanism
nonzero bracket != historical occurrence
central residue != semantic center
```

## 4. Frozen rational specimen

The executable fixture declares

```math
s=\frac23,
\qquad
t=\frac57.
```

Therefore

```math
st=\frac{10}{21}.
```

Forward order:

```math
\exp(\tfrac23X)\exp(\tfrac57Y)
=I+\frac23X+\frac57Y+\frac{10}{21}E_{13}.
```

Reverse order:

```math
\exp(\tfrac57Y)\exp(\tfrac23X)
=I+\frac23X+\frac57Y.
```

Exact delta:

```math
\frac{10}{21}E_{13}.
```

## 5. Rectangle lowering

Let the observed scalar surface be only the central `(1,3)` matrix coordinate.

For forward composition, switch the two generators on/off with Boolean axes `a,b in {0,1}`:

```math
F(a,b)=\left[\exp(asX)\exp(btY)\right]_{13}.
```

The four cells are

```text
F00 = 0
F10 = 0
F01 = 0
F11 = st
```

so the existing Dogram rectangle mixed delta is

```math
F_{11}-F_{10}-F_{01}+F_{00}=st.
```

For reverse composition

```math
G(a,b)=\left[\exp(btY)\exp(asX)\right]_{13},
```

all four cells are zero, so its mixed delta is zero.

For the frozen specimen:

```text
forward rectangle mixed delta = 10/21
reverse rectangle mixed delta = 0
```

This is the key Dogram result:

> **AN ORDER RESIDUE CAN APPEAR AS AN EXACT MIXED SECOND DIFFERENCE.**

And, more narrowly:

> **IN THIS STEP-2 SPECIMEN, THE RECTANGLE RESIDUAL IS THE DECLARED LIE-BRACKET COEFFICIENT.**

This is not a claim that every Dogram rectangle interaction is a Lie bracket.

## 6. Why no new operator is earned

The mathematics is new to the research frontier, but the required Dogram calculation already exists:

```text
matrix algebra / BCH derivation   -> research provenance
central-coordinate four-cell cut  -> rectangle@1
order comparison                  -> existing delta/trace vocabulary
```

Therefore the runtime verdict is:

```text
NO NEW PUBLIC OPERATOR.
```

Explicitly held:

```text
lie_bracket@1
bch@1
heisenberg@1
commutator_flow@1
mixed_curvature@1
```

## 7. Pressure boundaries

Documented math:

```text
[X,Y]=E13
exp(sX)exp(tY)-exp(tY)exp(sX)=stE13
step-2 BCH truncation
group commutator = I+stE13
```

Dogram inference:

```text
an exact order-sensitive algebraic residue may be receipted by an existing mixed-difference operator when a scalar projection is explicitly declared
```

Speculation / HOLD:

```text
rectangle residual ~= curvature
commutator residue ~= causal interaction
central coordinate ~= hidden state / home / semantic center
```

Those identifications are not established here.

## 8. Executable witness

Frozen fixture:

```text
tests/fixtures/heisenberg_bilinear_order_residue_001.json
```

Focused test:

```text
tests/test_heisenberg_bilinear_order_residue.py
```

The test independently reconstructs the rational matrices, checks `[X,Y]=E13`, checks the exact order delta and group commutator, and then feeds the declared central-coordinate four-cell surfaces into the existing `dogram.rectangle.evaluate_rectangle` implementation.

Fresh focused verification performed against the same rational formulas:

```text
3 logical groups passed
```

A WolframAlpha explicit-matrix query was attempted but returned no result; therefore no Wolfram verification claim is made. Wolfram's BCH documentation independently confirms that the second-order BCH term is one-half the commutator and that higher terms vanish when the relevant nested commutators vanish.

## 9. Strongest next frontier

The new frontier is not a larger Heisenberg example. It is the precise boundary between:

```text
mixed finite difference
Lie bracket
curvature / holonomy
```

A particularly strong next specimen would ask whether a small closed four-step transport loop has a receiptable residue that agrees with a curvature commutator in an exactly declared discrete connection, while preserving:

```text
LOOP RESIDUE != PHYSICAL CURVATURE
HOLONOMY != OCCURRENCE
STRUCTURE != EVIDENCE
```

That has not been promoted here.

## Seal

> **THE CROSS TERM IS NOT NOISE WHEN THE ALGEBRA EARNS IT.**

> **MIXED DELTA CAN RECEIPT ORDER WITHOUT DECIDING WHAT THE ORDER MEANS.**
