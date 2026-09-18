# MAPPING-TORUS-RECEIPT-001 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic exact-integer mapping-torus return calculations that preserve consumed inputs and reproduce the researched 72/5/7 case without promoting braid/spring metaphor into runtime semantics.

**Architecture:** Implement a focused `dogram.mapping_torus` module beside `transverse.py`, using the same validation discipline and `math.gcd` arithmetic. Keep the first landing as a pure executable research module plus tests/fixture; public `dogram.specimen/v0` dispatch is a separately reviewable final task and is skipped if it would require disproportionate schema special-casing.

**Tech Stack:** Python 3 standard library; `dataclasses`, `math.gcd`; current Dogram unittest/CI floor.

**Spec:** `docs/superpowers/specs/2026-08-31-mapping-torus-receipt-v0-design.md`

## Global Constraints

- Promote arithmetic, not metaphor.
- Accept only real integers; bools, floats, and strings refuse.
- `fiber_count` must be `> 0`.
- Preserve exact input shifts/traversal counts even when coarse outputs coincide.
- No floating-point twisted-mode output.
- Python standard library only.
- No `braid@1`, `spring@1`, phi privilege, physics/theology inference, evidence, support, or authority.

---

### Task 1: Implement the core mapping-torus analysis

**Files:**
- Create: `dogram/mapping_torus.py`
- Create: `tests/test_mapping_torus.py`

**Interfaces:**
- Produces:
  - `MappingTorusInputError(reason_code: str, residual: str)`
  - `MappingTorusAnalysis(fiber_count, shift, normalized_shift, components, orbit_length)`
  - `analyze_mapping_torus(fiber_count: int, shift: int) -> MappingTorusAnalysis`

- [ ] **Step 1: Write RED tests for the exact component/orbit law**

Create tests asserting:

```python
analysis = analyze_mapping_torus(72, 5)
self.assertEqual(analysis.components, 1)
self.assertEqual(analysis.orbit_length, 72)
self.assertEqual(analysis.normalized_shift, 5)

analysis = analyze_mapping_torus(72, 6)
self.assertEqual(analysis.components, 6)
self.assertEqual(analysis.orbit_length, 12)

analysis = analyze_mapping_torus(72, -1)
self.assertEqual(analysis.normalized_shift, 71)
```

Add refusals for `fiber_count in {0, -1, True}`, `shift=True`, `shift=1.5`, and `shift="5"`.

- [ ] **Step 2: Run focused RED**

```bash
python3 -m unittest tests.test_mapping_torus -v
```

Expected: import failure because the module does not exist.

- [ ] **Step 3: Implement validation + analysis**

Use:

```python
components = gcd(fiber_count, shift)
orbit_length = fiber_count // components
normalized_shift = shift % fiber_count
```

The dataclass `to_data()` must emit only JSON-safe integers with stable field names.

- [ ] **Step 4: Run focused GREEN**

```bash
python3 -m unittest tests.test_mapping_torus -v
```

- [ ] **Step 5: Commit the core analysis**

```bash
git add dogram/mapping_torus.py tests/test_mapping_torus.py
git commit -m "feat: calculate mapping torus return structure"
```

---

### Task 2: Add exact winding decomposition

**Files:**
- Modify: `dogram/mapping_torus.py`
- Modify: `tests/test_mapping_torus.py`

**Interfaces:**
- Produces `WindingDecomposition(fiber_count, traversal_count, winding, residue)`.
- Function: `decompose_winding(fiber_count: int, traversal_count: int) -> WindingDecomposition`.

- [ ] **Step 1: Add RED reconstruction tests**

For each `k in (0, 1, 71, 72, 145, -1, -73)` require:

```python
result = decompose_winding(72, k)
self.assertEqual(k, 72 * result.winding + result.residue)
self.assertGreaterEqual(result.residue, 0)
self.assertLess(result.residue, 72)
```

Also reject invalid fiber counts and non-integer traversal counts.

- [ ] **Step 2: Run focused RED**

