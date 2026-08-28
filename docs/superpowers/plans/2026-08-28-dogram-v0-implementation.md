# Dogram v0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, offline Python 3.12 calculation lab that can pressure-test MutatedMathal specimens through typed delta, 2×2 interaction, ablation, and reachability operators while emitting reproducible receipts and minting no semantic authority.

**Architecture:** Dogram is a pure calculation sidecar, not an ALEX kernel. A versioned JSON specimen is decoded into small typed values or directed graphs, dispatched to one of four pure operators (`delta`, `rectangle`, `ablate`, `reach`), and wrapped in a canonical calculation receipt that names consumed inputs. MutatedMathals remain external formulations; they become executable only by lowering a declared discriminator into one or more Dogram specimens.

**Tech Stack:** Python >= 3.12, standard library only (`json`, `hashlib`, `fractions`, `dataclasses`, `collections`, `argparse`, `unittest`).

**Spec:** `docs/superpowers/specs/2026-08-28-dogram-v0-design.md`

## Global Constraints

- Python >= 3.12.
- Standard library only for v0; no third-party runtime or test dependencies.
- No network access, model calls, hidden time dependence, randomness, environmental discovery, or dynamic code execution inside operators.
- Dogram output does not mint evidence, support, truth, authority, ALEX predicates, historical identity, or causal meaning.
- Public schemas are `dogram.specimen/v0` and `dogram.receipt/v0`.
- Public operators are `delta@1`, `rectangle@1`, `ablate@1`, and `reach@1`.
- Exact integers/rationals remain exact; opaque values receive equality/equivalence comparison only.
- Every successful calculation receipt names `consumed_inputs`; metadata is non-operative.
- Identical canonical specimens under the same operator version must produce byte-stable canonical receipt payloads.
- Ordinary malformed/under-typed specimens return structured `REFUSE` or `INSUFFICIENT_TO_TEST` receipts rather than uncaught exceptions.
- Graph paths are graph-theoretic witnesses only: `GRAPH PATH != CAUSAL PATH` and `GRAPH REACHABILITY != HISTORICAL OCCURRENCE`.
- The first MutatedMathal examples are lowering examples, not privileged runtime semantics.

---

## File Structure

Create the following focused modules:

```text
Dogram/
  README.md
  pyproject.toml
  dogram/
    __init__.py
    canonical.py
    values.py
    receipt.py
    delta.py
    rectangle.py
    graph.py
    ablate.py
    reach.py
    engine.py
    cli.py
  examples/
    mutated_mathals/
      interest-mediated-support.json
      hidden-world-policy-rectangle.json
      trust-withdrawal.json
      same-surface-different-history.json
  tests/
    __init__.py
    fixtures/
      delta/
        first-opaque-break.json
        exact-rational-delta.json
      rectangle/
        exact-mixed-delta.json
        opaque-interaction.json
      ablate/
        trust-edge-survives.json
        trust-edge-collapses.json
      reach/
        same-surface-different-history.json
    test_canonical.py
    test_values.py
    test_receipt.py
    test_delta.py
    test_rectangle.py
    test_graph.py
    test_ablate.py
    test_reach.py
    test_engine.py
    test_cli.py
    test_mutated_mathal_examples.py
```

Responsibilities:

- `canonical.py` — canonical JSON encoding and SHA-256 digests only.
- `values.py` — decode/encode typed scalar values; no operator policy.
- `receipt.py` — common receipt envelope and structured refusal helpers.
- `delta.py` — ordered trace comparison only.
- `rectangle.py` — 2×2 numeric/equivalence interaction only.
- `graph.py` — immutable normalized directed graph and traversal helpers.
- `ablate.py` — node/edge deletion and reachability-loss report only.
- `reach.py` — one explicit graph mutation and before/after reachability only.
- `engine.py` — specimen validation, static operator dispatch, receipt assembly.
- `cli.py` — stdin/file JSON adapter and deterministic stdout JSON only.
- `examples/mutated_mathals/*` — demonstrations of how external mathals lower into Dogram specimens; no runtime special-casing.

---

### Task 1: Establish package floor, canonicalization, and typed values

**Files:**
- Create: `pyproject.toml`
- Create: `dogram/__init__.py`
- Create: `dogram/canonical.py`
- Create: `dogram/values.py`
- Create: `tests/__init__.py`
- Create: `tests/test_canonical.py`
- Create: `tests/test_values.py`

