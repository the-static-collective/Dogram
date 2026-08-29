# Dogram Mathal VM + Standard Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic, data-only Mathal VM and migrate `delta`, `rectangle`, `ablate`, and `reach` onto versioned mathal programs while retaining the existing Python implementations as independent conformance oracles.

**Architecture:** Phase A remains the direct Python oracle floor described by `2026-08-28-dogram-v0-implementation.md`. This plan adds an inert `dogram.program/v0` representation, a static intrinsic registry, a bounded acyclic evaluator, automatic step tracing, and four stdlib mathal programs. The public engine does not switch to VM implementations until each operator agrees with its Python oracle across the hostile corpus.

**Tech Stack:** Python >= 3.12, standard library only (`json`, `hashlib`, `dataclasses`, `fractions`, `collections`, `unittest`).

**Spec:** `docs/superpowers/specs/2026-08-28-dogram-metaoscillatory-runtime-design.md`

## Global Constraints

- Phase A from `docs/superpowers/plans/2026-08-28-dogram-v0-implementation.md` must be green before this plan begins.
- Python >= 3.12; no third-party runtime dependencies.
- Program schemas are inert data. No `eval`, `exec`, dynamic import, callback, callable, file handle, module reference, or network access may cross the VM boundary.
- Program graphs are acyclic in `dogram.program/v0`; recursion is refused.
- VM fuel is explicit and deterministic; every executed step consumes one unit plus nested-call work.
- Trace emission is automatic runtime behavior, not an optional mathal opcode.
- `OK`, `REFUSE`, and `INSUFFICIENT_TO_TEST` remain the only top-level result statuses.
- `FUEL_EXHAUSTED` is a `REFUSE` reason code.
- A mathal stdlib operator is not considered conformant merely because it returns the same happy-path value; refusal behavior and the declared equivalence lens are part of conformance.
- `DOGRAM OUTPUT != SUPPORT`, `REACHABLE != TRUE`, `EQUIVALENT != IDENTICAL` remain unchanged.

---

## File Structure

```text
Dogram/
  dogram/
    program.py              # parse/validate/canonicalize inert programs
    registry.py             # static intrinsic + admitted-program lookup
    vm.py                   # bounded acyclic evaluator + automatic trace
    vm_types.py             # VM result/fuel/step trace dataclasses
    intrinsics/
      __init__.py
      core.py               # generic value/list/template operations
      graph.py              # graph mutation/query primitives
    stdlib/
      delta.mathal.json
      rectangle.mathal.json
      ablate.mathal.json
      reach.mathal.json
    engine.py               # adds oracle/vm execution mode after conformance
  tests/
    test_program.py
    test_registry.py
    test_vm.py
    test_vm_delta.py
    test_vm_rectangle.py
    test_vm_ablate.py
    test_vm_reach.py
    test_vm_conformance.py
```

The VM resolves operands recursively from three namespaces:

```text
{"ref":"input","path":[...]}
{"ref":"step","step":"step-id","path":[...]}
{"literal": <canonical JSON value>}
```

Program results are JSON templates containing those same operand references. This keeps record construction in data rather than adding a general code-evaluation surface.

---

### Task 1: Add inert program parsing, canonicalization, and cycle refusal

**Files:**
- Create: `dogram/program.py`
- Create: `tests/test_program.py`

**Interfaces:**
- Produces: `ProgramDecodeError(reason_code: str, residual: str)`.
- Produces: immutable `Program(program_id: str, program_version: int, steps: tuple[ProgramStep, ...], result: object)`.
- Produces: `decode_program(spec: dict) -> Program`.
- Produces: `encode_program(program: Program) -> dict`.
- Produces: `program_digest(program: Program) -> str`.

- [ ] **Step 1: Write RED tests for canonical program identity**

```python
import unittest

from dogram.program import ProgramDecodeError, decode_program, encode_program, program_digest


class ProgramTests(unittest.TestCase):
    def test_key_order_does_not_change_program_digest(self):
        a = {
            "schema": "dogram.program/v0",
            "program_id": "test/identity",
            "program_version": 1,
            "steps": [{"id": "s1", "op": "core.same@1", "args": [{"literal": 1}, {"literal": 1}]}],
            "result": {"ref": "step", "step": "s1"},
        }
        b = {"result": a["result"], "steps": a["steps"], "program_version": 1, "program_id": "test/identity", "schema": "dogram.program/v0"}
        self.assertEqual(program_digest(decode_program(a)), program_digest(decode_program(b)))

    def test_duplicate_step_ids_refuse(self):
        spec = {
            "schema": "dogram.program/v0",
            "program_id": "bad/dup",
            "program_version": 1,
            "steps": [
                {"id": "s1", "op": "core.same@1", "args": []},
                {"id": "s1", "op": "core.same@1", "args": []},
            ],
            "result": {"literal": None},
        }
        with self.assertRaises(ProgramDecodeError) as ctx:
            decode_program(spec)
        self.assertEqual(ctx.exception.reason_code, "DUPLICATE_STEP_ID")
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_program -v
```

