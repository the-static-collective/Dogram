# MATHBAND-INCUBATOR-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an internal Dogram research kernel that pressure-tests declared mathematical bridges, preserves partial/unmapped/extra/residual structure, and survives the Five Bats without adding a public Dogram operator.

**Architecture:** Keep v0 finite, exact-first, and fixture-driven. `dogram/mathband.py` owns only deterministic receipt classification over already-constituted finite probe observations; the test fixture and independent test-side mathematical oracles construct the complex-number and matrix voices so the evaluator cannot grade its own bats. Known exact bridges calibrate the receipt before partial, false-friend, or novel bridges are admitted.

**Tech Stack:** Python 3.12 standard library only; frozen dataclasses; `unittest`; JSON fixtures; existing Dogram canonical/operator floor.

**Spec:** `docs/superpowers/specs/2026-09-05-mathband-incubator-001-design.md`

## Global Constraints

- Status remains `EXPERIMENTAL ARCHITECTURAL INCUBATOR · NO PUBLIC OPERATOR ADMITTED`.
- Dogram law remains: `DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.`
- Production dependencies remain empty; do not modify `pyproject.toml` dependencies.
- Do not modify `dogram/engine.py` or add `mathband@1` to `OPERATORS`.
- No CLI route, schema promotion, symbolic parser, theorem prover, CAS, network dependency, automatic bridge discovery, or semantic/evidentiary authority.
- Probe families and decisive/load-bearing probes are frozen before evaluation.
- `EVALUATOR != BAT ORACLE`: fixture generation and expected hostile behavior remain outside `dogram.mathband`.
- No scalar `match_score`; a decisive broken probe cannot be overruled by aggregate similarity.
- `UNMAPPED != FALSE`, `EXTRA != ERROR`, `APPROXIMATE != EXACT`, `BRIDGE != IDENTITY`, `PRESERVED UNDER P != GLOBALLY EQUIVALENT`.
- Exact arithmetic is preferred. Numeric tolerance exists only to retain explicit residuals; it must never silently convert approximate equality into exact equality.

---

## File Structure

- Create `dogram/mathband.py` — frozen receipt types, input validation, deterministic probe classification, assumption gate, decisive-probe handling. No discipline-specific mathematics.
- Create `tests/fixtures/mathband_incubator_001.json` — frozen inputs for exact rotation calibration and all Five Bats; expected constitutional behavior is fixture/test data, never evaluator-generated.
- Create `tests/test_mathband.py` — independent mathematical oracles for complex quarter-turn and matrix action; TDD coverage for exact bridge, Five Bats, residuals, refusals, deterministic output, and public-operator non-promotion.
- Create `research/MATHBAND-INCUBATOR-001.md` — executable research receipt: question, frozen specimen, Five-Bat outcomes, documented math, inference, refusals, and HOLD boundary.
- Do not modify `dogram/engine.py`, `dogram/cli.py`, `pyproject.toml`, or any public schema/operator registry.

---

### Task 1: Exact Receipt Floor and Calibration Bridge

**Files:**
- Create: `dogram/mathband.py`
- Create: `tests/test_mathband.py`
- Create: `tests/fixtures/mathband_incubator_001.json`

**Interfaces:**
- Produces `ProbeObservation`, `ProbeOutcome`, `MathBandReceipt`, and `evaluate_bridge(...)` for later tasks.
- `evaluate_bridge` consumes already-computed common-stage probe outputs; it never computes complex or matrix mathematics itself.
- Exact probe equality is Python structural equality over frozen JSON-like values.

- [ ] **Step 1: Create the frozen calibration fixture**

Create `tests/fixtures/mathband_incubator_001.json` with this initial content:

```json
{
  "calibration": {
    "bridge_ref": "complex-quarter-turn__matrix-quarter-turn",
    "voice_a_ref": "complex-multiplication-by-i",
    "voice_b_ref": "matrix-quarter-turn",
    "required_assumptions": [
      "complex_pair_identification",
      "quarter_turn_action"
    ],
    "pairs": [[1, 2], [-3, 4], [0, 5], [7, 0]],
    "rotation_matrix": [[0, -1], [1, 0]],
    "scale_factor": 7
  }
}
```

