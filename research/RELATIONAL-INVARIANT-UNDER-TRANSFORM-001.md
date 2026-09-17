# RELATIONAL-INVARIANT-UNDER-TRANSFORM-001

**Status:** RESEARCH  
**Promotion:** none  
**Public operator:** none  
**Created:** 2026-09-17 America/Chicago

## Question

> **What makes a thing the same thing after transformation?**

This packet freezes one bounded mathematical specimen downstream of an ALEX inquiry into the number sets:

```text
123
321
369
963
```

The source inquiry arose from Numbers 28, where a recurring `3:2:1` grain-offering proportion is rendered by The Living Bible as `9:6:3` quarts. Dogram does not decide what that means. It asks only which declared relations survive exact transforms.

Governing contract:

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

---

## Frozen specimen

Let:

```text
v = (1,2,3)
R(v) = reverse(v)
S_k(v) = componentwise scalar multiplication by k
N(v) = v / sum(v), when sum(v) != 0
```

For `k = 3`:

```text
v        = (1,2,3)
R(v)     = (3,2,1)
S_3(v)   = (3,6,9)
R(S_3(v))= (9,6,3)
S_3(R(v))= (9,6,3)
```

Therefore:

```text
R(S_3(v)) = S_3(R(v))
```

The commutation is general for ordinary finite vectors because reversal changes component order while uniform scalar multiplication acts independently on each component.

---

## Number-set receipt

| Name | Tuple | Origin in this specimen |
| --- | --- | --- |
| `ASC_SOURCE` | `(1,2,3)` | source relation read in ascending orientation |
| `DESC_SOURCE` | `(3,2,1)` | textual bull/ram/lamb coefficient order |
| `ASC_SCALE_3` | `(3,6,9)` | `S_3(ASC_SOURCE)` |
| `DESC_SCALE_3` | `(9,6,3)` | `S_3(DESC_SOURCE)` |

Digit concatenations `123`, `321`, `369`, and `963` are mnemonic surfaces only. The Dogram object is the tuple and its declared transforms, not decimal concatenation magic.

---

## Exact invariants under uniform nonzero scaling

For a vector `v=(v1,...,vn)` and nonzero scalar `k`, the following are preserved when defined:

1. **component count**;
2. **zero pattern** if `k != 0`;
3. **pairwise ratios** `vi/vj` for `vj != 0`;
4. **relative order by magnitude** for positive `k`;
5. **normalized positive composition** `N(v)` for positive vectors;
6. **support pattern** `{i | vi != 0}`;
7. **reversal commutation** `R(S_k(v)) = S_k(R(v))`.

Not preserved automatically:

1. absolute magnitudes;
2. sums;
3. products;
4. Euclidean norm;
5. signs under negative `k`;
6. physical units;
7. meaning, provenance, or authority.

Therefore:

```text
SAME RATIO != SAME MAGNITUDE
SAME NORMALIZED FORM != SAME CARRIER
```

---

## Orientation

Reversal preserves:

- component multiset;
- sum;
- product;
- norm;
- support size;
- pairwise-value inventory.

Reversal changes:

- index assignment;
- directional order;
- first/last boundary;
- any operation sensitive to position or causally interpreted order.

Therefore:

```text
SAME MEMBERS != SAME ORIENTATION
SAME MULTISET != SAME ORDERED TRACE
```

This matters directly to Dogram because ordered traces are already first-class in `delta@1`: a reversed trace can retain all values while changing its boundary semantics.

---

## Commuting square

The frozen specimen forms:

```text
(1,2,3) --S3--> (3,6,9)
   |                 |
   R                 R
   |                 |
(3,2,1) --S3--> (9,6,3)
```

Both paths terminate at the same tuple.

Path A:

```text
(1,2,3)
  -> S3
(3,6,9)
  -> R
(9,6,3)
```

Path B:

```text
(1,2,3)
  -> R
(3,2,1)
  -> S3
(9,6,3)
```

