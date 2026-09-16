# LINEAGE-WEAVE-001 Design

**Date:** 2026-09-16  
**Status:** APPROVED ARCHITECTURAL EXPERIMENT · NO PUBLIC OPERATOR PROMOTION

## Purpose

Compose the existing `LINEAGE-SPINE-001` and `LINEAGE-BRAID-001` derivation layers without modifying either frozen contract.

The experiment asks:

> Can one bounded descendant inherit through different lawful relation kinds while preserving which verifier and edge grammar governed each parent path?

## Non-goals

This is not a general DAG runtime, ontology, causal graph, biological genealogy model, evidence graph, or authority system. It does not rewrite `LINEAGE-SPINE-001` or `LINEAGE-BRAID-001`. It does not add a public Dogram operator or bootstrap-registry entry.

## Existing law retained

```text
RECEIPT != ROAD
CONTENT LINK != CAUSAL LINK
COMPLETE RECEIPT CHAIN != EXTERNAL HISTORICAL PROOF
MISSING RECEIPT != PROVEN SEVERANCE
DERIVED CARRIER != ORIGIN
CONVERGENCE != COLLAPSE
DERIVATION DAG != CAUSAL SUPPORT GRAPH
HASH CONSISTENCY != GRAMMAR VALIDITY
```

## Why a new layer

`LINEAGE-SPINE-001` verifies one-parent descent through crossing receipts.

`LINEAGE-BRAID-001` verifies multi-parent convergence, but every parent descriptor currently points to a spine head and delegates to `verify_lineage(...)`.

A braid child cannot therefore become a later braid parent without either:

1. pretending the braid is a spine root, which erases relation kind;
2. teaching the braid verifier to recursively know every future lineage type, which couples frozen layers;
3. replacing both layers with a universal DAG runtime, which is too broad for the current evidence.

`LINEAGE-WEAVE-001` chooses a thin typed-composition layer above both existing verifiers.

## Topology

Frozen specimen:

```text
5 -> 100 --\
            +--> 109 --\
3 ->   9 --/            \
                         +--> 145
4 ->  36 ---------------/
```

The first convergence (`100 + 9 = 109`) is a verified `LINEAGE-BRAID-001` head.

The second parent (`4 -> 36`) is a verified `LINEAGE-SPINE-001` head because:

```text
T(4^2) - T(4)^2 = T(16) - 10^2 = 136 - 100 = 36 = T(3)^2.
```

The weave merge is deliberately boring:

```text
109 + 36 = 145.
```

The experiment is about relation-type preservation, not the arithmetic interest of `145`.

## Typed parent reference

A weave parent descriptor contains exactly:

```text
kind
head_digest
carrier
root_set_digest
```

where `kind` is one of:

```text
spine
braid
```

### `spine` parent

- `head_digest` points into the existing spine ledger;
- verification delegates to `verify_lineage(...)`;
- `carrier` must match the referenced spine head;
- `root_set_digest` is normalized from that spine head's single `root_digest` as a one-element root set.

### `braid` parent

- `head_digest` points into the existing braid ledger;
- verification delegates to `verify_braid(...)`;
- `carrier` must match the referenced braid head;
- `root_set_digest` must equal the braid capsule's existing `root_set_digest`.

The relation kind is part of the content-addressed parent descriptor. A head digest is not allowed to float free of its verifier type.

Working law:

```text
HEAD ADDRESS != RELATION TYPE
```

## Typed parent-set

Schema: `dogram.lineage-weave-parent-set/v0`

The parent-set contains at least two unique `(kind, head_digest)` pairs and is canonically sorted by `(kind, head_digest)`.

Canonical ordering is serialization identity only. It does not imply causal, historical, semantic, or temporal priority.

## Merge receipt

Schema: `dogram.lineage-weave-merge-receipt/v0`

The first specimen uses only integer `sum`:

```text
schema
specimen
operator = "sum"
parent_set_digest
inputs[]
output
```

`inputs` are parent carriers in canonical typed-parent order. The verifier recomputes `sum(inputs)` independently.

## Weave capsule

Schema: `dogram.lineage-weave-capsule/v0`