- [ ] **Step 2: Write the independent oracles and the first failing test**

Create `tests/test_mathband.py` with fixture loading, independent test-side oracles, and this first test:

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.mathband import ProbeObservation, evaluate_bridge


FIXTURE = Path(__file__).parent / "fixtures" / "mathband_incubator_001.json"


def _complex_quarter_turn(pair: tuple[int, int]) -> tuple[int, int]:
    a, b = pair
    return (-b, a)


def _matrix_apply(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    pair: tuple[int, int],
) -> tuple[int, int]:
    (m00, m01), (m10, m11) = matrix
    a, b = pair
    return (m00 * a + m01 * b, m10 * a + m11 * b)


class MathBandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.calibration = cls.fixture["calibration"]
        cls.matrix = tuple(tuple(row) for row in cls.calibration["rotation_matrix"])
        cls.pairs = tuple(tuple(pair) for pair in cls.calibration["pairs"])

    def _exact_probes(self) -> tuple[ProbeObservation, ...]:
        return tuple(
            ProbeObservation(
                name=f"quarter_turn:{pair[0]},{pair[1]}",
                left=_complex_quarter_turn(pair),
                right=_matrix_apply(self.matrix, pair),
                comparison="exact",
                must_preserve=True,
                decisive=True,
            )
            for pair in self.pairs
        )

    def test_exact_complex_matrix_calibration_preserves_all_probes(self) -> None:
        receipt = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=tuple(self.calibration["required_assumptions"]),
            provided_assumptions=tuple(self.calibration["required_assumptions"]),
            probes=self._exact_probes(),
        )

        self.assertEqual({outcome.status for outcome in receipt.outcomes}, {"PRESERVED"})
        self.assertEqual(receipt.first_decisive_probe, None)
        self.assertEqual(receipt.exactness, "exact")
        self.assertEqual(receipt.refusals, ())
```

- [ ] **Step 3: Run the test and verify the RED state**

Run:

```bash
python -m unittest tests.test_mathband.MathBandTests.test_exact_complex_matrix_calibration_preserves_all_probes -v
```

Expected: **FAIL/ERROR** because `dogram.mathband` does not exist yet.

- [ ] **Step 4: Implement the minimal exact receipt floor**

Create `dogram/mathband.py` with these concrete interfaces:

```python
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


ProbeStatus = Literal["PRESERVED", "CHANGED", "BROKEN", "UNMAPPED", "RESIDUAL"]
ComparisonKind = Literal["exact", "numeric"]
Exactness = Literal["exact", "approximate", "refused"]


@dataclass(frozen=True)
class ProbeObservation:
    name: str
    left: object | None
    right: object | None
    comparison: ComparisonKind = "exact"
    tolerance: float = 0.0
    must_preserve: bool = True
    decisive: bool = False
    left_defined: bool = True
    right_defined: bool = True


@dataclass(frozen=True)
class ProbeOutcome:
    name: str
    status: ProbeStatus
    left: object | None
    right: object | None
    delta: tuple[object | None, object | None] | None
    residual: float | None
    decisive: bool


@dataclass(frozen=True)
class MathBandReceipt:
    bridge_ref: str
    voice_a_ref: str
    voice_b_ref: str
    declared_assumptions: tuple[str, ...]
    declared_transforms: tuple[str, ...]
    outcomes: tuple[ProbeOutcome, ...]
    extra_a: tuple[str, ...]
    extra_b: tuple[str, ...]
    lossy_steps: tuple[str, ...]
    exactness: Exactness
    first_decisive_probe: str | None
    refusals: tuple[str, ...]


def evaluate_bridge(
    *,
    bridge_ref: str,
    voice_a_ref: str,
    voice_b_ref: str,
    required_assumptions: tuple[str, ...],
    provided_assumptions: tuple[str, ...],
    probes: tuple[ProbeObservation, ...],
    declared_transforms: tuple[str, ...] = (),
    extra_a: tuple[str, ...] = (),
    extra_b: tuple[str, ...] = (),
    lossy_steps: tuple[str, ...] = (),
) -> MathBandReceipt:
    ...
