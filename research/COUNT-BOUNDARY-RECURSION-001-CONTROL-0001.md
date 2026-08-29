# COUNT-BOUNDARY-RECURSION-001 — CONTROL-0001

**Run status:** POST-FREEZE CONTROL  
**Traversal constitution:** unchanged from `count-boundary-recursion/v0`  
**Semantic authority:** none

This receipt records the first controls run **after** the v0 traversal key was frozen. No operator or promotion gate was added in response to these results.

## Frozen operators

```text
prime_count@1
divisor_count_record@1
pair_count@1
```

## Control A — matched gap and magnitude

Motivating source pair:

```text
(1078,1087)
gap = 9
```

Control family:

```text
(a,a+9) for 900 <= a <= 1200
301 ordered pairs
```

Question:

> How often does a same-gap, similar-magnitude source pair produce any exact recurrence into the frozen historical registry in one admitted step?

Result:

```text
301 tested
4 produced a frozen-registry hit
```

All four hits were the same prime-count pair-image:

```text
(1078,1087) -> (180,181)
(1079,1088) -> (180,181)
(1080,1089) -> (180,181)
(1081,1090) -> (180,181)
```

Interpretation boundary:

- the motivating edge is exact;
- it is not unique even under a simple same-gap local control;
- this agrees with the previously calculated prime-count fiber pressure;
- the edge should be treated as a **lossy pair projection**, not an identifying fingerprint.

## Control B — every frozen historical seed

Running the exact frozen registry walk from every registered pair produced:

```text
(12,13)       -> sink
(17,18)       -> (136,137)
(81,82)       -> sink
(107,108)     -> sink
(136,137)     -> sink
(180,181)     -> (17,18) -> (136,137)
(207,208)     -> sink
(1007,1008)   -> sink
(1078,1087)   -> (180,181) -> (17,18) -> (136,137)
(1107,1108)   -> sink
```

Thus the three-edge cascade is the unique longest component inside this particular frozen retrospective registry under v0.

This is not yet a null-distribution rarity claim.

## Control C — shuffled historical endpoints

Shuffled ordered controls included:

```text
(12,108)
(17,137)
(81,181)
(107,208)
(136,1008)
(180,1087)
(207,1108)
```

Two shuffled pairs still entered the historical tail:

```text
(17,137) -> (136,137)
(180,1087) -> (17,18) -> (136,137)
```

This exposed a dependency mistake in the first prose description.

The tail is **not pair-supported**.

`divisor_count_record@1` on `(180,181)` depends only on carrier `180`.

`pair_count@1` on `(17,18)` depends only on carrier `17`.

Therefore receipts now preserve:

```text
support_arity
support_values
```

The motivating cascade should be read as:

```text
(1078,1087) -- support arity 2 --> (180,181)
180         -- support arity 1 --> (17,18)
17          -- support arity 1 --> (136,137)
```

The surrounding pair remains formation context where present, but an unused endpoint is not allowed to masquerade as a computational dependency.

## Hardening result

CONTROL-0001 weakens one claim and strengthens two methodological rules.

### Weakened

```text
"the whole cascade is pair-recursive"
```

is false.

Only the first edge is genuinely dyadic in v0.

### Strengthened

1. **Fiber pressure is load-bearing.** The first edge survives exactly but is visibly many-to-one.
2. **Dependency arity must travel.** A relation receipt must state which source coordinates actually paid for the derived edge.

## Next discriminator

Do not add operators.

Next useful control family:

```text
matched random pairs by magnitude + gap
held-out mathal pairs not used in v0 construction
registry permutations preserving marginal number frequencies
```

Measure the frequency and length of registered cascades under the frozen constitution.

## Seal

> **KEEP THE CONTEXT. MARK WHAT ACTUALLY PAID FOR THE EDGE.**
