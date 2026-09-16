# ANTI-COLLAPSE-REACHABILITY-001

**Status:** bounded internal research specimen  
**Authority:** none  
**Public operator:** none

## Question

When a richer projection is intentionally simplified, can Dogram receipt exactly which previously available pairwise distinctions become unavailable after the simplification?

The working pressure came from `LINEAGE-WEAVE-001`: Python value equality can identify `True` with `1`, and a head address alone cannot distinguish a spine relation from a braid relation when both point at the same address.

This specimen does **not** ask whether those distinctions are important, meaningful, causal, ontological, or worth preserving. It asks only whether the declared collapse destroys a declared distinguishability question.

## Lawful collapse

For finite states `S`, let:

- `r : S -> R` be the richer projection;
- `c : S -> C` be the proposed collapsed projection.

The collapse is accepted as lawful only if there exists a deterministic map `q : R -> C` such that:

```text
c = q after r
```

Operationally this is the existing Dogram partition-refinement/factorization test:

```text
rich equal => collapsed equal
```

If two states are already identical under the rich projection but split apart under the proposed collapsed projection, the proposal added information and is **not** a collapse.

## Reachability floor

For this first specimen, a "lawful future question" is deliberately restricted to one finite question family:

```text
CAN STATE A STILL BE DISTINGUISHED FROM STATE B?
```

For every pair separated by the rich projection:

- `preserved_distinction` means the collapsed projection still separates the pair;
- `lost_distinction` means the collapsed projection identifies the pair.

Thus the measured anti-collapse delta is:

```text
lost_distinctions
=
{ pairs distinguishable under rich projection
  but not distinguishable under collapsed projection }
```

This is information loss under declared equality semantics. It is **not yet** general executable-operation reachability.

## Frozen specimen A — numeric equality is not type identity

Rich projection:

```text
int:1      -> (int, 1)
bool:true  -> (bool, True)
int:0      -> (int, 0)
bool:false -> (bool, False)
```

Collapsed projection:

```text
int:1      -> 1
bool:true  -> True
int:0      -> 0
bool:false -> False
```

Under Python equality:

```text
1 == True
0 == False
```

The collapse is lawful and loses exactly two distinctions:

```text
int:1     != bool:true
int:0     != bool:false
```

The other four rich distinctions remain available.

This turns the hostile discovery from `LINEAGE-WEAVE-001` into a reusable calibration case.

## Frozen specimen B — head address is not relation type

Rich projection:

```text
spine@A -> (A, spine)
braid@A -> (A, braid)
spine@B -> (B, spine)
```

Collapsed projection:

```text
spine@A -> A
braid@A -> A
spine@B -> B
```

The collapse is lawful and loses exactly:

```text
spine@A != braid@A
```

while preserving both distinctions from the `B` address.

This receipts the earlier lineage law in a generic finite form:

> **HEAD ADDRESS != RELATION TYPE.**

## Controls

### Identity collapse

If `rich_projection == collapsed_projection`, the factorization exists and `lost_distinctions` is empty.

### Information-adding pseudo-collapse

If:

```text
rich:      a -> 0, b -> 0
collapsed: a -> 0, b -> 1
```

no deterministic factorization `rich -> collapsed` exists. The instrument returns `lawful_quotient = false` and does not report preservation/loss as though a lawful collapse had occurred.

## Receipt fields

`analyze_collapse(...)` returns:

```text
states
lawful_quotient
factorization_witness
collapse_classes
preserved_distinctions
lost_distinctions
```

The factorization witness is evidence only for the declared finite quotient relation. It does not certify semantics outside the supplied projections.

## Boundaries

```text
LAWFUL QUOTIENT != GOOD SIMPLIFICATION
LOST DISTINCTION != IMPORTANT DISTINCTION
PRESERVED DISTINCTION != SUFFICIENT MODEL
PAIRWISE DISTINGUISHABILITY != ALL FUTURE OPERATIONS
EQUALITY SEMANTICS != IDENTITY
INFORMATION LOSS != MEANING LOSS
```

No public Dogram operator or bootstrap registry entry is added.

## Next frontier

Only after this pairwise floor survives pressure should a later specimen ask the stronger question:

```text
which declared downstream operations remain executable
under rich state but cease to be executable after collapse?
```

That would move from **question reachability** to **operation reachability** and should be a separate experiment with its own declared operation family.

## Working seal

> **SHOW ME WHAT I CAN NO LONGER DISTINGUISH BECAUSE I THREW THIS INFORMATION AWAY.**

A stronger provisional research maxim, not promoted by this specimen:

> **A DISTINCTION EARNS FURTHER ATTENTION WHEN COLLAPSING IT DESTROYS A LAWFUL FUTURE QUESTION.**