```

For Task 1, implement only these behaviors:

```python
# validate non-empty refs, non-empty unique probe names, known comparison values
# exact + defined + left == right -> PRESERVED
# exact + defined + left != right + must_preserve -> BROKEN
# exact + defined + left != right + not must_preserve -> CHANGED
# first_decisive_probe = first input-order decisive BROKEN outcome
# exactness = "exact"
```

Keep `numeric`, assumption refusal, `UNMAPPED`, extras, and approximate exactness fields structurally present but do not implement their later behavior until their red tests exist.

Export only:

```python
__all__ = [
    "MathBandReceipt",
    "ProbeObservation",
    "ProbeOutcome",
    "evaluate_bridge",
]
```

- [ ] **Step 5: Run the exact calibration test and verify GREEN**

Run:

```bash
python -m unittest tests.test_mathband.MathBandTests.test_exact_complex_matrix_calibration_preserves_all_probes -v
```

Expected: **PASS**.

- [ ] **Step 6: Commit the exact floor**

```bash
git add dogram/mathband.py tests/test_mathband.py tests/fixtures/mathband_incubator_001.json
git commit -m "Research: add MathBand exact calibration floor"
```

---

### Task 2: Rename Bat and Gauge Bat

**Files:**
- Modify: `tests/fixtures/mathband_incubator_001.json`
- Modify: `tests/test_mathband.py`
- Modify: `dogram/mathband.py`

**Interfaces:**
- Consumes `ProbeObservation` and `evaluate_bridge(...)` from Task 1.
- Produces stable receipt semantics under reordered/renamed probes and preserves a caller-declared representation transform separately in `declared_transforms`.

- [ ] **Step 1: Extend the fixture with Rename/Gauge controls**

Add these keys under `calibration`:

```json
"rename_prefix": "bat-renamed",
"gauge_transform": "common_integer_scale:7"
```

- [ ] **Step 2: Write failing Rename Bat and Gauge Bat tests**

Add:

```python
def _semantic_signature(receipt) -> tuple[tuple[str, object, object], ...]:
    return tuple(sorted((outcome.status, outcome.left, outcome.right) for outcome in receipt.outcomes))
```

Then add:

```python
def test_rename_bat_preserves_semantics_under_reordering_and_renaming(self) -> None:
    baseline = evaluate_bridge(
        bridge_ref=self.calibration["bridge_ref"],
        voice_a_ref=self.calibration["voice_a_ref"],
        voice_b_ref=self.calibration["voice_b_ref"],
        required_assumptions=tuple(self.calibration["required_assumptions"]),
        provided_assumptions=tuple(self.calibration["required_assumptions"]),
        probes=self._exact_probes(),
    )
    renamed = tuple(
        ProbeObservation(
            name=f"{self.calibration['rename_prefix']}:{index}",
            left=probe.left,
            right=probe.right,
            comparison="exact",
            must_preserve=True,
            decisive=True,
        )
        for index, probe in enumerate(reversed(self._exact_probes()))
    )
    attacked = evaluate_bridge(
        bridge_ref=self.calibration["bridge_ref"],
        voice_a_ref="voice-a-renamed",
        voice_b_ref="voice-b-renamed",
        required_assumptions=tuple(self.calibration["required_assumptions"]),
        provided_assumptions=tuple(self.calibration["required_assumptions"]),
        probes=renamed,
    )

    self.assertEqual(_semantic_signature(attacked), _semantic_signature(baseline))
    self.assertEqual(attacked.first_decisive_probe, None)


