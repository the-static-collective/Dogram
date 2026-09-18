# OPERATION-REACHABILITY-QUOTIENT-001

**Status:** bounded internal research specimen  
**Authority:** none  
**Public operator:** none

## Question

After `ANTI-COLLAPSE-REACHABILITY-001` receipts pairwise distinctions lost by a lawful projection collapse, ask the stronger finite question:

> Does each declared operation's enabledness still have one exact answer on every collapsed state?

## Mathematics

Let `S` be a finite state set, `q : S -> Q` a declared collapse, and for each declared operation `a`, let `E_a : S -> {false,true}` state whether `a` is executable.

Exact operation reachability factors through the quotient iff, for every operation `a`, `E_a` is constant on every fiber of `q`:

```text
q(x) = q(y) => E_a(x) = E_a(y)
```

Equivalently, each enabledness predicate admits a deterministic quotient predicate `Ebar_a : Q -> {false,true}` with `E_a = Ebar_a after q`.

This is a finite congruence/factorization test. It is deliberately weaker than bisimulation: this specimen checks only declared one-step enabledness questions, not successor matching, trace equivalence, temporal properties, or occurrence history.

## Frozen hostile specimen

```text
states: ready, blocked, done
collapse: ready -> pending
          blocked -> pending
          done -> done

advance: ready=true, blocked=false, done=false
reset:   ready=false, blocked=false, done=true
```

The collapse merges `ready` and `blocked`, but `advance` has different enabledness on those states. Therefore there is no exact answer to `CAN advance EXECUTE?` at the collapsed state `pending` without adding a policy such as existential/may or universal/must semantics.

That policy choice is not silently made here.

## Control

If every operation signature is constant on each collapse fiber, exact enabledness factors through the quotient and `lost_operation_questions` is empty.

## Documented neighboring mathematics

Labeled transition systems use simulation/bisimulation and quotient constructions to reduce state spaces while controlling which behaviors are preserved. Exact simulation notions demand preservation conditions stronger than mere observational closeness; quotient transition systems explicitly operate on equivalence classes. See Yu, Yang, Wu & Song (2015), DOI `10.1155/2015/963597`, and Fu, Fan, An & Qiao (2026), DOI `10.1002/asjc.70082`.

The Dogram inference is narrower: before promoting a collapsed carrier as executable, receipt whether the declared enabled-operation predicates factor through that collapse.

## Boundaries

```text
ENABLED != OCCURRED
EXECUTABLE != EXECUTED
OPERATION SIGNATURE != COMPLETE BEHAVIOR
EXACT ONE-STEP FACTORIZATION != BISIMULATION
MAY-EXECUTE != MUST-EXECUTE
QUOTIENT CONGRUENCE != EVIDENCE OR AUTHORITY
```

No public operator, ontology, causal semantics, evidence semantics, or authority surface is added.

## Seal

> **IF A COLLAPSED STATE CANNOT ANSWER THE SAME DECLARED OPERATION QUESTION FOR ALL OF ITS MEMBERS, EXECUTABILITY DID NOT DESCEND EXACTLY THROUGH THE COLLAPSE.**

## Next frontier

Upgrade from enabledness to successor-sensitive behavior: require a collapsed transition relation to preserve both operation labels and successor classes. Compare existential quotient transitions, universal/must transitions, simulation, and bisimulation on one frozen finite carrier. Receipt exactly which behaviors are added or lost by each quotient policy rather than treating any one policy as canonical.
