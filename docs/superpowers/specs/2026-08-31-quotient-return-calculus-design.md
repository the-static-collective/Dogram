# Dogram QUOTIENT-RETURN CALCULUS — Honing Design

**Date:** 2026-08-31  
**Status:** approved research architecture; implementation not yet authorized  
**Repository:** `the-static-collective/Dogram`  
**Baseline:** `1b6253e5b6a27be1be16bfe4a53134d605dd5a35`  
**Research companion:** `research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md`

## 0. Decision

The newly converged return mathals justify one bounded Dogram honing, but not a new public operator and not a broad Ω rewrite.

The next executable slice, if separately approved, should do exactly three things:

1. preserve a typed **return relation** rather than one globally interpretable Boolean;
2. freeze exact quotient-return / carrier-return hostile specimens using current internal transverse mathematics and existing public comparison semantics;
3. refine the internal `PRODUCTIVE-DESYNC-001` input/receipt surface so `returned_to_coherence` cannot silently mean global state or history return.

It should **not** modify `omega.py`, the Mathal VM, public operator registry, proposal grammar, phase gate, or authority boundaries.

Compression:

```text
RETURN MUST NAME ITS QUOTIENT.
KEEP THE FINER RESIDUAL.
DO NOT PROMOTE CLOSURE INTO IDENTITY.
```

---

# 1. Why this seam exists now

Dogram independently contains several specimens with the same abstract calculation shape:

```text
PLJ:
  same projected phase
  different lifted carrier

PHASELIFT:
  same endpoint
  different approach history

OMEGA:
  same selected result
  different execution footprint

TRANSVERSE:
  same quotient sheet after a period
  potentially different exact carrier state
```

These do not share one ontology or physical mechanism.

They do support one reusable research law:

```text
EQUIVALENCE UNDER A DECLARED COARSE CUT
!=
EQUIVALENCE UNDER EVERY FINER CUT
```

Current Productive Desync accepts:

```python
returned_to_coherence: bool
```

as a local supplied fact. That is safe only while callers already understand the exact relation being asserted. The current repo now has enough independent return specimens that leaving the relation implicit creates avoidable ambiguity.

The honing should make that ambiguity impossible without enlarging Dogram's semantic authority.

---

# 2. Scope

## In scope for the future executable slice

- internal research-only return datatypes / helpers;
- typed return relation metadata;
- exact finite return-period calculations for the existing transverse cyclic quotient specimen;
- frozen hostile fixtures and tests;
- Productive Desync adapter/refinement;
- research documentation and receipts;
- constitutional tests proving the public operator floor and Ω surface remain unchanged.

## Out of scope

- public `return@1` operator;
- public `holonomy@1`, `monodromy@1`, `coherence@1`, or `lift@1`;
- generic topology or differential-geometry engine;
- automatic inference of quotient relationships;
- automatic inference of a fiber group;
- automatic experiment selection;
- semantic interpretation of reachability or return;
- modifying `omega.py`;
- changing the public bootstrap registry;
- promoting Productive Desync to an optimizer or authority-bearing classifier.

---

# 3. Core typed object

The minimum internal concept is a **ReturnRelation**.

Candidate research shape:

```python
@dataclass(frozen=True)
class ReturnRelation:
    relation_id: str
    quotient_id: str
    anchor_before: object
    anchor_after: object
    quotient_before: object
    quotient_after: object
    returned: bool
```

This is deliberately descriptive rather than magical.

It says only:

```text
under quotient_id,
quotient_before and quotient_after were compared,
and returned records equality under that declared comparison.
```

It does not infer:

```text
state identity
history identity
causal closure
semantic coherence
quality
truth
authority
```

## 3.1 Why anchor values remain present

A quotient-return claim with only:

```text
quotient_before == quotient_after
```

would erase the finer carrier difference that motivated the work.

The receipt must retain both anchors even if their internal comparison is delegated elsewhere.

## 3.2 Why this is not a universal quotient framework

Dogram does not need to implement arbitrary quotient construction.

For the first slice, callers supply already-declared quotient observations.

This preserves the current architectural pattern:

```text
Dogram calculates supplied typed relations.
It does not invent the decoder.
```

---

# 4. Optional finer residual

A return relation may carry a typed finer residual record:

```python
@dataclass(frozen=True)
class ReturnResidual:
    relation: str  # SAME | DIFFERENT or equivalent research-local enum/string
    before: object
    after: object
```

Do not make numeric subtraction mandatory.

The default lawful receipt is:

```text
before
!=
after
```

or:

```text
before
==
after
```

under a declared finer comparison.

Only specialized finite/group specimens should add a derived algebraic residual.

Hard rule:

```text
NO DECLARED ALGEBRA
-> NO INVENTED DIFFERENCE OPERATION
```

---