def test_gauge_bat_preserves_relation_and_receipts_common_scale(self) -> None:
    scale = self.calibration["scale_factor"]
    scaled_pairs = tuple((a * scale, b * scale) for a, b in self.pairs)
    probes = tuple(
        ProbeObservation(
            name=f"scaled:{a},{b}",
            left=_complex_quarter_turn((a, b)),
            right=_matrix_apply(self.matrix, (a, b)),
            comparison="exact",
            must_preserve=True,
            decisive=True,
        )
        for a, b in scaled_pairs
    )

    receipt = evaluate_bridge(
        bridge_ref=self.calibration["bridge_ref"],
        voice_a_ref=self.calibration["voice_a_ref"],
        voice_b_ref=self.calibration["voice_b_ref"],
        required_assumptions=tuple(self.calibration["required_assumptions"]),
        provided_assumptions=tuple(self.calibration["required_assumptions"]),
        probes=probes,
        declared_transforms=(self.calibration["gauge_transform"],),
    )

    self.assertEqual({outcome.status for outcome in receipt.outcomes}, {"PRESERVED"})
    self.assertEqual(receipt.declared_transforms, ("common_integer_scale:7",))
    self.assertEqual(receipt.exactness, "exact")
```

- [ ] **Step 3: Run both bat tests and verify at least one RED state**

Run:

```bash
python -m unittest \
  tests.test_mathband.MathBandTests.test_rename_bat_preserves_semantics_under_reordering_and_renaming \
  tests.test_mathband.MathBandTests.test_gauge_bat_preserves_relation_and_receipts_common_scale -v
```

Expected before implementation completion: **FAIL** if `declared_transforms` is not yet retained or deterministic semantics are unstable.

- [ ] **Step 4: Implement only the missing Rename/Gauge behavior**

Ensure `evaluate_bridge(...)`:

```python
# preserves caller-supplied declared_transforms exactly as an immutable tuple
# never uses bridge/voice/probe names to decide mathematical equality
# preserves input probe order in receipt while allowing semantic comparison independent of serialization order
```

Do not canonicalize or sort probe execution order inside the evaluator; decisive order is caller-declared and load-bearing.

- [ ] **Step 5: Run Task 2 tests and Task 1 regression**

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS** for all tests written so far.

- [ ] **Step 6: Commit Rename/Gauge bats**

```bash
git add dogram/mathband.py tests/test_mathband.py tests/fixtures/mathband_incubator_001.json
git commit -m "Test: hit MathBand with rename and gauge bats"
```

---

### Task 3: Domain Bat, Extra-Voice Bat, and Assumption Refusal

**Files:**
- Modify: `tests/fixtures/mathband_incubator_001.json`
- Modify: `tests/test_mathband.py`
- Modify: `dogram/mathband.py`

**Interfaces:**
- Adds constitutional handling for `UNMAPPED`, `EXTRA`, and whole-bridge `REFUSE` without changing exact bridge semantics.
- Missing required assumptions return a receipt with `exactness="refused"`; they do not raise or guess.

- [ ] **Step 1: Extend the fixture with frozen hostile data**

Add top-level keys:

```json
"domain_bat": {
  "declared_domain": "nonzero_pairs",
  "inside_pair": [3, 4],
  "outside_pair": [0, 0]
},
"extra_voice_bat": {
  "voice_a_extra": [],
  "voice_b_extra": ["independent_conjugation_operation"]
}
```

- [ ] **Step 2: Write the failing Domain Bat test**

Add:

```python
def test_domain_bat_keeps_outside_domain_unmapped(self) -> None:
    inside = tuple(self.fixture["domain_bat"]["inside_pair"])
    outside = tuple(self.fixture["domain_bat"]["outside_pair"])
    probes = (
        ProbeObservation(
            name="inside-domain",
            left=_complex_quarter_turn(inside),
            right=_matrix_apply(self.matrix, inside),
            decisive=True,
        ),
        ProbeObservation(
            name="outside-domain",
            left=None,
            right=None,
            decisive=False,
            left_defined=False,
            right_defined=False,
        ),
    )

    receipt = evaluate_bridge(
        bridge_ref="restricted-quarter-turn",
        voice_a_ref=self.calibration["voice_a_ref"],
        voice_b_ref=self.calibration["voice_b_ref"],
        required_assumptions=("domain=nonzero_pairs",),
        provided_assumptions=("domain=nonzero_pairs",),
        probes=probes,
    )

    self.assertEqual(receipt.outcomes[0].status, "PRESERVED")
    self.assertEqual(receipt.outcomes[1].status, "UNMAPPED")
    self.assertEqual(receipt.first_decisive_probe, None)
