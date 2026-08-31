import unittest

from dogram.gate import GateLimits, phase_gate
from dogram.program import decode_program, program_digest
from dogram.proposal import RemoveStepProposal, encode_proposal
from dogram.registry import build_bootstrap_registry
from dogram.reify import reify_execution
from dogram.vm import execute_program


def make_program(*, dangling_step=False, dangling_result=False, unknown_op=False):
    steps = [
        {
            "id": "value",
            "op": "core.get@1",
            "args": [{"ref": "input", "path": ["value"]}, {"literal": []}],
        },
        {
            "id": "diagnostic",
            "op": "host.eval@1" if unknown_op else "core.length@1",
            "args": [{"ref": "input", "path": ["diagnostic"]}],
        },
    ]
    if dangling_step:
        steps.append(
            {
                "id": "uses-diagnostic",
                "op": "core.same@1",
                "args": [
                    {"ref": "step", "step": "diagnostic"},
                    {"literal": 3},
                ],
            }
        )
    result = (
        {"ref": "step", "step": "diagnostic"}
        if dangling_result
        else {"ref": "step", "step": "value"}
    )
    return decode_program(
        {
            "schema": "dogram.program/v0",
            "program_id": "test/gate",
            "program_version": 1,
            "steps": steps,
            "result": result,
        }
    )


def gate_inputs(program):
    inputs = {"value": {"answer": 42}, "diagnostic": [1, 2, 3]}
    execution = execute_program(program, inputs, build_bootstrap_registry())
    execution_data, execution_digest = reify_execution(program, inputs, execution)
    proposal = RemoveStepProposal(
        proposal_id="proposal-gate",
        base_program_digest=program_digest(program),
        base_execution_digest=execution_digest,
        step_id="diagnostic",
    )
    return execution_data, encode_proposal(proposal)


class GateTests(unittest.TestCase):
    def test_admits_unused_step_removal_and_returns_new_digest(self):
        program = make_program()
        execution_data, proposal = gate_inputs(program)

        disposition = phase_gate(
            proposal,
            program,
            execution_data,
            build_bootstrap_registry(),
        )

        self.assertEqual(disposition.status, "ADMIT")
        self.assertIsNotNone(disposition.program)
        self.assertEqual([step.id for step in disposition.program.steps], ["value"])
        self.assertNotEqual(disposition.program_digest, program_digest(program))

    def test_stale_program_digest_refuses(self):
        program = make_program()
        execution_data, proposal = gate_inputs(program)
        proposal["base_program_digest"] = "sha256:" + "0" * 64
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "STALE_BASE_PROGRAM"))

    def test_stale_execution_digest_refuses(self):
        program = make_program()
        execution_data, proposal = gate_inputs(program)
        proposal["base_execution_digest"] = "sha256:" + "0" * 64
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "STALE_BASE_EXECUTION"))

    def test_missing_target_refuses(self):
        program = make_program()
        execution_data, proposal = gate_inputs(program)
        proposal["payload"]["step_id"] = "absent"
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "TARGET_NOT_FOUND"))

    def test_dangling_later_step_reference_refuses(self):
        program = make_program(dangling_step=True)
        execution_data, proposal = gate_inputs(program)
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "DANGLING_STEP_REFERENCE"))

    def test_dangling_final_result_reference_refuses(self):
        program = make_program(dangling_result=True)
        execution_data, proposal = gate_inputs(program)
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "DANGLING_RESULT_REFERENCE"))

    def test_unknown_remaining_operation_refuses(self):
        program = decode_program(
            {
                "schema": "dogram.program/v0",
                "program_id": "test/gate-unknown",
                "program_version": 1,
                "steps": [
                    {"id": "unknown", "op": "host.eval@1", "args": []},
                    {"id": "diagnostic", "op": "core.length@1", "args": [{"literal": []}]},
                ],
                "result": {"literal": "done"},
            }
        )
        execution_data = {
            "schema": "dogram.execution-data/v0",
            "program_digest": program_digest(program),
            "input_digest": "sha256:" + "3" * 64,
            "status": "REFUSE",
            "result": None,
            "reason_code": "UNKNOWN_OPERATION",
            "residuals": ["host.eval@1"],
            "step_trace": [],
            "consumed_input_addresses": [],
            "fuel_remaining": 1000,
        }
        from dogram.canonical import sha256_json
        proposal = encode_proposal(
            RemoveStepProposal(
                proposal_id="proposal-unknown",
                base_program_digest=program_digest(program),
                base_execution_digest=sha256_json(execution_data),
                step_id="diagnostic",
            )
        )
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "UNKNOWN_OPERATION"))

    def test_candidate_over_step_limit_refuses(self):
        program = make_program(dangling_step=True)
        execution_data, proposal = gate_inputs(program)
        proposal["payload"]["step_id"] = "uses-diagnostic"
        disposition = phase_gate(
            proposal,
            program,
            execution_data,
            build_bootstrap_registry(),
            GateLimits(max_program_steps=1),
        )
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "PROGRAM_TOO_LARGE"))

    def test_malformed_proposal_refuses_at_gate_boundary(self):
        program = make_program()
        execution_data, proposal = gate_inputs(program)
        proposal["payload"]["code"] = "eval('nope')"
        disposition = phase_gate(proposal, program, execution_data, build_bootstrap_registry())
        self.assertEqual((disposition.status, disposition.reason_code), ("REFUSE", "MALFORMED_PROPOSAL"))


if __name__ == "__main__":
    unittest.main()
