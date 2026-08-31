# Quotient-Return Honing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the landed quotient-return research into one bounded internal Dogram honing: exact return-period helpers for the existing transverse model, a typed return relation for Productive Desync, frozen hostile receipts, and no expansion of Dogram's public operator or authority surface.

**Architecture:** Keep all finite return arithmetic inside the existing internal transverse kernel, because the formulas are exact consequences of the current `Z_m x Z_n` quotient model. Keep the typed return relation adjacent to `PRODUCTIVE-DESYNC-001`, because this slice has only one executable consumer; do not create a generic return subsystem. Productive Desync consumes the declared return relation but does not infer a quotient, a decoder, a history, a fiber law, or holonomy. `omega.py`, the Mathal VM, proposal grammar, phase gate, public engine registry, and bootstrap registry remain byte-for-byte untouched.

**Tech Stack:** Python 3.12 standard library only; `dataclasses`, `math.gcd`, existing `unittest`; existing Dogram CI and constitutional checks.

**Spec:** `docs/superpowers/specs/2026-08-31-quotient-return-calculus-design.md`

## Global Constraints

- Keep project dependencies exactly `[]`.
- Keep public `dogram.engine.OPERATORS` exactly `{("delta", 1), ("rectangle", 1), ("ablate", 1), ("reach", 1)}`.
- Keep `build_bootstrap_registry().ids()` unchanged.
- Add no public `return@1`, `holonomy@1`, `monodromy@1`, `coherence@1`, `lift@1`, or other new public operator.
- Do not modify `dogram/omega.py`, `dogram/proposal.py`, `dogram/gate.py`, the VM, proposal grammar, or Ω receipt schema.
- Preserve `POTENTIAL REACHABILITY != ACTUAL HISTORY` and `GENERATOR CLOSURE != DECLARED WORD != ACTUAL HISTORY`.
- Preserve `QUOTIENT RETURN != EXACT CARRIER RETURN != HISTORY RETURN`.
- Preserve `NO DECLARED FIBER LAW -> NO HOLONOMY CLAIM`.
- Productive Desync remains a classifier of supplied facts; it must not infer or choose the quotient relation itself.
- Invalid integer inputs fail closed; `bool` is not accepted as an integer.
- Implementation is TDD-first and every task ends in a fresh green commit.

---

## File Structure

**Modify:**
- `dogram/transverse.py` — add exact single-generator quotient-return, exact-carrier-return, and return-debt helpers for the existing cyclic quotient model only.
- `dogram/productive_desync.py` — replace the unscoped `returned_to_coherence: bool` input with a typed `ReturnRelation` and preserve that relation in the assessment receipt.
- `tests/test_transverse.py` — add formula tests plus an independent brute-force return-period oracle.
- `tests/test_productive_desync.py` — add typed-return validation, coarse/fine return controls, and migrate existing classifier tests.
- `README.md` — after executable verification is green, add one factual internal-kernel status sentence; do not advertise a public operator.
- `research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md` — update status from research-only to research + frozen executable witnesses and point to the exact fixtures/tests.

**Create:**
- `tests/fixtures/return_relation/z6x9-r1.json`
- `tests/fixtures/return_relation/z8x12-r4.json`
- `tests/fixtures/return_relation/coprime-z5x7-r1.json`
- `tests/fixtures/return_relation/exact-return-z6x9-r6.json`
- `tests/fixtures/return_relation/multigenerator-word-control.json`
- `tests/fixtures/return_relation/productive-desync-scope-control.json`
- `research/QUOTIENT-RETURN-RECEIPTS-001.md` — concise executable receipt ledger for the six frozen specimens and exact-head verification.

**Do not create:**
- `dogram/return.py`
- `dogram/holonomy.py`
- any new intrinsic or stdlib Mathal
- any new public specimen/receipt schema

The first implementation has only one executable consumer of the typed return relation (`PRODUCTIVE-DESYNC-001`), so a generic return module would be premature.

---

### Task 1: Add Exact Return-Period Algebra to the Transverse Kernel

**Files:**
- Modify: `dogram/transverse.py`
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Consumes: existing `_validate_dimensions(m, n)` semantics from `dogram.transverse`.
- Produces:
  - `quotient_return_period(m: int, n: int, r: int) -> int`
  - `exact_carrier_return_period(m: int, r: int) -> int`
  - `return_debt(m: int, n: int, r: int) -> int`