```bash
python3 -m unittest tests.test_mapping_torus.MappingTorusTests.test_winding_reconstructs_exactly -v
```

- [ ] **Step 3: Implement via Python Euclidean `divmod`**

```python
winding, residue = divmod(traversal_count, fiber_count)
```

Return both original `traversal_count` and exact decomposition fields in `to_data()`.

- [ ] **Step 4: Run focused GREEN and full file**

```bash
python3 -m unittest tests.test_mapping_torus -v
```

- [ ] **Step 5: Commit winding support**

```bash
git add dogram/mapping_torus.py tests/test_mapping_torus.py
git commit -m "feat: decompose mapping torus winding exactly"
```

---

### Task 3: Add relative realignment

**Files:**
- Modify: `dogram/mapping_torus.py`
- Modify: `tests/test_mapping_torus.py`

**Interfaces:**
- Produces `RelativeRealignment(fiber_count, shift_a, shift_b, relative_delta, realignment_period)`.
- Function: `relative_realignment(fiber_count: int, shift_a: int, shift_b: int) -> RelativeRealignment`.

- [ ] **Step 1: Add RED tests for the research case**

Require:

```python
result = relative_realignment(72, 5, 7)
self.assertEqual(result.relative_delta, 70)  # (5 - 7) mod 72
self.assertEqual(result.realignment_period, 36)
```

Also require symmetry of the period:

```python
self.assertEqual(
    relative_realignment(72, 5, 7).realignment_period,
    relative_realignment(72, 7, 5).realignment_period,
)
```

and same-shift period `1`.

- [ ] **Step 2: Run focused RED**

```bash
python3 -m unittest tests.test_mapping_torus.MappingTorusTests.test_72_5_7_realigns_after_36_rounds -v
```

- [ ] **Step 3: Implement exact realignment**

```python
delta_raw = shift_a - shift_b
relative_delta = delta_raw % fiber_count
realignment_period = fiber_count // gcd(fiber_count, delta_raw)
```

Preserve `shift_a` and `shift_b` exactly in `to_data()`; do not collapse them to the residue.

- [ ] **Step 4: Run focused GREEN**

```bash
python3 -m unittest tests.test_mapping_torus -v
```

- [ ] **Step 5: Commit relative realignment**

```bash
git add dogram/mapping_torus.py tests/test_mapping_torus.py
git commit -m "feat: calculate exact relative realignment"
```

---

### Task 4: Add exact twisted-mode fractions

**Files:**
- Modify: `dogram/mapping_torus.py`
- Modify: `tests/test_mapping_torus.py`

**Interfaces:**
- Produces `RationalValue(numerator: int, denominator: int)` with positive denominator.
- Function: `twisted_mode_fraction(fiber_count: int, shift: int, longitudinal_index: int, fiber_mode: int) -> RationalValue`.

- [ ] **Step 1: Add RED reduction tests**

Test exact cases such as:

```python
self.assertEqual(
    twisted_mode_fraction(72, 6, 0, 12).to_data(),
    {"numerator": 1, "denominator": 1},
)
self.assertEqual(
    twisted_mode_fraction(72, 5, -1, 1).to_data(),
    {"numerator": -67, "denominator": 72},
)
```

Assert returned fields are integers, never floats.

- [ ] **Step 2: Run focused RED**

```bash
python3 -m unittest tests.test_mapping_torus.MappingTorusTests.test_twisted_mode_fraction_is_exact -v
```

- [ ] **Step 3: Implement reduced rational arithmetic**

Compute:

```python
numerator = longitudinal_index * fiber_count + fiber_mode * shift
denominator = fiber_count
factor = gcd(abs(numerator), denominator)
```

Special-case `numerator == 0` to return `0/1`.

- [ ] **Step 4: Run focused GREEN**

```bash
python3 -m unittest tests.test_mapping_torus -v
```

- [ ] **Step 5: Commit exact mode arithmetic**

```bash
git add dogram/mapping_torus.py tests/test_mapping_torus.py
git commit -m "feat: receipt twisted mode fractions exactly"
```

