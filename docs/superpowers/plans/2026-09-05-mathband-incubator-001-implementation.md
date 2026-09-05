# MATHBAND-INCUBATOR-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an internal Dogram research kernel that pressure-tests declared mathematical bridges, preserves partial/unmapped/extra/residual structure, and survives the Five Bats without adding a public Dogram operator.

**Architecture:** Keep v0 finite, exact-first, and fixture-driven. `dogram/mathband.py` owns only deterministic receipt classification over already-constituted finite probe observations; the JSON fixture and independent test-side mathematical oracles construct the complex-number and matrix voices so the evaluator cannot generate or grade its own bats. Known exact bridges calibrate the receipt before partial, false-friend, documented cross-discipline, or novel bridges are admitted.

**Tech Stack:** Python 3.12 standard library only; frozen dataclasses; `unittest`; JSON fixtures; existing Dogram operator floor.

**Spec:** `docs/superpowers/specs/2026-09-05-mathband-incubator-001-design.md`

## Global Constraints

- Status remains `EXPERIMENTAL ARCHITECTURAL INCUBATOR · NO PUBLIC OPERATOR ADMITTED`.
- Dogram law remains: `DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.`
- Production dependencies remain empty; do not modify `pyproject.toml` dependencies.
- Do not modify `dogram/engine.py` or add `mathband@1` to `OPERATORS`.
- No CLI route, schema promotion, symbolic parser, theorem prover, CAS, network dependency, automatic bridge discovery, or semantic/evidentiary authority.
- Probe families and decisive/load-bearing probes are frozen before evaluation.
- `EVALUATOR != BAT ORACLE`: fixture generation and hostile expected behavior stay outside `dogram.mathband`.
- No scalar `match_score`; a decisive broken probe cannot be overruled by aggregate similarity.
- `UNMAPPED != FALSE`, `EXTRA != ERROR`, `APPROXIMATE != EXACT`, `BRIDGE != IDENTITY`, `PRESERVED UNDER P != GLOBALLY EQUIVALENT`.
- Exact arithmetic is preferred. Numeric tolerance exists only to retain explicit residuals; it must never silently convert approximate equality into exact equality.

---

## File Structure

- Create `dogram/mathband.py` — frozen receipt types, validation, assumption gate, deterministic probe classification, decisive-probe handling. No discipline-specific mathematics.
- Create `tests/fixtures/mathband_incubator_001.json` — frozen inputs for exact rotation calibration and all Five Bats.
- Create `tests/test_mathband.py` — independent mathematical oracles plus TDD coverage for exact bridge, Five Bats, residuals, refusals, deterministic output, and non-promotion.
- Create `research/MATHBAND-INCUBATOR-001.md` — durable research receipt with verified outcomes and HOLD boundary.
- Do not modify `dogram/engine.py`, `dogram/cli.py`, `pyproject.toml`, or public schemas.

---

### Task 1: Exact Receipt Floor and Calibration Bridge

**Files:**
- Create: `dogram/mathband.py`
- Create: `tests/test_mathband.py`
- Create: `tests/fixtures/mathband_incubator_001.json`

**Interfaces:**
- Produces `ProbeObservation`, `ProbeOutcome`, `MathBandReceipt`, `evaluate_bridge(...)`.
- `evaluate_bridge` consumes already-computed common-stage observations; it never computes complex or matrix mathematics itself.

- [ ] **Step 1: Create the frozen calibration fixture**

Create `tests/fixtures/mathband_incubator_001.json`:

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

- [ ] **Step 2: Write independent mathematical oracles and the first failing test**

Create `tests/test_mathband.py`:

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


def _complex_apply_n(pair: tuple[int, int], turns: int) -> tuple[int, int]:
    result = pair
    for _ in range(turns):
        result = _complex_quarter_turn(result)
    return result


def _matrix_apply(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    pair: tuple[int, int],
) -> tuple[int, int]:
    (m00, m01), (m10, m11) = matrix
    a, b = pair
    return (m00 * a + m01 * b, m10 * a + m11 * b)


