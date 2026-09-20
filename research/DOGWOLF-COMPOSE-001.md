# DOGWOLF-COMPOSE-001 — One model, three independent calculation receipts

**Status:** stacked research draft, not a public Dogram operator. **Authority:** none. **Workbench runtime integration:** not yet wired.

## Purpose

Give a future read-only Workbench adapter **one JSON-serializable packet** for three separate questions over the **same explicitly declared finite state carrier and projection**:

1. `DESCEND-001`: do two named total transformations individually descend through the projection? Each operation has separate exact/raw and projected results, with its own finite witness, budget and possible induced table.
2. `SUCCESSOR-DESCENT-001`: do states collapsed by the projection agree on *independently declared* possible one-step successor sets, in raw and projected forms?
3. `COMMUTE-001`: do the two named transformations give the same raw and projected endpoints in both orders? Retain both ordered intermediate paths.

The results are **not collapsed** into one pass/fail field, score, readiness signal or merger permission. Inconclusive is never silently counted as preservation. Exact and projected equality remain separate.

## Exact inputs and output

`dogram.dogwolf_compose_001.compose_receipt(states, projection, first, second, successors, max_pair_checks=4096, max_state_checks=64)` delegates to the three independent bounded kernels with the same original `states` and `projection`. `first=(name, state_to_state_target_tuple)` and `second=(name, state_to_state_target_tuple)` must be distinct named total functions over the declared states. `successors` is a tuple of separately declared sets of possible successors, one per original state.

The composer explicitly does **not** infer that any transformation step belongs to the successor relation: those are two different user-declared structures until a future caller establishes a relation. This avoids inventing enabledness, occurrence, or operational permission.

The returned `dogram/dogwolf-compose-001/v0` packet has `model`, `model_sha256`, `results.descent`, `results.successor`, `results.commutation`, `authority=none`, `non_claims`, and `receipt_sha256`. Every nested kernel receipt carries its own independently computed `input_sha256`. The model checksum includes **typed projection identity** (so `True` and `1` do not collide), operation order, declared successor relation and calculation budgets. The receipt checksum binds the entire packet excluding its own checksum field. These digests are content checksums, not signatures, attestations that trusted software ran, or evidence of historical occurrence.

The result is a *Workbench-facing contract*, not a running Workbench feature: no UI element, API route, automatic repository scan, adapter subprocess, project mutation, or public Dogram dispatch is introduced. A future Workbench consumer should pin the exact Dogram code revision, preview exact model and scope, invoke the reviewed calculation under bounded resources, and verify the returned typed declaration and checksum before rendering separate result panels.

## Frozen three-lens collision

```
states = ("a", "b", "c")
projection = (0, 0, 1)
first = ("swap", ("b", "a", "c"))
second = ("redirect", ("a", "b", "a"))
successors = (("a",), ("c",), ())
```

Both declared transformations descend under this projection; the independently declared successor relation **fails** projected descent because `a` and `b` have different projected available successors; the two transformation orders **fail raw commutation** at `c` but their projected endpoints agree. The packet retains every outcome and its witness instead of reporting an invented overall verdict.

## Reproduce

```bash
python -m unittest tests.test_dogwolf_compose_001 -v
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

The independent isolated test-first harness observed a missing-module RED, then **8 focused composer tests** and **37 total combined research tests** passing locally with the three copied dependency kernels, as well as local compilation. GitHub CI on this exact stacked branch must be verified separately; isolated tests are not a claim that the full main-branch suite passed.

## PR ancestry and scope

This research branch begins from the **exact open DESCEND-001 PR #157 head**, rather than from main. It carries byte-identical copies of the module, tests and receipt from independently open SUCCESSOR-DESCENT-001 PR #158 and COMMUTE-001 PR #159 to exercise the three calculations *together* before any of the source PRs is prematurely promoted. Review the three source branches independently and reconcile/rebase the composite branch as they land. No main merge or public operator promotion is implied by this research PR.

**SAME MODEL ≠ SAME QUESTION. SAME PROJECTION ≠ SAME FUTURE. SAME ENDPOINT ≠ SAME PATH.**
