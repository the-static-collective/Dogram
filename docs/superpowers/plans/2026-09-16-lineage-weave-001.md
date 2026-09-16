# LINEAGE-WEAVE-001 Implementation Plan

> **For agentic workers:** use superpowers:subagent-driven-development when available, otherwise superpowers:executing-plans. Execute task-by-task with explicit RED -> GREEN receipts.

**Goal:** Add a bounded typed-composition layer that lets verified spine and braid heads participate in one later convergence while preserving which verifier governs each parent relation.

**Architecture:** Keep `LINEAGE-SPINE-001` and `LINEAGE-BRAID-001` unchanged. Add sibling `dogram/lineage_weave.py` with exact typed-parent descriptors, canonical typed parent sets, weave-normalized root sets, a sum-only merge receipt, fixed-shape weave capsules, a separate weave ledger, and a three-state verifier that dispatches each parent to its existing frozen verifier.

**Tech Stack:** Python 3.12 stdlib, existing `dogram.lineage_spine`, existing `dogram.lineage_braid`, unittest, existing Dogram CI.

**Spec:** `docs/superpowers/specs/2026-09-16-lineage-weave-001-design.md`

## Global Constraints

- Do not modify spine or braid capsule/verifier contracts.
- No new public Dogram operator or bootstrap-registry entry.
- Parent descriptors have exact keys `{kind, head_digest, carrier, root_set_digest}`.
- Supported kinds are exactly `spine` and `braid`.
- Typed parent identity is `(kind, head_digest)` and canonical sort is by that pair.
- Weave child never embeds parent histories or recursive ancestry.
- Parent verification dispatches to `verify_lineage(...)` or `verify_braid(...)` according to declared kind.
- Opposite-type positive witness yields `invalid / parent_kind_mismatch`; absence from both typed ledgers remains `incomplete`.
- Underlying roots are normalized into the weave root-set schema before comparison.
- `incomplete` remains distinct from `invalid`.
- Hash consistency never substitutes for verifier validity, type validity, arithmetic recomputation, or root-union recomputation.
- Frozen merge operator is integer `sum` only.

---

### Task 1: Typed parents and root-set normalization

**Files:** `dogram/lineage_weave.py`, `tests/test_lineage_weave.py`

- [x] Write RED tests for exact parent shape, closed `spine|braid` kinds, non-bool integer carriers, root normalization, duplicate typed-head rejection, and canonical parent order.
- [x] Confirm RED with the production module absent.
- [x] Implement `make_root_set(...)`, `make_typed_parent(...)`, and `make_parent_set(...)` minimally.
- [x] Verify unit tests, compile, constitutional floor, Omega scope scan, and structural-impact GREEN.

### Task 2: Merge, fixed child, and ledger

**Files:** `dogram/lineage_weave.py`, `tests/test_lineage_weave.py`

- [x] Write RED tests for canonical typed inputs `[109, 36]`, output `145`, fixed capsule shape, and content-addressed weave-ledger storage.
- [x] Confirm RED with merge/capsule/ledger APIs absent.
- [x] Implement sum-only merge receipt, fixed-shape child, and ledger buckets `capsules`, `parent_sets`, `root_sets`, `merge_receipts`.
- [x] Verify full Dogram CI GREEN.

### Task 3: Typed verifier dispatch

**Files:** `dogram/lineage_weave.py`, `tests/test_lineage_weave.py`

Frozen helper graph:

```text
5 -> 100 --\
            +--> 109
3 ->   9 --/

4 -> 36
```

- [x] Build genuine spine and braid heads in tests rather than fake descriptors.
- [x] Write RED verification tests for complete composition; missing/invalid spine and braid parents; carrier mismatch; root-set mismatch.
- [x] Confirm RED with `verify_weave(...)` absent.
- [x] Implement typed verifier dispatch.
- [x] Re-derive braid roots only after `verify_braid(...)` succeeds and normalize them into the weave root-set schema.
- [x] Implement positive opposite-type contradiction vs absent-witness distinction.
- [x] Independently verify merge inputs/output and child root union.
- [x] Verify full Dogram CI GREEN.

### Task 4: Hostile type-preservation controls

**Files:** `tests/test_lineage_weave.py`, `dogram/lineage_weave.py`

- [x] Re-hash a braid parent relabeled as `spine`; require `invalid / parent_kind_mismatch`.
- [x] Remove `kind` and re-hash dependents; require invalid descriptor shape.
- [x] Re-hash false `109 + 36 = 146`; require `invalid / merge_output_mismatch`.
- [x] Add nested `ancestry` to a re-hashed child; require `invalid / capsule_shape_mismatch`.
- [x] Re-hash a wrong but valid root-set object; require `invalid / root_union_mismatch`.
- [x] Hostile pass discovered a Python-specific alias: `True == 1` and `False == 0`. Add RED controls for `carrier=True` impersonating integer `1` and boolean merge inputs impersonating integer inputs.
- [x] Confirm both boolean attacks genuinely RED after correcting canonical input-order expectation.
- [x] Require non-boolean integer type before numeric equality; reject as `invalid_weave_carrier` / `merge_inputs_mismatch`.
- [x] Verify full Dogram CI GREEN.

### Task 5: Freeze `109 + 36 = 145` and document the boundary

**Files:** `tests/fixtures/lineage_weave_001.json`, `tests/test_lineage_weave_fixture.py`, `research/LINEAGE-WEAVE-001.md`, `README.md`

- [x] Add fixture test first and confirm RED with fixture absent.
- [x] Freeze canonical SHA-256 digests of the complete spine, braid, and weave ledgers, plus critical parent-set/root-set/merge/head addresses and the final verification result. This exact digest freeze replaces duplicating the full ledger literals while still detecting any serialized graph drift.
- [x] Document exact math, typed dispatch, root normalization, three-state verification, hostile controls, boolean/integer alias discovery, and explicit refusals.
- [x] Add README pointer without changing Dogram's public four-operator floor.
- [ ] Run fresh final CI on the final documentation head.
- [ ] Review the complete final PR diff for spine/braid/public-floor mutation.
- [ ] Merge only after both final gates are clean.

## Candidate seals

> **A DESCENDANT MAY INHERIT THROUGH DIFFERENT LAWFUL EDGE KINDS WITHOUT ERASING WHICH KIND EACH EDGE WAS.**

> **THE ADDRESS TELLS YOU WHERE. THE TYPE TELLS YOU HOW TO READ THE LINK.**

> **COMPOSITION MUST PRESERVE THE GRAMMAR OF THE CROSSING, NOT JUST THE RESULT.**

Implementation-level law discovered during hostile testing:

> **NUMERIC EQUALITY != TYPE IDENTITY.**