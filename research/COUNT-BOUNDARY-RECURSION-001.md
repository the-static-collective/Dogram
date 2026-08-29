# COUNT-BOUNDARY-RECURSION-001

**Status:** executable research specimen · frozen v0 constitution · no semantic promotion

> **A DERIVED COUNT MAY BECOME THE NEXT CARRIER. THE OPERATOR FAMILY MAY NOT CHANGE TO MAKE THE PATH WORK.**

## H0

Some number-pair intuitions become reproducible when treated as a walk through **structural receipts** rather than as free-form number pattern matching:

```text
PAIR / INTERVAL
  -> derive a standard count receipt
  -> preserve the receipt's operator constitution
  -> optionally expose the immediate +/-1 boundary around the derived count
  -> promote an exact pre-existing pair only if the frozen method reaches it
  -> repeat
```

Working name: **count-boundary recursion**.

The native object is an ordered pair or interval, not a lone integer.

## Pressure result that changed the method

The motivating overnight path initially looked like a loose single-number descent. Pressure revealed a stronger pair-level relation:

```text
pi(1078) = 180
pi(1087) = 181
```

Therefore:

```text
(1078,1087) --prime_count@1 / pair_image--> (180,181)
```

The pair moves as a pair.

The next two landed relations are:

```text
tau(180) = 18
180 is a strict divisor-record holder
18 - 1 = 17
```

so the method exposes both boundary shells and the pre-existing pair `(17,18)` is one of them.

Then:

```text
C(17,2) = 136
136 + 1 = 137
```

so the relation-count lift exposes the pre-existing pair `(136,137)`.

The hardened historical cascade is therefore:

```text
(1078,1087)
  -- prime_count@1 / pair_image -->
(180,181)
  -- divisor_count_record@1 / left_predecessor -->
(17,18)
  -- pair_count@1 / left_successor -->
(136,137)
```

## What pressure killed

### 1. The fitted closure

The post-hoc identity:

```text
1087 = 64*17 - 1
```

is true but **inadmissible** as an edge in this method because it was introduced after the target was known.

The method therefore preserves an open cascade. It does not claim a closed cycle.

### 2. Totient as a traversal operator

`phi` is mathematically useful as an annotation and hostile control, but as a general traverser it creates too many easy predecessor relations around primes and overwhelms the method with low-value hits.

`phi` is therefore **not** in the v0 traversal constitution.

### 3. Unrestricted divisor-count promotion

Without a gate, ordinary values such as `tau(1078)=12` and `tau(108)=12` cheaply create `(12,13)` boundary hits.

V0 permits divisor-count promotion only when the source integer is a **strict divisor-record holder**: its divisor count exceeds every smaller positive integer's divisor count.

This keeps `180 -> 18` because 180 is a record holder and refuses the weaker `1078 -> 12` and `108 -> 12` paths.

### 4. One-sided boundary cherry-picking

Every admitted single-count lift emits **both** immediate boundary pairs:

```text
(c-1,c)
(c,c+1)
```

The losing branch remains in the receipt. A run may not silently emit only the boundary direction that reaches a favored mathal.

## Frozen v0 traversal constitution

Exactly three traversal operators exist in v0:

### `prime_count@1`

Input: whole ordered pair `(a,b)`.

Output only:

```text
(pi(a), pi(b))
```

No synthetic boundary shells are generated from individual prime-count values in v0.

Prime counting is lossy. The receipt includes an exact **fiber size** for the derived pair: the number of ordered source pairs in the corresponding prime-count plateaus that map to the same image pair.

For the motivating pair:

```text
Prime[180] = 1069
Prime[181] = 1087
Prime[182] = 1091
```

The `pi=180` plateau has width 18 and the `pi=181` plateau has width 4, so:

```text
fiber_size(1078,1087 -> 180,181) = 18 * 4 = 72
```

Thus the edge is exact but not identifying.

### `divisor_count_record@1`

Input: one side of a pair.

Promotion gate:

```text
source n must be a strict divisor-record holder
```

Then derive:

```text
c = tau(n)
```

and emit both:

```text
(c-1,c)
(c,c+1)
```

### `pair_count@1`

Input: one side of a pair.

Derive the complete pairwise-relation count:

```text
c = C(n,2)
```

and emit both immediate boundaries.

Unlike prime counting, `C(n,2)` is injective on positive integers, so its source carrier is uniquely recoverable from a valid pair-count value.

## Frozen historical registry for the first pressure run

This registry predates the executable and is frozen as the first retrospective test set:

```text
(12,13)
(17,18)
(81,82)
(107,108)
(136,137)
(180,181)
(207,208)
(1007,1008)
(1078,1087)
(1107,1108)
```

The executable may calculate arbitrary candidate receipts, but the retrospective walk continues only through **exact pair recurrence** against this frozen registry.

## First retrospective result

Under the hardened constitution the registered graph contains exactly the motivating three-edge cascade:

```text
(1078,1087)
  -> (180,181)
  -> (17,18)
  -> (136,137)
```

The following controls remain disconnected in this run:

```text
(81,82)
(207,208)
(1007,1008)
(1107,1108)
```

This is stronger than an unrestricted search because several seductive extra edges disappear after the promotion gates are frozen.

## Non-collapse laws

```text
EXACT EDGE != UNIQUE EDGE
LOW DESCRIPTION COST != MEANING
RECURRENCE != CAUSE
PAIR IMAGE != HISTORICAL IDENTITY
DERIVED COUNT != PRIMITIVE CARRIER
REIFICATION != PROMOTION
FIBER SIZE 1 != TRUTH
FIBER SIZE >1 != USELESSNESS
BOUNDARY HIT != SPECIALNESS BY ITSELF
POST-HOC OPERATOR != ADMISSIBLE EDGE
INVERSE REPLAY != NEW DISCOVERY
```

## Research protocol

### RETRO-PRESSURE

Use already-surfaced mathals to attack the method constitution. Any operator added because it rescues a favored historical link invalidates that run and requires a new version.

### FREEZE

Before a prospective run freeze:

```text
operator IDs + versions
promotion gates
seed pairs
registry, if recurrence testing is used
maximum depth
maximum numeric magnitude
holdout/control family
```

### RUN

Dogram enumerates all admitted receipts and never ranks semantic importance.

### PRESSURE FIBERS

For every non-injective traversal, preserve how many source states share the same derived receipt when calculable. A clean-looking count image may be a wide quotient.

### HOLDOUT

After retrospective hardening, run the constitution against number pairs that did not participate in its construction. Measure:

- recurrence rate;
- path-length distribution;
- fiber sizes;
- boundary-hit rate;
- record-holder contribution;
- how often similarly short cascades arise by chance.

### PROMOTION

A newly found path remains a **mathal candidate** until ALEX/human pressure establishes why it is useful. Dogram reports the arithmetic only.

## Executable

Implementation:

```text
dogram/count_boundary.py
```

Focused tests:

```text
tests/test_count_boundary.py
```

The v0 executable is intentionally not wired into the general Dogram specimen schema yet. It is a bounded research harness whose constitution should survive prospective controls before any public operator promotion.

## Seal

> **LET THE COUNT BECOME A CARRIER. KEEP THE BOUNDARY. KEEP THE LOSING BRANCH. FREEZE THE KEY BEFORE YOU LOOK FOR THE DOOR.**
