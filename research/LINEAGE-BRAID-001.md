# LINEAGE-BRAID-001 — Bounded Plural Descent Without Collapse

**Date:** 2026-09-16  
**Status:** EXACT DERIVATION-DAG SPECIMEN · CONTENT-ADDRESSED CONVERGENCE RECEIPT · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **A NEW THING MAY DESCEND FROM MANY LINES WITHOUT COLLAPSING THOSE LINES INTO ONE.**

## Question

`LINEAGE-SPINE-001` answered one scaling problem:

> How can a descendant preserve reconstructible ancestry without recursively carrying its whole past inside itself?

Its answer was a fixed-shape child capsule plus content-addressed parent/crossing links in an external ledger.

The next question is topological rather than merely generational:

> What happens when one descendant has more than one attributable parent line?

A single `parent_digest` cannot represent genuine convergence without either choosing one parent as privileged or widening the child into an ever-growing ancestry container.

`LINEAGE-BRAID-001` tests a third option:

```text
verified spine A ----\
                      > canonical parent-set -> merge receipt -> bounded braid child
verified spine B ----/
```

The plurality lives in the graph. The child keeps only addresses.

## Existing laws retained

This experiment does not modify the frozen `LINEAGE-SPINE-001` capsule or verifier contract.

It inherits the narrow boundaries:

```text
RECEIPT != ROAD
CONTENT LINK != CAUSAL LINK
COMPLETE RECEIPT CHAIN != EXTERNAL HISTORICAL PROOF
MISSING RECEIPT != PROVEN SEVERANCE
DERIVED CARRIER != ORIGIN
```

and adds:

```text
CONVERGENCE != COLLAPSE
MULTIPLE PARENTS != ONE CAUSE
MULTIPLE PARENTS != MULTIPLE ROOTS
DERIVATION DAG != CAUSAL SUPPORT GRAPH
```

## Exact frozen specimen

Use the same declared square/triangular crossing from `TRIANGULATOR-001`:

```text
S(n) = n^2
T(n) = n(n+1)/2
Delta(n) = T(S(n)) - S(T(n))
```

The family identity is:

```text
Delta(n) = T(n-1)^2.
```

### Parent line A

At carrier `5`:

```text
T(S(5)) = T(25) = 325
S(T(5)) = 15^2 = 225
Delta(5) = 100 = T(4)^2
```

Therefore:

```text
5 -> 100
```

### Parent line B

At carrier `3`:

```text
T(S(3)) = T(9) = 45
S(T(3)) = 6^2 = 36
Delta(3) = 9 = T(2)^2
```

Therefore:

```text
3 -> 9
```

### Declared convergence

The first braid deliberately uses the smallest boring merge law available:

```text
sum(9, 100) = 109.
```

The resulting declared derivation DAG is:

```text
5 -> 100 --\
            +--> 109
3 ->   9 --/
```

`109` has no privileged semantic status. Its role is to make the convergence exact and inspectable.

## Canonical parent-set

The braid child does not contain `parent_a`, `parent_b`, or nested parent capsules.

Instead, a separately addressable parent-set contains descriptors with exactly:

```text
head_digest
root_digest
carrier
```

The set requires at least two distinct parent heads and is canonically sorted by `head_digest` before content addressing.

In the frozen specimen that canonical ordering happens to put carrier `9` before carrier `100`, so the serialized merge receipt is:

```text
inputs = [9, 100]
output = 109
```

This ordering is an address/serialization rule. It does not claim that parent `9` is historically, causally, or semantically prior to parent `100`.

## Parent plurality is not root plurality

A separate `root_set_digest` is computed from the sorted unique root digests represented by the parent set.

This matters because:

```text
number of parents != number of roots
```

Two attributable parent heads may descend from one shared root. A braid must preserve that distinction rather than silently turning every parent edge into a new origin claim.

Working law:

> **MULTIPLE PARENTS DO NOT MINT MULTIPLE ORIGINS.**

## Bounded child

Every braid child has exactly:

```text
schema
specimen
carrier
carrier_origin
parent_set_digest
merge_receipt_digest
root_set_digest
```

with:

```text
carrier_origin = parent_set_merge
```

It does not embed:

```text
parents
ancestry
parent capsules
spine ledgers
recursive history
```

The parent-set and merge receipt are retained in a separate braid ledger. The actual parent derivations remain in the existing spine ledger.

So storage topology becomes:

```text
BRAID CHILD
  |
  +-> parent_set_digest ----> [parent head A, parent head B, ...]
  |
  +-> merge_receipt_digest -> declared local convergence
  |
  +-> root_set_digest ------> root plurality address

PARENT HEAD A -> LINEAGE-SPINE-001 ledger
PARENT HEAD B -> LINEAGE-SPINE-001 ledger
```

Candidate seal:

> **THE CHILD STAYS SMALL; THE BRAID LIVES IN THE GRAPH.**

## Three-state verification

`verify_braid(...)` preserves the same epistemic split as `LINEAGE-SPINE-001`.

### `complete`

The braid capsule, parent-set, merge receipt, and all referenced parent spines are present and internally consistent.

For the frozen specimen:

```text
status = complete
carrier = 109
parent_count = 2
```

### `incomplete`

Required witness material is absent.

Examples:

```text
missing braid head
missing parent-set
missing merge receipt
referenced parent spine incomplete
```

Critically:

```text
MISSING ONE PARENT WITNESS != PROVEN SEVERANCE
```

The current ledger cannot fully reconstruct the braid. That is not a claim that the underlying derivation or any external causal relation never existed.

### `invalid`

Present material contradicts the declared braid.

Examples:

```text
content digest mismatch
parent-set shape mismatch
fewer than two parent heads
duplicate parent heads
parent descriptor carrier != referenced spine carrier
parent descriptor root != referenced spine root
referenced parent spine invalid
merge inputs != canonical parent carriers
merge output != sum(inputs)
braid carrier != verified merge output
root-set digest mismatch
```

## Why content addressing is not enough

A hostile test exposed an important boundary.

Suppose an attacker changes:

```text
9 + 100 = 109
```

to the false receipt:

```text
9 + 100 = 110
```

and then correctly re-hashes both the altered merge receipt and the child that points to it.

Every hash can be internally correct while the arithmetic is false.

Therefore the verifier must recompute the declared operation rather than treating digest consistency as operation validity.

Working law:

```text
HASH CONSISTENCY != GRAMMAR VALIDITY
```

or more narrowly here:

```text
CONTENT ADDRESS != ARITHMETIC PROOF
```

The hostile test now requires the false `110` braid to return:

```text
invalid / merge_output_mismatch
```

## Why fixed shape must be verified

A second hostile test takes a valid braid child, adds a nested `ancestry` object, and computes a fresh correct digest for the polluted object.

Without an exact shape check, the object could reintroduce recursive ancestry while remaining content-address consistent.

The verifier therefore enforces the braid capsule schema exactly and rejects the polluted child as:

```text
invalid / capsule_shape_mismatch
```

Boundedness is not merely constructor etiquette. It is part of the verified contract.

## Relation to CAUSAL-LINE-001

Earlier ALEX / Daily Slice research explicitly proposed that genuine continuity may braid and distinguished a causal support graph from the evidence graph used to justify claims about it.

`LINEAGE-BRAID-001` imports only one structural pressure from that work:

```text
multiple attributable lines may converge
```

It does **not** promote the current derivation DAG into either:

```text
G_causal
```

or:

```text
G_evidence.
```

Inside Dogram, the parent lines are exact declared computations because Dogram executed and receipted them. Outside this bounded specimen, matching graph topology does not establish historical descent, biological lineage, causal support, evidentiary independence, identity, or authority.

