import json
import unittest
from pathlib import Path

from dogram.tetrahedral_bianchi import (
    compose,
    identity,
    inverse,
    tetrahedral_bianchi_receipt,
)


FIXTURE = Path(__file__).parent / "fixtures" / "tetrahedral_bianchi_001.json"


def _edges(raw):
    return {
        tuple(int(part) for part in key.split(",")): tuple(value)
        for key, value in raw.items()
    }


class TetrahedralBianchiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_noncommuting_specimen_closes_only_after_transport(self):
        case = self.fixture["primary_noncommuting"]
        receipt = tetrahedral_bianchi_receipt(_edges(case["edges"]))
        expected = case["expected"]
        for field, value in expected.items():
            self.assertEqual(list(getattr(receipt, field)), value)
        self.assertEqual(receipt.transported_closure_residual, identity(3))
        self.assertNotEqual(receipt.naive_untransported_residual, identity(3))

    def test_commuting_control_can_hide_the_basepoint_error(self):
        case = self.fixture["commuting_control"]
        receipt = tetrahedral_bianchi_receipt(_edges(case["edges"]))
        expected = case["expected"]
        self.assertEqual(list(receipt.transported_closure_residual), expected["transported_closure_residual"])
        self.assertEqual(list(receipt.naive_untransported_residual), expected["naive_untransported_residual"])

    def test_naive_residual_is_the_commutator_in_the_frozen_specimen(self):
        case = self.fixture["primary_noncommuting"]
        edges = _edges(case["edges"])
        receipt = tetrahedral_bianchi_receipt(edges)
        a = edges[(0, 1)]
        b = edges[(1, 2)]
        commutator = compose(compose(compose(a, b), inverse(a)), inverse(b))
        self.assertEqual(receipt.naive_untransported_residual, commutator)
        self.assertEqual(list(commutator), [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