- [ ] **Step 1: Add focused failing formula tests**

Append to `tests/test_transverse.py`:

```python
from dogram.transverse import (
    # existing imports...
    exact_carrier_return_period,
    quotient_return_period,
    return_debt,
)
```

Add:

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

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_z6_x_z9_r1_returns_to_sheet_before_carrier \
  tests.test_transverse.TransverseTests.test_z8_x_z12_r4_is_quotient_inert_but_not_exactly_returned \
  tests.test_transverse.TransverseTests.test_coprime_world_has_trivial_quotient_return_period \
  tests.test_transverse.TransverseTests.test_r_divisible_by_m_is_exact_return_in_one_cycle -v
```

Expected: import failure because the three helpers do not exist.

- [ ] **Step 3: Implement strict generator validation shared by the three helpers**

In `dogram/transverse.py`, add:

```python
def _validate_generator(r: int) -> None:
    if not isinstance(r, int) or isinstance(r, bool):
        raise TransverseInputError("INVALID_GENERATOR", "generator must be an integer")
```

Change `_validate_generators()` to call `_validate_generator()` for every member, preserving the existing reason code.

- [ ] **Step 4: Implement the three exact helpers**

Add below `sheet_coordinate()`:

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

Export all three in `__all__`.

- [ ] **Step 5: Run the focused tests and verify GREEN**

Run the command from Step 2.

Expected: 4 tests PASS.

- [ ] **Step 6: Add invalid-input tests**

Add:

```python
    def test_return_period_helpers_reject_bool_and_non_integer_generators(self):
        for bad in (True, 1.5, "1"):
            with self.assertRaises(TransverseInputError) as caught:
                quotient_return_period(6, 9, bad)
            self.assertEqual(caught.exception.reason_code, "INVALID_GENERATOR")

    def test_exact_return_period_rejects_invalid_dimension(self):
        with self.assertRaises(TransverseInputError) as caught:
            exact_carrier_return_period(0, 1)
        self.assertEqual(caught.exception.reason_code, "INVALID_DIMENSION")
```

- [ ] **Step 7: Run the invalid-input tests and verify GREEN**

Run:

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_return_period_helpers_reject_bool_and_non_integer_generators \
  tests.test_transverse.TransverseTests.test_exact_return_period_rejects_invalid_dimension -v
```

Expected: 2 tests PASS.

- [ ] **Step 8: Commit Task 1**

```bash
git add dogram/transverse.py tests/test_transverse.py
git commit -m "feat: add transverse return-period math"
```

---

### Task 2: Prove the Closed Forms with an Independent Bounded Oracle

**Files:**
- Modify: `tests/test_transverse.py`

**Interfaces:**
- Consumes: `quotient_return_period`, `exact_carrier_return_period`, `return_debt` from Task 1.
- Produces: independent brute-force test witnesses; no production API.

- [ ] **Step 1: Add brute-force period helpers to the test module**

Near `brute_reach_count()`, add:

```python
def brute_quotient_return_period(m, n, r):
    d = __import__("math").gcd(m, n)
    sheet = 0
    for k in range(1, d + 1):
        sheet = (sheet + r) % d
        if sheet == 0:
            return k
    raise AssertionError((m, n, r, "quotient period not found"))


def brute_exact_carrier_return_period(m, r):
    a = 0
    for k in range(1, m + 1):
        a = (a + r) % m
        if a == 0:
            return k
    raise AssertionError((m, r, "carrier period not found"))
```

The oracle must not call the production helpers or reproduce their `gcd` closed forms.

- [ ] **Step 2: Add a bounded exhaustive oracle test**

Add:

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

Expected: PASS, `checked == 7220`.

- [ ] **Step 4: Re-run all transverse tests**

```bash
python -m unittest tests.test_transverse -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add tests/test_transverse.py
git commit -m "test: pressure quotient return periods by brute force"
```

---

### Task 3: Replace the Unscoped Return Boolean with a Typed Return Relation

**Files:**
- Modify: `dogram/productive_desync.py`
- Modify: `tests/test_productive_desync.py`

**Interfaces:**
- Produces:
  - `ReturnRelation`
  - `ReturnRelation.returned: bool` computed from declared quotient observations
  - `ReturnRelation.to_data() -> dict[str, Any]`
- Changes:
  - `assess_productive_desync(..., return_relation: ReturnRelation, ...) -> ProductiveDesyncAssessment`
  - removes `returned_to_coherence: bool` from the classifier signature and assessment payload