```

- [ ] **Step 3: Write failing Extra-Voice and refusal tests**

Add:

```python
def test_extra_voice_bat_preserves_unmatched_structure(self) -> None:
    receipt = evaluate_bridge(
        bridge_ref=self.calibration["bridge_ref"],
        voice_a_ref=self.calibration["voice_a_ref"],
        voice_b_ref=self.calibration["voice_b_ref"],
        required_assumptions=tuple(self.calibration["required_assumptions"]),
        provided_assumptions=tuple(self.calibration["required_assumptions"]),
        probes=self._exact_probes(),
        extra_a=tuple(self.fixture["extra_voice_bat"]["voice_a_extra"]),
        extra_b=tuple(self.fixture["extra_voice_bat"]["voice_b_extra"]),
    )

    self.assertEqual(receipt.extra_a, ())
    self.assertEqual(receipt.extra_b, ("independent_conjugation_operation",))
    self.assertEqual({outcome.status for outcome in receipt.outcomes}, {"PRESERVED"})


def test_missing_required_assumption_refuses_without_grading_probes(self) -> None:
    receipt = evaluate_bridge(
        bridge_ref=self.calibration["bridge_ref"],
        voice_a_ref=self.calibration["voice_a_ref"],
        voice_b_ref=self.calibration["voice_b_ref"],
        required_assumptions=("complex_pair_identification", "quarter_turn_action"),
        provided_assumptions=("complex_pair_identification",),
        probes=self._exact_probes(),
    )

    self.assertEqual(receipt.exactness, "refused")
    self.assertEqual(receipt.outcomes, ())
    self.assertEqual(receipt.refusals, ("missing assumption: quarter_turn_action",))
```

- [ ] **Step 4: Run the three new tests and verify RED**

```bash
python -m unittest \
  tests.test_mathband.MathBandTests.test_domain_bat_keeps_outside_domain_unmapped \
  tests.test_mathband.MathBandTests.test_extra_voice_bat_preserves_unmatched_structure \
  tests.test_mathband.MathBandTests.test_missing_required_assumption_refuses_without_grading_probes -v
```

Expected: **FAIL** until `UNMAPPED`, extras, and refusal are implemented.

- [ ] **Step 5: Implement domain, extra, and refusal behavior**

Extend `evaluate_bridge(...)` exactly as follows:

```python
missing = tuple(
    assumption
    for assumption in required_assumptions
    if assumption not in set(provided_assumptions)
)
if missing:
    return MathBandReceipt(
        bridge_ref=bridge_ref,
        voice_a_ref=voice_a_ref,
        voice_b_ref=voice_b_ref,
        declared_assumptions=provided_assumptions,
        declared_transforms=declared_transforms,
        outcomes=(),
        extra_a=extra_a,
        extra_b=extra_b,
        lossy_steps=lossy_steps,
        exactness="refused",
        first_decisive_probe=None,
        refusals=tuple(f"missing assumption: {item}" for item in missing),
    )
```

For each probe before equality comparison:

```python
if not probe.left_defined or not probe.right_defined:
    outcome = ProbeOutcome(
        name=probe.name,
        status="UNMAPPED",
        left=probe.left,
        right=probe.right,
        delta=None,
        residual=None,
        decisive=probe.decisive,
    )
