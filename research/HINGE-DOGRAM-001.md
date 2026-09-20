# HINGE-DOGRAM-001 — Exact Grammar-Delta Verification

**Status:** RESEARCH  
**Promotion:** none  
**Public operator:** none  
**Date:** 2026-09-18 America/Chicago

## Question

> Can Dogram independently verify an ALEX HINGE grammar-delta receipt without inheriting ALEX's interpretation or authority?

ALEX HINGE-001 proposes a bounded mapping:

```
Γ : selector -> declared relation
```

and witnesses before/after changes as:

```
ADDED
REMOVED
RETARGETED
UNCHANGED
```

Dogram's job is narrower:

> **Recompute the declared mapping delta exactly. Do not decide what any selector or relation means.**

---

## Input boundary

Dogram receives:

1. before rule set;
2. after rule set;
3. an ALEX HINGE receipt claiming the corresponding delta.

It does not receive or require:

- Project0 execution authority;
- ALEX semantic authority;
- source truth;
- theological truth;
- a model judgment;
- a causal verdict.

---

## Exact calculation

Let:

```
B = selector -> relation before
A = selector -> relation after
```

Then:

```
added      = dom(A) \ dom(B)
removed    = dom(B) \ dom(A)
retargeted = {q in dom(A) intersect dom(B) | A(q) != B(q)}
unchanged  = {q in dom(A) intersect dom(B) | A(q) == B(q)}
```

The rule lists are treated as mappings, not ordered traces.

Therefore:

```
RULE ORDER != GRAMMAR DELTA
```

Duplicate selectors are refused because they do not define a function.

---

## Verification relation

The verifier recomputes the delta from the before/after mappings and compares it exactly to ALEX's claimed:

- `added_rules`;
- `removed_rules`;
- `retargeted_rules`;
- `unchanged_rules`;
- `grammar_changed`.

Result:

```
EXACT_MATCH
|
MISMATCH
```

No score.

No preferred interpretation.

No inference that the encounter caused the change.

---

## Authority boundary

ALEX HINGE freezes:

```
authority: none
meaning_verdict: none
causal_status: not_established
```

Dogram exposes whether those fields remain so, but does not make them true.

In particular:

```
EXACT DELTA MATCH
!=
SEMANTIC TRUTH

EXACT DELTA MATCH
!=
CAUSATION

EXACT DELTA MATCH
!=
AUTHORITY
```

A hostile control deliberately changes the ALEX authority field while leaving the mathematical delta intact. Dogram must report:

```
verdict: EXACT_MATCH
authority_preserved: false
```

This prevents mathematical agreement from laundering authority.

---

## Executable specimen

- `research/hinge_dogram_001.py`
- `tests/test_hinge_dogram_001.py`

Controls:

1. exact recomputation succeeds;
2. input rule order does not matter;
3. tampered retargeted relation produces `MISMATCH`;
4. authority mutation is surfaced independently of the math;
5. duplicate selector is refused;
6. identical mappings in different order produce zero delta.

---

## Cross-repository composition

Current intended composition:

```
PROJECT0 / WHOLE RETURN
  crossing/native refs
        |
        v
ALEX / HINGE-001
  local grammar before/after
        |
        v
DOGRAM / HINGE-DOGRAM-001
  exact mapping delta verification
```

The jurisdictions remain independent:

```
WHOLE RETURN owns road continuity.

ALEX owns its declared reading/grammar witness.

DOGRAM owns exact delta verification.

NONE acquires the other's authority.
```

A future real specimen may pass opaque native references through the existing Whole Return contract rather than inventing a shared semantic identifier.

---

## Relation to current Dogram work

HINGE-DOGRAM-001 composes directly with:

### RELATIONAL-INVARIANT-UNDER-TRANSFORM-001

That packet asks:

> Which declared relation survived a transformation?

HINGE asks:

> Did the selector-to-relation structure itself change?

### TYPE-STABILIZER-AUTHORITY-001

That packet proves:

> **SYMMETRY CAN EXHIBIT A ROLE SWAP; IT CANNOT LICENSE THE SWAP.**

HINGE-DOGRAM applies the same brake:

> **A delta can exhibit a changed relation; it cannot license the relation.**

---

## External grounding

The originating ALEX packet is grounded in:

- Raffel et al. (2020), T5 unified text-to-text framework;
- Shaker (2026), *Code and Creed*, DOI 10.1111/jssr.70056;
- Huvila (2011), DOI 10.1002/asi.21639;
- Huvila et al. (2017), DOI 10.1002/asi.23817.

Dogram imports none of their semantic conclusions. They are provenance for the research question, not mathematical premises.

---

## Seal

```
DO THE MAPPING.
SHOW THE DELTA.
KEEP THE RECEIPT.
DO NOT DECIDE WHAT IT MEANS.
```

And:

> **The hinge can move. Dogram measures the movement; Dogram does not name the room.**
