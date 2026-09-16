import json
import unittest
from pathlib import Path

from dogram.lineage_spine import (
    append_from_crossing,
    make_ledger,
    make_root,
    store_capsule,
    store_receipt,
    verify_lineage,
)
from dogram.triangulator import compare_order, square, triangular, triangulator_001_receipt


FIXTURE = Path(__file__).parent / "fixtures" / "lineage_spine_001.json"


def build_specimen() -> dict[str, object]:
    ledger = make_ledger()
    root = make_root(5)
    root_digest = store_capsule(ledger, root)

    crossing0 = triangulator_001_receipt()
    store_receipt(ledger, crossing0)
    child1 = append_from_crossing(root, crossing0)
    child1_digest = store_capsule(ledger, child1)

    crossing1 = compare_order(
        child1["carrier"],
        square,
        triangular,
        structure_test=lambda n, delta: delta == triangular(n - 1) ** 2,
        structure_label="delta == triangular(carrier - 1)^2",
    )
    store_receipt(ledger, crossing1)
    child2 = append_from_crossing(child1, crossing1)
    child2_digest = store_capsule(ledger, child2)

    return {
        "head_digest": child2_digest,
        "root_digest": root_digest,
        "ledger": ledger,
        "verification": verify_lineage(child2_digest, ledger),
    }


class LineageSpineFixtureTests(unittest.TestCase):
    def test_frozen_multigeneration_ledger_matches_fixture(self):
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(build_specimen(), expected)


if __name__ == "__main__":
    unittest.main()
