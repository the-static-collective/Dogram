# Dogram PRODUCTIVE-DESYNC / TRANSVERSE-GENERATORS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a zero-dependency internal Dogram research kernel that computes quotient-sheet reachability for bounded asymmetric generators and classifies a strong `PRODUCTIVE-DESYNC-001` witness without adding a public operator or collapsing potential closure into realized history.

**Architecture:** Add one pure finite-algebra module (`dogram/transverse.py`) and one small classifier (`dogram/productive_desync.py`). The transverse module computes synchronized phase sheets, a declared bounded history of `cut -> complete coherent orbit` cycles, and generated closure. The classifier consumes explicit preservation, typed execution-residual, cut-budget, and reachability facts. It does not depend on unmerged PR #33; a later reviewed adapter may bind actual `OMEGA-QUOTIENT` receipts to this interface.

**Tech Stack:** Python 3.12 standard library only; `dataclasses`, `math.gcd`, `math.lcm`, `collections.deque`, `json`, `pathlib`, `unittest`; existing Dogram constitutional checks.

**Spec:** `docs/superpowers/specs/2026-08-30-productive-desync-transverse-generators-design.md`

## Global Constraints

- Keep project dependencies exactly `[]`.
- Keep public `dogram.engine.OPERATORS` exactly `{("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)}`.
- Keep `build_bootstrap_registry().ids()` unchanged; this slice adds no intrinsic.
- Add no `transverse@1`, `desync@1`, `productive_desync@1`, `phase@1`, `meta@1`, or other public calculation operator.
- Preserve `PRESERVATION != DIFFERENCE != EXPANSION` as separate data.
- Preserve `ONE CROSSING != GENERATOR CLOSURE` with separate bounded-history and closure APIs.
- Preserve `POTENTIAL GENERATOR CLOSURE != ACTUAL EXECUTION HISTORY`; closure-only expansion can be `POTENTIAL`, never `WITNESS`.
- The bounded-history API is valid only for a declared specimen where each recorded cut is followed by a completed traversal of the synchronized orbit on the reached sheet. It must not be used to summarize arbitrary partial execution traces.
- Every productive-desync specimen must declare a finite `cut_budget`; `cuts_used > cut_budget` refuses.
- Reachability gain must never be labeled truth, evidence, authority, safety, quality, or desirability.
- Complementary generators do not establish federation-over-centralization without separate locality/non-transferability constraints.
- Coprime dimensions (`gcd(m,n) == 1`) produce one synchronized sheet and no reachability lift under this model.
- Invalid dimensions, generators, histories, counts, or budgets fail closed.
- Do not modify `dogram/omega.py`, proposal grammar, phase gate semantics, public registry, or Ω receipt schema in this slice.
- Do not depend on PR #33. The classifier accepts explicit `target_preserved` and `execution_residual` data so a later adapter can bind reviewed quotient receipts.

---

## File Structure

- Create `dogram/transverse.py` — finite cyclic quotient math, bounded cycle history, and generated closure.
- Create `dogram/productive_desync.py` — strong witness classifier with explicit budget and potential/history separation.
- Create `tests/test_transverse.py` — focused algebra tests, frozen-specimen verification, and independent brute-force closure checks.
- Create `tests/test_productive_desync.py` — preservation/difference/expansion hostile controls and budget tests.
- Create six frozen files under `tests/fixtures/transverse/`.
- Modify `README.md` only after executable verification is green.

---

### Task 1: Implement the Pure Transverse Quotient Kernel

**Files:**
- Create: `dogram/transverse.py`
- Create: `tests/test_transverse.py`

**Interfaces:**
- Produces: `TransverseInputError(reason_code: str, residual: str)`
- Produces: `TransverseAnalysis`
- Produces: `analyze_transverse(m: int, n: int, generators: tuple[int, ...]) -> TransverseAnalysis`
- Produces: `sheet_coordinate(m: int, n: int, a: int, b: int) -> int`
- Produces: `bounded_history_sheet_trace(m: int, n: int, cuts: tuple[int, ...]) -> tuple[int, ...]`
- Produces: `bounded_history_reach_count(m: int, n: int, cuts: tuple[int, ...]) -> int`