**Interfaces:**
- Produces: `canonical_json_bytes(value: object) -> bytes`
- Produces: `sha256_json(value: object) -> str`
- Produces: `decode_value(spec: dict) -> ScalarValue`
- Produces: `encode_value(value: ScalarValue) -> dict`
- Produces: `compare_values(left: ScalarValue, right: ScalarValue) -> dict`
- `ScalarValue` supports kinds `integer`, `rational`, `float`, `opaque`.

- [ ] **Step 1: Write failing canonicalization tests**

Create `tests/test_canonical.py`:

```python
import unittest

from dogram.canonical import canonical_json_bytes, sha256_json


class CanonicalTests(unittest.TestCase):
    def test_object_key_order_does_not_change_bytes(self):
        a = {"b": 2, "a": 1}
        b = {"a": 1, "b": 2}
        self.assertEqual(canonical_json_bytes(a), canonical_json_bytes(b))
        self.assertEqual(sha256_json(a), sha256_json(b))

    def test_canonical_json_has_no_incidental_whitespace(self):
        self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run canonicalization tests and verify RED**

Run:

```bash
python -m unittest tests.test_canonical -v
```

Expected: import failure because `dogram.canonical` does not exist.

- [ ] **Step 3: Implement canonical JSON and digest helpers**

Create `dogram/canonical.py`:

```python
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    digest = hashlib.sha256(canonical_json_bytes(value)).hexdigest()
    return f"sha256:{digest}"
```

Create minimal `dogram/__init__.py` with `__version__ = "0.0.0"`.

- [ ] **Step 4: Run canonicalization tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_canonical -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Write failing typed-value tests**

Create `tests/test_values.py` covering exact rational arithmetic and opaque refusal:

```python
import unittest
from fractions import Fraction

from dogram.values import ValueDecodeError, compare_values, decode_value, encode_value


class ValueTests(unittest.TestCase):
    def test_decode_rational_is_exact(self):
        value = decode_value({"kind": "rational", "numerator": 1, "denominator": 3})
        self.assertEqual(value.value, Fraction(1, 3))

    def test_encode_rational_is_canonical(self):
        value = decode_value({"kind": "rational", "numerator": 2, "denominator": 6})
        self.assertEqual(encode_value(value), {"kind": "rational", "numerator": 1, "denominator": 3})

    def test_opaque_comparison_never_emits_numeric_delta(self):
        left = decode_value({"kind": "opaque", "value": "a"})
        right = decode_value({"kind": "opaque", "value": "b"})
        self.assertEqual(compare_values(left, right), {"relation": "DIFFERENT"})

    def test_exact_numeric_comparison_emits_exact_delta(self):
        left = decode_value({"kind": "rational", "numerator": 1, "denominator": 3})
        right = decode_value({"kind": "integer", "value": 1})
        self.assertEqual(
            compare_values(left, right),
            {"relation": "DIFFERENT", "delta": {"kind": "rational", "numerator": 2, "denominator": 3}},
        )

    def test_zero_denominator_refuses_decode(self):
        with self.assertRaises(ValueDecodeError):
            decode_value({"kind": "rational", "numerator": 1, "denominator": 0})
```

- [ ] **Step 6: Run typed-value tests and verify RED**

Run:

```bash
python -m unittest tests.test_values -v
```

Expected: import failure because `dogram.values` does not exist.

- [ ] **Step 7: Implement typed scalar values**

Create `dogram/values.py` using an immutable dataclass:

```python
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

ValueKind = Literal["integer", "rational", "float", "opaque"]


class ValueDecodeError(ValueError):
    pass


@dataclass(frozen=True)
class ScalarValue:
    kind: ValueKind
    value: int | Fraction | float | str


def decode_value(spec: dict[str, Any]) -> ScalarValue:
    if not isinstance(spec, dict):
        raise ValueDecodeError("value must be an object")
    kind = spec.get("kind")
    if kind == "integer" and type(spec.get("value")) is int:
        return ScalarValue("integer", spec["value"])
    if kind == "rational" and type(spec.get("numerator")) is int and type(spec.get("denominator")) is int:
        if spec["denominator"] == 0:
            raise ValueDecodeError("rational denominator must be non-zero")
        return ScalarValue("rational", Fraction(spec["numerator"], spec["denominator"]))
    if kind == "float" and isinstance(spec.get("value"), (int, float)) and not isinstance(spec.get("value"), bool):
        return ScalarValue("float", float(spec["value"]))
    if kind == "opaque" and isinstance(spec.get("value"), str):
        return ScalarValue("opaque", spec["value"])
    raise ValueDecodeError("unsupported or malformed value kind")


