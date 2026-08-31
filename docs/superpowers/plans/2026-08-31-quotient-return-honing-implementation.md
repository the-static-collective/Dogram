# Quotient-Return Honing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the landed quotient-return research into one bounded internal Dogram honing: exact return-period helpers for the existing transverse model, a typed return relation for Productive Desync, frozen hostile receipts, and no expansion of Dogram's public operator or authority surface.

**Architecture:** Keep all finite return arithmetic inside `dogram/transverse.py`, because the formulas are exact consequences of the current `Z_m x Z_n` quotient model. Keep `ReturnRelation` inside `dogram/productive_desync.py`, because this slice has one executable consumer and does not justify a generic return subsystem. Productive Desync consumes the declared relation; it does not infer a quotient, decoder, history, fiber law, or holonomy. `omega.py`, the Mathal VM, proposal grammar, phase gate, public engine registry, and bootstrap registry remain untouched.

**Tech Stack:** Python 3.12 standard library only; `dataclasses`, `math.gcd`, `unittest`; existing Dogram CI and constitutional checks.

**Spec:** `docs/superpowers/specs/2026-08-31-quotient-return-calculus-design.md`

## Global Constraints

- Keep project dependencies exactly `[]`.
- Keep public `dogram.engine.OPERATORS` exactly `{("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)}`.
- Keep `build_bootstrap_registry().ids()` unchanged.
- Add no public `return@1`, `holonomy@1`, `monodromy@1`, `coherence@1`, `lift@1`, or other public operator.
- Do not modify `dogram/omega.py`, `dogram/proposal.py`, `dogram/gate.py`, `dogram/program.py`, `dogram/vm.py`, or the Ω receipt schema.
- Preserve `POTENTIAL REACHABILITY != ACTUAL HISTORY`.
- Preserve `GENERATOR CLOSURE != DECLARED WORD != ACTUAL HISTORY`.
- Preserve `QUOTIENT RETURN != EXACT CARRIER RETURN != HISTORY RETURN`.
- Preserve `NO DECLARED FIBER LAW -> NO HOLONOMY CLAIM`.
- Productive Desync remains a classifier of supplied facts; it must not choose or infer the return relation.
- Invalid integer inputs fail closed; `bool` is not accepted as an integer.
- Implementation is TDD-first and every task ends with a fresh green commit.

---

## File Structure

**Modify**

- `dogram/transverse.py` — exact quotient-sheet return period, exact carrier-return period, finite return debt.
- `dogram/productive_desync.py` — `ReturnRelation` plus classifier migration away from the broad return Boolean.
- `tests/test_transverse.py` — closed-form tests, independent period oracle, fixture verification.
- `tests/test_productive_desync.py` — typed relation validation and relation-scope controls.
- `README.md` — one factual internal-kernel status sentence after executable verification is green.
- `research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md` — update status and link frozen executable witnesses.

**Create**

- `tests/fixtures/return_relation/z6x9-r1.json`
- `tests/fixtures/return_relation/z8x12-r4.json`
- `tests/fixtures/return_relation/coprime-z5x7-r1.json`
- `tests/fixtures/return_relation/exact-return-z6x9-r6.json`
- `tests/fixtures/return_relation/multigenerator-word-control.json`
- `tests/fixtures/return_relation/productive-desync-scope-control.json`
- `research/QUOTIENT-RETURN-RECEIPTS-001.md`

**Do not create**

- `dogram/return.py`
- `dogram/holonomy.py`
- a new intrinsic or stdlib Mathal
- a new public specimen or receipt schema

---

### Task 1: Add Exact Return-Period Algebra

**Files:**
- Modify: `dogram/transverse.py`
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Produces `quotient_return_period(m: int, n: int, r: int) -> int`
- Produces `exact_carrier_return_period(m: int, r: int) -> int`
- Produces `return_debt(m: int, n: int, r: int) -> int`

- [ ] **Step 1: Replace the transverse import block in the test with the complete target import set**

```python
from dogram.transverse import (
    TransverseInputError,
    analyze_transverse,
    bounded_history_reach_count,
    bounded_history_sheet_trace,
    exact_carrier_return_period,
    quotient_return_period,
    return_debt,
    sheet_coordinate,
)
```

