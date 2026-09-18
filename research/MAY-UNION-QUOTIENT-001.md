# MAY-UNION-QUOTIENT-001

Status: bounded research specimen. Authority: none. Public operator: none.

## Question

Can a quotient preserve the enabled action label and the aggregate existential/may successor surface while still erasing which successor classes belonged to which representative?

Yes.

## Frozen specimen

Collapse `left` and `right` to quotient state `pending`.

- `left --advance--> green`
- `right --advance--> hold`

Both representatives enable `advance`. The existential/may quotient successor surface is the union `{green, hold}`. But the representative receipts are `{green}` and `{hold}`, so exact successor factorization fails. The representative-common/must-style intersection is empty.

Thus:

`SAME ENABLED LABEL + SAME AGGREGATE MAY SURFACE != REPRESENTATIVE-STABLE SUCCESSOR STRUCTURE.`

Seal:

> THE SAME AGGREGATE MENU OF POSSIBLE FUTURES DOES NOT MEAN EVERY COLLAPSED REPRESENTATIVE HAD THE SAME MENU.

## Documented mathematics

Modal transition systems distinguish may transitions (permitted/possible) from must transitions (required). See Bauer, Juhl, Larsen, Legay & Srba, *Extending modal transition systems with structured labels*, Mathematical Structures in Computer Science 22(4), 2012, DOI 10.1017/S0960129511000697. Standard bisimulation/quotient constructions impose representative-matching transition conditions stronger than merely taking an existential union of outgoing transitions.

This specimen does not claim a new theorem. It is a finite hostile control exposing the information lost by an existential union quotient.

## Dogram inference

A may/union quotient can be useful when that is the declared abstraction. It must not be mistaken for an exact descent of representative transition structure. Receipt both the quotient policy and, when exactness matters, whether successor-class sets are constant across the collapsed fiber.

## Refusals

- ENABLED != OCCURRED.
- EXECUTABLE != EXECUTED.
- MAY SUCCESSOR != HISTORICAL DESTINATION.
- MUST/COMMON SUCCESSOR != INEVITABLE REAL-WORLD FUTURE.
- AGGREGATE UNION != REPRESENTATIVE-STABLE STRUCTURE.
- EXACT ONE-STEP FACTORIZATION != BISIMULATION.
- QUOTIENT SEMANTICS != EVIDENCE, TRUTH, OR AUTHORITY.

## Reproduce

`pytest -q tests/test_may_union_quotient.py`

The kernel is dependency-free and finite; the fixture freezes the hostile specimen exactly.

## Next frontier

Two quotient states can agree on may-union and must-intersection surfaces while differing in the intermediate family of representative successor sets. Search for the smallest such collision. This would show that even the pair `(may, must)` can be a lossy summary of representative-wise branching geometry.