def encode_value(value: ScalarValue) -> dict[str, Any]:
    if value.kind == "integer":
        return {"kind": "integer", "value": value.value}
    if value.kind == "rational":
        assert isinstance(value.value, Fraction)
        return {"kind": "rational", "numerator": value.value.numerator, "denominator": value.value.denominator}
    if value.kind == "float":
        return {"kind": "float", "value": value.value}
    return {"kind": "opaque", "value": value.value}


def _numeric(value: ScalarValue) -> int | Fraction | float:
    if value.kind == "opaque":
        raise ValueDecodeError("opaque values are not numeric")
    assert isinstance(value.value, (int, Fraction, float))
    return value.value


def _encode_numeric_result(value: int | Fraction | float) -> dict[str, Any]:
    if isinstance(value, float):
        return {"kind": "float", "value": value}
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return {"kind": "integer", "value": value.numerator}
        return {"kind": "rational", "numerator": value.numerator, "denominator": value.denominator}
    return {"kind": "integer", "value": value}


def compare_values(left: ScalarValue, right: ScalarValue) -> dict[str, Any]:
    if left.kind == "opaque" or right.kind == "opaque":
        if left.kind != right.kind:
            raise ValueDecodeError("opaque and numeric values are incompatible")
        return {"relation": "SAME" if left.value == right.value else "DIFFERENT"}
    delta = _numeric(right) - _numeric(left)
    result = {"relation": "SAME" if delta == 0 else "DIFFERENT"}
    if delta != 0:
        result["delta"] = _encode_numeric_result(delta)
    return result
```

- [ ] **Step 8: Run value and canonical tests**

Run:

```bash
python -m unittest tests.test_canonical tests.test_values -v
```

Expected: all tests pass.

- [ ] **Step 9: Add package metadata**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "dogram"
version = "0.0.0"
description = "Deterministic operations for graph, relation, and mathal pressure"
requires-python = ">=3.12"
dependencies = []
```

No console script entry point yet; `python -m dogram.cli` is the v0 execution surface.

- [ ] **Step 10: Commit Task 1**

```bash
git add pyproject.toml dogram/__init__.py dogram/canonical.py dogram/values.py tests/__init__.py tests/test_canonical.py tests/test_values.py
git commit -m "feat: establish deterministic typed value floor"
```

---

### Task 2: Add deterministic calculation receipts and refusal envelopes

**Files:**
- Create: `dogram/receipt.py`
- Create: `tests/test_receipt.py`

**Interfaces:**
- Consumes: `sha256_json()` from `dogram.canonical`.
- Produces: `ok_receipt(...) -> dict`
- Produces: `refusal_receipt(...) -> dict`
- Produces: `canonical_receipt_bytes(receipt: dict) -> bytes`

- [ ] **Step 1: Write failing receipt tests**