Signed component delta at the terminus:

```text
(0,0,0)
```

This is an exact commuting result for the declared operators.

It does **not** imply that arbitrary operations commute.

---

## Hostile controls

### H1 — nonuniform pseudo-scale

Candidate:

```text
(1,2,3) -> (3,5,9)
```

Pairwise ratios:

```text
1:2:3 != 3:5:9
```

Normalized forms:

```text
(1/6, 2/6, 3/6)
!=
(3/17, 5/17, 9/17)
```

Verdict:

```text
NOT UNIFORM SCALE
RELATIONAL FORM CHANGED
```

This prevents `scaling` from becoming a vague label for any larger-looking vector.

### H2 — arbitrary permutation

Candidate:

```text
P(1,2,3) = (2,1,3)
```

The multiset survives but reversal identity does not:

```text
P(v) != R(v)
```

Verdict:

```text
MEMBERS PRESERVED
DECLARED ORIENTATION TRANSFORM NOT PRESERVED
```

### H3 — additive shift

Candidate:

```text
A_1(1,2,3) = (2,3,4)
```

Differences between adjacent components remain `1`, but ratios change.

Verdict:

```text
SAME FIRST DIFFERENCE
!=
SAME PROPORTIONAL FORM
```

This is useful because different invariants may survive different transform families.

### H4 — zero scale

```text
S_0(1,2,3) = (0,0,0)
```

All nonzero component distinctions collapse.

Verdict:

```text
ZERO SCALE IS A COLLAPSE, NOT A RELATION-PRESERVING SCALE FOR THIS SPECIMEN
```

### H5 — negative scale

```text
S_-3(1,2,3) = (-3,-6,-9)
```

Absolute ratios survive; sign and monotone direction change.

Verdict:

```text
WHICH INVARIANT YOU DECLARE MATTERS
```

---

## Recurrence / embedding axis

Define a context embedding operator abstractly as:

```text
E_t(v) = (t, v)
```

where `t` is a declared context or time address and `v` is the unchanged specimen.

Then:

```text
E_t1(v) != E_t2(v)
```

as addressed occurrences, while both contain the same relational body `v`.

Therefore:

```text
SAME RELATIONAL BODY
!=
SAME OCCURRENCE
```

and:

```text
RECURRENCE != IDENTITY
```

This is the correct Dogram boundary for the Numbers 28 recurrence: repeated use of a ratio can be documented without collapsing repeated contexts into one event or assigning spiritual meaning.

---

## Equivalence families

For strictly positive vectors, define proportional equivalence:

```text
v ~_scale w
iff
exists k > 0 such that w = S_k(v)
```

Then:

```text
(1,2,3) ~_scale (3,6,9)
(3,2,1) ~_scale (9,6,3)
```

but:

```text
(1,2,3) !~_scale (3,5,9)
```

Define reversal-relatedness separately:

```text
v ~_R w
iff
w = R(v)
```

Then:

```text
(1,2,3) ~_R (3,2,1)
(3,6,9) ~_R (9,6,3)
```

Do not collapse these relations into one unlabeled `same` edge.

A composite relation may be declared:

```text
v ~_{scale,R} w
iff
w = S_k(v) or S_k(R(v)) for some k > 0
```

but the receipt must retain which path was actually used.

Seal:

```text
EQUIVALENCE CLASS != TRANSFORMATION HISTORY
```

---

## Relationship to current Dogram work

This specimen sits naturally beside the repository's current anti-collapse line:

```text
ANTI-COLLAPSE asks:
what distinction disappears if I quotient these surfaces?

RELATIONAL-INVARIANT asks:
what declared relation survives this transformation?
```

They are dual but not interchangeable questions.

A future executable kernel could compare:

```text
input specimen
transform receipt
candidate output
predeclared invariant probes
```

and report, for each probe:

```text
PRESERVED | CHANGED | UNDEFINED
```

