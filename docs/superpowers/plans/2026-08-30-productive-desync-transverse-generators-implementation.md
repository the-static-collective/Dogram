# Dogram PRODUCTIVE-DESYNC / TRANSVERSE-GENERATORS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a zero-dependency internal Dogram research kernel that computes quotient-sheet reachability for bounded asymmetric generators and classifies a strong `PRODUCTIVE-DESYNC-001` witness without adding a public operator or silently equating potential reachability with actual execution history.

**Architecture:** Add one pure finite-algebra module (`dogram/transverse.py`) and one small classification module (`dogram/productive_desync.py`). The transverse module computes synchronized sheet structure, exact bounded history, and generated closure independently of Ω; the classifier consumes already-declared preservation/difference facts plus historical and closure reach counts. This plan deliberately does not depend on unmerged PR #33 (`EXECUTION-CUT / OMEGA-QUOTIENT`); a future adapter may bind its receipts to this classifier without changing the math kernel.

**Tech Stack:** Python 3.12 standard library only; `dataclasses`, `math.gcd`, `math.lcm`, `collections.deque`, `json`, `pathlib`, `unittest`; existing Dogram canonical/runtime constitution.

**Spec:** `docs/superpowers/specs/2026-08-30-productive-desync-transverse-generators-design.md`

## Global Constraints

- Keep project dependencies exactly `[]`.
- Keep public `dogram.engine.OPERATORS` exactly `{("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)}`.
- Keep `build_bootstrap_registry().ids()` unchanged; this slice adds no intrinsic.
- Add no `transverse@1`, `desync@1`, `phase@1`, `meta@1`, or other public calculation operator.
- `PRESERVATION != DIFFERENCE != EXPANSION` must remain explicit in data and tests.
- `ONE CROSSING != GENERATOR CLOSURE` must be enforced by separate history and closure APIs.
- `POTENTIAL GENERATOR CLOSURE != ACTUAL EXECUTION HISTORY` must be represented in result types, not only prose.
- Reachability gain must never be labeled truth, evidence, authority, safety, quality, or desirability.
- A complementary-generator result must not claim federation is stronger than centralized union without separate locality/non-transferability constraints.
- Coprime dimensions (`gcd(m,n) == 1`) must produce one synchronized sheet and no reachability lift under this model.
- Invalid dimensions, cuts, or malformed fixture data must fail closed with explicit reason codes.
- Do not modify `dogram/omega.py`, proposal grammar, phase gate semantics, public registry, or existing Ω receipt schema in this slice.
- Do not depend on PR #33. `PRODUCTIVE-DESYNC-001` receives `target_preserved` and `execution_changed` as explicit facts so a later reviewed adapter can bind them to quotient receipts.

---

## File Structure

- Create `dogram/transverse.py` — pure finite cyclic quotient math, history tracking, generated closure, and inert report data.
- Create `dogram/productive_desync.py` — strong witness classifier that keeps historical expansion separate from closure-only potential.
- Create `tests/test_transverse.py` — focused algebra tests plus independent brute-force closure checks.
- Create `tests/test_productive_desync.py` — preservation/difference/expansion non-collapse and hostile controls.
- Create `tests/fixtures/transverse/pd-001-a-two-sheet.json` — `Z6 x Z4`, full two-sheet one-cut specimen.
- Create `tests/fixtures/transverse/pd-001-b-one-shot-vs-closure.json` — `Z6 x Z9`, one-shot/closure separation.
- Create `tests/fixtures/transverse/tg-001-c-partial-lift.json` — `Z8 x Z12`, `r=2`, partial lift.
- Create `tests/fixtures/transverse/tg-001-d-complementary.json` — `Z12 x Z18`, `r=2,3`, complementary full closure.
- Create `tests/fixtures/transverse/tg-001-e-inert.json` — non-transverse increment divisible by `d`.
- Create `tests/fixtures/transverse/tg-001-f-coprime.json` — `Z5 x Z7`, no hidden quotient sheet.
- Modify `README.md` only after all executable tests are green — add one factual internal-kernel status paragraph; preserve authority/operator wording.

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
- Produces: `historical_sheet_trace(m: int, n: int, cuts: tuple[int, ...]) -> tuple[int, ...]`
- Produces: `historical_reach_count(m: int, n: int, cuts: tuple[int, ...]) -> int`
- No dependency on `dogram.omega`, `dogram.gate`, or PR #33.