- [ ] **Step 2: Add four failing exact examples**

```python
    def test_z6_x_z9_r1_returns_to_sheet_before_carrier(self):
        self.assertEqual(quotient_return_period(6, 9, 1), 3)
        self.assertEqual(exact_carrier_return_period(6, 1), 6)
        self.assertEqual(return_debt(6, 9, 1), 2)

    def test_z8_x_z12_r4_is_quotient_inert_but_not_exactly_returned(self):
        self.assertEqual(quotient_return_period(8, 12, 4), 1)
        self.assertEqual(exact_carrier_return_period(8, 4), 2)
        self.assertEqual(return_debt(8, 12, 4), 2)

    def test_coprime_world_has_trivial_quotient_return_period(self):
        self.assertEqual(quotient_return_period(5, 7, 1), 1)
        self.assertEqual(exact_carrier_return_period(5, 1), 5)
        self.assertEqual(return_debt(5, 7, 1), 5)

    def test_r_divisible_by_m_is_exact_return_in_one_cycle(self):
        self.assertEqual(quotient_return_period(6, 9, 6), 1)
        self.assertEqual(exact_carrier_return_period(6, 6), 1)
        self.assertEqual(return_debt(6, 9, 6), 1)
```

- [ ] **Step 3: Run the four tests and verify RED**

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_z6_x_z9_r1_returns_to_sheet_before_carrier \
  tests.test_transverse.TransverseTests.test_z8_x_z12_r4_is_quotient_inert_but_not_exactly_returned \
  tests.test_transverse.TransverseTests.test_coprime_world_has_trivial_quotient_return_period \
  tests.test_transverse.TransverseTests.test_r_divisible_by_m_is_exact_return_in_one_cycle -v
```

Expected: import failure because the three helpers do not exist.

- [ ] **Step 4: Add strict single-generator validation**

In `dogram/transverse.py`:

```python
def _validate_generator(r: int) -> None:
    if not isinstance(r, int) or isinstance(r, bool):
        raise TransverseInputError("INVALID_GENERATOR", "generator must be an integer")
```

Rewrite `_validate_generators()` as:

```python
def _validate_generators(generators: tuple[int, ...]) -> None:
    if not isinstance(generators, tuple) or not generators:
        raise TransverseInputError("EMPTY_GENERATOR_FAMILY", "generators must be a non-empty tuple")
    for r in generators:
        _validate_generator(r)
```

- [ ] **Step 5: Add the three exact helpers**

```python
def quotient_return_period(m: int, n: int, r: int) -> int:
    """First positive bounded-cycle count returning to the original quotient sheet."""
    _validate_dimensions(m, n)
    _validate_generator(r)
    d = gcd(m, n)
    return d // gcd(d, r)


def exact_carrier_return_period(m: int, r: int) -> int:
    """First positive bounded-cycle count returning the first carrier coordinate."""
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        raise TransverseInputError("INVALID_DIMENSION", "m must be a positive integer")
    _validate_generator(r)
    return m // gcd(m, r)


def return_debt(m: int, n: int, r: int) -> int:
    """Number of quotient-return periods inside one exact carrier-return period."""
    quotient_period = quotient_return_period(m, n, r)
    exact_period = exact_carrier_return_period(m, r)
    if exact_period % quotient_period != 0:
        raise AssertionError("exact carrier return must refine quotient return")
    return exact_period // quotient_period
```

Add all three names to `__all__`.

- [ ] **Step 6: Run the four exact tests and verify GREEN**

Use the Step 3 command. Expected: 4 PASS.

- [ ] **Step 7: Add input-refusal tests**

```python
    def test_return_period_helpers_reject_invalid_generators(self):
        for bad in (True, 1.5, "1"):
            with self.assertRaises(TransverseInputError) as caught:
                quotient_return_period(6, 9, bad)
            self.assertEqual(caught.exception.reason_code, "INVALID_GENERATOR")

    def test_exact_return_period_rejects_invalid_dimension(self):
        with self.assertRaises(TransverseInputError) as caught:
            exact_carrier_return_period(0, 1)
        self.assertEqual(caught.exception.reason_code, "INVALID_DIMENSION")
