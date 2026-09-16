# LINEAGE-BRAID-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded, content-addressed multi-parent derivation layer that converges two or more verified spine heads into one braid child without embedding full parent histories in the child.

**Architecture:** Keep `LINEAGE-SPINE-001` unchanged. Add sibling `dogram/lineage_braid.py` with canonical parent-set objects, a narrow sum merge receipt, fixed-shape braid capsules, a separate braid ledger, and a three-state verifier that delegates each parent-line check to `verify_lineage(...)`. Freeze the exact `100 + 9 = 109` two-parent specimen and hostile controls.

**Tech Stack:** Python 3.12 stdlib, existing `dogram.lineage_spine`, unittest, existing Dogram CI.

**Spec:** `docs/superpowers/specs/2026-09-16-lineage-braid-001-design.md`

## Global Constraints

- Do not modify the `LINEAGE-SPINE-001` capsule schema or verifier contract.
- No new public Dogram operator or bootstrap-registry entry.
- Parent plurality lives in a content-addressed parent-set object; the braid child never recursively embeds parent histories.
- Parent enumeration order must not change parent-set identity.
- `incomplete` means missing witness material and must not be promoted to severance or invalidity.
- A referenced parent spine marked `invalid` makes the braid invalid; a referenced parent spine marked `incomplete` makes the braid incomplete.
- Content links remain integrity/address witnesses only: content link != causal link; merge receipt != authority.
- The frozen merge operator is integer `sum` only.

---

### Task 1: Canonical parent sets

**Files:**
- Create: `dogram/lineage_braid.py`
- Create: `tests/test_lineage_braid.py`

**Interfaces:**
- Consumes: `canonical_digest(...)` from `dogram.lineage_spine`.
- Produces: `make_parent_set(parents: list[dict[str, object]]) -> dict[str, object]`, `root_set_digest(parent_set: dict[str, object]) -> str`.

- [ ] **Step 1: Write failing tests** for canonical order, two-parent minimum, duplicate-head rejection, exact descriptor shape, and root-set deduplication.

Representative test:

```python
def test_parent_order_canonicalizes_to_same_digest():
    a = {"head_digest": "a", "root_digest": "r1", "carrier": 100}
    b = {"head_digest": "b", "root_digest": "r2", "carrier": 9}
    left = make_parent_set([a, b])
    right = make_parent_set([b, a])
    assert left == right
    assert canonical_digest(left) == canonical_digest(right)
```

- [ ] **Step 2: Run the focused test module and verify RED** because `dogram.lineage_braid` does not exist.
- [ ] **Step 3: Implement minimal parent-set constructors.** Use exact parent descriptor keys `{head_digest, root_digest, carrier}`, reject bool carriers, require two unique head digests, sort by `head_digest`, and compute the root-set digest over sorted unique root digests.
- [ ] **Step 4: Run focused tests and full Dogram CI checks to verify GREEN.**
- [ ] **Step 5: Commit.**

### Task 2: Merge receipts and bounded braid capsules

**Files:**
- Modify: `dogram/lineage_braid.py`
- Modify: `tests/test_lineage_braid.py`

**Interfaces:**
- Consumes: `make_parent_set(...)`, `root_set_digest(...)`.
- Produces: `make_sum_merge(parent_set: dict[str, object]) -> dict[str, object]`, `make_braid_capsule(parent_set: dict[str, object], merge_receipt: dict[str, object]) -> dict[str, object]`.

- [ ] **Step 1: Write failing tests** showing parent carriers `100` and `9` produce merge inputs `[100, 9]` in canonical parent order, output `109`, and a fixed-shape braid capsule containing only schema/specimen/carrier/carrier_origin/parent_set_digest/merge_receipt_digest/root_set_digest.
- [ ] **Step 2: Run focused tests and verify RED.**
- [ ] **Step 3: Implement the minimal sum-only merge receipt and capsule constructor.** Require merge `parent_set_digest` to match the supplied parent set and require merge output to be an integer.
- [ ] **Step 4: Run focused tests and full CI checks to verify GREEN.**
- [ ] **Step 5: Commit.**