```

Preserve `extra_a`, `extra_b`, and `lossy_steps` verbatim in the receipt. Do not attempt to interpret or eliminate them.

- [ ] **Step 6: Run full MathBand tests**

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS**.

- [ ] **Step 7: Commit Domain/Extra/Refusal bats**

```bash
git add dogram/mathband.py tests/test_mathband.py tests/fixtures/mathband_incubator_001.json
git commit -m "Test: preserve MathBand domain and extra-voice boundaries"
```

---

### Task 4: False-Friend Bat and Explicit Residuals

**Files:**
- Modify: `tests/fixtures/mathband_incubator_001.json`
- Modify: `tests/test_mathband.py`
- Modify: `dogram/mathband.py`

**Interfaces:**
- Adds numeric residual classification and predeclared decisive failure handling.
- A false friend may pass many non-decisive probes but still records `first_decisive_probe` when the load-bearing probe breaks.

- [ ] **Step 1: Extend the fixture with the false friend and residual thresholds**

Add:

```json
"false_friend_bat": {
  "matrix": [[0, 1], [1, 0]],
  "probe_pair": [2, 5],
  "decisive_probe": "two-turn-output"
},
"residual_bat": {
  "within_tolerance": [1.0, 1.0005, 0.001],
  "outside_tolerance": [1.0, 1.01, 0.001]
}
```

- [ ] **Step 2: Add a matrix composition helper in the test oracle**

Add to `tests/test_mathband.py`:

```python
def _matrix_apply_twice(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    pair: tuple[int, int],
) -> tuple[int, int]:
    return _matrix_apply(matrix, _matrix_apply(matrix, pair))


def _norm_sq(pair: tuple[int, int]) -> int:
    a, b = pair
    return a * a + b * b
```

- [ ] **Step 3: Write the failing False-Friend Bat test**

Add:

```python
def test_false_friend_bat_cannot_outvote_decisive_failure(self) -> None:
    pair = tuple(self.fixture["false_friend_bat"]["probe_pair"])
    false_matrix = tuple(tuple(row) for row in self.fixture["false_friend_bat"]["matrix"])
    complex_once = _complex_quarter_turn(pair)
    complex_twice = _complex_quarter_turn(complex_once)
    false_once = _matrix_apply(false_matrix, pair)
    false_twice = _matrix_apply_twice(false_matrix, pair)

    probes = (
        ProbeObservation("norm-input", _norm_sq(pair), _norm_sq(pair), decisive=False),
        ProbeObservation("norm-output", _norm_sq(complex_once), _norm_sq(false_once), decisive=False),
        ProbeObservation("origin-fixed", (0, 0), _matrix_apply(false_matrix, (0, 0)), decisive=False),
        ProbeObservation("four-step-return-available", True, True, decisive=False),
        ProbeObservation(
            "two-turn-output",
            complex_twice,
            false_twice,
            decisive=True,
            must_preserve=True,
        ),
    )

    receipt = evaluate_bridge(
        bridge_ref="complex-quarter-turn__reflection-false-friend",
        voice_a_ref=self.calibration["voice_a_ref"],
        voice_b_ref="reflection-like-matrix",
        required_assumptions=("pair_identification",),
        provided_assumptions=("pair_identification",),
        probes=probes,
    )

    self.assertEqual(sum(o.status == "PRESERVED" for o in receipt.outcomes), 4)
    self.assertEqual(receipt.outcomes[-1].status, "BROKEN")
    self.assertEqual(receipt.first_decisive_probe, "two-turn-output")
```

This fixture deliberately gives the false bridge four superficially successful probes and one load-bearing failure. No aggregate similarity score exists to rescue it.

- [ ] **Step 4: Write failing residual tests**

Add:

```python
def test_numeric_disagreement_within_tolerance_is_residual_not_exact(self) -> None:
    left, right, tolerance = self.fixture["residual_bat"]["within_tolerance"]
    receipt = evaluate_bridge(
        bridge_ref="approximate-control",
        voice_a_ref="numeric-a",
        voice_b_ref="numeric-b",
        required_assumptions=(),
        provided_assumptions=(),
        probes=(ProbeObservation(
            name="approximate-probe",
            left=left,
            right=right,
            comparison="numeric",
            tolerance=tolerance,
            must_preserve=True,
            decisive=True,
        ),),
    )

    self.assertEqual(receipt.outcomes[0].status, "RESIDUAL")
    self.assertAlmostEqual(receipt.outcomes[0].residual, abs(left - right))
    self.assertEqual(receipt.exactness, "approximate")
    self.assertEqual(receipt.first_decisive_probe, None)


