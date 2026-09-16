# LINEAGE-WEAVE-001 — Typed Composition Without Relation Erasure

**Date:** 2026-09-16  
**Status:** EXACT TYPED-DERIVATION SPECIMEN · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **A DESCENDANT MAY INHERIT THROUGH DIFFERENT LAWFUL EDGE KINDS WITHOUT ERASING WHICH KIND EACH EDGE WAS.**

## Question

`LINEAGE-SPINE-001` preserved bounded one-parent descent.

`LINEAGE-BRAID-001` preserved bounded multi-parent convergence while keeping the child small.

The next pressure is composition across those two grammars:

> Can a braid result become a later parent beside a spine result without pretending that both links are the same kind of relation?

The frozen specimen is:

```text
5 -> 100 --\
            +--> 109 --\
3 ->   9 --/            \
                         +--> 145
4 ->  36 ---------------/
```

The answer tested here is a thin typed layer above the existing verifiers.

## Exact mathematics

The same square/triangular order comparison from `TRIANGULATOR-001` gives:

```text
Delta(n) = T(n^2) - T(n)^2 = T(n-1)^2.
```

At `n=5`:

```text
325 - 225 = 100.
```

At `n=3`:

```text
45 - 36 = 9.
```

Those two spine descendants converge under the already frozen braid merge:

```text
9 + 100 = 109.
```

Independently, at `n=4`:

```text
T(16) - T(4)^2 = 136 - 100 = 36.
```

The typed weave then uses the deliberately boring merge:

```text
109 + 36 = 145.
```

`145` has no semantic privilege here. It is only an exact inspectable output.

## Why a typed layer

A content address tells us which stored object is named. It does not tell us which grammar makes the reference lawful.

A spine head is verified by `verify_lineage(...)`.

A braid head is verified by `verify_braid(...)`.

If a braid head were silently reintroduced as a spine root, the numerical carrier could survive while the relation that produced it disappeared from the receipt.

Working law:

```text
HEAD ADDRESS != RELATION TYPE
```

`LINEAGE-WEAVE-001` therefore stores `kind` beside every parent head.

## Typed parent descriptor

Each parent descriptor has exactly:

```text
kind
head_digest
carrier
root_set_digest
```

Supported kinds are frozen to:

```text
spine
braid
```

Typed identity is:

```text
(kind, head_digest)
```

and the parent set is canonically ordered by that pair.

The order is a serialization rule only. It does not imply time, causal precedence, importance, or authority.

## Verifier dispatch

For a `spine` parent:

1. find the declared head in the spine ledger;
2. run `verify_lineage(...)`;
3. inspect the verified head carrier and root;
4. normalize that root into the weave root-set grammar;
5. compare the resulting carrier/root-set claim with the typed descriptor.

For a `braid` parent:

1. find the declared head in the braid ledger;
2. run `verify_braid(...)`;
3. inspect the verified braid carrier;
4. recover the roots represented by the braid's verified parent set;
5. normalize those roots into the weave root-set grammar;
6. compare the resulting carrier/root-set claim with the typed descriptor.

The weave does not replace either verifier. It delegates to them.

Working law:

```text
VERIFIER DISPATCH != ONTOLOGY
```

## Kind contradiction versus missing witness

The verifier preserves the old `complete / incomplete / invalid` split.

If a parent is declared `spine`, its head is absent from the spine ledger, and the same digest is present as a braid capsule, that is positive contradictory material:

```text
invalid / parent_kind_mismatch
```

The mirror case is treated the same way.

If the declared head is absent from both typed ledgers, the verifier returns `incomplete` rather than inventing a contradiction from absence.

So:

```text
MISSING TYPED WITNESS != PROVEN TYPE ERROR
PRESENT OPPOSITE-TYPE WITNESS = DECLARED TYPE CONTRADICTION
```

## Root identity normalization

The existing braid layer and the new weave layer serialize root sets differently.

The weave therefore does not compare their raw root-set digest bytes as though equal schemas implied equal identity.

Instead it recovers the underlying root digests from the verified parent, then creates a weave-normalized root-set object.

Working law:

```text
ROOT IDENTITY != ROOT-SET SERIALIZATION FORMAT
```

That boundary let the existing `LINEAGE-BRAID-001` contract remain frozen.

## Fixed-shape weave child