# 5. Exact transverse return helpers

The current transverse kernel already provides:

```text
d = gcd(m,n)
sheet coordinate = (a-b) mod d
closure_lift_index = d / gcd(d,r)
```

The first executable honing may add pure helpers with no public registry exposure.

Candidate functions:

```python
def quotient_return_period(m: int, n: int, r: int) -> int:
    d = gcd(m, n)
    return d // gcd(d, r)


def exact_carrier_return_period(m: int, r: int) -> int:
    return m // gcd(m, r)


def return_debt(m: int, n: int, r: int) -> int:
    q = quotient_return_period(m, n, r)
    e = exact_carrier_return_period(m, r)
    assert e % q == 0
    return e // q
```

These helpers should either live in `dogram/transverse.py` or a very small adjacent internal module if the existing file becomes conceptually overloaded.

Recommendation: keep them in `dogram/transverse.py` for the first slice because they are direct algebraic facts of the exact same cyclic quotient model.

Do not create a generic `return.py` module unless a second independent executable carrier requires it.

YAGNI applies.

---

# 6. Productive Desync honing

## 6.1 Problem

Current classifier signature includes:

```python
returned_to_coherence: bool
```

The field is intentionally local, but its name is broader than the exact mathematical relation now available.

## 6.2 Recommended migration

Do **not** simply rename the Boolean and break every caller.

Introduce one typed research input whose semantics are explicit, then adapt the classifier internally.

Candidate shape:

```python
return_relation: ReturnRelation
```

The classifier's bounded-desync gate becomes:

```text
return_relation.returned must be true
```

and the receipt preserves:

```text
return_relation_id
quotient_id
anchor before/after
quotient before/after
returned under relation
```

The reason code can remain:

```text
NO_COHERENCE_RETURN
```

for compatibility in the first slice, but the receipt must make clear that this means failure of the **declared return relation**, not failure of global coherence.

Alternative later cleanup:

```text
NO_DECLARED_RETURN
```

would be semantically cleaner but is not necessary for the first bounded implementation.

## 6.3 Compatibility option

If changing the function signature would create excessive churn, add a new classifier entry point and retain the old one as a thin internal compatibility wrapper for one release/research cycle.

Do not preserve dual semantics indefinitely.

The implementation plan should decide based on actual call-site count at implementation time.

---

# 7. Frozen specimens

The future executable slice should freeze a minimum set of hostile fixtures.

## R1 — `Z6xZ9-r1-quotient-before-carrier-return`

Expected:

```text
d = 3
quotient_return_period = 3
exact_carrier_return_period = 6
return_debt = 2
```

After 3 bounded cycles:

```text
sheet returned = true
exact carrier returned = false
```

After 6:

```text
sheet returned = true
exact carrier returned = true
```

## R2 — `Z8xZ12-r4-quotient-inert`

Expected:

```text
d = 4
quotient_return_period = 1
exact_carrier_return_period = 2
return_debt = 2
```

The quotient returns every cycle while the exact carrier alternates.

## R3 — coprime control

Example:

```text
m=5
n=7
r=1
```

There is one synchronized sheet.

Expected:

```text
quotient_return_period = 1
```

This proves that a trivial quotient-return is not evidence of useful lift.

## R4 — exact return control

Choose `r` divisible by `m`.

Expected:

```text
quotient_return_period = 1
exact_carrier_return_period = 1
return_debt = 1
```

No hidden residual.

## R5 — multi-generator word control

Use a declared quotient with more than one generator.

Freeze two words over the same admitted generator family:

```text
word A returns
word B does not
```

while generated closure is identical.

This locks:

```text
GENERATOR CLOSURE != DECLARED WORD
```

## R6 — Productive Desync relation-scope control

Same reach counts and execution residual, two supplied return relations:

```text
coarse quotient returned = true
fine quotient returned = false
```

Classifier results must differ only according to the declared relation actually supplied.

No global return inference.

---

# 8. PLJ and Ω dispositions

## 8.1 PLJ

Keep PLJ as an exact analytic research fixture/documented control in this slice.

Do not build a general Euclidean projection engine merely to executable-ize it.

Its job is to prove that the abstract return grammar occurs independently in a geometric carrier.

## 8.2 Ω

Do not modify `omega.py`.

The current Ω receipt already preserves:

```text
result
execution digest
step trace
consumed inputs
fuel
```

The existing `EXECUTION-CUT / OMEGA-QUOTIENT` design owns future runtime binding of target-return to execution residuals.

The return-calculus slice may reference that design and add hostile documentation, but it must not preempt it.

---

# 9. No-holonomy boundary

The research packet identifies a legitimate connection to holonomy/monodromy only under additional structure.

The first executable honing must **not** introduce those words as runtime types.

Tests should explicitly preserve:

```text
quotient return
!=
holonomy
```

