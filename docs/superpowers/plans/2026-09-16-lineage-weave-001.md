# LINEAGE-WEAVE-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded typed-composition layer that lets verified spine and braid heads participate in one later convergence while preserving which verifier governs each parent relation.

**Architecture:** Keep `LINEAGE-SPINE-001` and `LINEAGE-BRAID-001` unchanged. Add sibling `dogram/lineage_weave.py` with exact typed-parent descriptors, canonical typed parent sets, a content-addressed root-set object, a narrow sum merge receipt, fixed-shape weave capsules, a separate weave ledger, and a three-state verifier that dispatches each parent to the existing spine or braid verifier according to its declared kind.

**Tech Stack:** Python 3.12 stdlib, existing `dogram.lineage_spine`, existing `dogram.lineage_braid`, unittest, existing Dogram CI.

**Spec:** `docs/superpowers/specs/2026-09-16-lineage-weave-001-design.md`

## Global Constraints

- Do not modify `LINEAGE-SPINE-001` capsule schema or verifier behavior.
- Do not modify `LINEAGE-BRAID-001` capsule schema or verifier behavior.
- No new public Dogram operator or bootstrap-registry entry.
- Parent descriptors contain exact keys `{kind, head_digest, carrier, root_set_digest}`.
- Supported kinds are exactly `spine` and `braid`.
- Typed parent identity is the pair `(kind, head_digest)`; canonical sort is by that pair.
- Weave child never embeds parent capsules or recursive ancestry.
- The verifier independently dispatches each parent to `verify_lineage(...)` or `verify_braid(...)` according to `kind`.
- `incomplete` remains distinct from `invalid`.
- Hash consistency never substitutes for verifier validity or arithmetic recomputation.
- Frozen merge operator is integer `sum` only.

---

### Task 1: Typed parent descriptors and root-set normalization

**Files:**
- Create: `dogram/lineage_weave.py`
- Create: `tests/test_lineage_weave.py`

**Interfaces:**
- Consumes: `canonical_digest(...)` from `dogram.lineage_spine`.
- Produces: `make_typed_parent(kind: str, head_digest: str, carrier: int, root_digests: list[str]) -> dict[str, object]`, `make_root_set(root_digests: list[str]) -> dict[str, object]`, `make_parent_set(parents: list[dict[str, object]]) -> dict[str, object]`.

- [ ] **Step 1: Write failing tests** proving exact parent shape, only `spine|braid` kinds are accepted, duplicate `(kind, head_digest)` pairs are rejected, root digests canonicalize as sorted unique values, and input parent order does not change parent-set identity.

Representative tests:

```python
def test_parent_order_does_not_change_identity():
    a = make_typed_parent("braid", "b-head", 109, ["r1", "r2"])
    b = make_typed_parent("spine", "s-head", 36, ["r3"])
    assert make_parent_set([a, b]) == make_parent_set([b, a])


def test_kind_is_required_and_closed():
    with pytest.raises(ValueError):
        make_typed_parent("unknown", "head", 1, ["r"])
```

- [ ] **Step 2: Run the focused test module and verify RED** because `dogram.lineage_weave` does not exist.
- [ ] **Step 3: Implement minimal constructors** with exact shapes, non-bool integer carriers, non-empty digests, sorted unique roots, and canonical `(kind, head_digest)` ordering.
- [ ] **Step 4: Run focused tests and full Dogram CI checks to verify GREEN.**
- [ ] **Step 5: Commit.**

### Task 2: Sum merge, fixed-shape capsule, and weave ledger

**Files:**
- Modify: `dogram/lineage_weave.py`
- Modify: `tests/test_lineage_weave.py`

**Interfaces:**
- Consumes: `make_parent_set(...)`, `make_root_set(...)`.
- Produces: `make_sum_merge(parent_set: dict[str, object]) -> dict[str, object]`, `make_weave_capsule(parent_set: dict[str, object], root_set: dict[str, object], merge_receipt: dict[str, object]) -> dict[str, object]`, `make_weave_ledger() -> dict[str, object]`, `store_parent_set(...) -> str`, `store_root_set(...) -> str`, `store_merge_receipt(...) -> str`, `store_weave_capsule(...) -> str`.

- [ ] **Step 1: Write failing tests** showing carriers `109` and `36` produce output `145`, the capsule has exactly `{schema, specimen, carrier, carrier_origin, parent_set_digest, merge_receipt_digest, root_set_digest}`, and no embedded `parents` or `ancestry` fields.
- [ ] **Step 2: Run focused tests and verify RED.**
- [ ] **Step 3: Implement minimal sum receipt, fixed-shape capsule, and content-addressed ledger buckets** `capsules`, `parent_sets`, `root_sets`, `merge_receipts`.
- [ ] **Step 4: Run focused tests and full CI checks to verify GREEN.**
- [ ] **Step 5: Commit.**

### Task 3: Typed verifier dispatch

**Files:**
- Modify: `dogram/lineage_weave.py`
- Modify: `tests/test_lineage_weave.py`

