# CROSSED-MODULE-FACE-LIFT-001

**Date:** 2026-09-03  
**Status:** RESEARCH LEDGER · EXACT FINITE GROUP ARITHMETIC · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0 — Why this seam survived

The current Dogram frontier has ordinary group-valued edge/loop holonomy and a tetrahedral Bianchi receipt under review. The advertised next question was whether a genuinely two-dimensional algebraic carrier can preserve a distinction that ordinary group-valued face-boundary bookkeeping forgets.

A finite crossed module gives the smallest exact specimen.

## 1 — Documented mathematics

A crossed module consists of groups `H`, `G`, a boundary homomorphism

```text
∂ : H -> G
```

and a `G`-action on `H` satisfying equivariance and the Peiffer identity. Strict 2-groups are equivalently described by crossed modules.

In discrete higher lattice gauge models, ordinary group data live on links while crossed-module / higher labels live on plaquettes. Fake-flatness relates the boundary of the higher label to the ordinary group-valued boundary holonomy of the plaquette.

References:

- A. Bochniak, L. Hadasz, B. Ruba, **Dynamical generalization of Yetter's model based on a crossed module of discrete groups**, *Journal of High Energy Physics* (2021), arXiv:2010.00888. Finite crossed modules are used with link and plaquette degrees of freedom.
- R. Zucchini, **Wilson Surfaces for Surface Knots: A Field Theoretic Route to Higher Knots**, *Fortschritte der Physik* 67 (2019), DOI `10.1002/prop.201910026`. Strict higher gauge transport is expressed through crossed modules; closed surface holonomy lands in the kernel of the target/boundary map.
- J. H. C. Whitehead, **Combinatorial homotopy. II**, *Bulletin of the American Mathematical Society* 55 (1949), classical crossed-module foundation.

## 2 — Frozen finite crossed module

Work additively with cyclic groups

```text
H = Z/4Z
G = Z/2Z
```

with trivial `G`-action on `H` and boundary

```text
∂(h) = h mod 2.
```

Because both groups are abelian and the action is trivial, the Peiffer identities hold. The boundary is surjective but not injective:

```text
ker ∂ = {0, 2}.
```

Freeze one face whose ordinary boundary holonomy in `G` is identity `0`.

The valid higher face lifts are exactly the fiber

```text
∂^-1(0) = {0, 2}.
```

Both produce the same ordinary boundary image:

```text
∂(0) = 0
∂(2) = 0
```

but their higher-label delta is

```text
2 - 0 = 2 mod 4,
```

which is the nontrivial element of `ker ∂`.

Therefore:

```text
SAME ORDINARY FACE-BOUNDARY HOLONOMY
!=
SAME HIGHER FACE LIFT
```

and more precisely:

```text
THE BOUNDARY MAP CAN FORGET A KERNEL RESIDUE.
```

## 3 — Injective hostile control

Hold the same additive/trivial-action grammar but use

```text
H = Z/2Z
G = Z/2Z
∂ = identity.
```

Now

```text
ker ∂ = {0}
∂^-1(0) = {0}.
```

The same ordinary boundary value has only one higher lift. This isolates the lost distinction to noninjectivity of the declared boundary map rather than to the presence of a face label by itself.

## 4 — Dogram inference

The useful computational law is narrower than higher gauge theory:

> **A LOWER-DIMENSIONAL RECEIPT NEED NOT DETERMINE ITS HIGHER-DIMENSIONAL LIFT.**

The exact obstruction/freedom is the fiber of the declared boundary map. When two lifts share one boundary image, their difference lies in `ker ∂` in this cyclic additive specimen.

Candidate seals:

```text
SAME BOUNDARY != SAME LIFT.
THE MAP CAN CLOSE WHILE THE FIBER STILL HAS ROOM.
KEEP THE KERNEL RESIDUE; DO NOT INVENT ITS MEANING.
```

## 5 — Contract pressure / refusals

```text
HIGHER FACE LIFT != HISTORICAL OCCURRENCE
KERNEL ELEMENT != HIDDEN CAUSE
2-HOLONOMY != PHYSICAL FIELD
SAME BOUNDARY IMAGE != SEMANTIC EQUIVALENCE
DISTINCT LIFTS != DISTINCT REAL-WORLD EVENTS
CROSSED-MODULE COHERENCE != TRUTH
```

The ordinary `G` boundary is a projection under a declared mathematical decoder. It is not evidence that a source actually carries an `H`-valued layer.

## 6 — Executable research kernel

`dogram/crossed_module_face_lift.py` is deliberately restricted to cyclic groups with trivial action. It:

- validates that `h -> k*h mod |G|` is well-defined on the declared cyclic `H`;
- enumerates the exact kernel of `∂`;
- enumerates the complete lift fiber of one declared boundary value;
- receipts all boundary images and nonzero pairwise lift deltas;
- compares a noninjective specimen with an injective control.

It does not implement arbitrary crossed modules, nontrivial actions, 2-group composition, gauge transformations, 2-holonomy on general cell complexes, or fake-curvature dynamics.

No `crossed_module@1`, `face_lift@1`, `2holonomy@1`, `higher_gauge@1`, or `kernel_residue@1` is promoted.

## 7 — Verification

TDD RED was observed on the first PR head: repository CI failed specifically with

```text
ModuleNotFoundError: No module named 'dogram.crossed_module_face_lift'
```

After the minimal kernel was added, the full Dogram CI passed unit tests, compile, constitutional-floor, and scope-scan steps.

Frozen fixture:

```text
tests/fixtures/crossed_module_face_lift_001.json
```

Focused test:

```text
tests/test_crossed_module_face_lift.py
```

## 8 — Strongest live frontier

The next legitimate step is **composition of multiple higher face lifts**, not a larger cyclic group. The bounded question is whether two cellulations or two ordered 2-dimensional compositions can have the same ordinary boundary data while differing by an attributable higher coherence residue.

That points toward interchange laws, Peiffer commutators, crossed squares / 2-crossed modules, or explicit 2-group pasting — but none is promoted here.

## Seal

> **THE BOUNDARY CAN AGREE WHILE THE LIFT STILL DIFFERS. RECEIPT THE FIBER BEFORE YOU DECIDE THE STORY.**