- [ ] **Step 1: Write failing input and sheet-structure tests**

Create `tests/test_transverse.py` with:

```python
import unittest

from dogram.transverse import (
    TransverseInputError,
    analyze_transverse,
    historical_reach_count,
    historical_sheet_trace,
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
        before = sheet_coordinate(8, 12, 3, 7)
        after = sheet_coordinate(8, 12, 4, 8)
        self.assertEqual(before, after)

    def test_transverse_cut_changes_sheet_coordinate(self):
        before = sheet_coordinate(8, 12, 3, 7)
        after = sheet_coordinate(8, 12, 5, 7)
        self.assertNotEqual(before, after)

    def test_invalid_dimension_refuses(self):
        with self.assertRaises(TransverseInputError) as caught:
            analyze_transverse(0, 4, (1,))
        self.assertEqual(caught.exception.reason_code, "INVALID_DIMENSION")

    def test_empty_generator_family_refuses(self):
        with self.assertRaises(TransverseInputError) as caught:
            analyze_transverse(6, 4, ())
        self.assertEqual(caught.exception.reason_code, "EMPTY_GENERATOR_FAMILY")
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: import failure because `dogram.transverse` does not exist.

- [ ] **Step 3: Implement the minimal algebra types and formulas**

Create `dogram/transverse.py` with this public internal surface:

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
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise TransverseInputError("INVALID_DIMENSION", "m must be a positive integer")
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise TransverseInputError("INVALID_DIMENSION", "n must be a positive integer")


def _validate_generators(generators: tuple[int, ...]) -> None:
    if not isinstance(generators, tuple) or not generators:
        raise TransverseInputError("EMPTY_GENERATOR_FAMILY", "generators must be a non-empty tuple")
    if any(not isinstance(r, int) or isinstance(r, bool) for r in generators):
        raise TransverseInputError("INVALID_GENERATOR", "every generator must be an integer")


def sheet_coordinate(m: int, n: int, a: int, b: int) -> int:
    _validate_dimensions(m, n)
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (a, b)):
        raise TransverseInputError("INVALID_STATE", "state coordinates must be integers")
    d = gcd(m, n)
    return (a - b) % d


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
    divisor = gcd(d, *generators)
    lift = d // divisor
    sheets = _generated_sheets(d, generators)
    if len(sheets) != lift:
        raise AssertionError("generated quotient closure disagrees with gcd lift formula")
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


def historical_sheet_trace(m: int, n: int, cuts: tuple[int, ...]) -> tuple[int, ...]:
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


def historical_reach_count(m: int, n: int, cuts: tuple[int, ...]) -> int:
    trace = historical_sheet_trace(m, n, cuts)
    return lcm(m, n) * len(set(trace))


__all__ = [
    "TransverseAnalysis",
    "TransverseInputError",
    "analyze_transverse",
    "historical_reach_count",
    "historical_sheet_trace",
    "sheet_coordinate",
]
```

- [ ] **Step 4: Add the one-shot/closure separation tests**

Append to `TransverseTests`:

```python
    def test_z6_x_z9_one_cut_reaches_36_but_closure_reaches_54(self):
        result = analyze_transverse(6, 9, (1,))
        self.assertEqual(result.sync_sheet_size, 18)
        self.assertEqual(result.sheet_count, 3)
        self.assertEqual(historical_sheet_trace(6, 9, (1,)), (0, 1))
        self.assertEqual(historical_reach_count(6, 9, (1,)), 36)
        self.assertEqual(result.closure_reach_count, 54)

    def test_repeated_bounded_cut_can_visit_third_sheet(self):
        self.assertEqual(historical_sheet_trace(6, 9, (1, 1)), (0, 1, 2))
        self.assertEqual(historical_reach_count(6, 9, (1, 1)), 54)

    def test_inert_cut_changes_no_sheet(self):
        result = analyze_transverse(8, 12, (4,))
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(result.closure_reach_count, 24)
        self.assertEqual(historical_sheet_trace(8, 12, (4,)), (0, 0))

    def test_coprime_dimensions_have_no_hidden_sheet(self):
        result = analyze_transverse(5, 7, (1,))
        self.assertEqual(result.sheet_count, 1)
        self.assertEqual(result.sync_sheet_size, 35)
        self.assertEqual(result.closure_lift_index, 1)
        self.assertEqual(result.closure_reach_count, 35)
```

