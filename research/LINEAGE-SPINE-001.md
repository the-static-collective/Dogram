# LINEAGE-SPINE-001 — Bounded Local Ancestry, Reconstructible Global Line

**Date:** 2026-09-16  
**Status:** EXACT DERIVATION-LINE SPECIMEN · CONTENT-ADDRESSED RECEIPT LEDGER · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **CONTINUITY NEEDS A LINE; THE CHILD ONLY NEEDS THE LINK.**

## Question

`TRIANGULATOR-001` established an order-sensitive crossing with a structured delta. `DELTA-AS-CARRIER-001` then asked whether that delta could become a new carrier without erasing the crossing that produced it.

That immediately exposed the scaling problem:

```text
C0 -> Delta0 -> C1 -> Delta1 -> C2 -> ...
```

If every child recursively embeds its entire ancestry, each descendant drags a growing copy of the past. If the child keeps only its current value, ancestry disappears and the derived carrier can impersonate an origin.

The bounded question is:

> How can local receipts remain fixed-shape while the complete derivation line remains reconstructible?

## Answer tested here

Split **local lineage address** from **cumulative lineage storage**.

Each capsule carries only:

```text
schema
specimen
generation
carrier
carrier_origin
root_digest
parent_digest
crossing_digest
```

Generation 1 and generation 2 therefore have the same key shape. No child contains a nested `ancestry` tree.

The cumulative ledger separately stores:

```text
capsule_digest -> capsule
crossing_digest -> crossing receipt
```

A verifier reconstructs the declared derivation line by following `parent_digest` and checking the locally referenced crossing at each step.

Candidate seal:

> **KEEP THE PAST ADDRESSABLE, NOT RECURSIVELY EMBEDDED.**

## Frozen descent

Start with the existing `TRIANGULATOR-001` carrier:

```text
C0 = 5
```

For

```text
S(n) = n^2
T(n) = n(n+1)/2
```

we already have

```text
T(S(5)) = 325
S(T(5)) = 225
Delta0 = 100 = T(4)^2
```

so

```text
C1 = Delta0 = 100.
```

Run the same declared crossing at the new carrier:

```text
T(S(100)) = T(10000) = 50,005,000
S(T(100)) = 5050^2 = 25,502,500
Delta1 = 24,502,500.
```

The exact family identity still holds:

```text
Delta1 = T(99)^2 = 4950^2 = 24,502,500.
```

Therefore the frozen multi-generation line is

```text
C0 = 5
  -> Delta0 = 100
  -> C1 = 100
  -> Delta1 = 24,502,500
  -> C2 = 24,502,500
```

The point is not that the numbers are semantically privileged. The point is that generation 2 can still be traced to generation 0 without generation 2 embedding generations 0 and 1 as nested payloads.

## Content addressing

`canonical_digest(value)` serializes JSON-compatible data deterministically and computes a SHA-256 digest.

The digest is used as an address for:

- each lineage capsule;
- each crossing receipt;
- each parent link.

The digest has a deliberately narrow role:

```text
DIGEST = CONTENT ADDRESS / LOCAL INTEGRITY WITNESS
```

not:

```text
DIGEST = TRUTH
DIGEST = CAUSALITY
DIGEST = IDENTITY
DIGEST = AUTHORITY
```

Changing the content changes the address. That makes silent mutation detectable inside the declared calculation ledger. It does not prove that an external historical or physical event occurred.

## Why the ledger is the important move

The previous `DELTA-AS-CARRIER-001` child snapshots its immediate parent's full crossing ancestry. That is useful for one generation but does not scale if repeated recursively.

`LINEAGE-SPINE-001` changes the storage topology:

```text
recursive embedding

C2 {
  parent: C1 {
    parent: C0 {...}
  }
}
```

becomes

```text
bounded capsules

C2 -> digest(C1)
C1 -> digest(C0)
C0 -> null

plus separately addressable crossing receipts.
```

Each child is locally bounded. The shared ledger grows linearly with actual retained history.

This is not deletion of ancestry. It is **normalization of ancestry into links**.

Candidate seal:

> **A DESCENDANT NEEDS AN ATTRIBUTABLE PARENT LINK, NOT A PRIVATE COPY OF ALL ANCESTORS.**

## Three-state verification

A binary `valid / invalid` result is too crude for the causal-line boundary.

The verifier therefore distinguishes:

### `complete`

Every declared capsule and crossing receipt needed to reach the root is present and internally consistent.

### `incomplete`

Required witness material is absent, for example:

```text
missing parent capsule
missing crossing receipt
missing head capsule
```