def test_numeric_disagreement_outside_tolerance_breaks_decisive_probe(self) -> None:
    left, right, tolerance = self.fixture["residual_bat"]["outside_tolerance"]
    receipt = evaluate_bridge(
        bridge_ref="approximate-control",
        voice_a_ref="numeric-a",
        voice_b_ref="numeric-b",
        required_assumptions=(),
        provided_assumptions=(),
        probes=(ProbeObservation(
            name="approximate-probe",
            left=left,
            right=right,
            comparison="numeric",
            tolerance=tolerance,
            must_preserve=True,
            decisive=True,
        ),),
    )

    self.assertEqual(receipt.outcomes[0].status, "BROKEN")
    self.assertGreater(receipt.outcomes[0].residual, tolerance)
    self.assertEqual(receipt.first_decisive_probe, "approximate-probe")
```

- [ ] **Step 5: Run False-Friend and residual tests and verify RED**

```bash
python -m unittest \
  tests.test_mathband.MathBandTests.test_false_friend_bat_cannot_outvote_decisive_failure \
  tests.test_mathband.MathBandTests.test_numeric_disagreement_within_tolerance_is_residual_not_exact \
  tests.test_mathband.MathBandTests.test_numeric_disagreement_outside_tolerance_breaks_decisive_probe -v
```

Expected: **FAIL** until numeric comparison and decisive failure are fully implemented.

- [ ] **Step 6: Implement numeric residual classification**

Add a private validator:

```python
def _finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and isfinite(float(value))
    )
```

For `comparison == "numeric"`:

```python
if (
    not _finite_number(probe.left)
    or not _finite_number(probe.right)
    or not _finite_number(probe.tolerance)
    or probe.tolerance < 0.0
):
    raise ValueError("numeric probes require finite numbers and nonnegative tolerance")

residual = abs(float(probe.left) - float(probe.right))
if residual == 0.0:
    status = "PRESERVED"
elif residual <= probe.tolerance:
    status = "RESIDUAL"
elif probe.must_preserve:
    status = "BROKEN"
else:
    status = "CHANGED"
```

Set receipt `exactness`:

```python
"approximate" if any(outcome.status == "RESIDUAL" for outcome in outcomes) or lossy_steps else "exact"
```

Set `first_decisive_probe` to the first input-order outcome satisfying:

```python
outcome.decisive and outcome.status == "BROKEN"
```

Never select a decisive probe after inspecting results; the evaluator only consumes the predeclared `decisive` field.

- [ ] **Step 7: Run all MathBand tests**

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS**.

- [ ] **Step 8: Commit False-Friend and residual behavior**

```bash
git add dogram/mathband.py tests/test_mathband.py tests/fixtures/mathband_incubator_001.json
git commit -m "Test: kill MathBand false friends with decisive probes"
```

---

### Task 5: Research Receipt and Constitutional Regression

**Files:**
- Create: `research/MATHBAND-INCUBATOR-001.md`
- Modify: `tests/test_mathband.py`
- Read-only regression target: `dogram/engine.py`

**Interfaces:**
- Produces the durable research receipt for the incubator.
- Adds a regression proving MathBand remains outside the public `OPERATORS` registry.

- [ ] **Step 1: Write the failing public-operator regression test**

Add this import and test:

```python
from dogram.engine import OPERATORS


