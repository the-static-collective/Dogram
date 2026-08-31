from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ProposalDecodeError(ValueError):
    def __init__(self, reason_code: str, residual: str):
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


@dataclass(frozen=True)
class RemoveStepProposal:
    proposal_id: str
    base_program_digest: str
    base_execution_digest: str
    step_id: str


def _malformed(residual: str) -> None:
    raise ProposalDecodeError("MALFORMED_PROPOSAL", residual)


def _is_sha256_digest(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    payload = value[7:]
    return len(payload) == 64 and all(char in "0123456789abcdef" for char in payload)


def decode_proposal(spec: Any) -> RemoveStepProposal:
    required = {
        "schema",
        "proposal_id",
        "proposal_version",
        "kind",
        "base_program_digest",
        "base_execution_digest",
        "payload",
    }
    if not isinstance(spec, dict) or set(spec) != required:
        _malformed("invalid dogram.proposal/v0 envelope")
    if spec.get("schema") != "dogram.proposal/v0":
        _malformed("unsupported proposal schema")
    if spec.get("proposal_version") != 1 or type(spec.get("proposal_version")) is not int:
        _malformed("proposal_version must be exactly 1")
    if spec.get("kind") != "program_patch":
        _malformed("only program_patch is admitted")

    proposal_id = spec.get("proposal_id")
    if not isinstance(proposal_id, str) or not proposal_id:
        _malformed("proposal_id must be non-empty")

    base_program_digest = spec.get("base_program_digest")
    base_execution_digest = spec.get("base_execution_digest")
    if not _is_sha256_digest(base_program_digest):
        _malformed("base_program_digest must be a canonical sha256 digest")
    if not _is_sha256_digest(base_execution_digest):
        _malformed("base_execution_digest must be a canonical sha256 digest")

    payload = spec.get("payload")
    if not isinstance(payload, dict) or set(payload) != {"op", "step_id"}:
        _malformed("program_patch payload must contain only op and step_id")
    if payload.get("op") != "remove_step":
        _malformed("only remove_step is admitted")
    step_id = payload.get("step_id")
    if not isinstance(step_id, str) or not step_id:
        _malformed("step_id must be non-empty")

    return RemoveStepProposal(
        proposal_id=proposal_id,
        base_program_digest=base_program_digest,
        base_execution_digest=base_execution_digest,
        step_id=step_id,
    )


def encode_proposal(proposal: RemoveStepProposal) -> dict[str, Any]:
    return {
        "schema": "dogram.proposal/v0",
        "proposal_id": proposal.proposal_id,
        "proposal_version": 1,
        "kind": "program_patch",
        "base_program_digest": proposal.base_program_digest,
        "base_execution_digest": proposal.base_execution_digest,
        "payload": {
            "op": "remove_step",
            "step_id": proposal.step_id,
        },
    }


__all__ = [
    "ProposalDecodeError",
    "RemoveStepProposal",
    "decode_proposal",
    "encode_proposal",
]