- [ ] **Step 1: Write the failing structural tests**

Create `tests/test_transverse.py`:

```python
import unittest

from dogram.transverse import (
    TransverseInputError,
    analyze_transverse,
    bounded_history_reach_count,
    bounded_history_sheet_trace,
    sheet_coordinate,
)


class TransverseTests(unittest.TestCase):
    def test_z6_x_z4_has_two_twelve_state_sync_sheets(self):
        result = analyze_transverse(6, 4, (1,))
        self.assertEqual(result.state_capacity, 24)
        self.assertEqual(result.sync_sheet_size, 12)
        self.assertEqual(result.sheet_count, 2)
        self.assertEqual(result.closure_lift_index, 2)
        self.assertEqual(result.closure_reach_count, 24)

    def test_sheet_coordinate_is_preserved_by_sync_motion(self):
        self.assertEqual(
            sheet_coordinate(8, 12, 3, 7),
            sheet_coordinate(8, 12, 4, 8),
        )

    def test_transverse_cut_changes_sheet_coordinate(self):
        self.assertNotEqual(
            sheet_coordinate(8, 12, 3, 7),
            sheet_coordinate(8, 12, 5, 7),
        )

    def test_invalid_dimension_refuses(self):
        with self.assertRaises(TransverseInputError) as caught:
            analyze_transverse(0, 4, (1,))
        self.assertEqual(caught.exception.reason_code, "INVALID_DIMENSION")

    def test_empty_generator_family_refuses(self):
        with self.assertRaises(TransverseInputError) as caught:
            analyze_transverse(6, 4, ())
        self.assertEqual(caught.exception.reason_code, "EMPTY_GENERATOR_FAMILY")
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: import failure because `dogram.transverse` does not exist.

- [ ] **Step 3: Implement the minimal algebra kernel**

Create `dogram/transverse.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm


@dataclass
class TransverseInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class TransverseAnalysis:
    m: int
    n: int
    generators: tuple[int, ...]
    state_capacity: int
    sync_sheet_size: int
    sheet_count: int
    closure_lift_index: int
    closure_reach_count: int
    closure_sheets: tuple[int, ...]

    def to_data(self) -> dict[str, object]:
        return {
            "m": self.m,
            "n": self.n,
            "generators": list(self.generators),
            "state_capacity": self.state_capacity,
            "sync_sheet_size": self.sync_sheet_size,
            "sheet_count": self.sheet_count,
            "closure_lift_index": self.closure_lift_index,
            "closure_reach_count": self.closure_reach_count,
            "closure_sheets": list(self.closure_sheets),
        }


def _validate_dimensions(m: int, n: int) -> None:
    for name, value in (("m", m), ("n", n)):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise TransverseInputError("INVALID_DIMENSION", f"{name} must be a positive integer")


def _validate_generators(generators: tuple[int, ...]) -> None:
    if not isinstance(generators, tuple) or not generators:
        raise TransverseInputError("EMPTY_GENERATOR_FAMILY", "generators must be a non-empty tuple")
    if any(not isinstance(r, int) or isinstance(r, bool) for r in generators):
        raise TransverseInputError("INVALID_GENERATOR", "every generator must be an integer")


def sheet_coordinate(m: int, n: int, a: int, b: int) -> int:
    _validate_dimensions(m, n)
    if any(not isinstance(x, int) or isinstance(x, bool) for x in (a, b)):
        raise TransverseInputError("INVALID_STATE", "state coordinates must be integers")
    return (a - b) % gcd(m, n)


def _generated_sheets(d: int, generators: tuple[int, ...]) -> tuple[int, ...]:
    seen = {0}
    frontier = [0]
    normalized = tuple(r % d for r in generators)
    while frontier:
        current = frontier.pop()
        for step in normalized:
            nxt = (current + step) % d
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return tuple(sorted(seen))