- [ ] **Step 5: Run the focused test and verify GREEN**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: all transverse tests pass.

- [ ] **Step 6: Commit the pure kernel**

```bash
git add dogram/transverse.py tests/test_transverse.py
git commit -m "feat: add transverse quotient reachability kernel"
```

---

### Task 2: Freeze the Six Canonical Research Specimens

**Files:**
- Create: `tests/fixtures/transverse/pd-001-a-two-sheet.json`
- Create: `tests/fixtures/transverse/pd-001-b-one-shot-vs-closure.json`
- Create: `tests/fixtures/transverse/tg-001-c-partial-lift.json`
- Create: `tests/fixtures/transverse/tg-001-d-complementary.json`
- Create: `tests/fixtures/transverse/tg-001-e-inert.json`
- Create: `tests/fixtures/transverse/tg-001-f-coprime.json`
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Consumes: `analyze_transverse`, `historical_sheet_trace`, `historical_reach_count`
- Produces: frozen JSON specimens with exact expected history and closure fields
- Fixture schema is test-local and must not be promoted as a public Dogram schema.

- [ ] **Step 1: Add a fixture loader and a failing fixture test**

Add imports and helpers to `tests/test_transverse.py`:

```python
import json
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "transverse"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())
```

Add:

```python
    def test_frozen_specimens_match_exact_history_and_closure(self):
        names = sorted(path.name for path in FIXTURES.glob("*.json"))
        self.assertEqual(len(names), 6)
        for name in names:
            fixture = load_fixture(name)
            system = fixture["system"]
            cuts = tuple(fixture["cuts"])
            generators = tuple(fixture["generators"])
            analysis = analyze_transverse(system["m"], system["n"], generators)
            self.assertEqual(analysis.to_data(), fixture["expected"]["analysis"], name)
            self.assertEqual(
                list(historical_sheet_trace(system["m"], system["n"], cuts)),
                fixture["expected"]["historical_sheet_trace"],
                name,
            )
            self.assertEqual(
                historical_reach_count(system["m"], system["n"], cuts),
                fixture["expected"]["historical_reach_count"],
                name,
            )
```

- [ ] **Step 2: Run the fixture test and verify RED**

Run:

```bash
python -m unittest tests.test_transverse.TransverseTests.test_frozen_specimens_match_exact_history_and_closure -v
```

Expected: FAIL because the fixture directory/files do not yet exist and the fixture count is zero.

- [ ] **Step 3: Create the exact frozen fixture files**

Create `pd-001-a-two-sheet.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"PD-001-A","system":{"m":6,"n":4},"generators":[1],"cuts":[1],"expected":{"analysis":{"m":6,"n":4,"generators":[1],"state_capacity":24,"sync_sheet_size":12,"sheet_count":2,"closure_lift_index":2,"closure_reach_count":24,"closure_sheets":[0,1]},"historical_sheet_trace":[0,1],"historical_reach_count":24}}
```

Create `pd-001-b-one-shot-vs-closure.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"PD-001-B","system":{"m":6,"n":9},"generators":[1],"cuts":[1],"expected":{"analysis":{"m":6,"n":9,"generators":[1],"state_capacity":54,"sync_sheet_size":18,"sheet_count":3,"closure_lift_index":3,"closure_reach_count":54,"closure_sheets":[0,1,2]},"historical_sheet_trace":[0,1],"historical_reach_count":36}}
```