### Task 3: Braid ledger and three-state verification

**Files:**
- Modify: `dogram/lineage_braid.py`
- Modify: `tests/test_lineage_braid.py`

**Interfaces:**
- Consumes: `verify_lineage(head_digest, spine_ledger)` from `dogram.lineage_spine`.
- Produces: `make_braid_ledger() -> dict[str, object]`, `store_parent_set(...) -> str`, `store_merge_receipt(...) -> str`, `store_braid_capsule(...) -> str`, `verify_braid(head_digest: str, braid_ledger: dict[str, object], spine_ledger: dict[str, object]) -> dict[str, object]`.

- [ ] **Step 1: Write failing tests** for a complete braid, a missing parent witness returning `incomplete`, a contradictory parent carrier returning `invalid`, an invalid parent spine propagating `invalid`, and a missing merge receipt returning `incomplete`.
- [ ] **Step 2: Run focused tests and verify RED.**
- [ ] **Step 3: Implement the ledger and verifier.** Verify content addresses, exact object shapes, parent-set membership, each parent descriptor against its referenced spine head, each referenced spine via `verify_lineage`, merge input/output consistency, child carrier equality with merge output, and root-set digest consistency.
- [ ] **Step 4: Run focused tests and full CI checks to verify GREEN.**
- [ ] **Step 5: Commit.**

### Task 4: Hostile boundedness controls

**Files:**
- Modify: `tests/test_lineage_braid.py`
- Modify: `dogram/lineage_braid.py` only if tests expose a hole.

**Interfaces:**
- Consumes: `verify_braid(...)`.
- Produces: enforced fixed-shape braid capsule and parent-set contracts.

- [ ] **Step 1: Add a RED hostile test** that re-hashes a braid capsule after adding an `ancestry` field and stores it under its new correct digest.
- [ ] **Step 2: Verify the test fails if the verifier accepts the polluted capsule.**
- [ ] **Step 3: Enforce exact braid capsule keys and exact parent-set/descriptor keys so the polluted capsule returns `invalid / capsule_shape_mismatch`.**
- [ ] **Step 4: Add a merge-tamper hostile test:** re-hash a merge receipt with wrong output `110`; verifier must return `invalid / merge_output_mismatch` rather than trusting the new digest.
- [ ] **Step 5: Run focused and full CI checks to verify GREEN, then commit.**

### Task 5: Freeze `100 + 9 = 109` and document the boundary

**Files:**
- Create: `tests/fixtures/lineage_braid_001.json`
- Create: `tests/test_lineage_braid_fixture.py`
- Create: `research/LINEAGE-BRAID-001.md`
- Modify: `README.md`

**Interfaces:**
- Frozen parent line A: `5 -> 100` under the TRIANGULATOR square/triangular crossing.
- Frozen parent line B: `3 -> 9` under the same crossing.
- Frozen braid child: `100 + 9 = 109`.

- [ ] **Step 1: Add the fixture test first and verify RED with the fixture absent.**
- [ ] **Step 2: Generate and add the exact frozen spine ledger + braid ledger + verification fixture, then verify GREEN.**
- [ ] **Step 3: Write `research/LINEAGE-BRAID-001.md` with exact math, data topology, three-state verification, hostile controls, and explicit refusals:** `CONVERGENCE != COLLAPSE`, `MULTIPLE PARENTS != ONE CAUSE`, `MULTIPLE PARENTS != MULTIPLE ROOTS`, `MISSING ONE PARENT WITNESS != PROVEN SEVERANCE`, `DERIVATION DAG != CAUSAL SUPPORT GRAPH`.
- [ ] **Step 4: Add a README pointer without changing the four public Dogram operators.**
- [ ] **Step 5: Run fresh final CI on the final head and review the complete PR diff before merge.**

## Candidate seals

> **A NEW THING MAY DESCEND FROM MANY LINES WITHOUT COLLAPSING THOSE LINES INTO ONE.**

> **THE CHILD STAYS SMALL; THE BRAID LIVES IN THE GRAPH.**

> **CONVERGENCE DOES NOT ERASE PLURALITY.**