Expected: import failure because `dogram.program` does not exist.

- [ ] **Step 3: Implement immutable program types and canonical encoding**

Use focused dataclasses:

```python
@dataclass(frozen=True)
class ProgramStep:
    id: str
    op: str
    args: tuple[object, ...]

@dataclass(frozen=True)
class Program:
    program_id: str
    program_version: int
    steps: tuple[ProgramStep, ...]
    result: object
```

Validation must require exact schema `dogram.program/v0`, non-empty `program_id`, positive integer version, unique step IDs, and operand references only to input or earlier steps. A step referencing itself or a later step refuses with `CYCLIC_OR_FORWARD_REFERENCE`.

- [ ] **Step 4: Add cycle/unknown-reference tests and run GREEN**

```bash
python -m unittest tests.test_program -v
```

Expected: all program tests pass.

- [ ] **Step 5: Commit**

```bash
git add dogram/program.py tests/test_program.py
git commit -m "feat: add inert versioned mathal programs"
```

---

### Task 2: Add the static intrinsic registry and generic bootstrap floor

**Files:**
- Create: `dogram/registry.py`
- Create: `dogram/intrinsics/__init__.py`
- Create: `dogram/intrinsics/core.py`
- Create: `dogram/intrinsics/graph.py`
- Create: `tests/test_registry.py`

**Interfaces:**
- Produces: `Intrinsic = Callable[[tuple[object, ...]], object]` internally; callables never appear in program data or receipts.
- Produces: `build_bootstrap_registry() -> Registry`.
- Registry resolves exact versioned names only.
- Initial admitted intrinsic IDs:

```text
core.get@1
core.same@1
core.add@1
core.sub@1
core.length@1
core.gt@1
core.select_first@1
trace.compare_ordered@1
graph.apply_mutation@1
graph.reachable_pairs@1
graph.query_paths@1
set.difference@1
```

- [ ] **Step 1: Write RED registry tests**

```python
class RegistryTests(unittest.TestCase):
    def test_unknown_intrinsic_is_not_resolved(self):
        registry = build_bootstrap_registry()
        with self.assertRaises(RegistryLookupError):
            registry.resolve("host.eval@1")

    def test_registry_contains_exact_bootstrap_floor(self):
        registry = build_bootstrap_registry()
        self.assertEqual(
            set(registry.ids()),
            {
                "core.get@1", "core.same@1", "core.add@1", "core.sub@1",
                "core.length@1", "core.gt@1", "core.select_first@1",
                "trace.compare_ordered@1", "graph.apply_mutation@1",
                "graph.reachable_pairs@1", "graph.query_paths@1", "set.difference@1",
            },
        )
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_registry -v
```

- [ ] **Step 3: Implement the core intrinsics**

`core.get@1` accepts `(container, path_list)` and performs only dict-key/list-index traversal. `core.same@1` returns a boolean using canonical JSON equality for JSON-like values. `core.add@1` and `core.sub@1` delegate typed exact arithmetic to the existing Phase-A value helpers rather than duplicating number policy. `core.select_first@1` requires a non-empty list and returns index `0`; an empty list raises `IntrinsicRefusal("EMPTY_SEQUENCE", ...)`.

`trace.compare_ordered@1` accepts `(boundary_order, left, right)` and returns:

```json
{
  "comparisons": [{"boundary":"...","relation":"SAME|DIFFERENT","delta":null}],
  "differences": ["boundary-id", "..."]
}
```

It is generic ordered comparison, not a final `delta` receipt.

- [ ] **Step 4: Implement graph/set intrinsics by delegating to Phase-A graph primitives**

`graph.apply_mutation@1` applies exactly one existing `ADD_NODE|REMOVE_NODE|ADD_EDGE|REMOVE_EDGE` mutation and returns normalized graph spec. `graph.reachable_pairs@1` returns deterministic reachable-pair lists. `graph.query_paths@1` returns deterministic path reports for supplied queries. `set.difference@1` accepts two JSON lists and returns canonical sorted list difference.

- [ ] **Step 5: Run registry + Phase-A regression**

```bash
python -m unittest tests.test_registry tests.test_values tests.test_graph -v
```

- [ ] **Step 6: Commit**

```bash
git add dogram/registry.py dogram/intrinsics tests/test_registry.py
git commit -m "feat: add explicit Dogram bootstrap registry"
```

---

### Task 3: Build the bounded acyclic Mathal VM with automatic tracing

**Files:**
- Create: `dogram/vm_types.py`
- Create: `dogram/vm.py`
- Create: `tests/test_vm.py`