def analyze_transverse(m: int, n: int, generators: tuple[int, ...]) -> TransverseAnalysis:
    _validate_dimensions(m, n)
    _validate_generators(generators)
    d = gcd(m, n)
    sheet_size = lcm(m, n)
    lift = d // gcd(d, *generators)
    sheets = _generated_sheets(d, generators)
    if len(sheets) != lift:
        raise AssertionError("quotient traversal disagrees with gcd lift formula")
    return TransverseAnalysis(
        m=m,
        n=n,
        generators=generators,
        state_capacity=m * n,
        sync_sheet_size=sheet_size,
        sheet_count=d,
        closure_lift_index=lift,
        closure_reach_count=sheet_size * lift,
        closure_sheets=sheets,
    )


def bounded_history_sheet_trace(m: int, n: int, cuts: tuple[int, ...]) -> tuple[int, ...]:
    """Return sheets reached by declared cut->complete-sync-orbit cycles."""
    _validate_dimensions(m, n)
    if not isinstance(cuts, tuple):
        raise TransverseInputError("INVALID_CUT_HISTORY", "cuts must be a tuple")
    if any(not isinstance(r, int) or isinstance(r, bool) for r in cuts):
        raise TransverseInputError("INVALID_CUT_HISTORY", "every cut must be an integer")
    d = gcd(m, n)
    current = 0
    trace = [0]
    for cut in cuts:
        current = (current + cut) % d
        trace.append(current)
    return tuple(trace)


def bounded_history_reach_count(m: int, n: int, cuts: tuple[int, ...]) -> int:
    """Count states covered when every recorded sheet receives a full sync orbit."""
    trace = bounded_history_sheet_trace(m, n, cuts)
    return lcm(m, n) * len(set(trace))


__all__ = [
    "TransverseAnalysis",
    "TransverseInputError",
    "analyze_transverse",
    "bounded_history_reach_count",
    "bounded_history_sheet_trace",
    "sheet_coordinate",
]
```

- [ ] **Step 4: Add one-shot, repeated, inert, and coprime controls**

Append to `TransverseTests`:

```python
    def test_z6_x_z9_one_cut_is_36_while_closure_is_54(self):
        result = analyze_transverse(6, 9, (1,))
        self.assertEqual(result.sync_sheet_size, 18)
        self.assertEqual(result.sheet_count, 3)
        self.assertEqual(bounded_history_sheet_trace(6, 9, (1,)), (0, 1))
        self.assertEqual(bounded_history_reach_count(6, 9, (1,)), 36)
        self.assertEqual(result.closure_reach_count, 54)

    def test_second_bounded_cut_can_reach_third_sheet(self):
        self.assertEqual(bounded_history_sheet_trace(6, 9, (1, 1)), (0, 1, 2))
        self.assertEqual(bounded_history_reach_count(6, 9, (1, 1)), 54)

    def test_inert_cut_stays_on_same_sheet(self):
        result = analyze_transverse(8, 12, (4,))
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(bounded_history_sheet_trace(8, 12, (4,)), (0, 0))
        self.assertEqual(bounded_history_reach_count(8, 12, (4,)), 24)

    def test_coprime_dimensions_have_no_hidden_sheet(self):
        result = analyze_transverse(5, 7, (1,))
        self.assertEqual(result.sheet_count, 1)
        self.assertEqual(result.sync_sheet_size, 35)
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(result.closure_reach_count, 35)
```

- [ ] **Step 5: Run focused tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: all transverse tests pass.

- [ ] **Step 6: Commit the kernel**

```bash
git add dogram/transverse.py tests/test_transverse.py
git commit -m "feat: add transverse quotient reachability kernel"
```

---

### Task 2: Freeze the Six Research Specimens and Their Cut Budgets

**Files:**
- Create: `tests/fixtures/transverse/pd-001-a-two-sheet.json`
- Create: `tests/fixtures/transverse/pd-001-b-one-shot-vs-closure.json`
- Create: `tests/fixtures/transverse/tg-001-c-partial-lift.json`
- Create: `tests/fixtures/transverse/tg-001-d-complementary.json`
- Create: `tests/fixtures/transverse/tg-001-e-inert.json`
- Create: `tests/fixtures/transverse/tg-001-f-coprime.json`
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Each fixture declares `system`, `generators`, `cuts`, `cut_budget`, and exact expected analysis/history.
- Fixture schema remains test-local: `dogram.test.transverse-fixture/v0`.

- [ ] **Step 1: Add the failing fixture loader test**

Add to `tests/test_transverse.py`:

```python
import json
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "transverse"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())
```

Append:

```python
    def test_frozen_specimens_match_exact_history_closure_and_budget(self):
        names = sorted(path.name for path in FIXTURES.glob("*.json"))
        self.assertEqual(len(names), 6)
        for name in names:
            fixture = load_fixture(name)
            system = fixture["system"]
            cuts = tuple(fixture["cuts"])
            generators = tuple(fixture["generators"])
            self.assertLessEqual(len(cuts), fixture["cut_budget"], name)
            analysis = analyze_transverse(system["m"], system["n"], generators)
            self.assertEqual(analysis.to_data(), fixture["expected"]["analysis"], name)
            self.assertEqual(
                list(bounded_history_sheet_trace(system["m"], system["n"], cuts)),
                fixture["expected"]["bounded_history_sheet_trace"],
                name,
            )
            self.assertEqual(
                bounded_history_reach_count(system["m"], system["n"], cuts),
                fixture["expected"]["bounded_history_reach_count"],
                name,
            )
