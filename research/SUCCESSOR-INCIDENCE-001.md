# SUCCESSOR-INCIDENCE-001

**Status:** bounded exact research specimen  
**Authority:** none  
**Promotion:** none

## Formation

This slice is downstream of the current anti-collapse sequence:

```text
ANTI-COLLAPSE-REACHABILITY
-> OPERATION-REACHABILITY-QUOTIENT
-> SUCCESSOR-CLASS-QUOTIENT
-> MAY-UNION-QUOTIENT
-> MODAL-EXTREMA-INCIDENCE
```

The live question is what exact object remains after union/intersection summaries collide.

## Frozen collision

Compare representative-successor families:

```text
F0:
r0 -> {a,b}
r1 -> {a,c}

F1:
r0 -> {a}
r1 -> {a,b,c}
```

Both have:

```text
MAY  = {a,b,c}
MUST = {a}
```

But their exact incidence relations differ. Their member-size multisets also differ:

```text
F0 -> (2,2)
F1 -> (1,3)
```

Therefore:

```text
SAME MAY + SAME MUST != SAME REPRESENTATIVE-SUCCESSOR INCIDENCE
```

## Executable surface

`dogram.successor_incidence.receipt_successor_incidence()` receipts:

- deterministic representative-local successor sets;
- exact representative × successor incidence;
- `may` union;
- `must` intersection;
- member-size multiset;
- `authority: none`.

The exact incidence is the retained structure. The modal extrema and size multiset are derived summaries, not replacements for it.

## Boundary

```text
INCIDENCE != CAUSALITY
SUCCESSOR != OCCURRENCE
MAY != HISTORICAL DESTINATION
MUST-IN-FAMILY != INEVITABILITY
EXACT ONE-STEP FAMILY != BISIMULATION
STRUCTURE != TRUTH / AUTHORITY
```

No public Dogram operator, schema, registry, or semantic promotion is introduced.
