import json
import unittest
from pathlib import Path

from dogram.lineage_braid import (
    make_braid_capsule,
    make_braid_ledger,
    make_parent_set,
    make_sum_merge,
    store_braid_capsule,
    store_merge_receipt,
    store_parent_set,
    verify_braid,
)
from dogram.lineage_spine import (
    append_from_crossing,
    make_ledger as make_spine_ledger,
    make_root,
    store_capsule as store_spine_capsule,
    store_receipt as store_spine_receipt,
)
from dogram.triangulator import compare_order, square, triangular, triangulator_001_receipt


FIXTURE = Path(__file__).parent / "fixtures" / "lineage_braid_001.json"


def crossing_at(carrier: int) -> dict[str, object]:
    receipt = compare_order(
        carrier,
        square,
        triangular,
        structure_test=lambda n, delta: delta == triangular(n - 1) ** 2,
        structure_label="delta == triangular(carrier - 1)^2",
    )
    receipt["specimen"] = "TRIANGULATOR-001"
    return receipt


def build_specimen() -> dict[str, object]:
    spine_ledger = make_spine_ledger()

    root5 = make_root(5)
    store_spine_capsule(spine_ledger, root5)
    crossing5 = triangulator_001_receipt()
    store_spine_receipt(spine_ledger, crossing5)
    child5 = append_from_crossing(root5, crossing5)
    head5 = store_spine_capsule(spine_ledger, child5)

    root3 = make_root(3)
    store_spine_capsule(spine_ledger, root3)
    crossing3 = crossing_at(3)
    store_spine_receipt(spine_ledger, crossing3)
    child3 = append_from_crossing(root3, crossing3)
    head3 = store_spine_capsule(spine_ledger, child3)

    parent_set = make_parent_set(
        [
            {
                "head_digest": head5,
                "root_digest": child5["root_digest"],
                "carrier": child5["carrier"],
            },
            {
                "head_digest": head3,
                "root_digest": child3["root_digest"],
                "carrier": child3["carrier"],
            },
        ]
    )
    merge_receipt = make_sum_merge(parent_set)
    capsule = make_braid_capsule(parent_set, merge_receipt)

    braid_ledger = make_braid_ledger()
    parent_set_digest = store_parent_set(braid_ledger, parent_set)
    merge_receipt_digest = store_merge_receipt(braid_ledger, merge_receipt)
    head_digest = store_braid_capsule(braid_ledger, capsule)

    return {
        "spine_ledger": spine_ledger,
        "braid_ledger": braid_ledger,
        "parent_set_digest": parent_set_digest,
        "merge_receipt_digest": merge_receipt_digest,
        "head_digest": head_digest,
        "verification": verify_braid(head_digest, braid_ledger, spine_ledger),
    }


class LineageBraidFixtureTests(unittest.TestCase):
    def test_frozen_braid_matches_fixture(self):
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(build_specimen(), expected)


if __name__ == "__main__":
    unittest.main()