```python
import unittest

from dogram.receipt import canonical_receipt_bytes, ok_receipt, refusal_receipt


class ReceiptTests(unittest.TestCase):
    def test_ok_receipt_names_consumed_inputs_and_input_digest(self):
        specimen = {"schema": "dogram.specimen/v0", "specimen_id": "s1", "operator": "delta", "operator_version": 1, "inputs": {}, "assumptions": [], "metadata": {"ignored": True}}
        receipt = ok_receipt(specimen, "delta", 1, ["inputs"], {"x": 1})
        self.assertEqual(receipt["schema"], "dogram.receipt/v0")
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(receipt["consumed_inputs"], ["inputs"])
        self.assertTrue(receipt["input_digest"].startswith("sha256:"))

    def test_refusal_is_structured_data(self):
        specimen = {"schema": "dogram.specimen/v0", "specimen_id": "bad"}
        receipt = refusal_receipt(specimen, "delta", 1, "REFUSE", "MALFORMED_SPECIMEN", ["operator missing"])
        self.assertEqual(receipt["status"], "REFUSE")
        self.assertEqual(receipt["reason_code"], "MALFORMED_SPECIMEN")

    def test_canonical_receipt_bytes_are_stable(self):
        specimen = {"schema": "dogram.specimen/v0", "specimen_id": "s1", "operator": "delta", "operator_version": 1, "inputs": {}, "assumptions": [], "metadata": {}}
        a = ok_receipt(specimen, "delta", 1, ["inputs"], {"b": 2, "a": 1})
        b = ok_receipt(specimen, "delta", 1, ["inputs"], {"a": 1, "b": 2})
        self.assertEqual(canonical_receipt_bytes(a), canonical_receipt_bytes(b))
```

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_receipt -v
```

Expected: import failure.

- [ ] **Step 3: Implement receipt builders**

`dogram/receipt.py` must:

- always emit `schema`, `specimen_id`, `operator`, `operator_version`, `input_digest`, `status`, `consumed_inputs`, `result`, `residuals`, `warnings`;
- emit `reason_code` for non-OK status;
- sort/deduplicate `consumed_inputs` while preserving deterministic lexicographic order;
- keep `metadata` out of operative semantics but include it in the canonical input digest because it is still part of the supplied specimen receipt;
- use `canonical_json_bytes()` for byte-stable output.

- [ ] **Step 4: Run receipt tests and verify GREEN**

```bash
python -m unittest tests.test_receipt -v
```

- [ ] **Step 5: Commit Task 2**

```bash
git add dogram/receipt.py tests/test_receipt.py
git commit -m "feat: add deterministic calculation receipts"
```

---

### Task 3: Implement `delta@1`

**Files:**
- Create: `dogram/delta.py`
- Create: `tests/test_delta.py`
- Create: `tests/fixtures/delta/first-opaque-break.json`
- Create: `tests/fixtures/delta/exact-rational-delta.json`

**Interfaces:**
- Consumes: `decode_value()`, `compare_values()`.
- Produces: `evaluate_delta(inputs: dict) -> tuple[dict, list[str]]` where tuple is `(result, consumed_inputs)`.

- [ ] **Step 1: Write RED fixture and tests for first opaque break**

Fixture `tests/fixtures/delta/first-opaque-break.json`:

```json
{
  "boundary_order": ["LOADOUT", "PROJECTION", "DERIVATION"],
  "left": {
    "LOADOUT": {"kind": "opaque", "value": "ctx-a"},
    "PROJECTION": {"kind": "opaque", "value": "proj-a"},
    "DERIVATION": {"kind": "integer", "value": 4}
  },
  "right": {
    "LOADOUT": {"kind": "opaque", "value": "ctx-a"},
    "PROJECTION": {"kind": "opaque", "value": "proj-b"},
    "DERIVATION": {"kind": "integer", "value": 7}
  }
}
```

Test expected:

```python
result, consumed = evaluate_delta(inputs)
self.assertEqual(result["first_difference"], "PROJECTION")
self.assertEqual(result["comparisons"][0], {"boundary": "LOADOUT", "relation": "SAME"})
self.assertEqual(result["comparisons"][1], {"boundary": "PROJECTION", "relation": "DIFFERENT"})
self.assertEqual(result["comparisons"][2]["delta"], {"kind": "integer", "value": 3})
self.assertIn("inputs.left.PROJECTION", consumed)
```

- [ ] **Step 2: Run focused test and verify RED**

```bash
python -m unittest tests.test_delta -v
```

- [ ] **Step 3: Implement minimal ordered trace comparison**

`evaluate_delta()` must validate:

- `boundary_order` is a non-empty list of unique strings;
- `left` and `right` are objects with exactly the same declared boundary keys as `boundary_order`;
- each boundary value decodes via `decode_value()`;
- first differing boundary is the earliest declared order position;
- every visited boundary names both left/right consumed paths;
- `first_difference` is `None` when all compare `SAME`.

Raise a local `DeltaInputError(reason_code, residual)` for the engine to translate later; direct unit tests may assert it.

- [ ] **Step 4: Add exact rational fixture/test**

`tests/fixtures/delta/exact-rational-delta.json` compares `1/3` and `1` and asserts exact `2/3`, never float `0.666...`.

- [ ] **Step 5: Run delta tests plus value regression**

```bash
python -m unittest tests.test_values tests.test_delta -v
```

- [ ] **Step 6: Commit Task 3**

```bash
git add dogram/delta.py tests/test_delta.py tests/fixtures/delta
git commit -m "feat: add typed delta-peel operator"
```

---

### Task 4: Implement `rectangle@1`

**Files:**
- Create: `dogram/rectangle.py`
- Create: `tests/test_rectangle.py`
- Create: `tests/fixtures/rectangle/exact-mixed-delta.json`
- Create: `tests/fixtures/rectangle/opaque-interaction.json`

**Interfaces:**
- Produces: `evaluate_rectangle(inputs: dict) -> tuple[dict, list[str]]`.
- Numeric mode consumes four compatible numeric scalar cells.
- Equivalence mode consumes four opaque cells.

- [ ] **Step 1: Write RED exact mixed-delta test**

Use cells equivalent to:

```text
F00 = 0
F01 = 2
F10 = 3
F11 = 8
```

Expected:

```text
mixed_delta = 8 - 3 - 2 + 0 = 3
interaction_detected = true
```

Receipt result must encode `3` as `{"kind":"integer","value":3}`.

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_rectangle -v
```