Create `tg-001-c-partial-lift.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-C","system":{"m":8,"n":12},"generators":[2],"cuts":[2],"expected":{"analysis":{"m":8,"n":12,"generators":[2],"state_capacity":96,"sync_sheet_size":24,"sheet_count":4,"closure_lift_index":2,"closure_reach_count":48,"closure_sheets":[0,2]},"historical_sheet_trace":[0,2],"historical_reach_count":48}}
```

Create `tg-001-d-complementary.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-D","system":{"m":12,"n":18},"generators":[2,3],"cuts":[2,3],"expected":{"analysis":{"m":12,"n":18,"generators":[2,3],"state_capacity":216,"sync_sheet_size":36,"sheet_count":6,"closure_lift_index":6,"closure_reach_count":216,"closure_sheets":[0,1,2,3,4,5]},"historical_sheet_trace":[0,2,5],"historical_reach_count":108}}
```

Create `tg-001-e-inert.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-E","system":{"m":8,"n":12},"generators":[4],"cuts":[4],"expected":{"analysis":{"m":8,"n":12,"generators":[4],"state_capacity":96,"sync_sheet_size":24,"sheet_count":4,"closure_lift_index":1,"closure_reach_count":24,"closure_sheets":[0]},"historical_sheet_trace":[0,0],"historical_reach_count":24}}
```

Create `tg-001-f-coprime.json`:

```json
{"schema":"dogram.test.transverse-fixture/v0","id":"TG-001-F","system":{"m":5,"n":7},"generators":[1],"cuts":[1],"expected":{"analysis":{"m":5,"n":7,"generators":[1],"state_capacity":35,"sync_sheet_size":35,"sheet_count":1,"closure_lift_index":1,"closure_reach_count":35,"closure_sheets":[0]},"historical_sheet_trace":[0,0],"historical_reach_count":35}}
```

- [ ] **Step 4: Add explicit complementary-generator assertions**

Append:

```python
    def test_complementary_generators_span_more_than_either_alone(self):
        a = analyze_transverse(12, 18, (2,))
        b = analyze_transverse(12, 18, (3,))
        together = analyze_transverse(12, 18, (2, 3))
        self.assertEqual(a.closure_reach_count, 108)
        self.assertEqual(b.closure_reach_count, 72)
        self.assertEqual(together.closure_reach_count, 216)
        self.assertLess(a.closure_reach_count, together.closure_reach_count)
        self.assertLess(b.closure_reach_count, together.closure_reach_count)
```

- [ ] **Step 5: Run all transverse tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_transverse -v
```

Expected: all tests pass and all six frozen specimens match exact calculated outputs.

- [ ] **Step 6: Commit the fixtures**

```bash
git add tests/fixtures/transverse tests/test_transverse.py
git commit -m "test: freeze transverse generator specimens"
```

---

### Task 3: Add the Strong PRODUCTIVE-DESYNC Witness Classifier

**Files:**
- Create: `dogram/productive_desync.py`
- Create: `tests/test_productive_desync.py`

**Interfaces:**
- Consumes explicit facts only; no hidden Ω dependency.
- Produces: `ProductiveDesyncAssessment`
- Produces: `assess_productive_desync(...) -> ProductiveDesyncAssessment`
- Status values: `WITNESS`, `POTENTIAL`, `REFUSE`.
- `WITNESS` requires historical expansion; `POTENTIAL` means closure expands but actual history has not yet demonstrated expansion.

- [ ] **Step 1: Write failing classification tests**

Create `tests/test_productive_desync.py`:

```python
import unittest

from dogram.productive_desync import assess_productive_desync


