# LINEAGE-WEAVE-001 Design

**Date:** 2026-09-16  
**Status:** APPROVED ARCHITECTURAL EXPERIMENT · NO PUBLIC OPERATOR PROMOTION

## Purpose

Compose the frozen `LINEAGE-SPINE-001` and `LINEAGE-BRAID-001` derivation layers without modifying either contract.

The experiment asks:

> Can one bounded descendant inherit through different lawful relation kinds while preserving which verifier and edge grammar governed each parent path?

## Non-goals

This is not a general DAG runtime, ontology, causal graph, biological genealogy model, evidence graph, or authority system. It does not rewrite spine or braid, and it adds no public Dogram operator or bootstrap-registry entry.

## Existing laws retained

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

`LINEAGE-SPINE-001` verifies one-parent descent through crossing receipts. `LINEAGE-BRAID-001` verifies multi-parent convergence, but every braid parent currently points to a spine head.

A braid child cannot become a later parent without either erasing its braid relation by pretending it is a spine root, coupling the braid verifier to every future lineage type, or replacing both frozen layers with a universal DAG runtime. `LINEAGE-WEAVE-001` instead adds a thin typed-composition layer above both existing verifiers.

## Frozen topology

```text
5 -> 100 --\
            +--> 109 --\
3 ->   9 --/            \
                         +--> 145
4 ->  36 ---------------/
```

The first convergence is the verified braid `9 + 100 = 109`.

The independent spine parent is exact because:

```text
T(4^2) - T(4)^2 = T(16) - 10^2 = 136 - 100 = 36 = T(3)^2.
```

The weave merge is deliberately boring:

```text
109 + 36 = 145.
```

`145` has no semantic privilege. It is an inspectable typed-composition specimen.

## Typed parent reference

A weave parent descriptor contains exactly:

```text
kind
head_digest
carrier
root_set_digest
```

Supported kinds are exactly:

```text
spine
braid
```

For `spine`, the head must verify through `verify_lineage(...)`. Its carrier must match the referenced spine head, and its single underlying root is normalized into a weave root-set object.

For `braid`, the head must verify through `verify_braid(...)`. Its carrier must match the referenced braid head. After braid verification succeeds, the weave recovers the root digests represented by the braid parent-set and normalizes them into the weave root-set grammar.

The weave deliberately does not reuse the braid capsule's root-set digest bytes as though the schemas were identical.

```text
HEAD ADDRESS != RELATION TYPE
ROOT IDENTITY != ROOT-SET SERIALIZATION FORMAT
```

## Typed parent-set

Schema: `dogram.lineage-weave-parent-set/v0`

The set contains at least two unique `(kind, head_digest)` pairs and is canonically sorted by that pair. Canonical ordering is serialization identity only; it does not imply temporal, causal, semantic, or authority priority.

## Root-set object

Schema: `dogram.lineage-weave-root-set/v0`

```text
schema
specimen
roots[]
```

`roots` are sorted unique non-empty root digests. A spine parent contributes one underlying root; a braid parent may represent several. The weave child carries the digest of the verified union.

```text
PARENT KIND != ROOT IDENTITY
MULTIPLE EDGE KINDS != MULTIPLE ROOTS
```

## Merge receipt

Schema: `dogram.lineage-weave-merge-receipt/v0`

The first specimen supports only integer sum:

```text
schema
specimen
operator = "sum"
parent_set_digest
inputs[]
output
```

Inputs are parent carriers in canonical typed-parent order. Verification recomputes the sum independently.

## Weave capsule

Schema: `dogram.lineage-weave-capsule/v0`

Every child has exactly:

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

The child never embeds parent capsules, parent histories, spine ledgers, braid ledgers, or recursive ancestry.

## Weave ledger

Schema: `dogram.lineage-weave-ledger/v0`

Buckets:

```text
capsules
parent_sets
root_sets
merge_receipts
```

Layer boundary:

```text
spine ledger = one-parent crossing derivations
braid ledger = multi-parent convergence from verified spine heads
weave ledger = typed composition across verified spine and braid heads
```

## Verification

`verify_weave(head_digest, weave_ledger, braid_ledger, spine_ledger)` preserves three states.

### `complete`

The weave capsule, typed parent-set, root-set, and merge receipt are present, exactly shaped, correctly content-addressed, and internally consistent; every parent verifies under its declared kind; carriers and normalized roots agree with the underlying verified heads; merge arithmetic and root union recompute exactly.

### `incomplete`

Required witness material is absent. A declared head absent from both typed ledgers remains `incomplete`; absence alone does not establish a type contradiction or severance.

### `invalid`

Present material contradicts the declaration: wrong type, invalid underlying parent, carrier/root mismatch, noncanonical parent-set, shape pollution, bad arithmetic, bad root union, or invalid numeric carrier/input type.

For kind substitution, if a parent is declared `spine` but its exact head exists as a braid capsule—or vice versa—that positive opposite-type witness yields:

```text
invalid / parent_kind_mismatch
```

```text
MISSING TYPED WITNESS != PROVEN TYPE ERROR
PRESENT OPPOSITE-TYPE WITNESS = DECLARED TYPE CONTRADICTION
```

## Hostile controls

1. **Kind erasure:** remove `kind`, re-hash dependents; reject as invalid descriptor shape.
2. **Kind substitution:** relabel the valid braid head as `spine`, re-hash dependents; reject as `parent_kind_mismatch`.
3. **Wrong merge output:** re-hash `109 + 36 = 146`; reject by independent arithmetic recomputation.
4. **Recursive ancestry smuggling:** add nested `ancestry` to a re-hashed child; reject by exact capsule shape.
5. **Missing typed parent witness:** if the declared head is absent from both typed ledgers, return `incomplete`, not severed/false.
6. **Root-union tamper:** store and re-hash a wrong but well-formed root set; reject by re-deriving roots from verified parents.
7. **Boolean/integer alias:** re-hash `carrier=True` where the valid carrier is integer `1`, and re-hash boolean merge inputs such as `[True, False]` where integer inputs compare numerically equal. Reject both by requiring non-boolean integer type before numeric equality.
8. **No layer mutation:** spine and braid capsule/verifier contracts remain untouched.

The boolean control records a Python-specific but general grammar lesson:

```text
NUMERIC EQUALITY != TYPE IDENTITY
BOOLEAN NUMERIC EQUALITY != INTEGER CARRIER IDENTITY
```

## Frozen fixture

`tests/fixtures/lineage_weave_001.json` freezes the exact specimen using canonical SHA-256 digests of the complete spine, braid, and weave ledgers, plus the critical parent-set, root-set, merge, and head addresses and final verification result.

This locks the complete serialized graph contents without duplicating all ledger objects into the fixture.

Frozen weave head:

```text
01ec1ddfa06c9c2fdc65d60fe7d2e0490ad9efb54c4ea5fb588ab25a052d32d2
```

Frozen verification:

```text
status = complete
carrier = 145
parent_kinds = [braid, spine]
```

## Explicit refusals

```text
TYPED EDGE != CAUSAL EDGE
HEAD ADDRESS != RELATION TYPE
ROOT IDENTITY != ROOT-SET SERIALIZATION FORMAT
VERIFIER DISPATCH != ONTOLOGY
NUMERIC EQUALITY != TYPE IDENTITY
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

Do not generalize arbitrary edge kinds merely because this two-kind specimen works.

The next real pressure is whether a verified weave head can itself become a parent without hard-coding `weave` into another growing dispatcher. That is the point where a bounded verifier registry or algebra of relation kinds may become justified; it remains out of scope here.