def _matrix_apply_n(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    pair: tuple[int, int],
    turns: int,
) -> tuple[int, int]:
    result = pair
    for _ in range(turns):
        result = _matrix_apply(matrix, result)
    return result


def _norm_sq(pair: tuple[int, int]) -> int:
    a, b = pair
    return a * a + b * b


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
        self.assertIsNone(receipt.first_decisive_probe)
        self.assertEqual(receipt.exactness, "exact")
        self.assertEqual(receipt.refusals, ())
```

The complex and matrix action helpers are the independent bat oracle. They must remain in tests, not move into `dogram.mathband`.

- [ ] **Step 3: Run the test to verify RED**

```bash
python -m unittest tests.test_mathband.MathBandTests.test_exact_complex_matrix_calibration_preserves_all_probes -v
```

Expected: **ERROR/FAIL** because `dogram.mathband` does not exist.

- [ ] **Step 4: Implement the minimal exact receipt floor**

Create `dogram/mathband.py` with these exact public interfaces:

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

Task-1 behavior:

```python
# validate non-empty bridge/voice refs
# validate non-empty unique probe names
# reject unknown comparison values
# exact + defined + left == right -> PRESERVED
# exact + defined + left != right + must_preserve -> BROKEN
# exact + defined + left != right + not must_preserve -> CHANGED
# first_decisive_probe = first input-order decisive BROKEN outcome
# exactness = "exact"
# until later red tests exist, ignore caller-supplied transforms/extras/lossy_steps and emit empty tuples
```

Export only:

```python
__all__ = [
    "MathBandReceipt",
    "ProbeObservation",
    "ProbeOutcome",
    "evaluate_bridge",
]
```

- [ ] **Step 5: Run the calibration test to verify GREEN**

```bash
python -m unittest tests.test_mathband.MathBandTests.test_exact_complex_matrix_calibration_preserves_all_probes -v
```

Expected: **PASS**.

- [ ] **Step 6: Commit Task 1**

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
- Consumes Task-1 interfaces.
- Makes receipt semantics independent of familiar names/order while preserving a caller-declared representation transform separately.

- [ ] **Step 1: Extend fixture controls**

Under `calibration`, add:

```json
"rename_prefix": "bat-renamed",
"gauge_transform": "common_integer_scale:7"
```

- [ ] **Step 2: Write failing Rename and Gauge tests**

Add:

```python
def _semantic_signature(receipt) -> tuple[tuple[str, object, object], ...]:
    return tuple(sorted((outcome.status, outcome.left, outcome.right) for outcome in receipt.outcomes))
```

Add:

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
    self.assertIsNone(attacked.first_decisive_probe)


def test_gauge_bat_preserves_relation_and_receipts_common_scale(self) -> None:
    scale = self.calibration["scale_factor"]
    scaled_pairs = tuple((a * scale, b * scale) for a, b in self.pairs)
    probes = tuple(
        ProbeObservation(
            name=f"scaled:{a},{b}",
            left=_complex_quarter_turn((a, b)),
            right=_matrix_apply(self.matrix, (a, b)),
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
```

- [ ] **Step 3: Run to verify RED**

```bash
python -m unittest \
  tests.test_mathband.MathBandTests.test_rename_bat_preserves_semantics_under_reordering_and_renaming \
  tests.test_mathband.MathBandTests.test_gauge_bat_preserves_relation_and_receipts_common_scale -v
```

Expected: Gauge test **FAILS** because Task 1 intentionally discarded `declared_transforms`.

- [ ] **Step 4: Implement only Rename/Gauge behavior**

```python
# retain declared_transforms exactly as an immutable tuple
# never inspect names when deciding equality
# preserve input probe order; do not sort inside evaluator
```

- [ ] **Step 5: Run MathBand tests**

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS**.

- [ ] **Step 6: Commit Task 2**

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
- Adds `UNMAPPED`, explicit extra structure, and whole-bridge refusal for missing assumptions.

- [ ] **Step 1: Extend the fixture**