```

- [ ] **Step 2: Run the fixture test and verify RED**

Run:

```bash
python -m unittest tests.test_transverse.TransverseTests.test_frozen_specimens_match_exact_history_closure_and_budget -v
```

Expected: FAIL because the six fixture files do not exist.

- [ ] **Step 3: Create the six exact fixture files**

Create `pd-001-a-two-sheet.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"PD-001-A","system":{"m":6,"n":4},"generators":[1],"cuts":[1],"cut_budget":1,"expected":{"analysis":{"m":6,"n":4,"generators":[1],"state_capacity":24,"sync_sheet_size":12,"sheet_count":2,"closure_lift_index":2,"closure_reach_count":24,"closure_sheets":[0,1]},"bounded_history_sheet_trace":[0,1],"bounded_history_reach_count":24}}
```

Create `pd-001-b-one-shot-vs-closure.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"PD-001-B","system":{"m":6,"n":9},"generators":[1],"cuts":[1],"cut_budget":1,"expected":{"analysis":{"m":6,"n":9,"generators":[1],"state_capacity":54,"sync_sheet_size":18,"sheet_count":3,"closure_lift_index":3,"closure_reach_count":54,"closure_sheets":[0,1,2]},"bounded_history_sheet_trace":[0,1],"bounded_history_reach_count":36}}
```

Create `tg-001-c-partial-lift.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-C","system":{"m":8,"n":12},"generators":[2],"cuts":[2],"cut_budget":1,"expected":{"analysis":{"m":8,"n":12,"generators":[2],"state_capacity":96,"sync_sheet_size":24,"sheet_count":4,"closure_lift_index":2,"closure_reach_count":48,"closure_sheets":[0,2]},"bounded_history_sheet_trace":[0,2],"bounded_history_reach_count":48}}
```

Create `tg-001-d-complementary.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-D","system":{"m":12,"n":18},"generators":[2,3],"cuts":[2,3],"cut_budget":2,"expected":{"analysis":{"m":12,"n":18,"generators":[2,3],"state_capacity":216,"sync_sheet_size":36,"sheet_count":6,"closure_lift_index":6,"closure_reach_count":216,"closure_sheets":[0,1,2,3,4,5]},"bounded_history_sheet_trace":[0,2,5],"bounded_history_reach_count":108}}
```

Create `tg-001-e-inert.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-E","system":{"m":8,"n":12},"generators":[4],"cuts":[4],"cut_budget":1,"expected":{"analysis":{"m":8,"n":12,"generators":[4],"state_capacity":96,"sync_sheet_size":24,"sheet_count":4,"closure_lift_index":1,"closure_reach_count":24,"closure_sheets":[0]},"bounded_history_sheet_trace":[0,0],"bounded_history_reach_count":24}}
```

Create `tg-001-f-coprime.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-F","system":{"m":5,"n":7},"generators":[1],"cuts":[1],"cut_budget":1,"expected":{"analysis":{"m":5,"n":7,"generators":[1],"state_capacity":35,"sync_sheet_size":35,"sheet_count":1,"closure_lift_index":1,"closure_reach_count":35,"closure_sheets":[0]},"bounded_history_sheet_trace":[0,0],"bounded_history_reach_count":35}}
```

- [ ] **Step 4: Add the complementary-generator control**

Append:

```python
    def test_complementary_generators_span_more_than_either_alone(self):
        left = analyze_transverse(12, 18, (2,))
        right = analyze_transverse(12, 18, (3,))
        together = analyze_transverse(12, 18, (2, 3))
        self.assertEqual(left.closure_reach_count, 108)
        self.assertEqual(right.closure_reach_count, 72)
        self.assertEqual(together.closure_reach_count, 216)
        self.assertLess(left.closure_reach_count, together.closure_reach_count)
        self.assertLess(right.closure_reach_count, together.closure_reach_count)
