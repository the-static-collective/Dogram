# Dogram Bounded Branching + Bootstrap Peel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend Dogram Ω from one admitted successor to bounded explicit candidate branching, then prove the first lawful bootstrap shrink by replacing one host intrinsic with an equivalent mathal implementation.

**Architecture:** Branching is explicit data, never hidden nondeterminism. META may return a `BranchProposal` whose candidates are canonical replacement programs. The caller selects a declared deterministic policy (`CANONICAL_FIRST`, `EXPLICIT_PRIORITY`, or `RETURN_ALL_BOUNDED`). Bootstrap peeling is a separate proof procedure: host and candidate implementations run across the same frozen corpus, an independent parity harness compares them under a named lens, transitive intrinsic dependencies are checked, the target intrinsic is ablated, and the corpus is rerun without it.

**Tech Stack:** Python >= 3.12, standard library only.

**Spec:** `docs/superpowers/specs/2026-08-28-dogram-metaoscillatory-runtime-design.md`

## Global Constraints

- The Ω membrane + META plan must be green first.
- Branch width and all execution/meta fuel remain finite and deterministic.
- Branch identity includes explicit parent program/receipt digest and candidate program digest.
- No host iteration order may decide a branch.
- Peel proof uses independent Python structural comparison first; Dogram self-comparison is supplemental only.
- A candidate replacement may not invoke the intrinsic being peeled directly or transitively.
- Peeling never expands external dependencies or capabilities.
- `same behavior under corpus != universal equivalence`; every peel receipt names its lens and corpus digest.

---

## File Structure

```text
Dogram/
  dogram/
    branching.py
    dependencies.py
    peel.py
    proposal.py
    omega.py
    stdlib/bootstrap/
      select-first.mathal.json
  tests/
    test_branching.py
    test_branching_replay.py
    test_dependencies.py
    test_peel.py
    test_peel_hostile.py
```

---

### Task 1: Add typed BranchProposal and deterministic branch identities

**Files:**
- Modify: `dogram/proposal.py`
- Create: `dogram/branching.py`
- Create: `tests/test_branching.py`

**Interfaces:**
- Add proposal kind `BranchProposal`.
- Candidate shape: `{candidate_id, replacement_program, priority}`.
- Produce `branch_identity(parent_program_digest: str, parent_receipt_digest: str, candidate_program_digest: str) -> str` using canonical SHA-256 data.

- [ ] **Step 1: Write RED candidate identity test**

```python
class BranchingTests(unittest.TestCase):
    def test_identity_is_content_addressed(self):
        a = branch_identity("sha256:p", "sha256:r", "sha256:c")
        b = branch_identity("sha256:p", "sha256:r", "sha256:c")
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("sha256:"))
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_branching -v
```

- [ ] **Step 3: Implement BranchProposal decoding**

Require one or more candidates, unique candidate IDs, canonical replacement programs, integer priority when present, and exact schema `dogram.proposal/v0`.

- [ ] **Step 4: Add duplicate-candidate refusal test and run GREEN**

```bash
python -m unittest tests.test_branching -v
```

- [ ] **Step 5: Commit**

```bash
git add dogram/proposal.py dogram/branching.py tests/test_branching.py
git commit -m "feat: add explicit Dogram branch proposals"
```

---

### Task 2: Implement bounded branch policies without hidden nondeterminism

**Files:**
- Modify: `dogram/branching.py`
- Modify: `dogram/omega.py`
- Create: `tests/test_branching_replay.py`

**Interfaces:**
- Produce `BranchPolicy` values exactly `CANONICAL_FIRST`, `EXPLICIT_PRIORITY`, `RETURN_ALL_BOUNDED`.
- Produce `resolve_branch_proposal(proposal, parent_digests, registry, gate_limits, branch_policy, max_branch_width) -> list[GateDecision]`.

- [ ] **Step 1: Write RED canonical-first ordering test**

Construct two valid candidates in reverse input order and assert `CANONICAL_FIRST` chooses the lexicographically smallest candidate program digest, not list position.

- [ ] **Step 2: Write RED explicit-priority test**

Lowest integer priority wins; ties break by canonical candidate digest.

- [ ] **Step 3: Write RED width-bound test**

A proposal with `len(candidates) > max_branch_width` returns `REFUSE / BRANCH_WIDTH_EXCEEDED`; v0 does not truncate.

- [ ] **Step 4: Implement policy resolution by passing every selected candidate through the existing phase gate**

No candidate bypasses ordinary ProgramPatch validation.

- [ ] **Step 5: Run deterministic replay proof**

```bash
python -m unittest tests.test_branching tests.test_branching_replay -v
```

Identical parent/proposal/configuration must return branch decisions in byte-identical order.

- [ ] **Step 6: Commit**

```bash
git add dogram/branching.py dogram/omega.py tests/test_branching_replay.py
git commit -m "feat: resolve bounded Dogram branches deterministically"
```

---

### Task 3: Add static transitive dependency inspection for mathal programs

**Files:**
- Create: `dogram/dependencies.py`
- Create: `tests/test_dependencies.py`

**Interfaces:**
- Produce `program_dependencies(program: Program, registry: Registry) -> DependencyReport`.
- Report exact `intrinsic_ids`, `program_ids`, and `cycles`.

- [ ] **Step 1: Write RED direct/transitive dependency test**

A program `candidate/select-first` calling `helper/nonempty` which uses `core.length@1` and `core.gt@1` must report both intrinsics transitively.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_dependencies -v
```

- [ ] **Step 3: Implement static dependency walk**

Inspect admitted program definitions only; do not execute programs to discover dependencies. Track visited `(program_id, version)` pairs and report a cycle rather than recursing indefinitely.

- [ ] **Step 4: Add self-smuggle test**

A candidate replacement whose transitive dependency set includes the target intrinsic is marked non-peelable.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_dependencies -v
git add dogram/dependencies.py tests/test_dependencies.py
git commit -m "feat: inspect Dogram program dependencies"
```

