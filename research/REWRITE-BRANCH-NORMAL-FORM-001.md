# REWRITE-BRANCH-NORMAL-FORM-001

**Date:** 2026-09-02  
**Status:** EXECUTABLE RESEARCH RECEIPT · FINITE TERMINATING STRING REWRITES · NO PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## 0. Why this seam

`HOME-MOTION-COMMUTATOR-001` established an exact order residue for noncommuting transformations and left multiway/rewrite confluence as a HOLD frontier. `TRACE-DEPENDENCE-001` separately showed that declared commuting actions can quotient some order differences without erasing all history.

The next bounded question is different:

> Given one declared start state with more than one legal next rewrite, do all terminating branches reconcile to the same terminal normal form?

This packet computes only that question for one finite reachable rewrite graph. It does not infer causal convergence, truth, agreement, consensus, authority, or semantic identity.

## 1. Documented mathematical substrate

In rewriting theory, confluence means divergent reductions can be rejoined. Local confluence restricts the divergence to one-step peaks. For terminating rewrite systems, Newman's lemma links local confluence to confluence; critical-pair analysis provides finite syntactic criteria for important classes of term rewrite systems.

References:

- Gérard Huet, **Confluent Reductions: Abstract Properties and Applications to Term Rewriting Systems**, *Journal of the ACM* 27 (1980), 797–821. DOI `10.1145/322217.322230`.
- Salvador Lucas, **Local confluence of conditional and generalized term rewriting systems**, *Journal of Logical and Algebraic Methods in Programming* 136 (2024), 100926. DOI `10.1016/j.jlamp.2023.100926`.
- H. Kondo, M. Kurihara, A. Ohuchi, **Completion of term-rewriting systems with multiple reduction orderings**, *Systems and Computers in Japan* 27(6) (1996), 33–44. DOI `10.1002/scj.4690270604`.

The executable kernel below is intentionally weaker than a global confluence prover.

## 2. Kernel boundary

`dogram.rewrite_branch.analyze_rewrite_branch(start, rules)` accepts finite string rewrite rules only when every rule strictly decreases string length:

```text
len(rhs) < len(lhs)
```

This restriction guarantees that every path reachable from the declared finite start terminates. The kernel then enumerates the complete reachable rewrite graph and receipts:

```text
start
rules
immediate_successors
all reachable states
all rewrite edges
terminal normal forms
unique_normal_form = (number of terminal normal forms == 1)
```

It does **not** claim that the rule system is globally confluent on every possible input string.

## 3. Frozen convergent specimen

Start:

```text
abc
```

Rules:

```text
abc -> ab
abc -> ac
ab  -> a
ac  -> a
```

Exact reachable graph:

```text
       abc
      /   \
    ab     ac
      \   /
        a
```

Receipt:

```text
immediate successors = {ab, ac}
reachable states      = {abc, ab, ac, a}
terminal normal forms = {a}
unique normal form    = true
```

Both legal first steps reconcile.

## 4. Hostile control: same local branching, different terminal residue

Hold fixed:

```text
start term                 = abc
number of rules            = 4
number of immediate forks  = 2
first-step successors      = {ab, ac}
strict length decrease     = true for every rule
termination guarantee      = same
```

Change only the final rule:

```text
abc -> ab
abc -> ac
ab  -> a
ac  -> c
```

Exact reachable graph:

```text
       abc
      /   \
    ab     ac
    |       |
    a       c
```

Receipt:

```text
immediate successors = {ab, ac}
reachable states      = {abc, ab, ac, a, c}
terminal normal forms = {a, c}
unique normal form    = false
```

Therefore:

```text
SAME START
SAME FIRST BRANCHING SURFACE
SAME TERMINATION GUARANTEE
!=
SAME TERMINAL NORMAL-FORM SET
```

## 5. Dogram inference

The durable calculational distinction is:

```text
BRANCH EXISTS
!=
BRANCHES RECONCILE
```

and, more sharply:

> **THE SAME LOCAL FORK DOES NOT DETERMINE WHETHER ITS FUTURES REJOIN.**

This complements rather than replaces prior kernels:

```text
TRACE DEPENDENCE
  asks which order differences are licensed to commute away.

COMMUTATOR RECEIPT
  asks whether two declared transformations are order-sensitive.

REWRITE BRANCH NORMAL FORM
  asks whether all terminating futures from one declared start end in one terminal form or several.
```

## 6. Required refusals

```text
unique normal form for this start
!= global confluence of the whole rewrite system

branch reconciliation
!= causal equivalence

same terminal text
!= same formation history

distinct terminal forms
!= semantic contradiction

termination
!= correctness

joinability
!= truth
```

The kernel computes a finite transition property only.

## 7. Why no public operator

No new public Dogram operator is earned here. The current executable value is research pressure and fixture generation.

Explicit HOLD:

```text
rewrite@1
confluence@1
critical_pair@1
normal_form@1
completion@1
```

A public operator would require a stable input constitution, explicit rewrite semantics beyond strings, and a demonstrated need that cannot be cleanly handled as a research kernel.

## 8. Next frontier

The strongest next seam is **critical-pair attribution** rather than larger exhaustive search.

For a genuine term-rewrite system, a finite obstruction receipt should identify the overlapping rules and position that created a nonjoinable local peak, not merely report multiple terminal forms downstream.

Candidate future question:

> Can Dogram produce the smallest attributable overlap witness whose two reducts fail to join, while keeping rule syntax, matching semantics, and termination assumptions explicit?

That would connect directly to Knuth–Bendix/Huet critical-pair theory without promoting rewrite structure into evidence or meaning.