class ProductiveDesyncTests(unittest.TestCase):
    def assess(self, **overrides):
        values = {
            "target_preserved": True,
            "execution_changed": True,
            "baseline_reach_count": 18,
            "historical_reach_count": 36,
            "closure_reach_count": 54,
            "cut_declared": True,
            "bounded_return_to_coherence": True,
        }
        values.update(overrides)
        return assess_productive_desync(**values)

    def test_historical_expansion_is_witness(self):
        result = self.assess()
        self.assertEqual((result.status, result.reason_code), ("WITNESS", None))
        self.assertTrue(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_closure_only_expansion_is_potential_not_history(self):
        result = self.assess(historical_reach_count=18, closure_reach_count=54)
        self.assertEqual((result.status, result.reason_code), ("POTENTIAL", "CLOSURE_ONLY"))
        self.assertFalse(result.historical_expanded)
        self.assertTrue(result.closure_expanded)

    def test_target_failure_refuses_even_when_reach_expands(self):
        result = self.assess(target_preserved=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "TARGET_NOT_PRESERVED"))

    def test_no_execution_difference_refuses(self):
        result = self.assess(execution_changed=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_EXECUTION_DIFFERENCE"))

    def test_untyped_cut_refuses(self):
        result = self.assess(cut_declared=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "UNTYPED_CUT"))

    def test_permanent_incoherence_refuses_bounded_desync_label(self):
        result = self.assess(bounded_return_to_coherence=False)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_COHERENCE_RETURN"))

    def test_no_reachability_gain_refuses(self):
        result = self.assess(historical_reach_count=18, closure_reach_count=18)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_REACHABILITY_EXPANSION"))

    def test_shrinking_future_does_not_become_productive(self):
        result = self.assess(historical_reach_count=12, closure_reach_count=12)
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


@dataclass(frozen=True)
class ProductiveDesyncAssessment:
    status: str
    reason_code: str | None
    target_preserved: bool
    execution_changed: bool
    baseline_reach_count: int
    historical_reach_count: int
    closure_reach_count: int
    historical_expanded: bool
    closure_expanded: bool
    cut_declared: bool
    bounded_return_to_coherence: bool

    def to_data(self) -> dict[str, object]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "target_preserved": self.target_preserved,
            "execution_changed": self.execution_changed,
            "baseline_reach_count": self.baseline_reach_count,
            "historical_reach_count": self.historical_reach_count,
            "closure_reach_count": self.closure_reach_count,
            "historical_expanded": self.historical_expanded,
            "closure_expanded": self.closure_expanded,
            "cut_declared": self.cut_declared,
            "bounded_return_to_coherence": self.bounded_return_to_coherence,
        }


def _valid_count(value: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def assess_productive_desync(
    *,
    target_preserved: bool,
    execution_changed: bool,
    baseline_reach_count: int,
    historical_reach_count: int,
    closure_reach_count: int,
    cut_declared: bool,
    bounded_return_to_coherence: bool,
) -> ProductiveDesyncAssessment:
    flags = (target_preserved, execution_changed, cut_declared, bounded_return_to_coherence)
    if any(not isinstance(flag, bool) for flag in flags):
        raise ValueError("classification flags must be booleans")
    counts = (baseline_reach_count, historical_reach_count, closure_reach_count)
    if any(not _valid_count(value) for value in counts):
        raise ValueError("reach counts must be non-negative integers")
    if historical_reach_count > closure_reach_count:
        raise ValueError("historical reach cannot exceed declared closure reach")

    historical_expanded = historical_reach_count > baseline_reach_count
    closure_expanded = closure_reach_count > baseline_reach_count

    reason_code = None
    status = "WITNESS"
    if not cut_declared:
        status, reason_code = "REFUSE", "UNTYPED_CUT"
    elif not bounded_return_to_coherence:
        status, reason_code = "REFUSE", "NO_COHERENCE_RETURN"
    elif not target_preserved:
        status, reason_code = "REFUSE", "TARGET_NOT_PRESERVED"
    elif not execution_changed:
        status, reason_code = "REFUSE", "NO_EXECUTION_DIFFERENCE"
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
        execution_changed=execution_changed,
        baseline_reach_count=baseline_reach_count,
        historical_reach_count=historical_reach_count,
        closure_reach_count=closure_reach_count,
        historical_expanded=historical_expanded,
        closure_expanded=closure_expanded,
        cut_declared=cut_declared,
        bounded_return_to_coherence=bounded_return_to_coherence,
    )