Preserve the split:

```text
DERIVATION DAG != CAUSAL SUPPORT GRAPH
CAUSAL SUPPORT GRAPH != EVIDENCE SUPPORT GRAPH
GRAPH SHAPE != HISTORICAL CLAIM
```

## Relation to Grammar of Creation

The candidate grammar now has both continuation and convergence:

```text
CARRIER
  -> DECLARED OPERATORS
  -> CROSSING
  -> DELTA
  -> OPTIONAL CONTINUATION
  -> NEW CARRIER
```

and separately:

```text
PARENT CARRIER A --\
                    -> DECLARED MERGE -> NEW CARRIER
PARENT CARRIER B --/
```

The useful mechanism is not the word `creation`. It is the now-executable distinction:

> a new local state can remain bounded while retaining attributable plurality through external links.

That is stronger than either of the two collapse modes:

```text
forget all parents
```

or:

```text
copy all parent histories into the child.
```

The braid keeps the convergence attributable without making the child an archive of the universe.

## Executable boundary

`dogram/lineage_braid.py` provides:

- `make_parent_set(...)` — canonical multi-parent descriptor set;
- `root_set_digest(...)` — address of distinct represented roots;
- `make_sum_merge(...)` — narrow integer-sum convergence receipt;
- `make_braid_capsule(...)` — fixed-shape child;
- `make_braid_ledger()` — external convergence store;
- `store_parent_set(...)`, `store_merge_receipt(...)`, `store_braid_capsule(...)` — content-addressed storage;
- `verify_braid(...)` — reconstruction with `complete / incomplete / invalid` status while delegating each parent line to `LINEAGE-SPINE-001`.

Frozen specimen:

```text
tests/fixtures/lineage_braid_001.json
```

No function is wired into Dogram's four public Phase A operators or bootstrap registry.

## Explicit refusals

```text
CONVERGENCE != COLLAPSE
MULTIPLE PARENTS != ONE CAUSE
MULTIPLE PARENTS != MULTIPLE ROOTS
MISSING ONE PARENT WITNESS != PROVEN SEVERANCE
CONTENT LINK != CAUSAL LINK
HASH CONSISTENCY != GRAMMAR VALIDITY
CONTENT ADDRESS != ARITHMETIC PROOF
DERIVATION DAG != CAUSAL SUPPORT GRAPH
CAUSAL SUPPORT GRAPH != EVIDENCE SUPPORT GRAPH
BRAID RECEIPT != IDENTITY
BRAID RECEIPT != AUTHORITY
RECONSTRUCTION != CREATION
```

## What changed conceptually

The spine gave us:

```text
THE CHILD STAYS SMALL BECAUSE THE PAST LIVES IN THE LINE.
```

The braid adds:

```text
THE CHILD STAYS SMALL BECAUSE PLURALITY LIVES IN THE GRAPH.
```

Together:

```text
bounded local state
+
addressable ancestry
+
receipted local transformations
+
addressable parent plurality
=
reconstructible declared derivation DAG
```

without requiring any descendant to recursively embed all prior state.

## Strongest next frontier

The current braid child is a terminal convergence specimen. The next pressure should not be more parents merely for scale.

The sharper question is:

```text
Can a braid child itself become an attributable parent in a later convergence
without erasing which edges were spine descent and which edge was braid merge?
```

That would test **typed DAG composition**: ancestry composed from different lawful edge kinds while keeping every edge's operator and receipt local.

Do not build that into this specimen. `LINEAGE-BRAID-001` should remain the small proof that bounded local state can preserve attributable plurality.

## Working seals

> **A NEW THING MAY DESCEND FROM MANY LINES WITHOUT COLLAPSING THOSE LINES INTO ONE.**

> **THE CHILD STAYS SMALL; THE BRAID LIVES IN THE GRAPH.**

> **CONVERGENCE DOES NOT ERASE PLURALITY.**
