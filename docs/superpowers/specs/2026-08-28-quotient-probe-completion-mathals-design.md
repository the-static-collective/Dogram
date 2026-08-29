# Quotient / Probe / Completion Mathals Design

**Date:** 2026-08-28  
**Status:** RESEARCH DESIGN — deterministic calculations only; no semantic or authority promotion

## 1. Cold center

Recent FAR-SIDE, BINOCULAR, Projection Break, GlyphTrace, openness, and decoder-space work converges on one mathematical pressure:

> **A compression is lawful only relative to the distinctions and future consequences it promises to preserve.**

Let `W` be a set of detailed worlds, `O` an observation map, and `T` a declared family of target probes/questions.

Define target-relative equivalence:

```math
x ~_T y
iff
forall p in T,
O(P_p(x)) = O(P_p(y))
```

A single discriminating probe is enough to break that equivalence for the declared family:

```math
exists p in T:
O(P_p(x)) != O(P_p(y))
=>
x not~_T y
```

This does **not** mean `x` and `y` are globally different in every useful sense. It means the proposed quotient is too coarse for `T`.

The subscript is load-bearing.

```text
same for rendering
!=
same for replay
!=
same for archaeology
!=
same for future reachability
!=
same for evidence
```

## 2. Dogram ownership

Dogram should calculate finite differences, reachability changes, ablations, fibers, and probe-response partitions without deciding what those differences mean.

ALEX owns predeclaration pressure, post-hoc discriminator refusal, evidence/support boundaries, and authority non-expansion.

3rdi owns observer-local projection and formation candidates.

The owning world defines the target/probe family whose consequences matter.

Do **not** add generic operators such as `equivalent@1`, `simple@1`, or `bisimilar@1` from this design. Lower the first specimens into existing finite operators (`delta`, `reach`, `ablate`, `rectangle`) plus explicit fixture bookkeeping.

## 3. `FAR-SIDE-QUOTIENT-001`

### Question

Can one candidate compression lawfully collapse source states for one declared target family while remaining explicitly unlawful for another?

### Fixture

Detailed states:

```text
A1 A2 B1 B2
```

Candidate simplifier:

```text
q(A1) = q(A2) = A
q(B1) = q(B2) = B
```

Declare target families before scoring:

```text
T_render = final carrier rendering
T_replay = formation replay
T_future = reachability after intervention I
```

Expected lawful shape may be:

```text
A1 ~T_render A2      PASS
A1 ~T_replay A2      FAIL
A1 ~T_future A2      FAIL
```

Correct conclusion:

```text
compression lawful for T_render
compression unlawful for T_replay/T_future
```

Incorrect conclusions:

```text
A1 = A2 globally
compression is globally correct
compression is globally wrong
```

### Required receipt fields (fixture-local, not universal schema)

```text
compression_ref
source_partition
declared_survival_targets
preserved_distinctions
intentionally_discarded_distinctions
hostile_probes
known_failure_domain
regeneration_receipt
```

### Hostile sibling

Collapse `A1` and `A2` merely because a distinguishing field was forgotten.

Expected: the first declared probe that depends on that field breaks the quotient. Smaller output alone earns nothing.

## 4. Useful compression as basis selection

Two compressions may regenerate the same required material yet differ sharply in how cleanly they expose meaningful perturbations.

A useful basis should make declared changes local:

```text
meaningful perturbation
  -> few independent deltas
  -> low unintended blast radius
```

### `COMPRESSION-BASIS-001`

Give two equally regenerative compressions `C1`, `C2` of one fixture. Hold out three independent perturbations.

For each representation measure:

```text
number of coordinates changed
number of unrelated outputs changed
reachability spillover
required reconstruction preserved?
```

Do not prefer by byte length or elegance.

Candidate score:

```math
locality(C,p) = intended_delta / (intended_delta + unintended_delta)
```

The exact scalar is optional; the specimen may preserve the vector instead of collapsing to one score.

Goal: distinguish **short compression** from **experimentally useful compression**.

## 5. Residue as quotient counterexample

A residual is not automatically failed simplification.

It may witness a live distinction the current quotient erased:

```text
RESIDUE
  ↓
find smallest probe that separates collapsed states
  ↓
refine partition
  ↓
rerun compression
```

So BINOCULAR `RESIDUAL` may be interpreted, at the calculator layer, as a candidate refinement signal rather than noise to discard.

