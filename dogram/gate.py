from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_json
from .program import Program, ProgramDecodeError, decode_program, encode_program, program_digest
from .proposal import ProposalDecodeError, RemoveStepProposal, decode_proposal
from .registry import Registry, RegistryLookupError


@dataclass(frozen=True)
class GateLimits:
    max_program_steps: int = 1000

    def __post_init__(self) -> None:
        if type(self.max_program_steps) is not int or self.max_program_steps < 0:
            raise ValueError("max_program_steps must be a non-negative integer")


@dataclass(frozen=True)
class GateDisposition:
    status: str
    reason_code: str | None
    residuals: tuple[str, ...]
    proposal_id: str | None
    program: Program | None
    program_digest: str | None

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "residuals": list(self.residuals),
            "proposal_id": self.proposal_id,
            "program_digest": self.program_digest,
        }


def _refuse(
    reason_code: str,
    residual: str,
    proposal_id: str | None = None,
) -> GateDisposition:
    return GateDisposition(
        status="REFUSE",
        reason_code=reason_code,
        residuals=(residual,),
        proposal_id=proposal_id,
        program=None,
        program_digest=None,
    )


def _references_step(value: Any, target_step: str) -> bool:
    if isinstance(value, list):
        return any(_references_step(item, target_step) for item in value)
    if not isinstance(value, dict):
        return False
    if value.get("ref") == "step" and value.get("step") == target_step:
        return True
    return any(_references_step(item, target_step) for item in value.values())


def _remove_step(program: Program, proposal: RemoveStepProposal) -> Program:
    raw = encode_program(program)
    raw["steps"] = [
        step
        for step in raw["steps"]
        if step["id"] != proposal.step_id
    ]
    return decode_program(raw)


def phase_gate(
    proposal_data: Any,
    current_program: Program,
    current_execution_data: dict[str, Any],
    registry: Registry,
    limits: GateLimits | None = None,
) -> GateDisposition:
    limits = limits or GateLimits()

    try:
        proposal = decode_proposal(proposal_data)
    except ProposalDecodeError as exc:
        return _refuse(exc.reason_code, exc.residual)

    if proposal.base_program_digest != program_digest(current_program):
        return _refuse(
            "STALE_BASE_PROGRAM",
            "proposal base program digest does not match current program",
            proposal.proposal_id,
        )

    try:
        execution_digest = sha256_json(current_execution_data)
    except (TypeError, ValueError, OverflowError):
        return _refuse(
            "MALFORMED_EXECUTION_DATA",
            "current execution data is not canonical JSON",
            proposal.proposal_id,
        )

    if proposal.base_execution_digest != execution_digest:
        return _refuse(
            "STALE_BASE_EXECUTION",
            "proposal base execution digest does not match current execution",
            proposal.proposal_id,
        )

    target = next(
        (step for step in current_program.steps if step.id == proposal.step_id),
        None,
    )
    if target is None:
        return _refuse(
            "TARGET_NOT_FOUND",
            proposal.step_id,
            proposal.proposal_id,
        )

    target_seen = False
    for step in current_program.steps:
        if step.id == proposal.step_id:
            target_seen = True
            continue
        if target_seen and any(_references_step(arg, proposal.step_id) for arg in step.args):
            return _refuse(
                "DANGLING_STEP_REFERENCE",
                step.id,
                proposal.proposal_id,
            )

    if _references_step(current_program.result, proposal.step_id):
        return _refuse(
            "DANGLING_RESULT_REFERENCE",
            proposal.step_id,
            proposal.proposal_id,
        )

    try:
        candidate = _remove_step(current_program, proposal)
    except ProgramDecodeError as exc:
        return _refuse(
            exc.reason_code,
            exc.residual,
            proposal.proposal_id,
        )

    if len(candidate.steps) > limits.max_program_steps:
        return _refuse(
            "PROGRAM_TOO_LARGE",
            str(len(candidate.steps)),
            proposal.proposal_id,
        )

    for step in candidate.steps:
        try:
            registry.resolve(step.op)
        except RegistryLookupError:
            return _refuse(
                "UNKNOWN_OPERATION",
                step.op,
                proposal.proposal_id,
            )

    candidate_digest = program_digest(candidate)
    return GateDisposition(
        status="ADMIT",
        reason_code=None,
        residuals=(),
        proposal_id=proposal.proposal_id,
        program=candidate,
        program_digest=candidate_digest,
    )


__all__ = [
    "GateDisposition",
    "GateLimits",
    "phase_gate",
]
