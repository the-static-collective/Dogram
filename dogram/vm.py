from __future__ import annotations

from typing import Any

from .canonical import sha256_json
from .intrinsics import IntrinsicRefusal
from .program import Program
from .registry import Registry, RegistryLookupError
from .vm_types import StepTrace, VMConfig, VMExecution


def _path_get(container: Any, path: list[Any]) -> Any:
    current = container
    for part in path:
        if isinstance(current, dict) and isinstance(part, str) and part in current:
            current = current[part]
        elif isinstance(current, list) and type(part) is int and 0 <= part < len(current):
            current = current[part]
        else:
            raise KeyError(part)
    return current


def _resolve(value: Any, inputs: Any, step_results: dict[str, Any]) -> Any:
    if isinstance(value, list):
        return [_resolve(item, inputs, step_results) for item in value]
    if not isinstance(value, dict):
        return value
    if set(value) == {"literal"}:
        return value["literal"]
    if value.get("ref") == "input":
        return _path_get(inputs, value.get("path", []))
    if value.get("ref") == "step":
        base = step_results[value["step"]]
        return _path_get(base, value.get("path", []))
    return {key: _resolve(item, inputs, step_results) for key, item in value.items()}


def _refuse(reason_code: str, residual: str, trace: list[StepTrace], fuel: int) -> VMExecution:
    return VMExecution(
        status="REFUSE",
        result=None,
        reason_code=reason_code,
        residuals=(residual,),
        step_trace=tuple(trace),
        fuel_remaining=fuel,
    )


def execute_program(
    program: Program,
    inputs: Any,
    registry: Registry,
    config: VMConfig | None = None,
) -> VMExecution:
    config = config or VMConfig()
    fuel = config.max_exec_steps
    step_results: dict[str, Any] = {}
    trace: list[StepTrace] = []

    for step in program.steps:
        if fuel <= 0:
            return _refuse("FUEL_EXHAUSTED", "execution fuel exhausted", trace, fuel)
        try:
            args = tuple(_resolve(arg, inputs, step_results) for arg in step.args)
        except (KeyError, IndexError, TypeError) as exc:
            return _refuse("ADDRESS_NOT_FOUND", f"operand address not found: {exc}", trace, fuel)

        try:
            intrinsic = registry.resolve(step.op)
        except RegistryLookupError:
            return _refuse("UNKNOWN_OPERATION", step.op, trace, fuel)

        fuel_before = fuel
        fuel -= 1
        try:
            result = intrinsic(args)
        except IntrinsicRefusal as exc:
            return _refuse(exc.reason_code, exc.residual, trace, fuel)

        step_results[step.id] = result
        trace.append(
            StepTrace(
                step_id=step.id,
                op=step.op,
                arg_digest=sha256_json(list(args)),
                result_digest=sha256_json(result),
                fuel_before=fuel_before,
                fuel_after=fuel,
            )
        )

    try:
        result = _resolve(program.result, inputs, step_results)
    except (KeyError, IndexError, TypeError) as exc:
        return _refuse("ADDRESS_NOT_FOUND", f"result address not found: {exc}", trace, fuel)

    return VMExecution(
        status="OK",
        result=result,
        reason_code=None,
        residuals=(),
        step_trace=tuple(trace),
        fuel_remaining=fuel,
    )


__all__ = ["VMConfig", "VMExecution", "execute_program"]