---

### Task 4: Express `core.select_first@1` as a mathal candidate

**Files:**
- Create: `dogram/stdlib/bootstrap/select-first.mathal.json`
- Create: `tests/test_peel.py`

**Interfaces:**
- Candidate program id `bootstrap/select-first`, version `1`.
- Candidate may use `core.length@1`, `core.gt@1`, `core.get@1`, and generic conditional selection, but may not call `core.select_first@1`.

- [ ] **Step 1: Write RED parity tests**

Corpus:

```text
["a"]       -> "a"
["a","b"] -> "a"
[]          -> REFUSE / EMPTY_SEQUENCE
```

Run each specimen once through host `core.select_first@1` and once through the candidate mathal. Compare success result or refusal reason family independently in Python.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_peel.PeelCandidateTests -v
```

- [ ] **Step 3: Implement the candidate using smaller admitted operations**

The mathal computes `length > 0`; on true, returns `core.get@1(sequence, [0])`; on false, follows an existing generic refusal-producing path with reason `EMPTY_SEQUENCE`. If the VM lacks a generic typed refusal expression, add one general `core.require@1(condition, reason_code)` intrinsic and test it independently; do not add a select-first-specific helper.

- [ ] **Step 4: Run candidate parity tests GREEN**

```bash
python -m unittest tests.test_peel.PeelCandidateTests -v
```

- [ ] **Step 5: Commit**

```bash
git add dogram/stdlib/bootstrap/select-first.mathal.json dogram/intrinsics tests/test_peel.py
git commit -m "feat: express select-first as a Dogram mathal"
```

---

### Task 5: Implement the formal PeelProposal proof and ablated-kernel rerun

**Files:**
- Create: `dogram/peel.py`
- Modify: `dogram/proposal.py`
- Extend: `tests/test_peel.py`
- Create: `tests/test_peel_hostile.py`

**Interfaces:**
- Add proposal kind `PeelProposal`.
- Produce `evaluate_peel(target_intrinsic_id, candidate_program, corpus, equivalence_lens, registry, vm_config) -> PeelProof`.
- `PeelProof.to_data()` includes target/version, candidate id/version/digest, corpus digest, lens, oracle/candidate receipt digests, dependency report, ablation result, and residual failures.

- [ ] **Step 1: Write RED successful peel proof test**

Expected assertions:

```python
proof = evaluate_peel(...)
self.assertEqual(proof.status, "EARNED")
self.assertNotIn("core.select_first@1", proof.candidate_dependencies.intrinsic_ids)
self.assertEqual(proof.residual_failures, [])
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_peel -v
```

- [ ] **Step 3: Implement proof sequence exactly**

```text
freeze + digest corpus
run host target over corpus
run candidate over same corpus
compare under named lens using Python structural checks
inspect transitive candidate dependencies
construct registry with target intrinsic removed
rerun candidate corpus against ablated registry
emit PeelProof
```

The host target remains present only for the first oracle run; the ablated rerun must not retain it.

- [ ] **Step 4: Add hostile peel tests**

Cover:

```text
PEEL-SELF-SMUGGLE-001     -> NOT_EARNED
PEEL-BEHAVIOR-DRIFT-001   -> NOT_EARNED
candidate adds dependency -> NOT_EARNED
ablated rerun fails       -> NOT_EARNED
```

- [ ] **Step 5: Run GREEN**

```bash
python -m unittest tests.test_peel tests.test_peel_hostile -v
```

- [ ] **Step 6: Commit**

```bash
git add dogram/peel.py dogram/proposal.py tests/test_peel.py tests/test_peel_hostile.py
git commit -m "feat: prove first Dogram bootstrap peel"
```

---

### Task 6: Verify first reduced kernel and Ω graduation witness

**Files:**
- Modify only if verification exposes a defect.

**Interfaces:**
- Final proof only.

- [ ] **Step 1: Build the reduced registry without `core.select_first@1`**

Run the full stdlib corpus with the candidate mathal registered wherever select-first behavior is required.

- [ ] **Step 2: Run full suite**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

- [ ] **Step 3: Assert reduced bootstrap floor**

```python
registry = build_reduced_registry_without("core.select_first@1")
assert "core.select_first@1" not in set(registry.ids())
```

Then run all public stdlib conformance tests against that registry.

- [ ] **Step 4: Produce a canonical graduation receipt**

The receipt must cite the peel proof digest, reduced registry digest, complete corpus digest, exact equivalence lens, and final full-suite result. It may claim only:

```text
DOGRAM Ω METAOSCILLATORY RUNTIME — FIRST PROOF OF LIFE
```

when every graduation criterion in the architecture spec is independently satisfied.

---

## Plan Self-Review

- **Spec coverage:** typed branching, all three deterministic branch policies, branch bound refusal, transitive dependency inspection, candidate replacement, independent parity, intrinsic ablation, hostile peel cases, and reduced-kernel rerun are each assigned.
- **Placeholder scan:** no TODO/TBD placeholders remain.
- **Type consistency:** `BranchProposal`, `BranchPolicy`, `DependencyReport`, `PeelProposal`, and `PeelProof` are used consistently.
- **Circularity check:** peel equivalence is established independently before Dogram may produce any self-referential delta receipt.
- **Scope control:** unrestricted graph rewriting and metacircular interpreter implementation remain outside Ω graduation.