```

- [ ] **Step 8: Run the refusal tests**

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_return_period_helpers_reject_invalid_generators \
  tests.test_transverse.TransverseTests.test_exact_return_period_rejects_invalid_dimension -v
```

Expected: 2 PASS.

- [ ] **Step 9: Commit**

```bash
git add dogram/transverse.py tests/test_transverse.py
git commit -m "feat: add transverse return-period math"
```

---

### Task 2: Pressure the Closed Forms with an Independent Oracle

**Files:**
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Consumes the three helpers from Task 1.
- Produces only independent test witnesses.

- [ ] **Step 1: Add independent test-only period walkers**

Near `brute_reach_count()`:

```python
def brute_quotient_return_period(m, n, r):
    from math import gcd

    d = gcd(m, n)
    sheet = 0
    for k in range(1, d + 1):
        sheet = (sheet + r) % d
        if sheet == 0:
            return k
    raise AssertionError((m, n, r, "quotient period not found"))


def brute_exact_carrier_return_period(m, r):
    state = 0
    for k in range(1, m + 1):
        state = (state + r) % m
        if state == 0:
            return k
    raise AssertionError((m, r, "carrier period not found"))
```

The oracle walks states; it does not call the production helpers or their closed forms.

- [ ] **Step 2: Add the exhaustive bounded check**

```python
    def test_return_period_formulas_match_independent_bounded_oracle(self):
        checked = 0
        for m in range(2, 21):
            for n in range(2, 21):
                for r in range(1, 21):
                    quotient = quotient_return_period(m, n, r)
                    exact = exact_carrier_return_period(m, r)
                    self.assertEqual(quotient, brute_quotient_return_period(m, n, r), (m, n, r))
                    self.assertEqual(exact, brute_exact_carrier_return_period(m, r), (m, n, r))
                    self.assertEqual(exact % quotient, 0, (m, n, r))
                    self.assertEqual(return_debt(m, n, r), exact // quotient, (m, n, r))
                    checked += 1
        self.assertEqual(checked, 7220)
```

- [ ] **Step 3: Run the bounded oracle**

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_return_period_formulas_match_independent_bounded_oracle -v
```

Expected: PASS and `checked == 7220`.

- [ ] **Step 4: Run all transverse tests**

```bash
python -m unittest tests.test_transverse -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_transverse.py
git commit -m "test: pressure quotient return periods by brute force"
```

---

### Task 3: Type the Productive-Desync Return Relation

**Files:**
- Modify: `dogram/productive_desync.py`
- Modify: `tests/test_productive_desync.py`

**Interfaces:**
- Produces `ReturnRelation`.
- Changes `assess_productive_desync` to consume `return_relation: ReturnRelation` instead of `returned_to_coherence: bool`.
- Preserves reason code `NO_COHERENCE_RETURN` for this bounded migration.

- [ ] **Step 1: Replace the test import**

```python
from dogram.productive_desync import ReturnRelation, assess_productive_desync
```

- [ ] **Step 2: Add failing ReturnRelation tests**

```python
class ReturnRelationTests(unittest.TestCase):
    def test_return_is_computed_from_declared_quotient_observations(self):
        relation = ReturnRelation(
            relation_id="sheet-return",
            quotient_id="phi-mod-3",
            anchor_before=[0, 0],
            anchor_after=[3, 0],
            quotient_before=0,
            quotient_after=0,
        )
        self.assertTrue(relation.returned)
        self.assertNotEqual(relation.anchor_before, relation.anchor_after)

    def test_nonreturn_is_computed_without_global_inference(self):
        relation = ReturnRelation(
            relation_id="carrier-return",
            quotient_id="exact-state",
            anchor_before=[0, 0],
            anchor_after=[3, 0],
            quotient_before=[0, 0],
            quotient_after=[3, 0],
        )
        self.assertFalse(relation.returned)

    def test_empty_relation_or_quotient_id_refuses(self):
        for field in ("relation_id", "quotient_id"):
            values = {
                "relation_id": "sheet-return",
                "quotient_id": "phi-mod-3",
                "anchor_before": [0, 0],
                "anchor_after": [3, 0],
                "quotient_before": 0,
                "quotient_after": 0,
            }
            values[field] = ""
            with self.assertRaises(ValueError):
                ReturnRelation(**values)
