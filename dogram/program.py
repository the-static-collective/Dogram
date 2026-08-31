from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_json


class ProgramDecodeError(ValueError):
    def __init__(self, reason_code: str, residual: str):
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


@dataclass(frozen=True)
class ProgramStep:
    id: str
    op: str
    args: tuple[Any, ...]


@dataclass(frozen=True)
class Program:
    program_id: str
    program_version: int
    steps: tuple[ProgramStep, ...]
    result: Any


def _ref_error(reason_code: str, residual: str) -> None:
    raise ProgramDecodeError(reason_code, residual)


def _validate_value(value: Any, prior_steps: set[str]) -> None:
    if isinstance(value, list):
        for item in value:
            _validate_value(item, prior_steps)
        return

    if not isinstance(value, dict):
        return

    if "literal" in value:
        if set(value) != {"literal"}:
            _ref_error("MALFORMED_OPERAND", "literal operand must contain only literal")
        return

    if "ref" in value:
        ref = value.get("ref")
        if ref == "input":
            if set(value) not in ({"ref", "path"}, {"ref"}):
                _ref_error("MALFORMED_OPERAND", "input reference has unknown fields")
            path = value.get("path", [])
            if not isinstance(path, list) or not all(isinstance(part, (str, int)) and not isinstance(part, bool) for part in path):
                _ref_error("MALFORMED_OPERAND", "input path must be a list of string/integer segments")
            return
        if ref == "step":
            if set(value) not in ({"ref", "step", "path"}, {"ref", "step"}):
                _ref_error("MALFORMED_OPERAND", "step reference has unknown fields")
            step = value.get("step")
            if not isinstance(step, str) or not step:
                _ref_error("MALFORMED_OPERAND", "step reference requires a non-empty step id")
            if step not in prior_steps:
                _ref_error("CYCLIC_OR_FORWARD_REFERENCE", f"step reference {step!r} is not an earlier step")
            path = value.get("path", [])
            if not isinstance(path, list) or not all(isinstance(part, (str, int)) and not isinstance(part, bool) for part in path):
                _ref_error("MALFORMED_OPERAND", "step path must be a list of string/integer segments")
            return
        _ref_error("MALFORMED_OPERAND", f"unsupported reference namespace: {ref!r}")

    for item in value.values():
        _validate_value(item, prior_steps)


def decode_program(spec: dict[str, Any]) -> Program:
    if not isinstance(spec, dict):
        raise ProgramDecodeError("MALFORMED_PROGRAM", "program must be an object")

    required = {"schema", "program_id", "program_version", "steps", "result"}
    if set(spec) != required or spec.get("schema") != "dogram.program/v0":
        raise ProgramDecodeError("MALFORMED_PROGRAM", "invalid dogram.program/v0 envelope")

    program_id = spec.get("program_id")
    program_version = spec.get("program_version")
    raw_steps = spec.get("steps")
    if not isinstance(program_id, str) or not program_id:
        raise ProgramDecodeError("MALFORMED_PROGRAM", "program_id must be non-empty")
    if type(program_version) is not int or program_version < 1:
        raise ProgramDecodeError("MALFORMED_PROGRAM", "program_version must be a positive integer")
    if not isinstance(raw_steps, list):
        raise ProgramDecodeError("MALFORMED_PROGRAM", "steps must be a list")

    prior_steps: set[str] = set()
    steps: list[ProgramStep] = []
    for raw_step in raw_steps:
        if not isinstance(raw_step, dict) or set(raw_step) != {"id", "op", "args"}:
            raise ProgramDecodeError("MALFORMED_STEP", "each step must contain id, op, and args")
        step_id = raw_step.get("id")
        op = raw_step.get("op")
        args = raw_step.get("args")
        if not isinstance(step_id, str) or not step_id:
            raise ProgramDecodeError("MALFORMED_STEP", "step id must be non-empty")
        if step_id in prior_steps:
            raise ProgramDecodeError("DUPLICATE_STEP_ID", step_id)
        if not isinstance(op, str) or not op:
            raise ProgramDecodeError("MALFORMED_STEP", "step op must be non-empty")
        if not isinstance(args, list):
            raise ProgramDecodeError("MALFORMED_STEP", "step args must be a list")
        for arg in args:
            _validate_value(arg, prior_steps)
        steps.append(ProgramStep(step_id, op, tuple(args)))
        prior_steps.add(step_id)

    result = spec.get("result")
    _validate_value(result, prior_steps)
    return Program(program_id, program_version, tuple(steps), result)


def encode_program(program: Program) -> dict[str, Any]:
    return {
        "schema": "dogram.program/v0",
        "program_id": program.program_id,
        "program_version": program.program_version,
        "steps": [
            {"id": step.id, "op": step.op, "args": list(step.args)}
            for step in program.steps
        ],
        "result": program.result,
    }


def program_digest(program: Program) -> str:
    return sha256_json(encode_program(program))
