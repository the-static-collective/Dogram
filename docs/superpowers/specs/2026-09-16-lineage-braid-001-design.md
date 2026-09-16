# LINEAGE-BRAID-001 Design

**Date:** 2026-09-16
**Status:** APPROVED ARCHITECTURAL EXPERIMENT · NO PUBLIC OPERATOR PROMOTION

## Purpose

Extend `LINEAGE-SPINE-001` from one attributable parent line to multiple attributable parent lines without widening the frozen spine capsule contract and without recursively embedding parent histories in the descendant.

The experiment asks:

> Can bounded local state preserve attributable plurality?

## Non-goals

This experiment does not model historical causality, biological parenthood, personal identity, evidentiary support, authorship authority, or metaphysical creation. It does not merge causal topology with evidentiary topology. It does not add a public Dogram operator or bootstrap-registry entry.

## Existing law retained

`LINEAGE-SPINE-001` remains unchanged. Each parent is first a valid spine head in a shared content-addressed spine ledger. The braid layer references those heads; it does not copy their ancestry.

The existing boundaries remain:

```text
RECEIPT != ROAD
CONTENT LINK != CAUSAL LINK
COMPLETE RECEIPT CHAIN != EXTERNAL HISTORICAL PROOF
MISSING RECEIPT != PROVEN SEVERANCE
```

## Topology

A braid descendant is not given `parent_a` and `parent_b` fields. That would hard-code arity into the local capsule. Instead it carries one digest of a separately stored parent-set object.

```text
lineage A head ----\
                    > parent-set -> merge receipt -> braid child
lineage B head ----/
```

The parent-set may contain two or more distinct parent heads. Its members are canonically sorted by head digest so parent enumeration order does not create accidental identity.

## Parent-set object

Schema: `dogram.lineage-parent-set/v0`

```text
schema
specimen
parents[]
```

Each parent descriptor contains exactly:

```text
head_digest
root_digest
carrier
```

Requirements:

- at least two parents;
- unique `head_digest` values;
- integer carriers;
- non-empty head/root digests;
- canonical sort by `head_digest`;
- exact descriptor shape.

The parent-set is content-addressed with the existing deterministic `canonical_digest(...)` function from `lineage_spine.py`.

## Merge receipt

Schema: `dogram.lineage-merge-receipt/v0`

The first hostile specimen uses one deliberately boring merge operation: integer addition.

```text
schema
specimen
operator = "sum"
parent_set_digest
inputs[]
output
```

`inputs` are the parent carriers in the parent-set's canonical order. `output = sum(inputs)`.

The narrow operator is intentional. The experiment is about attributable convergence, not about inventing a general merge algebra.

## Braid capsule

Schema: `dogram.lineage-braid-capsule/v0`

Every braid child has the same local field shape:

```text
schema
specimen
carrier
carrier_origin
parent_set_digest
merge_receipt_digest
root_set_digest
```

where:

```text
carrier_origin = "parent_set_merge"
```

`root_set_digest` is the digest of the canonically sorted unique root digests represented by the parent set. Multiple parents may share one root; parent plurality must not be silently rewritten as root plurality.

The child never embeds:

- parent capsules;
- parent-set members;
- recursive ancestry;
- full spine ledgers.

## Braid ledger

Schema: `dogram.lineage-braid-ledger/v0`

The braid ledger stores three content-addressed buckets:

```text
capsules
parent_sets
merge_receipts
```

The parent lineages themselves remain in the shared `LINEAGE-SPINE-001` ledger. This preserves the layer boundary:

```text
spine ledger = declared parent derivations
braid ledger = declared convergence
```

## Verification

`verify_braid(head_digest, braid_ledger, spine_ledger)` returns one of:

### `complete`

The braid capsule, parent set, merge receipt, and every referenced parent spine are present and internally consistent.

### `incomplete`

Required witness material is absent. Examples:

- missing braid head capsule;
- missing parent-set object;
- missing merge receipt;
- a referenced parent spine is `incomplete`.

`incomplete` must never be silently promoted to `severed`, `false`, or `invalid`.

### `invalid`

Present material contradicts the declared braid. Examples:

- content digest mismatch;
- capsule or parent-set shape mismatch;
- fewer than two parents;
- duplicate parent heads;
- parent carrier/root descriptor disagrees with the referenced spine head;
- a referenced parent spine is `invalid`;
- merge inputs/output disagree with the parent set;
- braid carrier differs from merge output;
- root-set digest mismatch.

## Frozen hostile specimen

Build two independent one-step spine lines under the same square/triangular crossing law.

Line A:

```text
C_A0 = 5
Delta_A0 = T(5^2) - T(5)^2 = 325 - 225 = 100
C_A1 = 100
```

Line B:

```text
C_B0 = 3
Delta_B0 = T(3^2) - T(3)^2 = 45 - 36 = 9
C_B1 = 9
```

The parent set contains the two heads `100` and `9`.

Declared merge:

```text
100 + 9 = 109
```

Frozen braid child:

```text
C_braid = 109
```

The number `109` has no special semantic status. It exists only to provide an exact, inspectable convergence specimen.

## Hostile controls

1. **Enumeration invariance:** parent input order must canonicalize to the same parent-set digest.
2. **Missing parent witness:** deleting one referenced parent spine receipt/capsule must yield `incomplete`, not `invalid` or `severed`.
3. **Descriptor contradiction:** changing a parent's declared carrier while keeping its head digest must yield `invalid`.
4. **Recursive ancestry smuggling:** a re-hashed braid capsule with extra ancestry fields must yield `invalid` via exact capsule-shape enforcement.
5. **Single-parent collapse:** a parent-set with fewer than two heads must be rejected.
6. **Merge tamper:** a re-hashed merge receipt with an incorrect output must yield `invalid`.

## Relation to earlier braid research

The older `CAUSAL-LINE-001` work proposed braided continuity and explicitly separated causal topology from evidence topology. `LINEAGE-BRAID-001` adopts only the structural pressure: multiple attributable lines may converge. It does not claim its derivation DAG is a causal support graph, and it does not implement an evidence support graph.

## Working laws

```text
CONVERGENCE != COLLAPSE
MULTIPLE PARENTS != ONE CAUSE
MULTIPLE PARENTS != MULTIPLE ROOTS
MISSING ONE PARENT WITNESS != PROVEN SEVERANCE
THE CHILD STAYS SMALL; THE BRAID LIVES IN THE GRAPH
```

Candidate seal:

> **A NEW THING MAY DESCEND FROM MANY LINES WITHOUT COLLAPSING THOSE LINES INTO ONE.**