__all__ = ["ProductiveDesyncAssessment", "assess_productive_desync"]
```

- [ ] **Step 4: Add malformed-count hostile controls**

Append:

```python
    def test_history_cannot_exceed_declared_closure(self):
        with self.assertRaises(ValueError):
            self.assess(historical_reach_count=55, closure_reach_count=54)

    def test_negative_reach_count_refuses_input(self):
        with self.assertRaises(ValueError):
            self.assess(historical_reach_count=-1)
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

### Task 4: Independently Verify the Lift Formula Against Brute-Force State Reachability

**Files:**
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Consumes: `analyze_transverse`
- Test-only independent oracle enumerates full states using explicit transitions rather than the gcd formula.
- Verifies 405 single-generator cases: `m=2..10`, `n=2..10`, `r=1..5`.

- [ ] **Step 1: Add an independent brute-force closure helper**

Add to `tests/test_transverse.py`:

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

- [ ] **Step 2: Add the 405-case law test**

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

- [ ] **Step 3: Add a multi-generator independent control**

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

Expected: all tests pass; exactly 405 single-generator combinations match the independent finite-state traversal oracle.

- [ ] **Step 5: Commit the independent law verification**

```bash
git add tests/test_transverse.py
git commit -m "test: verify transverse lift law by brute force"
```

---

### Task 5: Integrate the Research Kernel Without Expanding Dogram's Public Constitution

**Files:**
- Modify: `README.md`
- Test: existing full suite and constitutional checks

**Interfaces:**
- No new public operator.
- No new bootstrap intrinsic.
- No Ω receipt/schema change.
- Documents only that the internal finite research kernel exists.

- [ ] **Step 1: Run the full suite before documentation changes**

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

- [ ] **Step 3: Run the constitutional floor directly**

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

- [ ] **Step 4: Add one factual README paragraph**

Add after the current Ω implementation-status paragraph:

```markdown
Dogram also contains an internal finite research kernel for `PRODUCTIVE-DESYNC-001 / TRANSVERSE-GENERATORS-001`. It receipts synchronized quotient sheets, bounded cut history, and generated reachability closure while preserving `ONE CROSSING != GENERATOR CLOSURE` and `POTENTIAL REACHABILITY != ACTUAL HISTORY`. This kernel does not add a public operator, truth/evidence semantics, or automatic experiment selection.
```

- [ ] **Step 5: Re-run the full verification after the README edit**

Run:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Then re-run the constitutional-floor Python block from Step 3.

Expected: all tests pass, compile exits 0, constitutional floor prints `constitutional floor OK`.

- [ ] **Step 6: Run a scope scan for accidental authority/operator expansion**

Run:

```bash
python - <<'PY'
from pathlib import Path

forbidden_public_names = ("transverse@1", "desync@1", "productive_desync@1", "phase@1", "meta@1")
for path in [Path("dogram/engine.py"), Path("dogram/registry.py")]:
    text = path.read_text()
    for token in forbidden_public_names:
        assert token not in text, (path, token)
print("transverse scope scan OK")
PY
```

Expected: `transverse scope scan OK`.

- [ ] **Step 7: Commit documentation and final constitutional verification state**

```bash
git add README.md
git commit -m "docs: record transverse reachability research kernel"
```

---

## Final Verification Gate

Before opening or updating an implementation PR, run all of the following on the exact implementation head:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
python - <<'PY'
import pathlib
import tomllib
from dogram.engine import OPERATORS
from dogram.registry import build_bootstrap_registry
from dogram.transverse import analyze_transverse, historical_reach_count
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
assert historical_reach_count(6, 9, (1,)) == 36
assert case.closure_reach_count == 54

assessment = assess_productive_desync(
    target_preserved=True,
    execution_changed=True,
    baseline_reach_count=18,
    historical_reach_count=36,
    closure_reach_count=54,
    cut_declared=True,
    bounded_return_to_coherence=True,
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

The implementation PR must report the exact head SHA used for this verification and must not claim Ω-quotient integration until a separate reviewed adapter binds actual quotient receipts to `target_preserved` and `execution_changed`.