- [ ] **Step 3: Implement numeric mode**

The input shape is:

```json
{
  "axis_a": "world",
  "axis_b": "interest",
  "cells": {
    "00": {"kind": "integer", "value": 0},
    "01": {"kind": "integer", "value": 2},
    "10": {"kind": "integer", "value": 3},
    "11": {"kind": "integer", "value": 8}
  }
}
```

For exact integer/rational cells, coerce through `Fraction` and emit exact result. If any cell is float, numeric result is float. Reject numeric/opaque mixture.

- [ ] **Step 4: Add RED opaque interaction test**

Use:

```text
F00 == F10
F01 != F11
```

Expected result:

```json
{
  "mode": "equivalence",
  "equivalent_across_axis_a_when_b0": true,
  "equivalent_across_axis_a_when_b1": false,
  "interaction_detected": true
}
```

No numeric `mixed_delta` key may appear.

- [ ] **Step 5: Implement equivalence mode and run GREEN**

```bash
python -m unittest tests.test_rectangle -v
```

- [ ] **Step 6: Commit Task 4**

```bash
git add dogram/rectangle.py tests/test_rectangle.py tests/fixtures/rectangle
git commit -m "feat: add counterfactual rectangle operator"
```

---

### Task 5: Build immutable directed graph primitives

**Files:**
- Create: `dogram/graph.py`
- Create: `tests/test_graph.py`

**Interfaces:**
- Produces: immutable `DirectedGraph` dataclass.
- Produces: `DirectedGraph.from_spec(spec: dict) -> DirectedGraph`.
- Produces: `to_spec() -> dict`.
- Produces: `reachable(source: str, target: str) -> bool`.
- Produces: `shortest_path(source: str, target: str) -> list[str] | None`.
- Produces: `reachable_pairs() -> list[list[str]]` in deterministic order.
- Produces: `remove_node()`, `remove_edge()`, `add_node()`, `add_edge()` returning new graphs.

- [ ] **Step 1: Write RED graph normalization tests**

Assert:

- duplicate nodes/edges are rejected rather than silently collapsed;
- edge endpoints must exist;
- serialization sorts nodes lexicographically and edges by `(source, target)`;
- mutation returns a new graph and leaves original unchanged;
- shortest path tie-breaking is deterministic because neighbors are traversed lexicographically.

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_graph -v
```

- [ ] **Step 3: Implement immutable graph**

Use tuples internally:

```python
@dataclass(frozen=True)
class DirectedGraph:
    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