- [ ] **Step 1: Write failing ReturnRelation tests**

Change the test import to:

```python
from dogram.productive_desync import ReturnRelation, assess_productive_desync
```

Add:

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

- [ ] **Step 2: Run the new relation tests and verify RED**

```bash
python -m unittest tests.test_productive_desync.ReturnRelationTests -v
```

Expected: import failure because `ReturnRelation` does not exist.

- [ ] **Step 3: Implement ReturnRelation in `dogram/productive_desync.py`**

Add before `ProductiveDesyncAssessment`:

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

Export `ReturnRelation` in `__all__`.

This first slice intentionally uses ordinary equality over supplied quotient observations. It does not invent arbitrary quotient construction or comparison semantics.

- [ ] **Step 4: Run ReturnRelation tests and verify GREEN**

```bash
python -m unittest tests.test_productive_desync.ReturnRelationTests -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Rewrite the Productive Desync assessment shape**

In `ProductiveDesyncAssessment`, replace:

```python
returned_to_coherence: bool
```

with:

```python
return_relation: ReturnRelation
```

Update `to_data()` from:

```python
"returned_to_coherence": self.returned_to_coherence,
```

to:

```python
"return_relation": self.return_relation.to_data(),
```

- [ ] **Step 6: Rewrite the classifier signature and validation**

Change `assess_productive_desync()` to accept:

```python
return_relation: ReturnRelation,
```

instead of:

```python
returned_to_coherence: bool,
```

Replace the current combined boolean validation with:

```python
if not isinstance(cut_declared, bool):
    raise ValueError("cut_declared must be boolean")
if not isinstance(return_relation, ReturnRelation):
    raise ValueError("return_relation must be ReturnRelation")
```

Replace:

```python
elif not returned_to_coherence:
    status, reason_code = "REFUSE", "NO_COHERENCE_RETURN"
```

with:

```python
elif not return_relation.returned:
    status, reason_code = "REFUSE", "NO_COHERENCE_RETURN"
```

Preserve the reason code for compatibility in this slice; the receipt now makes its scope explicit.

Return the exact supplied relation in the assessment object.

- [ ] **Step 7: Migrate the existing classifier test helper**

In `ProductiveDesyncTests.assess()`, replace:

```python
"returned_to_coherence": True,
```

with:

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

Replace the no-return test with:

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
        data = result.to_data()
        self.assertEqual(data["return_relation"]["relation_id"], "bounded-coherence-return")
        self.assertEqual(data["return_relation"]["quotient_id"], "declared-coherence-cut")
        self.assertTrue(data["return_relation"]["returned"])
```

- [ ] **Step 8: Run all Productive Desync tests**

```bash
python -m unittest tests.test_productive_desync -v
```

Expected: all tests PASS.

- [ ] **Step 9: Assert the old broad field is gone from production and focused tests**

Run:

```bash
grep -R "returned_to_coherence" -n dogram tests/test_productive_desync.py && exit 1 || true
```

Expected: no matches.

Do not grep historical specs/plans; preserving the old design vocabulary there is part of provenance.

- [ ] **Step 10: Commit Task 3**

```bash
git add dogram/productive_desync.py tests/test_productive_desync.py
git commit -m "feat: scope productive desync return relation"
```

---

### Task 4: Freeze Six Quotient-Return Hostile Specimens

**Files:**
- Create: `tests/fixtures/return_relation/*.json` (six files listed in File Structure)
- Modify: `tests/test_transverse.py`
- Modify: `tests/test_productive_desync.py`

**Interfaces:**
- Consumes: return helpers from Task 1; `ReturnRelation` and classifier from Task 3.
- Produces: six durable fixture receipts covering quotient-before-carrier, quotient-inert, coprime, exact return, generator-word, and Productive Desync relation-scope controls.

- [ ] **Step 1: Add a shared fixture loader to `tests/test_transverse.py`**

Add:

```python
RETURN_FIXTURES = ROOT / "tests" / "fixtures" / "return_relation"


def load_return_fixture(name):
    return json.loads((RETURN_FIXTURES / name).read_text())
```

- [ ] **Step 2: Write the failing six-fixture contract**

Add:

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

- [ ] **Step 3: Run the fixture contract and verify RED**

```bash
python -m unittest \
  tests.test_transverse.TransverseTests.test_six_return_relation_fixtures_are_frozen -v
```

