# SUCCESSOR-DESCENT-001 — One-step possible futures under a quotient

**Status:** bounded internal research specimen. **Authority:** none. **Public operator:** none. **Mandatory dependencies:** none.

## Question and definition

Given a nonempty finite state space `X`, an explicitly declared projection `q:X→Q`, and a declared (possibly nondeterministic) successor relation `S:X→P(X)`, compare **one-step available successors** for each pair of distinct states in the same projection fiber:

- Raw incidence: `q(x)=q(y) ⇒ S(x)=S(y)`.
- Projected successor descent: `q(x)=q(y) ⇒ {q(z):z∈S(x)}={q(z):z∈S(y)}`.

Raw incidence equality is strictly stronger. When the second condition has been fully checked, the induced successor relation on the **image** `q(X)` is well-defined by `S_bar(q(x))={q(z):z∈S(x)}`. A witness of failure reports the distinct input states, their supplied successor IDs, their projected successor classes, and the symmetric-difference classes. An incomplete budgeted search without a witness is **inconclusive**; a witnessed failure is conclusive even when the budget is exhausted. No induced relation is emitted on incomplete checks.

This finite check is **not** bisimulation, temporal execution, causal reachability, historical occurrence, or operational permission. The raw finite successor data is caller-declared, not inferred from the world.

## Frozen hostile specimen

`X=(r0,r1,a,b,c)`, `q=(ready,ready,near,near,far)`, `S(r0)={a,b}`, `S(r1)={a,c}`: both source states project to `ready`, but their projected possible next states are `{near}` versus `{near,far}`. The witness retains the `far` discrepancy.

A separate positive specimen has `S(r0)={a}`, `S(r1)={b}`, `q(a)=q(b)=done`. Raw successor incidence differs, yet projected one-step descent holds. Thus:

**SAME PROJECTED CURRENT STATE DOES NOT GUARANTEE SAME PROJECTED NEXT-STEP CHOICES. DISTINCT RAW FUTURES CAN STILL SHARE A PROJECTED FUTURE.**

The earlier `SUCCESSOR-INCIDENCE-001` and `BIREGULAR-INCIDENCE-COLLISION-001` research motivates keeping per-state successor families, not merely MAY/MUST summaries or graph degree summaries.

## Contract and reproducer

- `dogram.successor_descent_001.analyze_successor_descent(states, projection, successors, max_pair_checks=4096)`
- 1–64 distinct nonempty string states; one tuple of distinct declared successor IDs for each input state (empty allowed); typed finite projection values `None | bool | int | str | tuple` recursively.
- `True` and `1` have different typed projection identities. Row order is normalized to declared state order; no duplicate successor entries are accepted.
- One SHA-256 input digest binds the typed declaration, normalized adjacency and budget. It is a deterministic checksum, not a signature or trusted occurrence timestamp.
- Tests: `python -m unittest tests.test_successor_descent_001 -v`.

A test-first isolated run observed the missing-module RED condition and then **10 passing focused unittest methods**, including all **4096** finite 3-state binary-projection × declared successor-table combinations and malformed-input controls. Local compileall passed. The repository full suite and this PR's GitHub Actions status must be checked independently.

## Integration boundary

This is a standalone research-only module against `main` and does not import unmerged DESCEND-001 #157 or DOGWOLF-001 #155. Subsequent review may unify receipt fields if there is a concrete consumer, but no public CLI/registry change or Workbench side effect is made here.