**Interfaces:**
- Consumes: `verify_lineage(...)` from `dogram.lineage_spine`, `verify_braid(...)` from `dogram.lineage_braid`.
- Produces: `verify_weave(head_digest: str, weave_ledger: dict[str, object], braid_ledger: dict[str, object], spine_ledger: dict[str, object]) -> dict[str, object]`.

- [ ] **Step 1: Build exact helper fixtures in tests** for:
  - spine `5 -> 100`;
  - spine `3 -> 9`;
  - braid `9 + 100 -> 109`;
  - independent spine `4 -> 36`.
- [ ] **Step 2: Write failing verification tests** for complete typed weave, missing spine witness => `incomplete`, missing braid witness => `incomplete`, invalid spine parent => `invalid`, invalid braid parent => `invalid`, parent carrier mismatch => `invalid`, and parent root-set mismatch => `invalid`.
- [ ] **Step 3: Run focused tests and verify RED.**
- [ ] **Step 4: Implement verifier dispatch.** For `spine`, call `verify_lineage(...)`, inspect the referenced spine head, and normalize its single root. For `braid`, call `verify_braid(...)`, inspect the braid capsule and its referenced braid parent-set, and derive the sorted unique root digests represented by that braid. Compare those re-derived roots with the typed parent's `root_set_digest`.
- [ ] **Step 5: Verify merge inputs/output and child root union independently** rather than trusting stored content.
- [ ] **Step 6: Run focused tests and full CI checks to verify GREEN.**
- [ ] **Step 7: Commit.**

### Task 4: Hostile type-preservation controls

**Files:**
- Modify: `tests/test_lineage_weave.py`
- Modify: `dogram/lineage_weave.py` only when tests expose holes.

**Interfaces:**
- Consumes: `verify_weave(...)`.
- Produces: verified relation-kind preservation and fixed-shape boundedness.

- [ ] **Step 1: Add RED hostile test:** take the valid braid-parent descriptor, change `kind` from `braid` to `spine`, re-hash the parent set, merge receipt, root set, and child so all content addresses are internally self-consistent. Expected result: `invalid / parent_kind_mismatch` or equivalent wrong-verifier failure.
- [ ] **Step 2: Add RED hostile test:** remove `kind` from a typed parent descriptor and re-hash dependents. Expected: `invalid / parent_descriptor_shape_mismatch`.
- [ ] **Step 3: Add RED hostile test:** re-hash merge receipt and child around false `109 + 36 = 146`. Expected: `invalid / merge_output_mismatch`.
- [ ] **Step 4: Add RED hostile test:** add nested `ancestry` to weave capsule and re-hash. Expected: `invalid / capsule_shape_mismatch`.
- [ ] **Step 5: Add RED hostile test:** replace the root-set object with an internally valid but wrong root set and re-hash child. Expected: `invalid / root_union_mismatch`.
- [ ] **Step 6: Implement the minimum verifier checks exposed by RED tests, then rerun focused/full CI to GREEN.**
- [ ] **Step 7: Commit.**

### Task 5: Freeze `109 + 36 = 145` and document the grammar boundary

**Files:**
- Create: `tests/fixtures/lineage_weave_001.json`
- Create: `tests/test_lineage_weave_fixture.py`
- Create: `research/LINEAGE-WEAVE-001.md`
- Modify: `README.md`

**Interfaces:**
- Frozen braid parent: `5 -> 100`, `3 -> 9`, then `9 + 100 = 109`.
- Frozen spine parent: `4 -> 36`.
- Frozen typed weave child: `109 + 36 = 145`.

- [ ] **Step 1: Add fixture test first and verify RED with fixture absent.**
- [ ] **Step 2: Generate and add the exact frozen spine ledger + braid ledger + weave ledger + verification fixture, then verify GREEN.**
- [ ] **Step 3: Write `research/LINEAGE-WEAVE-001.md` with exact math, typed dispatch topology, root union, three-state verification, hostile controls, and explicit refusals:** `TYPED EDGE != CAUSAL EDGE`, `HEAD ADDRESS != RELATION TYPE`, `VERIFIER DISPATCH != ONTOLOGY`, `HASH CONSISTENCY != GRAMMAR VALIDITY`, `RECONSTRUCTION != CREATION`.
- [ ] **Step 4: Add README pointer without changing the public four-operator floor.**
- [ ] **Step 5: Run fresh final CI on final head and review the full PR diff before merge.**
- [ ] **Step 6: Merge only after final-head green verification and diff review show no spine/braid contract mutation.**

## Candidate seals

> **A DESCENDANT MAY INHERIT THROUGH DIFFERENT LAWFUL EDGE KINDS WITHOUT ERASING WHICH KIND EACH EDGE WAS.**

> **THE ADDRESS TELLS YOU WHERE. THE TYPE TELLS YOU HOW TO READ THE LINK.**

> **COMPOSITION MUST PRESERVE THE GRAMMAR OF THE CROSSING, NOT JUST THE RESULT.**