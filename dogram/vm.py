from __future__ import annotations

from typing import Any

from .canonical import sha256_json
from .intrinsics import IntrinsicRefusal
from .program import Program
from .registry import Registry, RegistryLookupError
from .vm_types import InputAddress, StepTrace, VMConfig, VMExecution


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


def _resolve(
    value: Any,
    inputs: Any,
    step_results: dict[str, Any],
    consumed_input_addresses: list[InputAddress],
) -> Any:
    if isinstance(value, list):
        return [
            _resolve(item, inputs, step_results, consumed_input_addresses)
            for item in value
        ]
    if not isinstance(value, dict):
        return value
    if set(value) == {"literal"}:
        return value["literal"]
    if value.get("ref") == "input":
        path = value.get("path", [])
        resolved = _path_get(inputs, path)
        consumed_input_addresses.append(tuple(path))
        return resolved
    if value.get("ref") == "step":
        base = step_results[value["step"]]
        return _path_get(base, value.get("path", []))
    return {
        key: _resolve(item, inputs, step_results, consumed_input_addresses)
        for key, item in value.items()
    }


def _refuse(
    reason_code: str,
    residual: str,
    trace: list[StepTrace],
    consumed_input_addresses: list[InputAddress],
    fuel: int,
) -> VMExecution:
    return VMExecution(
        status="REFUSE",
        result=None,
        reason_code=reason_code,
        residuals=(residual,),
        step_trace=tuple(trace),
        consumed_input_addresses=tuple(consumed_input_addresses),
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
    consumed_input_addresses: list[InputAddress] = []

    for step in program.steps:
        if fuel <= 0:
            return _refuse(
                "FUEL_EXHAUSTED",
                "execution fuel exhausted",
                trace,
                consumed_input_addresses,
                fuel,
            )
        try:
            args = tuple(
                _resolve(arg, inputs, step_results, consumed_input_addresses)
                for arg in step.args
            )
        except (KeyError, IndexError, TypeError) as exc:
            return _refuse(
                "ADDRESS_NOT_FOUND",
                f"operand address not found: {exc}",
                trace,
                consumed_input_addresses,
                fuel,
            )

        try:
            intrinsic = registry.resolve(step.op)
        except RegistryLookupError:
            return _refuse(
                "UNKNOWN_OPERATION",
                step.op,
                trace,
                consumed_input_addresses,
                fuel,
            )

        fuel_before = fuel
        fuel -= 1
        try:
            result = intrinsic(args)
        except IntrinsicRefusal as exc:
            return _refuse(
                exc.reason_code,
                exc.residual,
                trace,
                consumed_input_addresses,
                fuel,
            )

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
        result = _resolve(program.result, inputs, step_results, consumed_input_addresses)
    except (KeyError, IndexError, TypeError) as exc:
        return _refuse(
            "ADDRESS_NOT_FOUND",
            f"result address not found: {exc}",
            trace,
            consumed_input_addresses,
            fuel,
        )

    return VMExecution(
        status="OK",
        result=result,
        reason_code=None,
        residuals=(),
        step_trace=tuple(trace),
        consumed_input_addresses=tuple(consumed_input_addresses),
        fuel_remaining=fuel,
    )


__all__ = ["VMConfig", "VMExecution", "execute_program"]
