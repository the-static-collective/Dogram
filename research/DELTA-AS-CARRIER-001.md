# DELTA-AS-CARRIER-001 — Continuation Without Ancestry Erasure

**Date:** 2026-09-16  
**Status:** EXACT CONTINUATION SPECIMEN · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **IF THE DELTA BECOMES A NEW CARRIER, RECEIPT THE CROSSING.**

## Question

`TRIANGULATOR-001` showed that two explicitly ordered operator paths can produce a nonzero delta with declared mathematical structure.

The next bounded question is narrower:

> If that delta is explicitly reused as a new carrier, what minimum ancestry must survive so the continuation cannot masquerade as an origin?

This specimen answers only that provenance question.

## Parent specimen

The frozen parent is `TRIANGULATOR-001` at carrier `5`:

```text
square -> triangular: 325
triangular -> square: 225
Delta = 100
classification = nonzero_structured
```

The parent receipt already preserves the operator order and path outputs.

## Continuation

The continuation explicitly chooses the parent delta as the next carrier:

```text
parent Delta = 100
new carrier = 100
operator = triangular
projection = T(100) = 5050
```

The child receipt does not merely say `came from TRIANGULATOR-001`. It snapshots:

```text
parent specimen
parent carrier
parent operator order
parent path outputs
parent delta
parent classification
```

Therefore the child state `5050` remains attributable to the crossing that produced its carrier.

## Ancestry rule

Candidate seal:

> **A DERIVED CARRIER MUST NOT IMPERSONATE AN ORIGIN.**

Operationally:

```text
parent paths
    -> parent Delta
    -> explicit continuation
    -> child carrier
    -> child projection
```

The ancestry snapshot is a value copy, not an alias to the mutable parent receipt. Mutating the caller's parent object after continuation does not rewrite the child's recorded ancestry.

## Explicit refusals

```text
DELTA != CREATION
CONTINUATION != NECESSITY
ANCESTRY != AUTHORITY
ANCESTRY != CAUSAL PROOF OUTSIDE THE DECLARED CALCULATION
STRUCTURED PARENT != MEANINGFUL CHILD
CHILD PROJECTION != NEW ORIGIN
```

Nothing in this specimen decides whether a delta ought to be continued. The caller makes that choice explicitly.

## Executable boundary

`dogram.triangulator.continue_from_delta(parent_receipt, operator)`:

- requires an integer `delta` and the ancestry fields needed to identify its declared parent calculation;
- uses that delta as the child carrier;
- applies one explicitly named `Operator`;
- returns a child receipt with a frozen ancestry snapshot;
- does not mutate the parent receipt;
- adds no public Dogram operator or registry entry.

Frozen receipt:

```text
tests/fixtures/delta_as_carrier_001.json
```

## Relation to the Grammar of Creation thread

This is a pressure test of one candidate grammatical move:

```text
DELTA -> NEW CARRIER
```

but only under the stronger typed form:

```text
DELTA(parent paths, order, operators)
    -> explicit continuation
    -> CARRIER(child)
```

The candidate grammar therefore becomes:

```text
CARRIER
  -> OPERATOR PATHS
  -> DELTA
  -> [optional explicit continuation]
  -> NEW CARRIER WITH ANCESTRY
```

The phrase `grammar of creation` remains interpretive research language. The executable claim is only provenance-preserving continuation.

## Strongest next frontier

Now that one generation can retain ancestry, the next meaningful hostile test is **multi-generation descent**:

```text
C0 -> Delta0 -> C1 -> Delta1 -> C2
```

Ask whether ancestry can remain bounded and reconstructible without copying an indefinitely growing receipt tree.

That would pressure the distinction:

> **CONTINUITY NEEDS A LINE; IT DOES NOT NECESSARILY NEED AN INFINITE COPY OF THE PAST.**