Dogram should only report the difference/probe relationship. It does not declare that the residual is explanatory or evidentiary.

## 6. `COMPLETION-MOVE-001`

### Question

Does adding one identical node produce materially different topology depending on **how relation is opened to receive it**?

Freeze graph `G` with edge `a--b` and new node `X`.

Construct:

```text
A: X isolated

B: a--b   a--X
   (leaf attachment)

C: a--X--b
   (peel existing edge; insert X)
```

Node-count delta is identical in all three worlds.

Calculate only:

- `delta` over edge set / incidence;
- `reach` changes;
- `ablate(X)` recovery behavior;
- ordinary graph invariants already available to the fixture environment.

Expected: same inventory change can yield materially different reachability and formation topology.

Candidate compression:

> **Completion may be an incidence move rather than an inventory move.**

This is the boring deterministic control for `OPEN BERTH`, 13th Cup, and symbolic “missing one” hypotheses. No symbolic significance is input to the test.

## 7. `BOUNDARY-SUFFICIENCY-001`

### Question

When may an internal motif be compressed to a carrier without erasing information required by declared downstream questions?

Take graph motif `G_int` with three internal nodes and an external interface `B`.

Construct compressed carrier `C` with:

- pointer/reference to formation/internal receipt;
- declared exact-query family `T_exact`;
- declared refused-query family `T_detail`.

Require:

```text
for q in T_exact:
answer(C,q) = answer(G_int,q)

for q in T_detail:
C must explicitly refuse or defer to interior receipt
```

Hostile sibling: fake carrier `C_bad` omits one relation necessary for one query in `T_exact`.

Expected: `C_bad` fails sufficiency even if its visible summary looks similar.

This gives SMASH a non-metaphorical candidate stopping rule:

> **Compress when the boundary becomes sufficient for the declared downstream task.**

Not all future questions. The declared task family.

## 8. Decoder lesion / excitation pair — HOLD after the core three

Two complementary calculations are worth preserving but should remain second-wave until quotient/probe semantics are stable.

### Lesion

```text
remove decoder coordinate d_i
-> record which predeclared invariants disappear
```

### Excitation

```text
apply probe u_i
-> record which previously collapsed worlds become distinguishable
```

Together they estimate dependency/support structure:

```text
remove capacity -> survival signature
add excitation   -> response signature
```

This is not a claim that “meaning lives” in one module. It is an attributable sensitivity map for declared invariants.

## 9. Information fiber

For any projection/compression `q`, define the fiber of output `c`:

```math
Fiber_q(c) = {x in W | q(x)=c}
```

A large fiber is not automatically bad. It is dangerous only if the declared target family still distinguishes members of the fiber.

This is the bridge to GlyphTrace:

```text
many lawful formation histories
  ↓ same final carrier
one visible glyph
```

The inverse problem is not necessarily to recover one historical formation. It may be to characterize which properties are invariant across the entire compatible fiber.

## 10. Probe-response partition refinement

Given hypothesis family:

```text
H = {H1, H2, ... Hn}
```

and candidate probes `u1...uk`, each probe induces a partition by observed response:

```math
Pi_u(H) = partition of H by O(P_u(H_i))
```

A discriminating probe refines the current partition.

A useful experiment-design calculation can therefore ask:

```text
which lawful u maximally refines the surviving partition?
```

Dogram may calculate candidate partition sizes/information gain if inputs are already explicit. It must not choose what experiment is ethically, historically, or operationally authorized.

## 11. Promotion gates

This design earns no new universal mathal operator.

Promotion pressure:

1. `FAR-SIDE-QUOTIENT-001` must show target-relative lawful/unlawful collapses on a bounded fixture.
2. `COMPLETION-MOVE-001` must produce distinct topology under identical node-count increment.
3. `BOUNDARY-SUFFICIENCY-001` must distinguish a sufficient carrier from a fake ring/boundary.
4. At least one foreign-domain specimen should reproduce the calculations without importing Dogram semantics as authority.

## Seal

> **A DISTINCTION MAY BE THROWN AWAY ONLY AFTER WE DECLARE THE QUESTIONS FOR WHICH IT NO LONGER MAKES A DIFFERENCE.**

> **THE SIMPLE THING IS USEFUL WHEN IT MAKES THE COMPLEXITY COME BACK IN THE RIGHT COORDINATE SYSTEM.**