Expected: FAIL because fixture directory/files do not exist.

- [ ] **Step 4: Create `z6x9-r1.json`**

```json
{
  "id": "RETURN-R1-Z6X9-R1",
  "system": {"m": 6, "n": 9, "r": 1},
  "expected": {
    "quotient_return_period": 3,
    "exact_carrier_return_period": 6,
    "return_debt": 2,
    "after_quotient_period": {
      "cycles": 3,
      "sheet_returned": true,
      "carrier_returned": false
    },
    "after_exact_period": {
      "cycles": 6,
      "sheet_returned": true,
      "carrier_returned": true
    }
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

Use one declared generator family but two different actual words:

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

This freezes:

```text
SAME GENERATOR CLOSURE != SAME DECLARED WORD RETURN.
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

- [ ] **Step 10: Add formula/word fixture verification to `tests/test_transverse.py`**

Add:

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

- [ ] **Step 11: Add Productive Desync scope fixture verification**

In `tests/test_productive_desync.py`, add a JSON fixture loader and:

```python
    def test_coarse_return_can_witness_while_fine_return_refuses_for_same_other_facts(self):
        fixture = load_return_fixture("productive-desync-scope-control.json")
        shared = fixture["assessment"]

        def relation(data):
            return ReturnRelation(
                relation_id=data["relation_id"],
                quotient_id=data["quotient_id"],
                anchor_before=data["anchor_before"],
                anchor_after=data["anchor_after"],
                quotient_before=data["quotient_before"],
                quotient_after=data["quotient_after"],
            )

        coarse = assess_productive_desync(**shared, return_relation=relation(fixture["coarse_return"]))
        fine = assess_productive_desync(**shared, return_relation=relation(fixture["fine_return"]))
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

Expected: all tests PASS.

- [ ] **Step 13: Commit Task 4**

```bash
git add tests/fixtures/return_relation tests/test_transverse.py tests/test_productive_desync.py
git commit -m "test: freeze quotient-return hostile specimens"
```

---

### Task 5: Record the Executable Receipt Without Promoting Runtime Authority

**Files:**
- Create: `research/QUOTIENT-RETURN-RECEIPTS-001.md`
- Modify: `research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: exact green behavior from Tasks 1-4.
- Produces: durable research receipt and factual repo status only; no runtime code.

- [ ] **Step 1: Create the receipt ledger**

Create `research/QUOTIENT-RETURN-RECEIPTS-001.md` with this structure and the exact final numbers from the green suite:

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

## Frozen fixtures

| fixture | quotient period | exact period | debt | control |
| --- | ---: | ---: | ---: | --- |
| `z6x9-r1.json` | 3 | 6 | 2 | quotient before carrier |
| `z8x12-r4.json` | 1 | 2 | 2 | quotient-inert cut |
| `coprime-z5x7-r1.json` | 1 | 5 | 5 | trivial quotient / no hidden sheet |
| `exact-return-z6x9-r6.json` | 1 | 1 | 1 | exact-return control |

`multigenerator-word-control.json` and `productive-desync-scope-control.json` freeze the non-scalar controls.

## Hard refusals

```text
QUOTIENT RETURN != EXACT CARRIER RETURN
EXACT CARRIER RETURN != HISTORY RETURN
GENERATOR CLOSURE != DECLARED WORD
QUOTIENT RETURN != HOLONOMY
REACHABILITY GAIN != TRUTH / EVIDENCE / AUTHORITY
```

## Verification

