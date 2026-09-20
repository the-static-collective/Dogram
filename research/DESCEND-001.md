# DESCEND-001 — Quotient-aware operation preservation

**Status:** bounded research-only kernel. **Authority:** none. **Public operator:** none. **Mandatory dependencies:** none.

## Mathematical contract

Given a finite nonempty state set `X`, declared projection `q: X → Q`, and one or more declared **total** state-to-state transition tables `f: X → X`, calculate independently:

- **Raw successor preservation:** `q(x)=q(y) ⇒ f(x)=f(y)`.
- **Projected successor preservation (descent):** `q(x)=q(y) ⇒ q(f(x))=q(f(y))`.

Only the second condition is necessary and sufficient for an induced operation `f_bar: q(X) → q(X)` satisfying `f_bar(q(x))=q(f(x))`. Exact raw preservation is a stronger condition. The induced table is emitted only if every pair in every projection fiber has been checked with no projected counterexample.

Each mode is `preserved | counterexample | inconclusive`. A bounded incomplete check without a counterexample is **inconclusive**, not preserved. A witnessed mismatch is conclusive even if the search is incomplete. The zero-pair case is vacuously preserved. Per-mode, per-operation pair budgets are explicit. Returned witnesses retain distinct supplied state IDs, raw successors, shared input projection and projected successor values.

Input bounds: 1–64 distinct string states; 1–16 operation tables; operation targets must name a declared state; finite typed projection values (`None`, `bool`, `int`, `str`, nested tuples). `1` and `True` are distinct. User callbacks and external execution are refused. The typed canonical SHA-256 input digest binds the declaration and budget; it is **not** a signature, trusted timestamp, execution receipt, or authority claim.

## Frozen counterexample

`states=("a","b","c")`, `q=(0,0,1)`.

- Identity table `("a","b","c")`: raw preservation **fails** for `a,b`, but projected descent **holds**; induced quotient table `((0,0),(1,1))`.
- Reset table `("b","a","b")`: raw preservation **fails**, projected descent **holds**; induced table `((0,0),(1,0))`.
- Advance table `("a","c","c")`: projected descent **fails** for `a,b`, because successor projections are `0,1`.

Hence **SAME INPUT QUOTIENT DOES NOT IMPLY SAME OUTPUT QUOTIENT; DISTINCT RAW SUCCESSORS DO NOT PREVENT QUOTIENT DESCENT.**

## Reproduce

```bash
python -m unittest tests.test_descend_001 -v
```

A separate local reconstruction of this module and its tests passed all 10 focused unittest methods, including an exhaustive 216-case oracle over all three-state binary projections and all three-state total transition tables. `python -m compileall -q dogram tests` also passed in that isolated reconstruction. This does **not** assert that the full repository suite or CI has passed on the GitHub branch; review and CI are pending.

## Relation to existing work and limits

- The already-merged `DECLARED-PATH-EQUIVALENCE-001` and `OPERATION-REACHABILITY-QUOTIENT-001` establish declared quotient relations and enabledness-loss controls.
- Open DOGWOLF-001 #155 checks whether **raw typed operation results** are constant on quotient fibers. DESCEND-001 is intentionally independent of that unmerged code; its distinctive test is **projected successor** constancy for explicitly declared total state transitions. Reconcile interfaces after review if useful.
- Descent under one declared quotient does not imply equivalence of supplied states, paths, witnesses, action histories, arbitrary future operations, or transitions over multiple steps. This kernel does not establish bisimulation, semantic correctness, causation, evidence, or execution permission.
- No public CLI/registry, schema migration, Workbench automation, or external runtime dependency is introduced.