---

### Task 5: Freeze a research fixture and same-surface controls

**Files:**
- Create: `tests/fixtures/mapping_torus/mapping-torus-001.json`
- Create: `research/MAPPING-TORUS-RECEIPT-001.md`
- Modify: `tests/test_mapping_torus.py`

**Interfaces:**
- Fixture records the declared inputs and expected exact outputs for `N=72`, shifts `5` and `7`.

- [ ] **Step 1: Write the fixture**

Include:

```json
{
  "schema": "dogram.mapping-torus-fixture/v0",
  "fiber_count": 72,
  "shift_a": 5,
  "shift_b": 7,
  "expected": {
    "shift_a_components": 1,
    "shift_a_orbit_length": 72,
    "shift_b_components": 1,
    "shift_b_orbit_length": 72,
    "realignment_period": 36
  }
}
```

- [ ] **Step 2: Add fixture-driven tests**

Load the fixture and reproduce every expected value from real functions. Add the coarse-collision control:

```python
left = analyze_mapping_torus(72, 5)
right = analyze_mapping_torus(72, 7)
self.assertEqual((left.components, left.orbit_length), (right.components, right.orbit_length))
self.assertNotEqual(left.shift, right.shift)
```

- [ ] **Step 3: Document the runtime boundary**

`research/MAPPING-TORUS-RECEIPT-001.md` must state:

```text
same coarse observable != same consumed inputs
calculation != interpretation
PROMOTE THE ARITHMETIC, NOT THE METAPHOR
```

- [ ] **Step 4: Run focused + full Dogram verification**

```bash
python3 -m unittest tests.test_mapping_torus -v
python3 -m unittest discover -s tests -v
```

If the repository CI uses additional static/compile checks, run the same commands declared in `.github/workflows/ci.yml` before committing.

- [ ] **Step 5: Commit fixture/research receipt**

```bash
git add tests/fixtures/mapping_torus/mapping-torus-001.json research/MAPPING-TORUS-RECEIPT-001.md tests/test_mapping_torus.py
git commit -m "test: freeze mapping torus receipt controls"
```

---

### Task 6: Decide public dispatch from evidence, not enthusiasm

**Files:**
- Inspect: `dogram/engine.py`
- Inspect: `dogram/cli.py`
- Inspect: `tests/test_engine.py`
- Inspect: `tests/test_cli.py`
- Modify only if the existing operator envelope accepts this calculation without a new special-case schema.

**Interfaces:**
- Optional public name: `mapping_torus@1`.
- If admitted, `consumed_inputs` must contain every operative numeric input and result remains calculation-only.

- [ ] **Step 1: Write a RED dispatch test only if the existing engine shape fits**

The specimen should be ordinary Dogram shape and request only core analysis:

```json
{
  "operator": "mapping_torus@1",
  "inputs": {"fiber_count": 72, "shift": 5}
}
```

Expected operative result:

```json
{
  "normalized_shift": 5,
  "components": 1,
  "orbit_length": 72
}
```

- [ ] **Step 2: Apply the stop rule**

If adding this operator requires a bespoke specimen schema, metaphor-specific branching, or changes unrelated to ordinary calculation dispatch, delete the RED dispatch test and stop. The pure module is the completed executable slice.

- [ ] **Step 3: If the slot is clean, implement minimum dispatch + CLI wiring**

Register `mapping_torus@1` using existing engine conventions only. Do not expose comparison/winding/mode variants until each has an explicit ordinary input shape.

- [ ] **Step 4: Verify public-boundary determinism**

```bash
python3 -m unittest tests.test_engine tests.test_cli tests.test_mapping_torus -v
python3 -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit only if public dispatch was actually admitted**

```bash
git add dogram/engine.py dogram/cli.py tests/test_engine.py tests/test_cli.py
git commit -m "feat: expose mapping torus calculation"
```

If the stop rule fired, make no commit for this task and record in the PR that executable-module completion was intentional.