Every weave child contains exactly:

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
carrier_origin = typed_parent_set_merge
```

It does not embed parent capsules, parent histories, spine ledgers, braid ledgers, or recursive ancestry.

The relation plurality remains externally addressable.

## Root union

After every typed parent verifies, the weave verifier re-derives the roots actually represented by those parents.

Those roots are normalized, deduplicated, sorted, and compared with the stored weave root-set object.

This prevents a self-consistent re-hash from silently changing the declared origin set.

```text
PARENT KIND != ROOT IDENTITY
MULTIPLE EDGE KINDS != MULTIPLE ROOTS
```

## Three-state verification

### `complete`

All weave objects are present, correctly addressed, exact-shape, and internally consistent; every parent verifies under its declared kind; merge arithmetic and root union recompute exactly.

Frozen result:

```text
status = complete
carrier = 145
parent_kinds = [braid, spine]
```

### `incomplete`

Witness material needed to reconstruct the declared composition is absent.

Examples:

```text
missing weave head
missing parent set
missing root set
missing merge receipt
missing spine parent witness
missing braid parent witness
```

### `invalid`

Present material contradicts the declared composition.

Examples:

```text
content digest mismatch
shape pollution
wrong parent kind
invalid underlying spine/braid
parent carrier mismatch
parent root-set mismatch
wrong merge inputs/output
wrong root union
non-integer carrier disguised through Python equality
```

## Hostile control: kind substitution

Take the valid braid parent and rewrite only:

```text
kind = braid
```

as:

```text
kind = spine
```

Then correctly re-hash the parent set, merge receipt, and child.

All content addresses can be self-consistent, but the referenced head is actually present in the braid ledger rather than the spine ledger.

The verifier rejects the result as:

```text
invalid / parent_kind_mismatch
```

Therefore:

```text
HASH CONSISTENCY != RELATION-TYPE VALIDITY
```

## Hostile control: arithmetic re-hash

A correctly re-hashed false merge:

```text
109 + 36 = 146
```

is rejected because the verifier recomputes the declared sum.

```text
HASH CONSISTENCY != GRAMMAR VALIDITY
CONTENT ADDRESS != ARITHMETIC PROOF
```

## Hostile control: recursive ancestry smuggling

A valid weave child can be modified to contain an extra nested `ancestry` field and then assigned a new correct content digest.

The verifier rejects it through exact capsule-shape enforcement:

```text
invalid / capsule_shape_mismatch
```

Boundedness is verified law, not constructor etiquette.

## Hostile control: root-union substitution

A wrong but internally well-formed root-set object can be stored, addressed, and referenced by a correctly re-hashed child.

The verifier re-derives roots from the already verified typed parents and rejects the altered union:

```text
invalid / root_union_mismatch
```

## Hostile control: Python boolean/integer alias

The hostile pass found a language-level edge case not in the original design.

In Python:

```python
True == 1
False == 0
```

and `bool` is a subclass of `int`.

That meant a re-hashed capsule with:

```text
carrier = True
```

could initially compare equal to the legitimate integer carrier `1`.

Likewise:

```text
[True, False] == [1, 0]
```

allowed boolean merge inputs to impersonate integer merge inputs under plain equality.

The verifier now checks non-boolean integer type before numeric equality and rejects both attacks.

Working law:

```text
NUMERIC EQUALITY != TYPE IDENTITY
BOOLEAN NUMERIC EQUALITY != INTEGER CARRIER IDENTITY
```

This is a useful implementation-level instance of the broader grammar rule: the value surface alone does not preserve the kind of thing being carried.

## Frozen fixture

`tests/fixtures/lineage_weave_001.json` freezes:

- the canonical digest of the complete spine ledger;
- the canonical digest of the complete braid ledger;
- the canonical digest of the complete weave ledger;
- braid parent-set, merge, and head digests;
- weave parent-set, root-set, merge, and head digests;
- the final verification result.

The three full-ledger digests lock their complete serialized contents without duplicating the entire graph literal into the fixture.

Frozen weave head:

```text
01ec1ddfa06c9c2fdc65d60fe7d2e0490ad9efb54c4ea5fb588ab25a052d32d2
```

## Relation to the candidate Grammar of Creation

The executable grammar now distinguishes at least three moves:

```text
CARRIER --crossing--> DELTA --continuation--> CARRIER

PARENT A --\
           --merge--> CARRIER
PARENT B --/

TYPED PARENT A --\
                  --typed merge--> CARRIER
TYPED PARENT B --/
```

The strongest new result is not a metaphysical conclusion. It is narrower:

> Composition can preserve not only where a parent came from, but the lawful grammar under which that parental relation is verified.

That supports the candidate seal:

> **COMPOSITION MUST PRESERVE THE GRAMMAR OF THE CROSSING, NOT JUST THE RESULT.**

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

## Executable boundary

`dogram/lineage_weave.py` provides a private research layer for:

- weave-normalized root sets;
- typed parent descriptors;
- canonical typed parent sets;
- sum-only local merge receipts;
- fixed-shape weave capsules;
- a content-addressed weave ledger;
- typed verification dispatch over existing spine and braid verifiers.

It does not change Dogram's public four-operator floor.

## Strongest next frontier

Do not add arbitrary kinds merely because the current two-kind specimen works.

The next real pressure is recursion of the type system itself:

> Can a verified weave head later become a parent without hard-coding `weave` into another increasingly large dispatcher?

That is the point where a **bounded verifier registry or algebra of relation kinds** may become justified.

Until then:

> **THE ADDRESS TELLS YOU WHERE. THE TYPE TELLS YOU HOW TO READ THE LINK.**

> **COMPOSITION MUST PRESERVE THE GRAMMAR OF THE CROSSING, NOT JUST THE RESULT.**