Add:

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

- [ ] **Step 2: Write failing Domain Bat test**

```python
def test_domain_bat_keeps_outside_domain_unmapped(self) -> None:
    inside = tuple(self.fixture["domain_bat"]["inside_pair"])
    probes = (
        ProbeObservation(
            "inside-domain",
            _complex_quarter_turn(inside),
            _matrix_apply(self.matrix, inside),
            decisive=True,
        ),
        ProbeObservation(
            "outside-domain",
            None,
            None,
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
```

- [ ] **Step 3: Write failing Extra-Voice and refusal tests**

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

- [ ] **Step 4: Run to verify RED**

```bash
python -m unittest \
  tests.test_mathband.MathBandTests.test_domain_bat_keeps_outside_domain_unmapped \
  tests.test_mathband.MathBandTests.test_extra_voice_bat_preserves_unmatched_structure \
  tests.test_mathband.MathBandTests.test_missing_required_assumption_refuses_without_grading_probes -v
```

Expected: **FAIL** until domain/extras/refusal behavior exists.

- [ ] **Step 5: Implement assumption refusal exactly**

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

For any probe with either side undefined, emit:

```python
ProbeOutcome(
    name=probe.name,
    status="UNMAPPED",
    left=probe.left,
    right=probe.right,
    delta=None,
    residual=None,
    decisive=probe.decisive,
)
```

Retain `extra_a`, `extra_b`, and `lossy_steps` verbatim. Do not interpret or eliminate them.

- [ ] **Step 6: Run MathBand tests**

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS**.

- [ ] **Step 7: Commit Task 3**

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
- A false friend may pass many non-decisive probes; one frozen decisive failure still kills the declared bridge.

- [ ] **Step 1: Extend the fixture**

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

The false-friend matrix is a reflection-like action. The test oracle must compute every probe independently from the two actions; do not hard-code successful booleans merely to inflate the apparent match count.

- [ ] **Step 2: Write the failing False-Friend Bat test**

```python
def test_false_friend_bat_cannot_outvote_decisive_failure(self) -> None:
    pair = tuple(self.fixture["false_friend_bat"]["probe_pair"])
    false_matrix = tuple(tuple(row) for row in self.fixture["false_friend_bat"]["matrix"])

    complex_once = _complex_apply_n(pair, 1)
    false_once = _matrix_apply_n(false_matrix, pair, 1)
    complex_twice = _complex_apply_n(pair, 2)
    false_twice = _matrix_apply_n(false_matrix, pair, 2)
    complex_four = _complex_apply_n(pair, 4)
    false_four = _matrix_apply_n(false_matrix, pair, 4)

    probes = (
        ProbeObservation("norm-input", _norm_sq(pair), _norm_sq(pair)),
        ProbeObservation("norm-output", _norm_sq(complex_once), _norm_sq(false_once)),
        ProbeObservation("origin-fixed", _complex_apply_n((0, 0), 1), _matrix_apply_n(false_matrix, (0, 0), 1)),
        ProbeObservation("four-step-return", complex_four, false_four),
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
    self.assertEqual(receipt.first_decisive_probe, self.fixture["false_friend_bat"]["decisive_probe"])
```

This fixture gives a naïve 4/5 surface similarity while the predeclared load-bearing probe fails.

- [ ] **Step 3: Write failing residual tests**

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
            "approximate-probe",
            left,
            right,
            comparison="numeric",
            tolerance=tolerance,
            decisive=True,
        ),),
    )

    self.assertEqual(receipt.outcomes[0].status, "RESIDUAL")
    self.assertAlmostEqual(receipt.outcomes[0].residual, abs(left - right))
    self.assertEqual(receipt.exactness, "approximate")
    self.assertIsNone(receipt.first_decisive_probe)


