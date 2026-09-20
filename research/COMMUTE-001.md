# COMMUTE-001 — Finite path-sensitive order comparison

**Status:** bounded research only. **Public operator:** none. **Authority:** none. **Mandatory dependencies:** none.

## Mathematical contract

Let `X` be a declared finite state set, `f,g:X→X` declared total transition tables, and `q:X→Q` a typed declared observation projection. For each supplied origin `x`, retain the separately supplied ordered paths:

```
x → f(x) → g(f(x))
x → g(x) → f(g(x))
```

Check these two independent predicates over **every** declared `x`:

1. Raw pointwise commutation: `g(f(x)) == f(g(x))` as supplied state IDs.
2. Projected endpoint agreement: `q(g(f(x))) == q(f(g(x)))` under type-sensitive equality.

The second condition is weaker; neither asserts that the supplied ordered paths, intermediate states, or histories are identical. In particular, projected endpoint agreement does **not** establish that either `f` or `g` descends individually through `q`, so this experiment must not claim to construct quotient operations or establish commutation *of* such operations. It only compares projected endpoints for the declared original states.

Each mode yields `preserved`, `counterexample` (the first original state with a difference, including both ordered path traces and both projected endpoints), or `inconclusive` when the state-check budget is exhausted without a difference. A complete finite pass is required to report preservation; a witnessed difference is conclusive even under a small budget. Both modes have independent state-check budgets. Paths are retained for all states, even if comparison is budgeted, and must not be interpreted as actual execution events.

## Frozen controls

1. `X=(a,b,c)`, `q=(0,0,1)`, `f=swap(a,b)`, `g(c)=a` and otherwise `g` is identity. At `c`, the two paths are `c→c→a` and `c→a→b`: **raw endpoints differ, projected endpoints agree (0,0)**.
2. `f=(b,c,a)`, `g=(a,a,c)`. At `b`, the two paths are `b→c→c` and `b→a→b`: **projected endpoints differ (1,0)**.
3. An identity transformation commutes with a nontrivial swap on the declared carrier, while the intermediate paths remain distinguishable.

## Runtime and testing

`dogram.commute_001.analyze_commutation(states, projection, first, second, max_state_checks=64)` accepts distinct nonempty string state IDs (1–64), two named, distinct, inert total transition tables, and a typed projection (`None`, `bool`, `int`, `str` or nested tuples). `True` and `1` have distinct typed identities. User-provided executable callables and unknown successor IDs are refused. No public Dogram operator/CLI dispatch, arbitrary `Callable`, automatic Workbench execution, network dependency, or repository mutation is added.

Run `python -m unittest tests.test_commute_001 -v`. The local test-first RED was `ModuleNotFoundError: No module named 'dogram.commute_001'`; the GREEN local suite reported 9 tests passing, including all `27×27×8=5832` three-state function-pair/binary-projection specimens checked against an independent definition. Full repository CI must be checked on the actual PR head separately.

The receipt SHA-256 binds the declared typed input, operation order, and comparison budget. It is not a signature, historical occurrence receipt, causal warrant, or authority claim.

## Existing Dogram seam

`TRIANGULATOR-001` already compares order of numerical operators and returns an exact signed integer delta. COMMUTE-001 does not reimplement that integer calculation: it compares declared finite state labels (which have no meaningful subtraction), retains intermediate paths, and tests projected endpoint agreement. `STRICT2-INTERCHANGE-WHISKERING-001` examines typed higher-categorical composition; neither its interchange law nor causal independence is inferred from this finite comparison.

**SAME PROJECTED ENDPOINT != SAME RAW ENDPOINT != SAME ORDERED PATH.**