**Interfaces:**
- Produces: `VMConfig(max_exec_steps: int = 1000, max_call_depth: int = 8)`.
- Produces: `VMExecution(status, result, reason_code, residuals, step_trace, fuel_remaining)`.
- Produces: `execute_program(program: Program, inputs: object, registry: Registry, config: VMConfig | None = None) -> VMExecution`.
- Step trace entries contain only canonical data: `step_id`, `op`, `arg_digest`, `result_digest`, `fuel_before`, `fuel_after`.

- [ ] **Step 1: Write RED identity execution test**

```python
class VMTests(unittest.TestCase):
    def test_executes_one_step_and_traces_automatically(self):
        program = decode_program({
            "schema": "dogram.program/v0",
            "program_id": "test/same",
            "program_version": 1,
            "steps": [{"id": "s1", "op": "core.same@1", "args": [{"literal": 7}, {"literal": 7}]}],
            "result": {"ref": "step", "step": "s1"},
        })
        result = execute_program(program, {}, build_bootstrap_registry(), VMConfig(max_exec_steps=2))
        self.assertEqual(result.status, "OK")
        self.assertIs(result.result, True)
        self.assertEqual(result.step_trace[0].step_id, "s1")
        self.assertEqual(result.fuel_remaining, 1)
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_vm -v
```

- [ ] **Step 3: Implement recursive operand/template resolution and one-fuel-per-step execution**

The VM iterates program steps in declared order. Before dispatch it resolves operands from input/earlier-step namespaces. It never places a registry callable into a resolved argument, step result, trace, or receipt.

- [ ] **Step 4: Add hostile tests**

Test exact refusals:

```text
unknown op                 -> REFUSE / UNKNOWN_OPERATION
fuel exhausted             -> REFUSE / FUEL_EXHAUSTED
bad input path             -> REFUSE / ADDRESS_NOT_FOUND
intrinsic refusal          -> REFUSE / intrinsic reason code
```

Also assert two identical executions produce byte-identical canonicalized `VMExecution.to_data()` payloads.

- [ ] **Step 5: Run GREEN**

```bash
python -m unittest tests.test_vm -v
```

- [ ] **Step 6: Commit**

```bash
git add dogram/vm.py dogram/vm_types.py tests/test_vm.py
git commit -m "feat: execute bounded mathal programs"
```

---

### Task 4: Lower `delta@1` into the Mathal VM and prove oracle parity

**Files:**
- Create: `dogram/stdlib/delta.mathal.json`
- Create: `tests/test_vm_delta.py`

**Interfaces:**
- Program id: `stdlib/delta`, version `1`.
- Consumes ordinary Phase-A delta `inputs` object unchanged.
- Produces the same result object as `evaluate_delta(inputs)` under `RESULT_EQUIVALENT`.

- [ ] **Step 1: Add RED stdlib program**

Program shape:

```json
{
  "schema":"dogram.program/v0",
  "program_id":"stdlib/delta",
  "program_version":1,
  "steps":[
    {"id":"cmp","op":"trace.compare_ordered@1","args":[
      {"ref":"input","path":["boundary_order"]},
      {"ref":"input","path":["left"]},
      {"ref":"input","path":["right"]}
    ]},
    {"id":"first","op":"core.select_first@1","args":[{"ref":"step","step":"cmp","path":["differences"]}]}
  ],
  "result":{
    "comparisons":{"ref":"step","step":"cmp","path":["comparisons"]},
    "first_difference":{"ref":"step","step":"first"}
  }
}
```

For the all-same case, `trace.compare_ordered@1` must expose a deterministic nullable `first_difference` field so the stdlib program does not turn an empty sequence into refusal. Update the program to read that field directly if needed; do not weaken `core.select_first@1` refusal semantics merely for this operator.

- [ ] **Step 2: Run oracle-vs-VM test and verify RED**

```bash
python -m unittest tests.test_vm_delta -v
```

- [ ] **Step 3: Make the smallest generic intrinsic/program adjustment needed for both differing and all-same traces**

The final delta mathal must not call `evaluate_delta` or any `delta.*` intrinsic.

- [ ] **Step 4: Run hostile parity corpus**

Assert for every Phase-A delta fixture:

```python
oracle_result, _ = evaluate_delta(inputs)
vm = execute_program(delta_program, inputs, registry)
self.assertEqual(vm.status, "OK")
self.assertEqual(vm.result, oracle_result)
```

Also compare malformed/refusal cases at engine boundary after Task 8.

- [ ] **Step 5: Commit**

```bash
git add dogram/stdlib/delta.mathal.json dogram/intrinsics tests/test_vm_delta.py
git commit -m "feat: lower delta into Dogram mathals"
```

---

### Task 5: Lower `rectangle`, `ablate`, and `reach` into stdlib mathals