def test_numeric_disagreement_outside_tolerance_breaks_decisive_probe(self) -> None:
    left, right, tolerance = self.fixture["residual_bat"]["outside_tolerance"]
    receipt = evaluate_bridge(
        bridge_ref="approximate-control",
        voice_a_ref="numeric-a",
        voice_b_ref="numeric-b",
        required_assumptions=(),
        provided_assumptions=(),
        probes=(ProbeObservation(
            "approximate-probe",
            left,
            right,
            comparison="numeric",
            tolerance=tolerance,
            decisive=True,
        ),),
    )

    self.assertEqual(receipt.outcomes[0].status, "BROKEN")
    self.assertGreater(receipt.outcomes[0].residual, tolerance)
    self.assertEqual(receipt.first_decisive_probe, "approximate-probe")
```

- [ ] **Step 4: Run to verify RED**

```bash
python -m unittest \
  tests.test_mathband.MathBandTests.test_false_friend_bat_cannot_outvote_decisive_failure \
  tests.test_mathband.MathBandTests.test_numeric_disagreement_within_tolerance_is_residual_not_exact \
  tests.test_mathband.MathBandTests.test_numeric_disagreement_outside_tolerance_breaks_decisive_probe -v
```

Expected: residual tests **FAIL** until numeric classification is implemented. False-friend behavior must also fail if decisive handling is incomplete.

- [ ] **Step 5: Implement numeric residual classification**

Add:

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

After all outcomes:

```python
first_decisive_probe = next(
    (
        outcome.name
        for outcome in outcomes
        if outcome.decisive and outcome.status == "BROKEN"
    ),
    None,
)
exactness = (
    "approximate"
    if any(outcome.status == "RESIDUAL" for outcome in outcomes) or lossy_steps
    else "exact"
)
```

The evaluator only consumes the predeclared `decisive` field. It never searches outputs for a convenient discriminator.

- [ ] **Step 6: Run MathBand tests**

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS**.

- [ ] **Step 7: Commit Task 4**

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
- Produces the durable research receipt.
- Proves MathBand remains outside the public `OPERATORS` registry.

- [ ] **Step 1: Add public-operator regression**

Add:

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

Expected: **PASS immediately**. If it fails, remove the accidental promotion; do not weaken the assertion.

- [ ] **Step 2: Add validation/determinism regression tests**

```python
def test_duplicate_probe_names_raise_deterministic_input_error(self) -> None:
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


def test_receipt_order_follows_predeclared_probe_order(self) -> None:
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
    self.assertEqual(
        tuple(outcome.name for outcome in receipt.outcomes),
        ("first", "second", "third"),
    )
```

Run:

```bash
python -m unittest tests.test_mathband -v
```

Expected: **PASS**. Task 1 already required unique-name validation; this test makes that constitutional assumption explicit.

- [ ] **Step 3: Write `research/MATHBAND-INCUBATOR-001.md`**

Use exactly these sections:

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

Only if verified by tests, record:

```text
BRIDGE != IDENTITY.
PRESERVED UNDER P != GLOBALLY EQUIVALENT.
UNMAPPED != FALSE.
EXTRA != ERROR.
APPROXIMATE != EXACT.
DECISIVE FAILURE CANNOT BE OUTVOTED BY SURFACE SIMILARITY.
EVALUATOR != BAT ORACLE.
```

`## HOLD` must retain:

```text
no automatic bridge discovery
no Terry/novel-math calibration claim
no public mathband@1 operator
no CLI/schema promotion
no theorem-prover/CAS claim
no literature-priority claim
no semantic or historical equivalence claim
```

`## Next gate` names **Level 1: one known partial bridge**. Do not jump directly to Terry or a novel cross-disciplinary candidate.

- [ ] **Step 4: Run complete verification**

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

- [ ] **Step 5: Inspect diff for forbidden promotion**

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

- [ ] **Step 6: Commit research receipt**

```bash
git add dogram/mathband.py tests/test_mathband.py tests/fixtures/mathband_incubator_001.json research/MATHBAND-INCUBATOR-001.md
git commit -m "Research: receipt MathBand incubator bats"
```

- [ ] **Step 7: Freshly verify committed head**

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

Only after this committed-head verification should the implementation branch be offered for review/PR.