```

Use `collections.deque` for breadth-first search.

- [ ] **Step 4: Run graph tests and verify GREEN**

```bash
python -m unittest tests.test_graph -v
```

- [ ] **Step 5: Commit Task 5**

```bash
git add dogram/graph.py tests/test_graph.py
git commit -m "feat: add deterministic immutable graph floor"
```

---

### Task 6: Implement `ablate@1`

**Files:**
- Create: `dogram/ablate.py`
- Create: `tests/test_ablate.py`
- Create: `tests/fixtures/ablate/trust-edge-survives.json`
- Create: `tests/fixtures/ablate/trust-edge-collapses.json`

**Interfaces:**
- Consumes: `DirectedGraph`.
- Produces: `evaluate_ablate(inputs: dict) -> tuple[dict, list[str]]`.

- [ ] **Step 1: Write RED trust-withdrawal fixtures**

`trust-edge-survives.json` should model:

```text
A -> P
B -> P
A -> B   # motivating/trust edge to remove
```

Remove `A -> B`; requested `A -> P` and `B -> P` remain reachable through independent direct paths.

`trust-edge-collapses.json` should model a candidate path that exists only through the removed edge and therefore loses reachability.

- [ ] **Step 2: Write tests**

Assert result includes:

```text
removed_component
graph_before_digest
graph_after_digest
lost_reachability
gained_reachability
requested_targets
```

Deletion-only ablation must never report gained reachability.

- [ ] **Step 3: Run and verify RED**

```bash
python -m unittest tests.test_ablate -v
```

- [ ] **Step 4: Implement node and edge ablation**

Accepted target shapes:

```json
{"kind":"node","node":"X"}
```

or

```json
{"kind":"edge","source":"A","target":"B"}
```

Missing targets raise `AblateInputError("MISSING_ABLATION_TARGET", ...)` for later structured translation.

Compute lost/gained reachability as deterministic set differences of `reachable_pairs()`.

- [ ] **Step 5: Run ablation + graph regression**

```bash
python -m unittest tests.test_graph tests.test_ablate -v
```

- [ ] **Step 6: Commit Task 6**

```bash
git add dogram/ablate.py tests/test_ablate.py tests/fixtures/ablate
git commit -m "feat: add graph ablation pressure operator"
```

---

### Task 7: Implement `reach@1`

**Files:**
- Create: `dogram/reach.py`
- Create: `tests/test_reach.py`
- Create: `tests/fixtures/reach/same-surface-different-history.json`

**Interfaces:**
- Produces: `evaluate_reach(inputs: dict) -> tuple[dict, list[str]]`.
- Mutation vocabulary exactly `ADD_NODE`, `REMOVE_NODE`, `ADD_EDGE`, `REMOVE_EDGE`.

- [ ] **Step 1: Write RED reachability mutation tests**

Input includes:

```json
{
  "graph": {"nodes": ["surface", "h1", "future"], "edges": [["surface", "h1"], ["h1", "future"]]},
  "mutation": {"op": "REMOVE_EDGE", "source": "h1", "target": "future"},
  "queries": [["surface", "future"]]
}
```

Expected query result:

```json
{
  "source": "surface",
  "target": "future",
  "reachable_before": true,
  "reachable_after": false,
  "changed": true,
  "path_before": ["surface", "h1", "future"],
  "path_after": null
}
```

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_reach -v
```

- [ ] **Step 3: Implement explicit mutation application**

Reject unknown operations with `UNSUPPORTED_MUTATION`.

Reject malformed queries or missing referenced nodes with `INVALID_GRAPH_REFERENCE`.

Return graph before/after digests and deterministic query results.

- [ ] **Step 4: Add same-surface/different-history fixture**

Represent two explicit graphs with the same non-operative surface label in metadata but different internal edges. Apply the same mutation separately and show different reachability futures. The test asserts Dogram only reports the graph delta; it does not emit `history_is_causal` or any semantic conclusion.

- [ ] **Step 5: Run reach + graph regression**

```bash
python -m unittest tests.test_graph tests.test_reach -v
```

- [ ] **Step 6: Commit Task 7**

```bash
git add dogram/reach.py tests/test_reach.py tests/fixtures/reach
git commit -m "feat: add explicit graph reachability mutation operator"
```

---

### Task 8: Add specimen engine with static operator dispatch and consumed-input receipts

**Files:**
- Create: `dogram/engine.py`
- Create: `tests/test_engine.py`

**Interfaces:**
- Consumes the four evaluator functions.
- Produces: `evaluate_specimen(specimen: dict) -> dict`.
- Static dispatch table only; no plugin loading.

- [ ] **Step 1: Write RED engine tests**

Cover:

1. wrong `schema` -> `REFUSE / MALFORMED_SPECIMEN`;
2. unknown operator -> `REFUSE / UNSUPPORTED_OPERATOR`;
3. wrong operator version -> `REFUSE / UNSUPPORTED_OPERATOR_VERSION`;
4. valid delta -> `OK` receipt;
5. malformed delta inputs -> structured receipt, no uncaught operator exception;
6. arbitrary metadata changes neither `result` nor `consumed_inputs` when operative inputs are unchanged;
7. metadata does change the whole-specimen `input_digest`, preserving what was actually supplied;
8. `consumed_inputs` never includes `metadata` unless a future operator explicitly declares it operative (none do in v0).

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_engine -v
```

- [ ] **Step 3: Implement static dispatch**

Use exactly:

```python
OPERATORS = {
    ("delta", 1): evaluate_delta,
    ("rectangle", 1): evaluate_rectangle,
    ("ablate", 1): evaluate_ablate,
    ("reach", 1): evaluate_reach,
}
```

The engine validates top-level fields:

```text
schema
specimen_id
operator
operator_version
inputs
assumptions
metadata
```

`assumptions` and `metadata` are retained in the input digest but are non-operative v0 fields.

Translate operator input exceptions to structured receipts with stable reason codes.

- [ ] **Step 4: Run engine and all operator tests**

```bash
python -m unittest tests.test_engine tests.test_delta tests.test_rectangle tests.test_ablate tests.test_reach -v
```

- [ ] **Step 5: Commit Task 8**

```bash
git add dogram/engine.py tests/test_engine.py
git commit -m "feat: add versioned Dogram specimen engine"
```

---

### Task 9: Add CLI JSON boundary and byte-stability proof

**Files:**
- Create: `dogram/cli.py`
- Create: `tests/test_cli.py`

**Interfaces:**
- Produces module execution: `python -m dogram.cli [PATH|-]`.
- `-` or omitted path reads stdin.
- stdout contains exactly one canonical JSON receipt plus newline.
- specimen/data errors return exit code `0` because refusal is a valid Dogram result; transport/JSON syntax failures return exit code `2` with a structured minimal receipt on stdout.

- [ ] **Step 1: Write RED CLI tests with subprocess**

Test:

- stdin valid specimen -> canonical receipt;
- file valid specimen -> same receipt bytes as stdin;
- identical runs -> byte-identical stdout;
- invalid JSON -> deterministic structured refusal and exit code 2;
- no timestamps/process IDs/runtime durations appear in receipt.

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_cli -v
```