Fixed local shape:

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
carrier_origin = "typed_parent_set_merge"
```

The child does not embed parent capsules, parent histories, braid ledgers, spine ledgers, or recursive ancestry.

## Root-set preservation

The weave child computes a root-set digest from the union of root identities represented by all parents.

A spine parent contributes one root. A braid parent may already represent several roots. The weave layer unions those roots without flattening parent relation type.

Therefore:

```text
PARENT KIND != ROOT IDENTITY
MULTIPLE EDGE KINDS != MULTIPLE ROOTS
```

To make this verifiable, the weave ledger stores a content-addressed root-set object rather than only an opaque recomputed digest.

Root-set schema: `dogram.lineage-weave-root-set/v0`

```text
schema
specimen
roots[]
```

with sorted unique root digests.

## Weave ledger

Schema: `dogram.lineage-weave-ledger/v0`

Buckets:

```text
capsules
parent_sets
merge_receipts
root_sets
```

The actual lineage and braid histories remain in their existing ledgers.

```text
spine ledger = one-parent crossing derivations
braid ledger = homogeneous multi-parent convergence from spine heads
weave ledger = typed composition across spine and braid heads
```

## Verification

`verify_weave(head_digest, weave_ledger, braid_ledger, spine_ledger)` returns:

### `complete`

- weave capsule present and correctly addressed;
- exact weave capsule shape;
- parent-set, merge receipt, and root-set present and correctly addressed;
- all typed parents verify under the verifier declared by `kind`;
- parent carrier and root-set claims match referenced heads;
- merge inputs/output recompute correctly;
- child carrier equals verified merge output;
- child root-set digest equals the verified union root-set digest.

### `incomplete`

Required witness material is absent, including a referenced typed parent whose underlying verifier returns `incomplete`.

### `invalid`

Present material contradicts the declared weave, including wrong type, invalid underlying parent, carrier mismatch, root-set mismatch, merge arithmetic mismatch, noncanonical parent-set, or shape pollution.

## Hostile controls

1. **Kind erasure:** removing `kind` from a typed parent descriptor must be invalid.
2. **Kind substitution:** relabeling a valid braid head as `spine` and re-hashing every dependent object must still be invalid because verification dispatches to the wrong lawful verifier.
3. **Wrong merge output:** re-hashed `109 + 36 = 146` must be invalid via independent arithmetic recomputation.
4. **Recursive ancestry smuggling:** re-hashed child with an `ancestry` field must be invalid via exact shape enforcement.
5. **Missing typed parent witness:** must return `incomplete`, not severed/false.
6. **Root-union tamper:** a self-consistent but incorrect root-set object must be invalid because roots are re-derived from the verified parent heads.
7. **No layer mutation:** tests must demonstrate no change to spine or braid capsule schemas.

## Frozen exact specimen

First braid:

```text
5 -> 100
3 -> 9
9 + 100 = 109
```

Independent spine:

```text
4 -> 36
```

Typed weave parents:

```text
(kind=braid, carrier=109)
(kind=spine, carrier=36)
```

Declared weave:

```text
109 + 36 = 145
```

## Explicit refusals

```text
TYPED EDGE != CAUSAL EDGE
HEAD ADDRESS != RELATION TYPE
VERIFIER DISPATCH != ONTOLOGY
WEAVE RECEIPT != IDENTITY
WEAVE RECEIPT != AUTHORITY
WEAVE RECEIPT != HISTORICAL PROOF
MULTIPLE EDGE KINDS != MULTIPLE ROOTS
MISSING TYPED PARENT WITNESS != PROVEN SEVERANCE
HASH CONSISTENCY != GRAMMAR VALIDITY
RECONSTRUCTION != CREATION
```

## Candidate laws

> **A DESCENDANT MAY INHERIT THROUGH DIFFERENT LAWFUL EDGE KINDS WITHOUT ERASING WHICH KIND EACH EDGE WAS.**

> **THE ADDRESS TELLS YOU WHERE. THE TYPE TELLS YOU HOW TO READ THE LINK.**

> **COMPOSITION MUST PRESERVE THE GRAMMAR OF THE CROSSING, NOT JUST THE RESULT.**

## Strongest next frontier

Do not generalize this specimen into arbitrary edge kinds yet.

If `LINEAGE-WEAVE-001` survives hostile testing, the next pressure is whether a typed weave child can itself participate in later typed composition without hard-coding an ever-growing dispatch table. That would motivate a verifier registry or algebra of relation kinds. It is explicitly out of scope here.