```

- [ ] **Step 5: Run transverse tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: all tests pass and all six frozen specimens match exactly.

- [ ] **Step 6: Commit the fixtures**

```bash
git add tests/fixtures/transverse tests/test_transverse.py
git commit -m "test: freeze transverse generator specimens"
```

---

### Task 3: Implement the Strong PRODUCTIVE-DESYNC Classifier

**Files:**
- Create: `dogram/productive_desync.py`
- Create: `tests/test_productive_desync.py`

**Interfaces:**
- Consumes explicit facts; no hidden Ω dependency.
- `execution_residual` is an inert non-empty dictionary supplied by the caller; this slice does not interpret it.
- Produces: `ProductiveDesyncAssessment`.
- Statuses: `WITNESS`, `POTENTIAL`, `REFUSE`.
- `WITNESS` requires historical expansion inside budget.
- `POTENTIAL` means generated closure expands but bounded history has not demonstrated expansion.

- [ ] **Step 1: Write failing classifier tests**

Create `tests/test_productive_desync.py`:

```python
import unittest

from dogram.productive_desync import assess_productive_desync


class ProductiveDesyncTests(unittest.TestCase):
    def assess(self, **overrides):
        values = {
            "target_preserved": True,
            "execution_residual": {"step_trace": {"changed": True}},
            "baseline_reach_count": 18,
            "historical_reach_count": 36,
            "closure_reach_count": 54,
            "cut_declared": True,
            "cut_budget": 1,
            "cuts_used": 1,
            "returned_to_coherence": True,
        }
        values.update(overrides)
        return assess_productive_desync(**values)

    def test_historical_expansion_inside_budget_is_witness(self):
        result = self.assess()
        self.assertEqual((result.status, result.reason_code), ("WITNESS", None))
        self.assertTrue(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_closure_only_expansion_is_potential(self):
        result = self.assess(historical_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("POTENTIAL", "CLOSURE_ONLY"))
        self.assertFalse(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_target_failure_refuses_even_when_reach_expands(self):
        result = self.assess(target_preserved=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "TARGET_NOT_PRESERVED"))

    def test_missing_execution_residual_refuses(self):
        result = self.assess(execution_residual={})
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_EXECUTION_RESIDUAL"))

    def test_untyped_cut_refuses(self):
        result = self.assess(cut_declared=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "UNTYPED_CUT"))

    def test_budget_exceeded_refuses(self):
        result = self.assess(cut_budget=1, cuts_used=2)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "CUT_BUDGET_EXCEEDED"))

    def test_no_coherence_return_refuses_bounded_desync_label(self):
        result = self.assess(returned_to_coherence=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_COHERENCE_RETURN"))

    def test_no_reachability_gain_refuses(self):
        result = self.assess(historical_reach_count=18, closure_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_REACHABILITY_EXPANSION"))
```

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
python -m unittest tests.test_productive_desync -v
```

Expected: import failure because `dogram.productive_desync` does not exist.

- [ ] **Step 3: Implement the minimal classifier**

Create `dogram/productive_desync.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProductiveDesyncAssessment:
    status: str
    reason_code: str | None
    target_preserved: bool
    execution_residual: dict[str, Any]
    baseline_reach_count: int
    historical_reach_count: int
    closure_reach_count: int
    historical_expanded: bool
    closure_expanded: bool
    cut_declared: bool
    cut_budget: int
    cuts_used: int
    returned_to_coherence: bool

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "target_preserved": self.target_preserved,
            "execution_residual": self.execution_residual,
            "baseline_reach_count": self.baseline_reach_count,
            "historical_reach_count": self.historical_reach_count,
            "closure_reach_count": self.closure_reach_count,
            "historical_expanded": self.historical_expanded,
            "closure_expanded": self.closure_expanded,
            "cut_declared": self.cut_declared,
            "cut_budget": self.cut_budget,
            "cuts_used": self.cuts_used,
            "returned_to_coherence": self.returned_to_coherence,
        }


def _is_count(value: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def assess_productive_desync(
    *,
    target_preserved: bool,
    execution_residual: dict[str, Any],
    baseline_reach_count: int,
    historical_reach_count: int,
    closure_reach_count: int,
    cut_declared: bool,
    cut_budget: int,
    cuts_used: int,
    returned_to_coherence: bool,
) -> ProductiveDesyncAssessment:
    if not isinstance(target_preserved, bool):
        raise ValueError("target_preserved must be boolean")
    if not isinstance(execution_residual, dict):
        raise ValueError("execution_residual must be an inert dictionary")
    if not isinstance(cut_declared, bool) or not isinstance(returned_to_coherence, bool):
        raise ValueError("cut/coherence flags must be booleans")
    for value in (baseline_reach_count, historical_reach_count, closure_reach_count, cut_budget, cuts_used):
        if not _is_count(value):
            raise ValueError("reach counts and cut counts must be non-negative integers")
    if historical_reach_count > closure_reach_count:
        raise ValueError("historical reach cannot exceed declared closure reach")

    historical_expanded = historical_reach_count > baseline_reach_count
    closure_expanded = closure_reach_count > baseline_reach_count

    if cuts_used > cut_budget:
        status, reason_code = "REFUSE", "CUT_BUDGET_EXCEEDED"
    elif not cut_declared:
        status, reason_code = "REFUSE", "UNTYPED_CUT"
    elif not returned_to_coherence:
        status, reason_code = "REFUSE", "NO_COHERENCE_RETURN"
    elif not target_preserved:
        status, reason_code = "REFUSE", "TARGET_NOT_PRESERVED"
    elif not execution_residual:
        status, reason_code = "REFUSE", "NO_EXECUTION_RESIDUAL"
    elif historical_expanded:
        status, reason_code = "WITNESS", None
    elif closure_expanded:
        status, reason_code = "POTENTIAL", "CLOSURE_ONLY"
    else:
        status, reason_code = "REFUSE", "NO_REACHABILITY_EXPANSION"

    return ProductiveDesyncAssessment(
        status=status,
        reason_code=reason_code,
        target_preserved=target_preserved,
        execution_residual=execution_residual,
        baseline_reach_count=baseline_reach_count,
        historical_reach_count=historical_reach_count,
        closure_reach_count=closure_reach_count,
        historical_expanded=historical_expanded,
        closure_expanded=closure_expanded,
        cut_declared=cut_declared,
        cut_budget=cut_budget,
        cuts_used=cuts_used,
        returned_to_coherence=returned_to_coherence,
    )


__all__ = ["ProductiveDesyncAssessment", "assess_productive_desync"]
```

- [ ] **Step 4: Add malformed-input controls**

Append:

```python
    def test_history_cannot_exceed_declared_closure(self):
        with self.assertRaises(ValueError):
            self.assess(historical_reach_count=55, closure_reach_count=54)

    def test_negative_cut_budget_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(cut_budget=-1)

    def test_non_dictionary_residual_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(execution_residual=True)
```

- [ ] **Step 5: Run classifier tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_productive_desync -v
```

Expected: all classifier tests pass.

- [ ] **Step 6: Commit the classifier**

```bash
git add dogram/productive_desync.py tests/test_productive_desync.py
git commit -m "feat: classify bounded productive desync witnesses"
```

---

### Task 4: Verify the Lift Formula Against an Independent Brute-Force Oracle

**Files:**
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Test-only oracle enumerates actual finite states using transition traversal, not the gcd formula.
- Verifies exactly 405 single-generator cases: `m=2..10`, `n=2..10`, `r=1..5`.

- [ ] **Step 1: Add the independent state traversal helper**

Add:

```python
from collections import deque


def brute_reach_count(m, n, generators):
    start = (0, 0)
    queue = deque([start])
    seen = {start}
    moves = ((1, 1),) + tuple((r, 0) for r in generators)
    while queue:
        a, b = queue.popleft()
        for da, db in moves:
            nxt = ((a + da) % m, (b + db) % n)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen)
```

- [ ] **Step 2: Add the 405-case formula test**

Append:

```python
    def test_single_generator_lift_formula_matches_405_bruteforce_cases(self):
        checked = 0
        for m in range(2, 11):
            for n in range(2, 11):
                for r in range(1, 6):
                    analysis = analyze_transverse(m, n, (r,))
                    self.assertEqual(
                        analysis.closure_reach_count,
                        brute_reach_count(m, n, (r,)),
                        (m, n, r),
                    )
                    checked += 1
        self.assertEqual(checked, 405)
```

- [ ] **Step 3: Add the complementary multi-generator oracle control**

Append:

```python
    def test_complementary_generators_match_bruteforce_closure(self):
        analysis = analyze_transverse(12, 18, (2, 3))
        self.assertEqual(analysis.closure_reach_count, 216)
        self.assertEqual(analysis.closure_reach_count, brute_reach_count(12, 18, (2, 3)))
```

- [ ] **Step 4: Run transverse tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: all tests pass and exactly 405 single-generator combinations match the independent oracle.

- [ ] **Step 5: Commit the law verification**

```bash
git add tests/test_transverse.py
git commit -m "test: verify transverse lift law by brute force"
```

---

### Task 5: Preserve the Public Constitution and Document the Internal Kernel

**Files:**
- Modify: `README.md`

**Interfaces:**
- No public operator or intrinsic changes.
- No Ω schema changes.
- README reports only the existence and boundaries of the internal research kernel.

- [ ] **Step 1: Run full tests before documentation**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 2: Run compile verification**

Run:

```bash
python -m compileall -q dogram tests
```

Expected: exit code 0.

- [ ] **Step 3: Run the exact constitutional floor**

Run:

```bash
python - <<'PY'
import pathlib
import tomllib
from dogram.engine import OPERATORS
from dogram.registry import build_bootstrap_registry

pyproject = tomllib.loads(pathlib.Path("pyproject.toml").read_text())
assert pyproject["project"]["dependencies"] == []
assert set(OPERATORS) == {
    ("delta", 1),
    ("rectangle", 1),
    ("ablate", 1),
    ("reach", 1),
}
assert set(build_bootstrap_registry().ids()) == {
    "core.get@1",
    "core.same@1",
    "core.add@1",
    "core.sub@1",
    "core.length@1",
    "core.gt@1",
    "core.select_first@1",
    "trace.compare_ordered@1",
    "graph.apply_mutation@1",
    "graph.reachable_pairs@1",
    "graph.query_paths@1",
    "set.difference@1",
}
print("constitutional floor OK")
PY
```

Expected: `constitutional floor OK`.

- [ ] **Step 4: Add one factual README paragraph after the Ω implementation status**

```markdown
Dogram also contains an internal finite research kernel for `PRODUCTIVE-DESYNC-001 / TRANSVERSE-GENERATORS-001`. It receipts synchronized quotient sheets, declared bounded cut history, and generated reachability closure while preserving `ONE CROSSING != GENERATOR CLOSURE` and `POTENTIAL REACHABILITY != ACTUAL HISTORY`. This kernel adds no public operator, truth/evidence semantics, or automatic experiment selection.
```

- [ ] **Step 5: Re-run full tests and compile after the README edit**

Run:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Expected: all tests pass and compile exits 0.

- [ ] **Step 6: Run the scope scan**

Run:

```bash
python - <<'PY'
from pathlib import Path

forbidden = ("transverse@1", "desync@1", "productive_desync@1", "phase@1", "meta@1")
for path in (Path("dogram/engine.py"), Path("dogram/registry.py")):
    text = path.read_text()
    for token in forbidden:
        assert token not in text, (path, token)
print("transverse scope scan OK")
PY
```

Expected: `transverse scope scan OK`.

- [ ] **Step 7: Commit documentation**

```bash
git add README.md
git commit -m "docs: record transverse reachability research kernel"
```

---

## Final Verification Gate

Before opening or updating the implementation PR, run on the exact implementation head:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
python - <<'PY'
import pathlib
import tomllib
from dogram.engine import OPERATORS
from dogram.registry import build_bootstrap_registry
from dogram.transverse import analyze_transverse, bounded_history_reach_count
from dogram.productive_desync import assess_productive_desync

pyproject = tomllib.loads(pathlib.Path("pyproject.toml").read_text())
assert pyproject["project"]["dependencies"] == []
assert set(OPERATORS) == {
    ("delta", 1),
    ("rectangle", 1),
    ("ablate", 1),
    ("reach", 1),
}
assert set(build_bootstrap_registry().ids()) == {
    "core.get@1",
    "core.same@1",
    "core.add@1",
    "core.sub@1",
    "core.length@1",
    "core.gt@1",
    "core.select_first@1",
    "trace.compare_ordered@1",
    "graph.apply_mutation@1",
    "graph.reachable_pairs@1",
    "graph.query_paths@1",
    "set.difference@1",
}

case = analyze_transverse(6, 9, (1,))
assert case.sync_sheet_size == 18
assert bounded_history_reach_count(6, 9, (1,)) == 36
assert case.closure_reach_count == 54

assessment = assess_productive_desync(
    target_preserved=True,
    execution_residual={"step_trace": {"changed": True}},
    baseline_reach_count=18,
    historical_reach_count=36,
    closure_reach_count=54,
    cut_declared=True,
    cut_budget=1,
    cuts_used=1,
    returned_to_coherence=True,
)
assert (assessment.status, assessment.reason_code) == ("WITNESS", None)

coprime = analyze_transverse(5, 7, (1,))
assert coprime.sheet_count == 1
assert coprime.closure_reach_count == 35

print("PRODUCTIVE-DESYNC / TRANSVERSE-GENERATORS verification OK")
PY
```

Expected final line:

```text
PRODUCTIVE-DESYNC / TRANSVERSE-GENERATORS verification OK
```

The implementation PR must report the exact head SHA used for verification. It must not claim `OMEGA-QUOTIENT` integration until a separate reviewed adapter binds actual quotient receipts to `target_preserved` and `execution_residual`.