No scalar score is needed.

---

## Possible future bounded kernel — not implemented here

Candidate interface:

```python
analyze_transform(
    source: tuple[float, ...],
    transformed: tuple[float, ...],
    probes: tuple[str, ...],
) -> receipt
```

Possible probe vocabulary:

```text
component_count
support_pattern
normalized_positive_ratio
ordered_sign_pattern
adjacent_difference_pattern
multiset
reverse_relation
uniform_scale_relation
```

The kernel should refuse ambiguous floating-point equality unless a tolerance policy is explicitly supplied and receipted.

No generic ontology of `sameness` should be introduced. The caller declares which invariant question is being asked.

---

## Toaster handoff

A media planner can consume a weight vector without importing the Numbers 28 interpretation.

For positive weights `w_i` and a total temporal budget `B`:

```text
segment_i = B * w_i / sum(w)
```

Example:

```text
weights = (1,2,3)
B = 18 seconds
result = (3,6,9) seconds
```

Reversed orientation:

```text
weights = (3,2,1)
B = 18 seconds
result = (9,6,3) seconds
```

This preserves normalized ratio exactly in real arithmetic.

However:

```text
TEMPORAL BUDGET FIT
!=
MEDIA QUALITY OPTIMIZATION
```

Compression, resolution, bitrate, frame rate, and perceptual quality involve nonlinear encoder/content interactions. A Toaster descendant should receipt those as constrained optimization rather than falsely claiming exact scalar equivalence.

---

## Working laws

```text
CARRIER != RELATION
SURFACE != INVARIANT
SCALE != ORIENTATION
MEMBERS != ORDER
RECURRENCE != IDENTITY
EQUIVALENCE CLASS != TRANSFORMATION HISTORY
PRESERVED PROBE != GLOBAL SAMENESS

A TRANSFORMATION MAY CHANGE THE SURFACE
WITHOUT DESTROYING A DECLARED RELATION.

THE QUESTION "IS IT THE SAME?" IS UNDER-SPECIFIED.
ASK: WHICH RELATION SURVIVED?
```

---

## Delta receipt

Frozen source:

```text
(1,2,3)
```

Path A terminus:

```text
R(S_3(v)) = (9,6,3)
```

Path B terminus:

```text
S_3(R(v)) = (9,6,3)
```

Terminus delta:

```text
(0,0,0)
```

Hostile pseudo-scale:

```text
candidate = (3,5,9)
normalized source = (1/6,2/6,3/6)
normalized candidate = (3/17,5/17,9/17)
relation delta = nonzero
```

---

## Research frontier

1. **RELATIONAL-INVARIANT-KERNEL-001:** implement the smallest internal probe engine with no public operator registration.
2. **ROUNDING-RESIDUAL-001:** allocate integer frame/tick budgets from rational weights and receipt rounding residual instead of silently losing total duration.
3. **TRANSFORM-GROUP-001:** examine composition/inverses for reversal, positive scale, and selected permutations without overclaiming a full group where domains differ.
4. **LOCAL-vs-GLOBAL-INVARIANT-001:** show that preserving one probe does not establish global equivalence.
5. **MEDIA-BUDGET-BRIDGE-001:** formalize the boundary between exact proportional allocation and nonlinear quality-constrained encoding.
6. **TOASTER-RELATIONAL-FIT-001:** use the bounded allocation law experimentally for phrase scheduling before any compression/quality application.

---

## Receipt

- **Input provenance:** ALEX `ORDER-SCALE-RECURRENCE-001` inquiry and explicit number sets `123/321/369/963`.
- **Math:** exact finite-vector arithmetic and elementary algebra.
- **External semantic authority:** none.
- **Runtime change:** none.
- **Public operator change:** none.
- **Meaning decision:** none.
- **Durable location:** `research/RELATIONAL-INVARIANT-UNDER-TRANSFORM-001.md`
- **Promotion:** none
