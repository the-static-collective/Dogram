import unittest

from dogram.proposal import (
    ProposalDecodeError,
    RemoveStepProposal,
    decode_proposal,
    encode_proposal,
)


PROGRAM_DIGEST = "sha256:" + "1" * 64
EXECUTION_DIGEST = "sha256:" + "2" * 64


def valid_proposal_data():
    return {
        "schema": "dogram.proposal/v0",
        "proposal_id": "proposal-001",
        "proposal_version": 1,
        "kind": "program_patch",
        "base_program_digest": PROGRAM_DIGEST,
        "base_execution_digest": EXECUTION_DIGEST,
        "payload": {
            "op": "remove_step",
            "step_id": "diagnostic",
        },
    }


class ProposalTests(unittest.TestCase):
    def test_decodes_and_reencodes_exact_remove_step_proposal(self):
        raw = valid_proposal_data()
        proposal = decode_proposal(raw)
        self.assertEqual(
            proposal,
            RemoveStepProposal(
                proposal_id="proposal-001",
                base_program_digest=PROGRAM_DIGEST,
                base_execution_digest=EXECUTION_DIGEST,
                step_id="diagnostic",
            ),
        )
        self.assertEqual(encode_proposal(proposal), raw)

    def test_unknown_top_level_field_refuses(self):
        raw = valid_proposal_data()
        raw["authority"] = "self-granted"
        with self.assertRaises(ProposalDecodeError) as raised:
            decode_proposal(raw)
        self.assertEqual(raised.exception.reason_code, "MALFORMED_PROPOSAL")

    def test_unknown_kind_refuses(self):
        raw = valid_proposal_data()
        raw["kind"] = "peel"
        with self.assertRaises(ProposalDecodeError) as raised:
            decode_proposal(raw)
        self.assertEqual(raised.exception.reason_code, "MALFORMED_PROPOSAL")

    def test_unknown_patch_operation_refuses(self):
        raw = valid_proposal_data()
        raw["payload"]["op"] = "replace_program"
        with self.assertRaises(ProposalDecodeError) as raised:
            decode_proposal(raw)
        self.assertEqual(raised.exception.reason_code, "MALFORMED_PROPOSAL")

    def test_payload_unknown_field_refuses(self):
        raw = valid_proposal_data()
        raw["payload"]["code"] = "eval('nope')"
        with self.assertRaises(ProposalDecodeError) as raised:
            decode_proposal(raw)
        self.assertEqual(raised.exception.reason_code, "MALFORMED_PROPOSAL")

    def test_invalid_ancestry_digest_refuses(self):
        raw = valid_proposal_data()
        raw["base_execution_digest"] = "latest"
        with self.assertRaises(ProposalDecodeError) as raised:
            decode_proposal(raw)
        self.assertEqual(raised.exception.reason_code, "MALFORMED_PROPOSAL")


if __name__ == "__main__":
    unittest.main()