unless a specimen supplies:

```text
fiber action
transport law
composition rule
```

No generic fiber algebra is part of this design.

---

# 10. Data flow

Future bounded flow:

```text
DECLARED TRANSVERSE SPECIMEN
    -> exact quotient facts
    -> bounded history / generator closure receipts
    -> quotient return period
    -> exact carrier return period
    -> return debt
    -> typed return relation

DECLARED PRODUCTIVE-DESYNC INPUT
    -> preservation facts
    -> execution residual
    -> historical reach
    -> closure reach
    -> typed return relation
    -> classifier
    -> WITNESS | POTENTIAL | REFUSE
```

The classifier still does not create any of those facts itself.

It consumes them.

---

# 11. Error handling

All finite return helpers fail closed on invalid dimensions/generators using existing transverse validation conventions.

Required invalid cases:

```text
m <= 0
n <= 0
bool supplied where integer expected
non-integer r
malformed ReturnRelation
missing relation_id
missing quotient_id
```

Do not silently coerce values.

Productive Desync must refuse a missing/false declared return relation before issuing `WITNESS` or `POTENTIAL`.

A quotient equality with missing finer anchors may be valid as a narrow return relation, but then no finer residual claim may be emitted.

---

# 12. Testing strategy

Implementation must use TDD.

Minimum suites:

```text
tests/test_transverse.py
  -> new exact return-period formula tests
  -> independent bounded brute-force period oracle

new focused return-relation tests
  -> equality under quotient vs inequality under anchors
  -> nested refinement control
  -> malformed input refusal

tests/test_productive_desync.py
  -> typed return relation witness/refusal controls
  -> coarse/fine return distinction
```

Independent brute-force oracle should check a bounded grid distinct from the closed-form helper implementation.

Suggested bounded exhaustive range:

```text
m,n in 2..20
r in 1..20
```

For every specimen verify:

```text
first brute quotient-return period
== d/gcd(d,r)

first brute exact-state return period
== m/gcd(m,r)

exact_period % quotient_period == 0
```

Do not use the production formula inside the oracle.

---

# 13. Constitutional verification

Before merge, verify on the exact head:

```text
full unit suite passes
compile passes
public Phase A operator floor unchanged
bootstrap registry ids unchanged
omega.py unchanged
proposal grammar unchanged
phase gate unchanged
no new public runtime schema admitted
```

If the repository already has constitutional CI checks covering these, use them rather than adding redundant bespoke checks.

---

# 14. File plan for future implementation

Expected minimal production changes:

```text
dogram/transverse.py
  -> add exact return period helpers

dogram/productive_desync.py
  -> consume typed return relation or a bounded adapter
```

Expected new internal/support files only if needed after call-site inspection:

```text
dogram/return_relation.py
```

Recommendation: avoid this file in the first implementation unless the typed object is reused independently by more than Productive Desync and transverse tests.

Expected tests/fixtures:

```text
tests/test_transverse.py
tests/test_productive_desync.py
possibly tests/test_return_relation.py
tests/fixtures/return_relation/*.json
```

Documentation:

```text
research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md
README factual status note only if executable behavior lands
```

Do not modify README for research-only design landing.

---

# 15. Alternatives considered

## A — New public `return@1` operator

Rejected.

Reason:

The first exact calculations are already compositions or internal finite-algebra helpers. There is no demonstrated calculational gap on the public floor.

## B — Generic holonomy subsystem

Rejected.

Reason:

Most current specimens lack the required declared fiber/transport structure. Adding generic holonomy now would promote metaphor into runtime architecture.

## C — Leave `returned_to_coherence` Boolean untouched forever

Rejected as long-term architecture.

Reason:

The repo now contains enough independent quotient-return specimens that the relation's scope is materially important to interpretation and testing.

## D — Typed return relation + finite exact helpers + Productive Desync honing

Recommended.

It preserves the mathematical survivor with the smallest authority and implementation surface.

---

# 16. Self-review checklist

This spec intentionally contains no:

```text
TBD
TODO
placeholder operator
implicit physical fifth-dimension claim
implicit holonomy claim
semantic definition of coherence
```

The implementation seam is bounded to existing internal research behavior.

The public operator floor remains unchanged.

Ω remains untouched.

Productive Desync remains a classifier of supplied calculational facts, not an experiment chooser.

---

# 17. Seal

> **RETURN IS A RELATION, NOT AN ATTRIBUTE.**
>
> **THE QUOTIENT MAY CLOSE WHILE THE CARRIER LIFTS.**
>
> **KEEP THE FINER RESIDUAL.**
>
> **GENERATOR CLOSURE != DECLARED WORD != ACTUAL HISTORY.**
>
> **NO FIBER LAW -> NO HOLONOMY CLAIM.**
>
> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**
