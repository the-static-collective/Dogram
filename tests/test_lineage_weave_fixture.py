import json
import unittest
from pathlib import Path

from dogram.lineage_braid import (
    make_braid_capsule,
    make_braid_ledger,
    make_parent_set as make_braid_parent_set,
    make_sum_merge as make_braid_sum_merge,
    store_braid_capsule,
    store_merge_receipt as store_braid_merge_receipt,
    store_parent_set as store_braid_parent_set,
)
from dogram.lineage_spine import (
    append_from_crossing,
    canonical_digest,
    make_ledger as make_spine_ledger,
    make_root,
    store_capsule as store_spine_capsule,
    store_receipt as store_spine_receipt,
)
from dogram.lineage_weave import (
    make_parent_set,
    make_root_set,
    make_sum_merge,
    make_typed_parent,
    make_weave_capsule,
    make_weave_ledger,
    store_merge_receipt,
    store_parent_set,
    store_root_set,
    store_weave_capsule,
    verify_weave,
)
from dogram.triangulator import compare_order, square, triangular, triangulator_001_receipt


FIXTURE = Path(__file__).parent / "fixtures" / "lineage_weave_001.json"


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
    children: dict[int, dict[str, object]] = {}
    heads: dict[int, str] = {}

    for carrier in (5, 3, 4):
        root = make_root(carrier)
        store_spine_capsule(spine_ledger, root)
        crossing = triangulator_001_receipt() if carrier == 5 else crossing_at(carrier)
        store_spine_receipt(spine_ledger, crossing)
        child = append_from_crossing(root, crossing)
        head = store_spine_capsule(spine_ledger, child)
        children[carrier] = child
        heads[carrier] = head

    braid_parent_set = make_braid_parent_set(
        [
            {
                "head_digest": heads[5],
                "root_digest": children[5]["root_digest"],
                "carrier": children[5]["carrier"],
            },
            {
                "head_digest": heads[3],
                "root_digest": children[3]["root_digest"],
                "carrier": children[3]["carrier"],
            },
        ]
    )
    braid_merge = make_braid_sum_merge(braid_parent_set)
    braid_capsule = make_braid_capsule(braid_parent_set, braid_merge)
    braid_ledger = make_braid_ledger()
    braid_parent_set_digest = store_braid_parent_set(braid_ledger, braid_parent_set)
    braid_merge_digest = store_braid_merge_receipt(braid_ledger, braid_merge)
    braid_head = store_braid_capsule(braid_ledger, braid_capsule)

    braid_roots = [children[5]["root_digest"], children[3]["root_digest"]]
    spine_roots = [children[4]["root_digest"]]
    typed_braid = make_typed_parent("braid", braid_head, braid_capsule["carrier"], braid_roots)
    typed_spine = make_typed_parent("spine", heads[4], children[4]["carrier"], spine_roots)
    weave_parent_set = make_parent_set([typed_spine, typed_braid])
    weave_root_set = make_root_set(braid_roots + spine_roots)
    weave_merge = make_sum_merge(weave_parent_set)
    weave_capsule = make_weave_capsule(weave_parent_set, weave_root_set, weave_merge)
    weave_ledger = make_weave_ledger()
    weave_parent_set_digest = store_parent_set(weave_ledger, weave_parent_set)
    weave_root_set_digest = store_root_set(weave_ledger, weave_root_set)
    weave_merge_digest = store_merge_receipt(weave_ledger, weave_merge)
    weave_head = store_weave_capsule(weave_ledger, weave_capsule)

    return {
        "spine_ledger_digest": canonical_digest(spine_ledger),
        "braid_ledger_digest": canonical_digest(braid_ledger),
        "weave_ledger_digest": canonical_digest(weave_ledger),
        "braid_parent_set_digest": braid_parent_set_digest,
        "braid_merge_digest": braid_merge_digest,
        "braid_head": braid_head,
        "weave_parent_set_digest": weave_parent_set_digest,
        "weave_root_set_digest": weave_root_set_digest,
        "weave_merge_digest": weave_merge_digest,
        "weave_head": weave_head,
        "verification": verify_weave(weave_head, weave_ledger, braid_ledger, spine_ledger),
    }


class LineageWeaveFixtureTests(unittest.TestCase):
    def test_frozen_weave_matches_fixture(self):
        expected = json.loads(FIXTURE.read_text())
        self.assertEqual(build_specimen(), expected)


if __name__ == "__main__":
    unittest.main()