def test_mathband_does_not_enter_public_operator_floor(self) -> None:
    self.assertEqual(
        set(OPERATORS),
        {("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)},
    )
    self.assertNotIn(("mathband", 1), OPERATORS)
```

Run:

```bash
python -m unittest tests.test_mathband.MathBandTests.test_mathband_does_not_enter_public_operator_floor -v
```

Expected: **PASS immediately** if no previous task accidentally promoted MathBand. If it fails, remove the promotion rather than changing this expected set.

- [ ] **Step 2: Add deterministic validation tests before documenting success**

Add:

```python
def test_duplicate_probe_names_refuse_malformed_input_by_exception(self) -> None:
    probe = ProbeObservation("duplicate", 1, 1)
    with self.assertRaisesRegex(ValueError, "probe names must be unique"):
        evaluate_bridge(
            bridge_ref="duplicate-control",
            voice_a_ref="a",
            voice_b_ref="b",
            required_assumptions=(),
            provided_assumptions=(),
            probes=(probe, probe),
        )


def test_receipt_order_is_deterministic_and_follows_predeclared_probe_order(self) -> None:
    probes = (
        ProbeObservation("first", 1, 1),
        ProbeObservation("second", 2, 2),
        ProbeObservation("third", 3, 3),
    )
    receipt = evaluate_bridge(
        bridge_ref="ordering-control",
        voice_a_ref="a",
        voice_b_ref="b",
        required_assumptions=(),
        provided_assumptions=(),
        probes=probes,
    )
    self.assertEqual(tuple(outcome.name for outcome in receipt.outcomes), ("first", "second", "third"))
```

Run:

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS** after adding any missing validation in `dogram/mathband.py`.

- [ ] **Step 3: Write `research/MATHBAND-INCUBATOR-001.md`**

Use this exact section structure:

```markdown
# MATHBAND-INCUBATOR-001

Status: experimental research kernel. No public operator.

## Question
## Constitutional contract
## Calibration bridge
## Five Bats
### BAT-1 Rename
### BAT-2 Gauge
### BAT-3 Domain
### BAT-4 Extra Voice
### BAT-5 False Friend
## Residual control
## Documented mathematics
## Dogram inference
## Explicit refusals
## HOLD
## Next gate
```

The receipt must state these earned results only if verified by tests:

```text
BRIDGE != IDENTITY.
PRESERVED UNDER P != GLOBALLY EQUIVALENT.
UNMAPPED != FALSE.
EXTRA != ERROR.
APPROXIMATE != EXACT.
DECISIVE FAILURE CANNOT BE OUTVOTED BY SURFACE SIMILARITY.
EVALUATOR != BAT ORACLE.
```

`## HOLD` must explicitly retain:

```text
no automatic bridge discovery
no Terry/novel-math calibration claim
no public mathband@1 operator
no CLI/schema promotion
no theorem-prover/CAS claim
no literature-priority claim
no semantic or historical equivalence claim
```

`## Next gate` should name Level 1 (known partial bridge) as the next research specimen. Do not jump directly to Terry or a novel cross-disciplinary candidate.

- [ ] **Step 4: Run the complete verification floor**

Run all of the following:

```bash
python -m unittest tests.test_mathband -v
python -m unittest discover -s tests -v
python -m compileall dogram tests
```

Expected:

```text
all MathBand tests PASS
full Dogram unit suite PASS
compileall PASS
```

Do not claim success from the MathBand test file alone.

- [ ] **Step 5: Inspect the diff for forbidden promotion**

Run:

```bash
git diff --check
git diff -- dogram/engine.py dogram/cli.py pyproject.toml
git status --short
```

Expected:

```text
git diff --check -> no output
dogram/engine.py -> no diff
dogram/cli.py -> no diff
pyproject.toml -> no diff
status -> only intended MathBand/research files
```

- [ ] **Step 6: Commit the research receipt and constitutional regression**

```bash
git add dogram/mathband.py tests/test_mathband.py tests/fixtures/mathband_incubator_001.json research/MATHBAND-INCUBATOR-001.md
git commit -m "Research: receipt MathBand incubator bats"
```

- [ ] **Step 7: Freshly verify the committed head**

Run:

```bash
git status --short
git log -1 --oneline
python -m unittest discover -s tests -v
python -m compileall dogram tests
```

Expected:

```text
working tree clean
HEAD is the MathBand receipt commit
full unit suite PASS
compileall PASS
```

Only after this fresh committed-head verification should the branch be offered for review/PR.