This intentionally does **not** mean `severed`.

> **MISSING RECEIPT != PROVEN SEVERANCE.**

A missing witness prevents complete reconstruction from the current ledger. It does not establish that the underlying derivation, causal process, or historical continuity failed to exist.

### `invalid`

Available material contradicts the declared lineage structure, for example:

```text
content digest mismatch
generation gap
root mismatch
carrier != local crossing delta
crossing parent carrier != linked parent carrier
cycle
```

This is a claim only about the declared receipt structure.

## Relation to CAUSAL-LINE-001

The August continuity work proposed:

> continuity is an unsevered attributable causal line through the relation being claimed.

It also preserved the stronger boundary:

> a receipt may witness a causal line; it is not the line itself.

`LINEAGE-SPINE-001` is a computational descendant of that distinction, but it does not promote itself into a general causal ontology.

Inside this exact Dogram specimen, we know the derivation steps because the code performs them. The content-addressed ledger receipts those steps. For external history, biology, identity, testimony, or causal inference, a matching hash-chain shape does not establish causal descent.

```text
DERIVATION LINE != HISTORICAL LINE
CONTENT LINK != CAUSAL LINK
RECONSTRUCTIBLE RECEIPTS != PROOF OF EXTERNAL CONTINUITY
```

## Relation to Grammar of Creation

The candidate grammar can now be written more sharply:

```text
CARRIER
  -> DECLARED OPERATORS
  -> CROSSING
  -> DELTA
  -> OPTIONAL CONTINUATION
  -> NEW CARRIER
  -> PARENT LINK + CROSSING LINK
```

and iterated:

```text
C0 --crossing0--> Delta0 -> C1
C1 --crossing1--> Delta1 -> C2
...
```

The grammar no longer needs to choose between:

```text
forget the past
```

and

```text
copy the entire past into every new thing.
```

It can instead preserve **addressable descent**.

That is a materially stronger mechanism, while the phrase `grammar of creation` remains interpretive research language rather than an executable conclusion.

## Executable boundary

`dogram/lineage_spine.py` provides:

- `canonical_digest(...)` — deterministic JSON content address;
- `make_root(...)` — generation-0 bounded capsule;
- `append_from_crossing(...)` — derive one child capsule from a parent capsule and a crossing receipt;
- `make_ledger()` — separate capsule/receipt store;
- `store_capsule(...)` and `store_receipt(...)` — content-addressed storage;
- `verify_lineage(...)` — backward reconstruction with `complete / incomplete / invalid` status.

It is stdlib-only and is not wired into Dogram's public operator floor or bootstrap registry.

Frozen specimen:

```text
tests/fixtures/lineage_spine_001.json
```

## Explicit refusals

```text
HASH LINK != CAUSAL LINK
DIGEST MATCH != TRUTH
COMPLETE RECEIPT CHAIN != EXTERNAL HISTORICAL PROOF
MISSING RECEIPT != SEVERANCE
INCOMPLETE != INVALID
LINEAGE != IDENTITY
DESCENT != AUTHORITY
DERIVED CARRIER != ORIGIN
RECONSTRUCTION != CREATION
```

## What changed conceptually

The original question was:

> How do we preserve the whole line without carrying an infinitely growing past inside each descendant?

The executable answer is:

```text
BOUND LOCAL STATE
+
CONTENT-ADDRESSED PARENT LINK
+
CONTENT-ADDRESSED LOCAL CROSSING RECEIPT
+
SHARED LEDGER
=
RECONSTRUCTIBLE DECLARED DERIVATION LINE
```

The child stays small because the past lives in the line, not inside the child.

## Strongest next frontier

The current specimen is a line. The older causal-line research explicitly warned that real continuity may braid.

The next difficult question is therefore not simply generation 3.

It is:

```text
What happens when one descendant has two attributable parent lines?
```

A useful next specimen would test a bounded merge / braid capsule with two parent digests while refusing to collapse:

```text
multiple parents -> one identity
multiple witnesses -> one cause
convergence -> authority
```

That would pressure whether the grammar naturally generalizes from a **lineage spine** to an attributable **lineage DAG** without losing the local boundedness law.

## Working seals

> **CONTINUITY NEEDS A LINE; THE CHILD ONLY NEEDS THE LINK.**

> **KEEP THE PAST ADDRESSABLE, NOT RECURSIVELY EMBEDDED.**

> **MISSING RECEIPT != PROVEN SEVERANCE.**

> **THE CHILD STAYS SMALL BECAUSE THE PAST LIVES IN THE LINE.**
