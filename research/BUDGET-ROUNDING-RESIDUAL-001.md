# BUDGET-ROUNDING-RESIDUAL-001

**Status:** bounded exact research specimen  
**Authority:** none  
**Promotion:** none

## Formation

This slice is downstream of ALEX `ORDER-SCALE-RECURRENCE-001` and Dogram `RELATIONAL-INVARIANT-UNDER-TRANSFORM-001`.

The prior work establishes exact proportional scaling. This slice asks what happens when an exact proportional target must be realized in an indivisible integer budget such as frames, samples, blocks, or other discrete units.

## Exact target

For positive weights `w_i` and integer budget `B`:

```text
x_i = B * w_i / sum(w)
```

The `x_i` values are retained exactly as rational numbers.

### Zero-residual control

```text
weights = 3 : 2 : 1
budget = 12
exact = 6 : 4 : 2
```

No rounding residual is introduced.

## Hostile discrete control

Freeze:

```text
weights = 5 : 4 : 1
budget = 7
exact = 7/2 : 14/5 : 7/10
```

Two explicitly declared realization rules consume the same exact target and the same total budget.

### largest_fractional_remainder

```text
allocation = 3 : 3 : 1
```

### declared_order_remainder

```text
allocation = 4 : 3 : 0
```

Both allocate exactly seven units. Their per-bin residuals differ and each residual family sums exactly to zero.

Therefore:

```text
SAME EXACT PROPORTION
+
SAME INTEGER TOTAL
!=
SAME INTEGER REALIZATION
```

and:

```text
ROUNDING CONSTITUTION IS PART OF THE RECEIPT
```

## Executable surface

`dogram.budget_rounding_residual.receipt_integer_budget()` receipts:

- positive integer weights;
- non-negative integer budget;
- exact rational target per label;
- declared integer realization rule;
- realized integer allocation;
- exact signed residual per label;
- zero-sum residual check surface;
- total allocated budget;
- `authority: none`.

The two included realization rules are bounded controls, not declarations that either is universally preferable.

## Haunted Toaster handoff

This is sufficient to support later owner-local questions such as:

```text
allocate N frames across weighted phrases
allocate N samples across weighted regions
allocate N discrete work units across weighted segments
```

while retaining exactly where indivisibility changed the ideal proportional surface.

It does **not** solve nonlinear media compression or quality optimization. In particular:

```text
FRAME ALLOCATION != ENCODER QUALITY
BYTE BUDGET != PERCEPTUAL QUALITY
PROPORTIONAL TARGET != OPTIMAL COMPRESSION
ROUNDING RULE != ARTISTIC AUTHORITY
```

A later Toaster adapter should consume this receipt only when the target is genuinely a discrete allocation problem. Compression/quality research remains a separate frontier.

## Boundary

No public Dogram operator, codec policy, optimization engine, artistic ranking, or Toaster runtime mutation is introduced.