- [ ] **Step 3: Implement CLI**

Use `argparse`, `json.loads`, `evaluate_specimen`, and `canonical_receipt_bytes` only. Do not add logging to stdout.

- [ ] **Step 4: Run CLI tests and verify GREEN**

```bash
python -m unittest tests.test_cli -v
```

- [ ] **Step 5: Commit Task 9**

```bash
git add dogram/cli.py tests/test_cli.py
git commit -m "feat: add deterministic JSON CLI boundary"
```

---

### Task 10: Prove MutatedMathal lowering without adding mathal ontology

**Files:**
- Create: `examples/mutated_mathals/interest-mediated-support.json`
- Create: `examples/mutated_mathals/hidden-world-policy-rectangle.json`
- Create: `examples/mutated_mathals/trust-withdrawal.json`
- Create: `examples/mutated_mathals/same-surface-different-history.json`
- Create: `tests/test_mutated_mathal_examples.py`

**Interfaces:**
- No new runtime API.
- Examples must execute through `evaluate_specimen()` unchanged.

- [ ] **Step 1: Add interest-mediated-support example**

Lower the mathal into a `delta@1` specimen comparing a baseline trace and an interest-guided trace. The example metadata may name:

```json
{
  "mathal": "MEDIATED-SUPPORT-001",
  "claim_boundary": "formation-only",
  "note": "Dogram computes differences only; ALEX owns support semantics"
}
```

The operative inputs should show selected evidence and downstream score changing in the guided branch.

- [ ] **Step 2: Add frozen-evidence control inside the test**

Construct a sibling specimen in test code where interest metadata differs but operative evidence/score inputs do not. Assert identical Dogram result despite differing whole-specimen digest.

This directly proves `PRESENCE != CONSUMPTION` at the calculator boundary.

- [ ] **Step 3: Add hidden-world-policy rectangle example**

Use `rectangle@1` opaque mode where hidden-world equivalence holds under policy 0 and breaks under policy 1. Assert `interaction_detected == True` and no causal interpretation field exists.

- [ ] **Step 4: Add trust-withdrawal example**

Use `ablate@1` to remove one motivating edge. Choose the surviving version for the committed example so the candidate primitive remains reachable by independent domain paths after trust withdrawal.

Assert the receipt says only what reachability changed.

- [ ] **Step 5: Add same-surface-different-history example**

Use `reach@1` with graph mutation to demonstrate different reachable futures from explicitly different graph states while metadata holds the same surface label.

- [ ] **Step 6: Run examples through public engine**

```bash
python -m unittest tests.test_mutated_mathal_examples -v
```

Expected: all four examples produce `OK` and retain no special-case mathal logic in runtime modules.

- [ ] **Step 7: Commit Task 10**

```bash
git add examples/mutated_mathals tests/test_mutated_mathal_examples.py
git commit -m "test: prove mutated mathals lower into Dogram specimens"
```

---

### Task 11: Add README contract and operator cookbook

**Files:**
- Create: `README.md`

**Interfaces:**
- Documents existing runtime only; introduces no new behavior.

- [ ] **Step 1: Write README with constitutional boundary**

README must visibly include:

```text
DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.

TRUST MAY OPEN THE BRIDGE. IT MAY NOT CERTIFY THE BRIDGE.
PRESENCE IS NOT CONSUMPTION.
GRAPH PATH != CAUSAL PATH.
```

- [ ] **Step 2: Document the MutatedMathal lowering recipe**