```

- [ ] **Step 3: Run the relation tests and verify RED**

```bash
python -m unittest tests.test_productive_desync.ReturnRelationTests -v
```

Expected: import failure because `ReturnRelation` does not exist.

- [ ] **Step 4: Implement `ReturnRelation` before `ProductiveDesyncAssessment`**

```python
@dataclass(frozen=True)
class ReturnRelation:
    relation_id: str
    quotient_id: str
    anchor_before: Any
    anchor_after: Any
    quotient_before: Any
    quotient_after: Any

    def __post_init__(self) -> None:
        if not isinstance(self.relation_id, str) or not self.relation_id:
            raise ValueError("relation_id must be a non-empty string")
        if not isinstance(self.quotient_id, str) or not self.quotient_id:
            raise ValueError("quotient_id must be a non-empty string")

    @property
    def returned(self) -> bool:
        return self.quotient_before == self.quotient_after

    def to_data(self) -> dict[str, Any]:
        return {
            "relation_id": self.relation_id,
            "quotient_id": self.quotient_id,
            "anchor_before": self.anchor_before,
            "anchor_after": self.anchor_after,
            "quotient_before": self.quotient_before,
            "quotient_after": self.quotient_after,
            "returned": self.returned,
        }
```

Add `ReturnRelation` to `__all__`.

- [ ] **Step 5: Run relation tests and verify GREEN**

```bash
python -m unittest tests.test_productive_desync.ReturnRelationTests -v
```

Expected: 3 PASS.

- [ ] **Step 6: Replace the assessment field**

In `ProductiveDesyncAssessment`, replace:

```python
returned_to_coherence: bool
```

with:

```python
return_relation: ReturnRelation
```

In `to_data()`, replace the old Boolean entry with:

```python
"return_relation": self.return_relation.to_data(),
```

- [ ] **Step 7: Replace the classifier argument and gate**

Change the function argument to:

```python
return_relation: ReturnRelation,
```

Validate it with:

```python
if not isinstance(cut_declared, bool):
    raise ValueError("cut_declared must be boolean")
if not isinstance(return_relation, ReturnRelation):
    raise ValueError("return_relation must be ReturnRelation")
```

Replace the old coherence-return branch with:

```python
elif not return_relation.returned:
    status, reason_code = "REFUSE", "NO_COHERENCE_RETURN"
```

Return the supplied relation in `ProductiveDesyncAssessment`.

- [ ] **Step 8: Migrate the existing test helper**

In `ProductiveDesyncTests.assess()`, use:

```python
"return_relation": ReturnRelation(
    relation_id="bounded-coherence-return",
    quotient_id="declared-coherence-cut",
    anchor_before={"sheet": 0},
    anchor_after={"sheet": 0},
    quotient_before=0,
    quotient_after=0,
),
```

Replace the prior no-return test with:

```python
    def test_no_declared_return_refuses_bounded_desync_label(self):
        relation = ReturnRelation(
            relation_id="bounded-coherence-return",
            quotient_id="declared-coherence-cut",
            anchor_before={"sheet": 0},
            anchor_after={"sheet": 1},
            quotient_before=0,
            quotient_after=1,
        )
        result = self.assess(return_relation=relation)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "NO_COHERENCE_RETURN"))
```

Add:

```python
    def test_assessment_receipt_preserves_return_scope(self):
        result = self.assess()
        relation = result.to_data()["return_relation"]
        self.assertEqual(relation["relation_id"], "bounded-coherence-return")
        self.assertEqual(relation["quotient_id"], "declared-coherence-cut")
        self.assertTrue(relation["returned"])
```

- [ ] **Step 9: Run all Productive Desync tests**

```bash
python -m unittest tests.test_productive_desync -v
```

Expected: all PASS.

- [ ] **Step 10: Prove the broad production/test field is gone**

```bash
if grep -R "returned_to_coherence" -n dogram tests/test_productive_desync.py; then
  echo "broad return field still present"
  exit 1