**Files:**
- Create: `dogram/stdlib/rectangle.mathal.json`
- Create: `dogram/stdlib/ablate.mathal.json`
- Create: `dogram/stdlib/reach.mathal.json`
- Create: `tests/test_vm_rectangle.py`
- Create: `tests/test_vm_ablate.py`
- Create: `tests/test_vm_reach.py`

**Interfaces:**
- Program ids `stdlib/rectangle`, `stdlib/ablate`, `stdlib/reach`, version `1`.
- No stdlib program may call its corresponding Phase-A evaluator.

- [ ] **Step 1: Lower numeric rectangle through generic exact `core.sub@1` / `core.add@1` steps**

Use the algebra:

```text
mixed = (F11 - F10) - (F01 - F00)
```

Return the Phase-A result shape using a result template. Add one generic `core.kind@1` and one bounded conditional result selector only if the opaque-mode fixture requires them; do not add `rectangle.evaluate@1`.

- [ ] **Step 2: Prove rectangle parity**

```bash
python -m unittest tests.test_vm_rectangle -v
```

Numeric and opaque fixtures must agree with the oracle result under `RESULT_EQUIVALENT`.

- [ ] **Step 3: Lower ablate through graph primitives**

The mathal program must compute before/after graph digests, `reachable_pairs`, and deterministic lost/gained set differences from generic graph/set intrinsics. It may use `graph.apply_mutation@1`; it may not call `evaluate_ablate`.

- [ ] **Step 4: Prove ablate parity**

```bash
python -m unittest tests.test_vm_ablate -v
```

- [ ] **Step 5: Lower reach through `graph.apply_mutation@1` + `graph.query_paths@1`**

The program obtains before and after query reports independently and builds the final result template. It may not call `evaluate_reach`.

- [ ] **Step 6: Prove reach parity**

```bash
python -m unittest tests.test_vm_reach -v
```

- [ ] **Step 7: Commit**

```bash
git add dogram/stdlib tests/test_vm_rectangle.py tests/test_vm_ablate.py tests/test_vm_reach.py dogram/intrinsics
git commit -m "feat: lower Dogram operators into mathal stdlib"
```

---

### Task 6: Add oracle/VM conformance gate and switch the public engine only after proof

**Files:**
- Modify: `dogram/engine.py`
- Create: `tests/test_vm_conformance.py`

**Interfaces:**
- Preserve `evaluate_specimen(specimen: dict) -> dict`.
- Add internal `evaluate_specimen_oracle(specimen: dict) -> dict`.
- Add internal `evaluate_specimen_vm(specimen: dict) -> dict`.
- Public default switches to VM only after all conformance tests pass.

- [ ] **Step 1: Write RED conformance matrix**

Matrix covers every committed positive fixture and explicit malformed/refusal fixture for all four operators. For positive cases compare `status`, `result`, and declared operative `consumed_inputs`. For refusals compare `status` and `reason_code`.

The parity harness itself must use ordinary Python structural equality, not Dogram `delta`; Dogram-on-Dogram comparison may be emitted as an additional receipt but cannot be the sole oracle gate.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_vm_conformance -v
```

- [ ] **Step 3: Add explicit stdlib loader and VM dispatch**

Map exactly:

```python
STDLIB_PROGRAMS = {
    ("delta", 1): "stdlib/delta",
    ("rectangle", 1): "stdlib/rectangle",
    ("ablate", 1): "stdlib/ablate",
    ("reach", 1): "stdlib/reach",
}
```

Load packaged JSON by local package path only. No discovery scan and no network.

- [ ] **Step 4: Keep oracle path callable for tests and migration receipts**

Do not delete Phase-A `evaluate_*` modules.

- [ ] **Step 5: Run the full Phase A + Mathal VM suite**

```bash
python -m unittest discover -s tests -v
python -m compileall -q dogram tests
```

Expected: all tests pass; no operator-specific VM program invokes its Python oracle.

- [ ] **Step 6: Commit**

```bash
git add dogram/engine.py tests/test_vm_conformance.py
git commit -m "feat: make mathal stdlib the conformed execution path"
```

---

## Plan Self-Review

- **Spec coverage:** inert programs, static registry, acyclic evaluation, explicit fuel, automatic trace, stdlib lowering, oracle independence, and public-path migration are each assigned to a task.
- **Placeholder scan:** no TODO/TBD or unspecified error-handling steps remain.
- **Type consistency:** `Program`, `Registry`, `VMConfig`, `VMExecution`, operand references, stdlib IDs, and status/reason semantics are consistent across tasks.
- **Circularity check:** conformance uses independent Python structural equality before any Dogram-on-Dogram comparison.
- **Scope control:** reification-as-first-class runtime data, META, ProgramPatch, branching, and bootstrap peeling are intentionally excluded from this plan and belong to the next reviewed slices.
