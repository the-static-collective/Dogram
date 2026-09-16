# LINEAGE-SPINE-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve reconstructible multi-generation derivation ancestry without recursively embedding the entire past in every child receipt.

**Architecture:** Add a stdlib-only content-addressed lineage layer beside `triangulator.py`. Each lineage capsule is constant-shape and stores only its generation, carrier, root digest, parent capsule digest, and the digest of the local crossing receipt that produced it. A separate ledger stores capsules and crossing receipts by digest; verification walks links and distinguishes `complete`, `incomplete`, and `invalid`, because a missing receipt is not proof that the underlying line was severed.

**Tech Stack:** Python 3.12 stdlib (`dataclasses`, `hashlib`, `json`), unittest, existing Dogram CI.

**Spec:** `research/LINEAGE-SPINE-001.md`

## Global Constraints

- No new public Dogram operator or bootstrap-registry entry.
- `receipt != road`; missing witness material must not be labeled a proven severance.
- Canonical digests are content addresses / integrity witnesses only; digest equality does not mint causal, semantic, historical, or evidentiary authority.
- Local capsule shape must stay bounded across generations; cumulative history may grow only in the external ledger.
- Preserve deterministic, offline, dependency-free Dogram behavior.

---

### Task 1: Content-addressed lineage capsules

**Files:**
- Create: `dogram/lineage_spine.py`
- Create: `tests/test_lineage_spine.py`

**Interfaces:**
- Produces: `canonical_digest(value) -> str`, `make_root(carrier, source_receipt) -> dict`, `append_from_crossing(parent_capsule, crossing_receipt) -> dict`.

- [ ] **Step 1: Write failing tests** for deterministic digesting, a generation-0 root, a generation-1 child, and a generation-2 child whose capsule has the same key shape as generation 1.
- [ ] **Step 2: Run CI / unit tests and verify RED** because `dogram.lineage_spine` does not exist.
- [ ] **Step 3: Implement minimal canonical JSON + SHA-256 digesting and bounded capsule constructors.**
- [ ] **Step 4: Verify GREEN** for unit tests, compile, constitutional floor, and scope scan.
- [ ] **Step 5: Commit.**

### Task 2: Ledger reconstruction and three-state verification

**Files:**
- Modify: `dogram/lineage_spine.py`
- Modify: `tests/test_lineage_spine.py`

**Interfaces:**
- Produces: `store_capsule(ledger, capsule) -> str`, `store_receipt(ledger, receipt) -> str`, `verify_lineage(head_digest, ledger) -> dict`.

- [ ] **Step 1: Write failing tests** for a complete 3-generation line, an intentionally missing parent/receipt yielding `incomplete`, and a tampered digest/generation yielding `invalid`.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Implement the minimal ledger + verifier.** The verifier follows parent digests to root, checks content digests, generation decrement, stable root digest, carrier equality with the local crossing delta, and local crossing receipt presence.
- [ ] **Step 4: Verify GREEN.**
- [ ] **Step 5: Commit.**

### Task 3: Freeze the hostile specimen and document the law

**Files:**
- Create: `tests/fixtures/lineage_spine_001.json`
- Create: `tests/test_lineage_spine_fixture.py`
- Create: `research/LINEAGE-SPINE-001.md`
- Modify: `README.md`

**Interfaces:**
- Frozen descent: `C0=5 -> Δ0=100 -> C1=100 -> Δ1=24,502,500 -> C2=24,502,500` using the same square/triangular ordered crossing identity.

- [ ] **Step 1: Add fixture test first and verify RED** with the fixture absent.
- [ ] **Step 2: Add the frozen ledger/capsule fixture and verify GREEN.**
- [ ] **Step 3: Document exact math, bounded-size property, content-address boundary, and explicit refusals.**
- [ ] **Step 4: Add README pointer.**
- [ ] **Step 5: Run full final CI and review the complete diff before merge.**

## Candidate seals

> **CONTINUITY NEEDS A LINE; THE CHILD ONLY NEEDS THE LINK.**

> **KEEP THE PAST ADDRESSABLE, NOT RECURSIVELY EMBEDDED.**

> **MISSING RECEIPT != PROVEN SEVERANCE.**