fi
```

Expected: exit 0 with no matches. Historical specs and research notes are intentionally outside this scan.

- [ ] **Step 11: Commit**

```bash
git add dogram/productive_desync.py tests/test_productive_desync.py
git commit -m "feat: scope productive desync return relation"
```

---

### Task 4: Freeze Six Hostile Return Specimens

**Files:**
- Create the six `tests/fixtures/return_relation/*.json` files listed above.
- Modify `tests/test_transverse.py`.
- Modify `tests/test_productive_desync.py`.

**Interfaces:**
- Consumes all Task 1 and Task 3 APIs.
- Produces durable frozen specimens only.

- [ ] **Step 1: Add return-fixture paths and loaders to both test modules**

In `tests/test_transverse.py`:

```python
RETURN_FIXTURES = ROOT / "tests" / "fixtures" / "return_relation"


def load_return_fixture(name):
    return json.loads((RETURN_FIXTURES / name).read_text())
```

In `tests/test_productive_desync.py`, add:

```python
import json
import pathlib

ROOT = pathlib.Path(__file__).parents[1]
RETURN_FIXTURES = ROOT / "tests" / "fixtures" / "return_relation"


def load_return_fixture(name):
    return json.loads((RETURN_FIXTURES / name).read_text())
```

- [ ] **Step 2: Write the failing fixture-count contract**

```python
    def test_six_return_relation_fixtures_are_frozen(self):
        names = sorted(path.name for path in RETURN_FIXTURES.glob("*.json"))
        self.assertEqual(
            names,
            [
                "coprime-z5x7-r1.json",
                "exact-return-z6x9-r6.json",
                "multigenerator-word-control.json",
                "productive-desync-scope-control.json",
                "z6x9-r1.json",
                "z8x12-r4.json",
            ],
        )
```

- [ ] **Step 3: Run the count contract and verify RED**

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_six_return_relation_fixtures_are_frozen -v
```

Expected: FAIL because the six files are absent.

- [ ] **Step 4: Create `z6x9-r1.json`**

```json
{
  "id": "RETURN-R1-Z6X9-R1",
  "system": {"m": 6, "n": 9, "r": 1},
  "expected": {
    "quotient_return_period": 3,
    "exact_carrier_return_period": 6,
    "return_debt": 2,
    "after_quotient_period": {"cycles": 3, "sheet_returned": true, "carrier_returned": false},
    "after_exact_period": {"cycles": 6, "sheet_returned": true, "carrier_returned": true}
  }
}
```

- [ ] **Step 5: Create `z8x12-r4.json`**

```json
{
  "id": "RETURN-R2-Z8X12-R4",
  "system": {"m": 8, "n": 12, "r": 4},
  "expected": {
    "quotient_return_period": 1,
    "exact_carrier_return_period": 2,
    "return_debt": 2,
    "first_cycle_sheet_returned": true,
    "first_cycle_carrier_returned": false
  }
}
```

- [ ] **Step 6: Create `coprime-z5x7-r1.json`**

```json
{
  "id": "RETURN-R3-COPRIME-Z5X7-R1",
  "system": {"m": 5, "n": 7, "r": 1},
  "expected": {
    "sheet_count": 1,
    "quotient_return_period": 1,
    "exact_carrier_return_period": 5,
    "return_debt": 5,
    "strict_reachability_lift": false
  }
}
```

- [ ] **Step 7: Create `exact-return-z6x9-r6.json`**

```json
{
  "id": "RETURN-R4-EXACT-Z6X9-R6",
  "system": {"m": 6, "n": 9, "r": 6},
  "expected": {
    "quotient_return_period": 1,
    "exact_carrier_return_period": 1,
    "return_debt": 1,
    "first_cycle_sheet_returned": true,
    "first_cycle_carrier_returned": true
  }
}
```

- [ ] **Step 8: Create `multigenerator-word-control.json`**

```json
{
  "id": "RETURN-R5-MULTIGENERATOR-WORD",
  "system": {"m": 6, "n": 9, "generators": [1, 2]},
  "word_a": [1, 2],
  "word_b": [1, 1],
  "expected": {
    "closure_reach_count": 54,
    "word_a_sheet_trace": [0, 1, 0],
    "word_a_returns": true,
    "word_b_sheet_trace": [0, 1, 2],
    "word_b_returns": false
  }
}
```

- [ ] **Step 9: Create `productive-desync-scope-control.json`**

```json
{
  "id": "RETURN-R6-PRODUCTIVE-DESYNC-SCOPE",
  "assessment": {
    "target_preserved": true,
    "execution_residual": {"step_trace": {"changed": true}},
    "baseline_reach_count": 18,
    "historical_reach_count": 36,
    "closure_reach_count": 54,
    "cut_declared": true,
    "cut_budget": 1,
    "cuts_used": 1
  },
  "coarse_return": {
    "relation_id": "sheet-return",
    "quotient_id": "phi-mod-3",
    "anchor_before": [0, 0],
    "anchor_after": [3, 0],
    "quotient_before": 0,
    "quotient_after": 0,
    "expected_status": "WITNESS"
  },
  "fine_return": {
    "relation_id": "carrier-return",
    "quotient_id": "exact-state",
    "anchor_before": [0, 0],
    "anchor_after": [3, 0],
    "quotient_before": [0, 0],
    "quotient_after": [3, 0],
    "expected_status": "REFUSE",
    "expected_reason_code": "NO_COHERENCE_RETURN"
  }
}
```

- [ ] **Step 10: Add formula and word fixture verification**

In `tests/test_transverse.py`:

```python
    def test_return_relation_fixtures_match_exact_transverse_math(self):
        for name in (
            "z6x9-r1.json",
            "z8x12-r4.json",
            "coprime-z5x7-r1.json",
            "exact-return-z6x9-r6.json",
        ):
            fixture = load_return_fixture(name)
            system = fixture["system"]
            expected = fixture["expected"]
            m, n, r = system["m"], system["n"], system["r"]
            self.assertEqual(quotient_return_period(m, n, r), expected["quotient_return_period"], name)
            self.assertEqual(exact_carrier_return_period(m, r), expected["exact_carrier_return_period"], name)
            self.assertEqual(return_debt(m, n, r), expected["return_debt"], name)

    def test_same_generator_closure_can_hold_returning_and_nonreturning_words(self):
        fixture = load_return_fixture("multigenerator-word-control.json")
        system = fixture["system"]
        analysis = analyze_transverse(system["m"], system["n"], tuple(system["generators"]))
        self.assertEqual(analysis.closure_reach_count, fixture["expected"]["closure_reach_count"])
        trace_a = bounded_history_sheet_trace(system["m"], system["n"], tuple(fixture["word_a"]))
        trace_b = bounded_history_sheet_trace(system["m"], system["n"], tuple(fixture["word_b"]))
        self.assertEqual(list(trace_a), fixture["expected"]["word_a_sheet_trace"])
        self.assertEqual(trace_a[-1] == trace_a[0], fixture["expected"]["word_a_returns"])
        self.assertEqual(list(trace_b), fixture["expected"]["word_b_sheet_trace"])
        self.assertEqual(trace_b[-1] == trace_b[0], fixture["expected"]["word_b_returns"])
```

- [ ] **Step 11: Add Productive Desync scope-fixture verification**

```python
    def test_coarse_return_can_witness_while_fine_return_refuses_for_same_other_facts(self):
        fixture = load_return_fixture("productive-desync-scope-control.json")
        shared = fixture["assessment"]

        def build_relation(data):
            return ReturnRelation(
                relation_id=data["relation_id"],
                quotient_id=data["quotient_id"],
                anchor_before=data["anchor_before"],
                anchor_after=data["anchor_after"],
                quotient_before=data["quotient_before"],
                quotient_after=data["quotient_after"],
            )

        coarse = assess_productive_desync(**shared, return_relation=build_relation(fixture["coarse_return"]))
        fine = assess_productive_desync(**shared, return_relation=build_relation(fixture["fine_return"]))
        self.assertEqual(coarse.status, fixture["coarse_return"]["expected_status"])
        self.assertEqual(
            (fine.status, fine.reason_code),
            (
                fixture["fine_return"]["expected_status"],
                fixture["fine_return"]["expected_reason_code"],
            ),
        )
```

- [ ] **Step 12: Run both focused suites**

```bash
python -m unittest tests.test_transverse tests.test_productive_desync -v
```

Expected: all PASS.

- [ ] **Step 13: Commit**

```bash
git add tests/fixtures/return_relation tests/test_transverse.py tests/test_productive_desync.py
git commit -m "test: freeze quotient-return hostile specimens"
```

---

### Task 5: Preserve the Executable Receipt

**Files:**
- Create: `research/QUOTIENT-RETURN-RECEIPTS-001.md`
- Modify: `research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md`
- Modify: `README.md`

**Interfaces:**
- Consumes green behavior from Tasks 1-4.
- Produces durable documentation only.

- [ ] **Step 1: Create the executable receipt ledger with all now-known fixed facts**

```markdown
# QUOTIENT-RETURN RECEIPTS-001

**Status:** FROZEN EXECUTABLE WITNESSES · INTERNAL RESEARCH KERNEL · NO PUBLIC OPERATOR

## Laws frozen

- `Lambda = gcd(m,n) / gcd(gcd(m,n), r)` is the single-generator quotient-sheet return period.
- `M = m / gcd(m,r)` is the exact first-coordinate carrier-return period for the declared bounded-cycle action.
- `Lambda | M`.
- `mu = M / Lambda` is the narrowly typed finite return debt.
- same generator closure does not determine the return of a particular declared word.
- Productive Desync consumes a scoped return relation; coarse return does not imply fine return.

## Frozen finite fixtures

| fixture | quotient period | exact period | debt | control |
| --- | ---: | ---: | ---: | --- |
| `z6x9-r1.json` | 3 | 6 | 2 | quotient before carrier |
| `z8x12-r4.json` | 1 | 2 | 2 | quotient-inert cut |
| `coprime-z5x7-r1.json` | 1 | 5 | 5 | trivial quotient / no hidden sheet |
| `exact-return-z6x9-r6.json` | 1 | 1 | 1 | exact return |

`multigenerator-word-control.json` freezes `GENERATOR CLOSURE != DECLARED WORD`.

`productive-desync-scope-control.json` freezes coarse-return witness vs fine-return refusal with every other classifier input held fixed.

## Hard refusals

```text
QUOTIENT RETURN != EXACT CARRIER RETURN
EXACT CARRIER RETURN != HISTORY RETURN
GENERATOR CLOSURE != DECLARED WORD
QUOTIENT RETURN != HOLONOMY
REACHABILITY GAIN != TRUTH / EVIDENCE / AUTHORITY
```

## Exact-head verification

The final implementation task appends the literal commit SHA and literal observed test count from the verification commands, followed by `PASS` for compile, constitutional floor, and Omega scope scan.
```

- [ ] **Step 2: Update the FATDOG status**

Change its status line to:

```text
RESEARCH + FROZEN EXECUTABLE RETURN WITNESSES · NO NEW PUBLIC OPERATOR
```

Add a short executable-witness section naming:

```text
tests/test_transverse.py
tests/test_productive_desync.py
tests/fixtures/return_relation/
research/QUOTIENT-RETURN-RECEIPTS-001.md
```

Do not rewrite the derivation or conditional holonomy boundary.

- [ ] **Step 3: Add one factual README sentence**

Append to the internal Productive-Desync/transverse paragraph:

```markdown
The internal transverse/Productive-Desync research kernel also carries typed quotient-return receipts: exact finite sheet-return and carrier-return periods remain separate, declared generator closure remains separate from actual word/history, and Productive Desync consumes an explicitly scoped return relation. This adds no public operator or holonomy semantics.
```

- [ ] **Step 4: Run focused tests and compile**

```bash
python -m unittest tests.test_transverse tests.test_productive_desync -v
python -m compileall -q dogram tests
```

Expected: all PASS and compile exits 0.

- [ ] **Step 5: Commit**

```bash
git add README.md research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md research/QUOTIENT-RETURN-RECEIPTS-001.md
git commit -m "docs: receipt executable quotient-return honing"
```

---

### Task 6: Exact-Head Constitutional Verification and Seal

**Files:**
- Modify: `research/QUOTIENT-RETURN-RECEIPTS-001.md`
- Verify unchanged: `dogram/omega.py`, `dogram/proposal.py`, `dogram/gate.py`, `dogram/engine.py`, `dogram/registry.py`, `dogram/program.py`, `dogram/vm.py`

**Interfaces:**
- Produces the merge-ready exact-head receipt.

- [ ] **Step 1: Run the full unit suite**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests PASS. Copy the literal observed test count into the receipt ledger.

- [ ] **Step 2: Run compile**

```bash
python -m compileall -q dogram tests
```

Expected: exit 0.

- [ ] **Step 3: Run the exact CI constitutional floor**

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

- [ ] **Step 4: Run the exact CI Omega scope scan**

```bash
python - <<'PY'
from pathlib import Path

forbidden = ["eval(", "exec(", "importlib", "subprocess", "socket.", "requests."]
for path in Path("dogram").rglob("*.py"):
    text = path.read_text()
    for token in forbidden:
        assert token not in text, (path, token)

for path in [
    Path("dogram/proposal.py"),
    Path("dogram/gate.py"),
    Path("dogram/omega.py"),
    Path("dogram/reify.py"),
]:
    text = path.read_text()
    for token in ("TODO", "TBD", "FIXME", "PLACEHOLDER"):
        assert token not in text, (path, token)

print("scope scan OK")
PY
```

Expected: `scope scan OK`.

- [ ] **Step 5: Verify the implementation diff is constitutionally narrow**

```bash
BASE_SHA=$(git merge-base HEAD main)
git diff --name-only "$BASE_SHA"...HEAD
```

Expected production modifications are exactly:

```text
dogram/productive_desync.py
dogram/transverse.py
```

The output must not contain:

```text
dogram/engine.py
dogram/gate.py
dogram/omega.py
dogram/program.py
dogram/proposal.py
dogram/registry.py
dogram/vm.py
```

- [ ] **Step 6: Capture the literal exact-head SHA**

```bash
git rev-parse HEAD
```

Copy the printed SHA into `research/QUOTIENT-RETURN-RECEIPTS-001.md`. On the same receipt lines, record the literal test count from Step 1 and these exact status strings:

```text
compile: PASS
constitutional_floor: PASS
omega_scope_scan: PASS
public_operator_floor: unchanged
bootstrap_registry: unchanged
omega.py: unchanged
proposal.py: unchanged
gate.py: unchanged
```

- [ ] **Step 7: Commit the receipt seal**

```bash
git add research/QUOTIENT-RETURN-RECEIPTS-001.md
git commit -m "research: seal quotient-return executable receipts"
```

- [ ] **Step 8: Re-run full tests and compile after the receipt-only commit**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Expected: same green behavior.

---

## Plan Self-Review

**Spec coverage:** typed return relation is Task 3; exact quotient/carrier periods and debt are Tasks 1-2; all six hostile specimens are Task 4; executable receipt is Task 5; constitutional verification is Task 6; no-holonomy and no-public-operator boundaries are global constraints and Task 5 refusals.

**Completeness:** every code-changing step includes exact code or an exact command. Runtime-generated values are captured by explicit commands and copied literally into the final receipt rather than being guessed in advance.

**Type consistency:** `ReturnRelation` is defined once in Task 3 and reused unchanged later. The three transverse helper names/signatures are fixed in Task 1 and reused unchanged in Tasks 2, 4, and 5. `NO_COHERENCE_RETURN` remains the classifier reason code for this bounded migration.

---

## Completion Boundary

The implementation is complete only when Dogram can calculate and receipt:

```text
RETURN MUST NAME ITS QUOTIENT.
THE QUOTIENT MAY CLOSE WHILE THE CARRIER LIFTS.
KEEP THE FINER RESIDUAL.
GENERATOR CLOSURE != DECLARED WORD != ACTUAL HISTORY.
NO FIBER LAW -> NO HOLONOMY CLAIM.
```

No public operator, generic return engine, optimizer, automatic quotient inference, or authority-bearing semantic conclusion is part of this plan.