Use exactly this conceptual sequence:

```text
MUTATED MATHAL
    -> choose one discriminator
    -> choose the smallest Dogram operator
    -> declare typed specimen
    -> run calculation
    -> retain calculation receipt
    -> send receipt to ALEX / human pressure
```

Explain that one mathal may lower to several specimens and that a Dogram `OK` is execution success, not mathal promotion.

- [ ] **Step 3: Include one runnable example per operator**

Commands:

```bash
python -m dogram.cli examples/mutated_mathals/interest-mediated-support.json
python -m dogram.cli examples/mutated_mathals/hidden-world-policy-rectangle.json
python -m dogram.cli examples/mutated_mathals/trust-withdrawal.json
python -m dogram.cli examples/mutated_mathals/same-surface-different-history.json
```

- [ ] **Step 4: Commit Task 11**

```bash
git add README.md
git commit -m "docs: document Dogram mutated mathal workflow"
```

---

### Task 12: Full hostile verification and release floor

**Files:**
- Modify only if verification exposes a defect: files introduced by Tasks 1–11.

**Interfaces:**
- Final proof commands only.

- [ ] **Step 1: Run full offline unit suite**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass with no network requirement.

- [ ] **Step 2: Run byte-stability checks twice**

For each example:

```bash
python -m dogram.cli examples/mutated_mathals/trust-withdrawal.json > /tmp/dogram-a.json
python -m dogram.cli examples/mutated_mathals/trust-withdrawal.json > /tmp/dogram-b.json
cmp /tmp/dogram-a.json /tmp/dogram-b.json
```

Repeat for all four examples. Expected: every `cmp` exits 0.

- [ ] **Step 3: Run semantic-surface absence scan**

```bash
grep -RInE 'SUPPORTS|evidence authority|historically true|causal path' dogram/ || true
```

Review every match. Accept only explicit refusal/documentation strings; no operator may emit semantic promotion.

- [ ] **Step 4: Verify no runtime dependencies**

```bash
python - <<'PY'
import tomllib
with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
assert data['project']['dependencies'] == []
print('PASS stdlib-only dependency declaration')
PY
```

- [ ] **Step 5: Verify package compiles**

```bash
python -m compileall -q dogram tests
```

Expected: exit 0.

- [ ] **Step 6: Confirm exact public operator floor**

```bash
python - <<'PY'
from dogram.engine import OPERATORS
assert set(OPERATORS) == {('delta', 1), ('rectangle', 1), ('ablate', 1), ('reach', 1)}
print('PASS operator floor')
PY
```

- [ ] **Step 7: Commit any verification-only fixes, then record exact head**

If fixes were necessary, each fix gets its own focused commit and the full suite is rerun afterward. Record the final commit SHA and exact `python -m unittest discover -s tests -v` result in the eventual PR/release receipt.

---

## MutatedMathal Readiness Criterion

Dogram v0 is **ready for MutatedMathals** when a new mathal can be added without editing runtime code if its discriminator can be expressed as one or more of:

```text
ordered typed trace difference      -> delta@1
binary-coordinate interaction       -> rectangle@1
remove-one graph dependency         -> ablate@1
explicit graph mutation/reachability -> reach@1
```

The readiness test is therefore not “Dogram understands the mathal.” It is:

> **Can the mathal expose a falsifiable discriminator that lowers into a declared Dogram specimen while all semantic interpretation remains outside the calculator?**

If a genuinely useful MutatedMathal cannot be lowered into this floor without distorting the question, preserve that failure as the receipt that may justify Dogram v1 rather than widening v0 preemptively.

## Plan Self-Review

- **Spec coverage:** all four specified operators, typed values, exact arithmetic, canonical receipts, structured refusals, deterministic CLI, hostile synthetic specimens, stdlib-only floor, semantic boundary, and versioning are assigned to explicit tasks.
- **MutatedMathal readiness:** added as examples/tests only; no plugin system, mathal registry, or semantic predicate layer was introduced.
- **Placeholder scan:** no TODO/TBD/“implement later” instructions remain.
- **Type consistency:** `ScalarValue`, `DirectedGraph`, `evaluate_*`, `evaluate_specimen`, receipt statuses, operator versions, and specimen/receipt schema names are consistent throughout the plan.
- **Scope control:** symbolic algebra, Hodge decomposition, optimization, statistics, Wolfram integration, graph spectra, visualization, persistent storage, and ALEX semantic evaluation remain deferred exactly as the design requires.
