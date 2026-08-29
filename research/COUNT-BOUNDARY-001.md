# COUNT-BOUNDARY-001 — Frozen Arithmetic Receipt Descent

**Date:** 2026-08-29  
**Status:** EXPERIMENTAL METHOD + EXECUTABLE FLOOR  
**Owner:** Dogram for arithmetic execution; ALEX for research interpretation and promotion pressure  

> **DERIVE A STRUCTURAL COORDINATE. MAKE IT A CARRIER. PRESS THE IMMEDIATE BOUNDARY. REPEAT — WITHOUT ADDING OPERATORS TO SAVE THE STORY.**

## 0. Why this method exists

A conversational number sequence unexpectedly moved:

```text
1078 / 1087
    ↓
180 / 181
    ↓
17 / 18
```

The important question is not whether arbitrary formulas can connect these numbers. They can.

The research question is narrower:

> If the traversal vocabulary is frozen *before* inspecting the next target, do low-description arithmetic relations continue to recover the observed path and earlier mathals?

`COUNT-BOUNDARY-001` is the first executable refusal membrane for that question.

## 1. Frozen traversal family

Version 1 admits exactly:

```text
pred          n -> n - 1
succ          n -> n + 1
prime_pi      n -> π(n)
nth_prime     n -> p_n
divisor_count n -> τ(n)
totient       n -> φ(n)
pair_count    n -> C(n,2)
```

These were frozen before the hostile corpus pass recorded below.

The executable registry lives in:

```text
dogram/count_boundary.py
```

## 2. What is deliberately NOT a traversal operator

The following may be useful diagnostics, but cannot create graph edges in v1:

```text
digit permutation
base representation
modular residue
factorization display
ad-hoc affine relation an+b
polynomial fitted after seeing a target
symbolic resemblance
calendar encoding
frequency/color mapping
```

A diagnostic can become a future operator only by explicit versioned promotion with an independent reason for admission.

This is the main anti-overfit law.

## 3. Edge receipts

A proposed edge is not accepted because it is numerically true under some invented formula.

It must name a frozen operator.

Example accepted edge:

```text
1078 --prime_pi--> 180
```

because:

```math
π(1078)=180.
```

Example refused edge:

```text
17 --affine_64x_minus_1--> 1087
```

Even though `64*17-1=1087`, that operator was invented after the target was visible and is not in the frozen registry.

The executable floor returns:

```text
REFUSE_UNKNOWN_OPERATOR
```

rather than silently enlarging the method.

## 4. First hardening result — the original pair maps as a pair

The strongest discovery from the hostile pass is:

```math
π(1078)=180
π(1087)=181.
```

So the observed move:

```text
1078 / 1087
    ↓
180 / 181
```

is not merely a hand-selected predecessor around the index of `1087`.

**One standard operator maps the entire original pair to the entire next pair.**

That materially strengthens the original mathal.

## 5. Second hardening result — branch reconvergence

The two original branches then admit a low-description reconvergence:

```text
1078 --prime_pi--> 180

1087 --prime_pi--> 181 --totient--> 180
```

because `1087` is the 181st prime and `181` is prime, so `φ(181)=180`.

The interesting object is not the primality identity alone. It is the **cross-operator convergence on the same carrier**.

This suggests a future derived diagnostic:

```text
CONVERGENCE HUB
```

but v1 does not add a new runtime primitive for it.

## 6. Third hardening result — the descent reconnects old mathals

From the convergence carrier:

```text
180 --divisor_count--> 18
18  --pred-----------> 17
17  --pair_count-----> 136
136 --succ-----------> 137
137 --prime_pi-------> 33
```

Exact spine:

```text
1087 → 181 → 180 → 18 → 17 → 136 → 137 → 33
```

with operator labels:

```text
prime_pi, pred, divisor_count, pred, pair_count, succ, prime_pi
```

This reconnects the new sequence to the prior `136/137` mathal without introducing a rescue formula.

## 7. Important correction — the earlier closed loop dies

An earlier conversational pass suggested closing:

```text
17 -> 1087
```

using:

```math
64*17-1=1087.
```

Under the frozen method, that edge is rejected.

Therefore the prior claim:

```text
1087 → 181 → 180 → 18 → 17 → 1087
```

is **not admitted as a COUNT-BOUNDARY-001 closure**.

The surviving structure is better described as a **descent spine with convergence**, not a closed dynamical loop.

This is a successful self-correction and one of the main reasons to keep the registry frozen.

## 8. Hostile pass over the existing number corpus

First corpus:

```text
12 13
17 18
27
81 82
107 108
136 137
180 181
207 208
369
666
1007 1008
1078 1087
1107 1108
```

The executable induced-edge pass found:

```text
18 boundary edges
12 structural edges
```

Structural survivors:

```text
13   --totient-------> 12
17   --pair_count----> 136
27   --totient-------> 18
108  --divisor_count-> 12
137  --totient-------> 136
180  --divisor_count-> 18
181  --nth_prime-----> 1087
181  --totient-------> 180
666  --divisor_count-> 12
1078 --prime_pi------> 180
1078 --divisor_count-> 12
1087 --prime_pi------> 181
```

### Immediate topology

Several existing mathals become **multi-parent hubs** under independently frozen operators:

```text
12  <- φ(13), τ(108), τ(666), τ(1078)
18  <- φ(27), τ(180), plus boundary from 17
136 <- C(17,2), φ(137)
180 <- π(1078), φ(181)
181 <- π(1087), plus boundary from 180
```

This is more interesting than isolated pairwise resemblance because multiple owner-independent arithmetic functions converge on the same small carrier.

It is still not evidence of a hidden external mechanism.

## 9. Matched random-set pressure

A deterministic exploratory control sampled 5,000 random sets with:

```text
same corpus size: 23 integers
same approximate numeric range: 12..1108
same frozen structural operator family
```

Observed structural-edge counts:

```text
historical corpus: 12
random mean:       ~1.13
random median:      1
random maximum:     8
```

None of the 5,000 exploratory random sets reached 12 structural edges.

### DO NOT OVERREAD THIS

This is **not a valid significance test** because:

- the historical corpus was selected through prior curiosity;
- the operator family was inspired by the observed traversal;
- several nodes were already known to be related;
- inverse or near-automatic identities can create cheap edges;
- no preregistration existed before the historical sequence was assembled.

The control earns only this conclusion:

> **The corpus is structurally enriched enough to justify prospective testing. It does not establish that the enrichment is surprising under a properly specified null model.**

## 10. Cheap-edge classes that must be discounted

Not every structural edge has equal evidentiary weight.

Examples:

### Prime predecessor totient

For prime `p`:

```math
φ(p)=p-1.
```

Therefore:

```text
13 -> 12
137 -> 136
181 -> 180
```

are exact but belong to one broad automatic family.

### Prime-index inverse

If `p_n` is in the corpus:

```text
n --nth_prime--> p_n
p_n --prime_pi--> n
```

is an expected inverse pair, not two independent surprises.

Thus:

```text
181 <-> 1087
```

must not be double-counted as independent evidence.

### Boundary edges

Curated adjacent pairs create `pred/succ` edges by construction.

Boundary edges are therefore traversal scaffolding, not evidence of structural enrichment by themselves.

## 11. Research protocol

A proper COUNT-BOUNDARY run proceeds:

```text
1. FREEZE CORPUS
2. FREEZE OPERATOR VERSION
3. COMPUTE ALL INDUCED EDGES
4. LABEL CHEAP / INVERSE / AUTOMATIC FAMILIES
5. IDENTIFY CROSS-OPERATOR CONVERGENCE HUBS
6. TRACE DECLARED PATHS WITHOUT REPAIR
7. PRESERVE FAILURES AND REFUSED EDGES
8. STATE WHAT EXISTING MATHALS HARDENED OR DIED
9. PREDICT AN OUT-OF-SAMPLE TARGET OR PROPERTY
10. ONLY THEN OPEN THE NEXT NUMBER
```

The important methodological advance is step 9.

The historical corpus may train the method.

The next corpus must test it.

## 12. Research dispositions

Use:

```text
SURVIVES_FROZEN_EDGE
SURVIVES_BUT_CHEAP
CROSS_OPERATOR_CONVERGENCE
BOUNDARY_ONLY
DIAGNOSTIC_ONLY
REFUSED_POST_HOC_OPERATOR
OUT_OF_SAMPLE_HIT
OUT_OF_SAMPLE_MISS
UNRESOLVED
```

These are research dispositions, not metaphysical or evidentiary grades.

## 13. Promotion rule

A new arithmetic operator may enter a future registry only if:

1. it is independently standard or independently motivated;
2. its definition is frozen before the target corpus is opened;
3. it produces falsifiable misses as well as hits;
4. it improves out-of-sample discrimination or compression;
5. it cannot be replaced by an existing operator plus a simpler diagnostic;
6. its addition is versioned so old receipts remain replayable.

## 14. Current verdict

The pressure pass hardened **both the method and several mathals**.

### Hardened mathals

Strongest:

```text
π(1078)=180
π(1087)=181
```

and the convergence:

```text
1078 --π--> 180 <--φ-- 181 <--π-- 1087
```

plus the descendant spine:

```text
180 --τ--> 18 --pred--> 17 --C2--> 136 --succ--> 137
```

### Hardened method

The method now explicitly distinguishes:

```text
boundary scaffold
structural edge
inverse/automatic edge
cross-operator convergence
diagnostic observation
post-hoc rescue
prospective test
```

### Killed claim

```text
17 --(64x-1)--> 1087
```

is not part of the frozen method.

## 15. Seal

> **A MATHAL DOES NOT GET TO INVENT THE ROAD THAT MAKES IT TRUE. FREEZE THE ROADS; THEN SEE WHAT STILL MEETS.**