Record exact implementation head, full unit count, compile result, constitutional-floor result, and Ω scope-scan result here immediately before merge.
```

Do not fill the final exact-head receipt until Task 6.

- [ ] **Step 2: Update the FATDOG status line**

Change the research packet status from:

```text
RESEARCH + EXACT FINITE/GEOMETRIC PRESSURE · NO NEW PUBLIC OPERATOR
```

to:

```text
RESEARCH + FROZEN EXECUTABLE RETURN WITNESSES · NO NEW PUBLIC OPERATOR
```

Add one short section near the runtime disposition pointing to:

```text
tests/test_transverse.py
tests/test_productive_desync.py
tests/fixtures/return_relation/
research/QUOTIENT-RETURN-RECEIPTS-001.md
```

Do not rewrite the original derivation.

- [ ] **Step 3: Add a factual README status sentence**

Append to the existing internal-kernel paragraph:

```markdown
The internal transverse/Productive-Desync research kernel also carries typed quotient-return receipts: exact finite sheet-return and carrier-return periods remain separate, declared generator closure remains separate from actual word/history, and Productive Desync consumes an explicitly scoped return relation. This adds no public operator or holonomy semantics.
```

- [ ] **Step 4: Run focused docs/constitutional smoke tests**

```bash
python -m unittest tests.test_transverse tests.test_productive_desync -v
python -m compileall -q dogram tests
```

Expected: PASS.

- [ ] **Step 5: Commit Task 5**

```bash
git add README.md research/QUOTIENT-RETURN-LIFT-RESIDUAL-FATDOG-001.md research/QUOTIENT-RETURN-RECEIPTS-001.md
git commit -m "docs: receipt executable quotient-return honing"
```

---

### Task 6: Exact-Head Constitutional Verification and Receipt Seal

**Files:**
- Modify: `research/QUOTIENT-RETURN-RECEIPTS-001.md`
- Verify unchanged: `dogram/omega.py`, `dogram/proposal.py`, `dogram/gate.py`, `dogram/engine.py`, `dogram/registry.py`

**Interfaces:**
- Consumes: completed Tasks 1-5.
- Produces: exact-head verification receipt suitable for PR review/merge.

- [ ] **Step 1: Run the full unit suite**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests PASS. Record the exact test count from the command output.

- [ ] **Step 2: Run compile**

```bash
python -m compileall -q dogram tests
```

Expected: exit 0.

- [ ] **Step 3: Run the exact constitutional-floor command from CI**

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

- [ ] **Step 4: Run the exact Ω scope scan from CI**

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

- [ ] **Step 5: Verify forbidden architectural files were not modified**

Against the implementation branch base, run:

```bash
git diff --name-only <BASE_SHA>...HEAD
```

Expected modified production files are only:

```text
dogram/transverse.py
dogram/productive_desync.py
```

The diff must not contain:

```text
dogram/omega.py
dogram/proposal.py
dogram/gate.py
dogram/engine.py
dogram/registry.py
dogram/program.py
dogram/vm.py
```

- [ ] **Step 6: Record the exact-head receipt**

Run:

```bash
git rev-parse HEAD
```

Update `research/QUOTIENT-RETURN-RECEIPTS-001.md` with:

```text
implementation_head: <exact SHA>
full_unit_suite: <N> PASS
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

- [ ] **Step 8: Re-run verification after the receipt-only commit**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Expected: same green behavior after the final documentation commit.

---

## Plan Self-Review

### Spec coverage

- Typed return relation instead of globally interpretable Boolean: Task 3.
- Exact quotient-return period: Tasks 1-2.
- Exact carrier-return period: Tasks 1-2.
- Return debt and divisibility: Tasks 1-2.
- R1-R6 frozen hostile specimens: Task 4.
- Multi-generator word vs closure distinction: Task 4.
- Productive Desync coarse/fine relation-scope control: Tasks 3-4.
- No generic holonomy subsystem: Global Constraints + File Structure + Task 5 refusals.
- No Ω mutation: Global Constraints + Task 6 forbidden-file verification.
- Full constitutional verification: Task 6.
- Research receipt and factual README note after executable landing: Task 5.

### Placeholder scan

This plan contains no unresolved implementation placeholders. The angle-bracket values in Task 6 (`<BASE_SHA>`, `<exact SHA>`, `<N>`) are runtime receipts that cannot be known before execution; each is paired with an exact command that produces the required value.

### Type consistency

- `ReturnRelation` is defined once in Task 3 and used by all later classifier/fixture tests.
- `return_relation` replaces `returned_to_coherence` consistently in production and focused tests.
- Return helper names and signatures are fixed in Task 1 and reused unchanged in Tasks 2, 4, and 5.
- Existing reason code `NO_COHERENCE_RETURN` remains unchanged for this bounded migration.

---

## Completion Boundary

This plan is complete when Dogram can calculate and receipt the following without semantic promotion:

```text
RETURN MUST NAME ITS QUOTIENT.
THE QUOTIENT MAY CLOSE WHILE THE CARRIER LIFTS.
KEEP THE FINER RESIDUAL.
GENERATOR CLOSURE != DECLARED WORD != ACTUAL HISTORY.
NO FIBER LAW -> NO HOLONOMY CLAIM.
```

No public operator, generic return engine, optimizer, automatic quotient inference, or authority-bearing semantic conclusion is part of this implementation.
