import copy
import unittest

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


def sample_parent_set() -> dict[str, object]:
    braid = make_typed_parent("braid", "head-b", 109, ["root-a", "root-b"])
    spine = make_typed_parent("spine", "head-s", 36, ["root-c"])
    return make_parent_set([spine, braid])


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


def build_spine_graph() -> tuple[
    dict[str, object],
    dict[int, dict[str, object]],
    dict[int, str],
]:
    ledger = make_spine_ledger()
    children: dict[int, dict[str, object]] = {}
    heads: dict[int, str] = {}

    for carrier in (5, 3, 4):
        root = make_root(carrier)
        store_spine_capsule(ledger, root)
        crossing = triangulator_001_receipt() if carrier == 5 else crossing_at(carrier)
        store_spine_receipt(ledger, crossing)
        child = append_from_crossing(root, crossing)
        head = store_spine_capsule(ledger, child)
        children[carrier] = child
        heads[carrier] = head

    return ledger, children, heads


def build_complete_graph() -> dict[str, object]:
    spine_ledger, children, spine_heads = build_spine_graph()

    braid_parent_set = make_braid_parent_set(
        [
            {
                "head_digest": spine_heads[5],
                "root_digest": children[5]["root_digest"],
                "carrier": children[5]["carrier"],
            },
            {
                "head_digest": spine_heads[3],
                "root_digest": children[3]["root_digest"],
                "carrier": children[3]["carrier"],
            },
        ]
    )
    braid_merge = make_braid_sum_merge(braid_parent_set)
    braid_capsule = make_braid_capsule(braid_parent_set, braid_merge)
    braid_ledger = make_braid_ledger()
    store_braid_parent_set(braid_ledger, braid_parent_set)
    store_braid_merge_receipt(braid_ledger, braid_merge)
    braid_head = store_braid_capsule(braid_ledger, braid_capsule)

    braid_roots = [children[5]["root_digest"], children[3]["root_digest"]]
    spine_roots = [children[4]["root_digest"]]
    typed_braid = make_typed_parent("braid", braid_head, braid_capsule["carrier"], braid_roots)
    typed_spine = make_typed_parent("spine", spine_heads[4], children[4]["carrier"], spine_roots)
    weave_parent_set = make_parent_set([typed_spine, typed_braid])
    weave_root_set = make_root_set(braid_roots + spine_roots)
    weave_merge = make_sum_merge(weave_parent_set)
    weave_capsule = make_weave_capsule(weave_parent_set, weave_root_set, weave_merge)
    weave_ledger = make_weave_ledger()
    store_parent_set(weave_ledger, weave_parent_set)
    store_root_set(weave_ledger, weave_root_set)
    store_merge_receipt(weave_ledger, weave_merge)
    weave_head = store_weave_capsule(weave_ledger, weave_capsule)

    return {
        "spine_ledger": spine_ledger,
        "spine_children": children,
        "spine_heads": spine_heads,
        "braid_ledger": braid_ledger,
        "braid_head": braid_head,
        "braid_capsule": braid_capsule,
        "weave_ledger": weave_ledger,
        "weave_head": weave_head,
        "weave_parent_set": weave_parent_set,
        "weave_root_set": weave_root_set,
    }


def rebuild_weave(
    graph: dict[str, object],
    parent_set: dict[str, object],
    root_set: dict[str, object] | None = None,
) -> tuple[dict[str, object], str]:
    chosen_root_set = graph["weave_root_set"] if root_set is None else root_set
    assert isinstance(chosen_root_set, dict)
    merge = make_sum_merge(parent_set)
    capsule = make_weave_capsule(parent_set, chosen_root_set, merge)
    ledger = make_weave_ledger()
    store_parent_set(ledger, parent_set)
    store_root_set(ledger, chosen_root_set)
    store_merge_receipt(ledger, merge)
    head = store_weave_capsule(ledger, capsule)
    return ledger, head


def build_zero_one_weave() -> dict[str, object]:
    spine_ledger = make_spine_ledger()
    parents: list[dict[str, object]] = []
    for source in (1, 2):
        root = make_root(source)
        store_spine_capsule(spine_ledger, root)
        crossing = crossing_at(source)
        store_spine_receipt(spine_ledger, crossing)
        child = append_from_crossing(root, crossing)
        head = store_spine_capsule(spine_ledger, child)
        parents.append(
            make_typed_parent(
                "spine",
                head,
                child["carrier"],
                [child["root_digest"]],
            )
        )

    parent_set = make_parent_set(parents)
    root_sets = []
    for parent in parents:
        head = parent["head_digest"]
        root_sets.append(spine_ledger["capsules"][head]["root_digest"])
    root_set = make_root_set(root_sets)
    merge = make_sum_merge(parent_set)
    capsule = make_weave_capsule(parent_set, root_set, merge)
    weave_ledger = make_weave_ledger()
    store_parent_set(weave_ledger, parent_set)
    store_root_set(weave_ledger, root_set)
    store_merge_receipt(weave_ledger, merge)
    weave_head = store_weave_capsule(weave_ledger, capsule)
    return {
        "spine_ledger": spine_ledger,
        "braid_ledger": make_braid_ledger(),
        "weave_ledger": weave_ledger,
        "weave_head": weave_head,
    }


class LineageWeaveParentTests(unittest.TestCase):
    def test_root_set_canonicalizes_sorted_unique_roots(self):
        left = make_root_set(["root-b", "root-a", "root-b"])
        right = make_root_set(["root-a", "root-b"])

        self.assertEqual(left, right)
        self.assertEqual(left["roots"], ["root-a", "root-b"])
        self.assertEqual(canonical_digest(left), canonical_digest(right))

    def test_typed_parent_has_exact_shape_and_root_set_digest(self):
        parent = make_typed_parent("braid", "head-braid", 109, ["root-b", "root-a"])

        self.assertEqual(
            set(parent),
            {"kind", "head_digest", "carrier", "root_set_digest"},
        )
        self.assertEqual(parent["kind"], "braid")
        self.assertEqual(parent["carrier"], 109)
        self.assertEqual(
            parent["root_set_digest"],
            canonical_digest(make_root_set(["root-a", "root-b"])),
        )

    def test_typed_parent_rejects_unknown_kind(self):
        with self.assertRaisesRegex(ValueError, "kind"):
            make_typed_parent("unknown", "head", 1, ["root"])

    def test_typed_parent_rejects_bool_carrier_and_empty_digests(self):
        with self.assertRaisesRegex(ValueError, "carrier"):
            make_typed_parent("spine", "head", True, ["root"])
        with self.assertRaisesRegex(ValueError, "head"):
            make_typed_parent("spine", "", 1, ["root"])
        with self.assertRaisesRegex(ValueError, "root"):
            make_typed_parent("spine", "head", 1, [])

    def test_parent_order_canonicalizes_to_same_identity(self):
        braid = make_typed_parent("braid", "head-b", 109, ["root-a", "root-b"])
        spine = make_typed_parent("spine", "head-s", 36, ["root-c"])

        left = make_parent_set([spine, braid])
        right = make_parent_set([braid, spine])

        self.assertEqual(left, right)
        self.assertEqual(canonical_digest(left), canonical_digest(right))
        self.assertEqual(
            [(p["kind"], p["head_digest"]) for p in left["parents"]],
            [("braid", "head-b"), ("spine", "head-s")],
        )

    def test_parent_set_requires_two_unique_typed_heads(self):
        braid = make_typed_parent("braid", "same", 109, ["root-a"])

        with self.assertRaisesRegex(ValueError, "at least two"):
            make_parent_set([braid])

        with self.assertRaisesRegex(ValueError, "unique"):
            make_parent_set([braid, dict(braid)])

    def test_parent_descriptor_shape_is_exact(self):
        polluted = {
            "kind": "spine",
            "head_digest": "head-s",
            "carrier": 36,
            "root_set_digest": "roots",
            "ancestry": {"recursive": True},
        }
        braid = make_typed_parent("braid", "head-b", 109, ["root-a"])

        with self.assertRaisesRegex(ValueError, "shape"):
            make_parent_set([polluted, braid])


class LineageWeaveMergeTests(unittest.TestCase):
    def test_sum_merge_uses_canonical_parent_order_and_outputs_145(self):
        parent_set = sample_parent_set()

        receipt = make_sum_merge(parent_set)

        self.assertEqual(receipt["operator"], "sum")
        self.assertEqual(receipt["inputs"], [109, 36])
        self.assertEqual(receipt["output"], 145)
        self.assertEqual(receipt["parent_set_digest"], canonical_digest(parent_set))

    def test_weave_capsule_is_fixed_shape_and_externalizes_plurality(self):
        parent_set = sample_parent_set()
        root_set = make_root_set(["root-a", "root-b", "root-c"])
        receipt = make_sum_merge(parent_set)

        capsule = make_weave_capsule(parent_set, root_set, receipt)

        self.assertEqual(
            set(capsule),
            {
                "schema",
                "specimen",
                "carrier",
                "carrier_origin",
                "parent_set_digest",
                "merge_receipt_digest",
                "root_set_digest",
            },
        )
        self.assertEqual(capsule["carrier"], 145)
        self.assertEqual(capsule["carrier_origin"], "typed_parent_set_merge")
        self.assertEqual(capsule["parent_set_digest"], canonical_digest(parent_set))
        self.assertEqual(capsule["merge_receipt_digest"], canonical_digest(receipt))
        self.assertEqual(capsule["root_set_digest"], canonical_digest(root_set))
        self.assertNotIn("parents", capsule)
        self.assertNotIn("ancestry", capsule)

    def test_weave_ledger_stores_objects_by_content_digest(self):
        parent_set = sample_parent_set()
        root_set = make_root_set(["root-a", "root-b", "root-c"])
        receipt = make_sum_merge(parent_set)
        capsule = make_weave_capsule(parent_set, root_set, receipt)
        ledger = make_weave_ledger()

        parent_digest = store_parent_set(ledger, parent_set)
        root_digest = store_root_set(ledger, root_set)
        receipt_digest = store_merge_receipt(ledger, receipt)
        head_digest = store_weave_capsule(ledger, capsule)

        self.assertEqual(ledger["parent_sets"][parent_digest], parent_set)
        self.assertEqual(ledger["root_sets"][root_digest], root_set)
        self.assertEqual(ledger["merge_receipts"][receipt_digest], receipt)
        self.assertEqual(ledger["capsules"][head_digest], capsule)


class LineageWeaveVerificationTests(unittest.TestCase):
    def test_complete_weave_dispatches_braid_and_spine_parents(self):
        graph = build_complete_graph()

        result = verify_weave(
            graph["weave_head"], graph["weave_ledger"], graph["braid_ledger"], graph["spine_ledger"]
        )

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["carrier"], 145)
        self.assertEqual(result["parent_count"], 2)
        self.assertEqual(set(result["parent_kinds"]), {"braid", "spine"})

    def test_missing_spine_parent_witness_is_incomplete(self):
        graph = build_complete_graph()
        spine_parent = next(p for p in graph["weave_parent_set"]["parents"] if p["kind"] == "spine")
        del graph["spine_ledger"]["capsules"][spine_parent["head_digest"]]
        result = verify_weave(graph["weave_head"], graph["weave_ledger"], graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["reason"], "parent_spine_incomplete")

    def test_missing_braid_parent_witness_is_incomplete(self):
        graph = build_complete_graph()
        del graph["braid_ledger"]["capsules"][graph["braid_head"]]
        result = verify_weave(graph["weave_head"], graph["weave_ledger"], graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["reason"], "parent_braid_incomplete")

    def test_invalid_spine_parent_propagates_invalid(self):
        graph = build_complete_graph()
        spine_parent = next(p for p in graph["weave_parent_set"]["parents"] if p["kind"] == "spine")
        bad = copy.deepcopy(graph["spine_ledger"]["capsules"][spine_parent["head_digest"]])
        bad["carrier"] += 1
        graph["spine_ledger"]["capsules"][spine_parent["head_digest"]] = bad
        result = verify_weave(graph["weave_head"], graph["weave_ledger"], graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_spine_invalid")

    def test_invalid_braid_parent_propagates_invalid(self):
        graph = build_complete_graph()
        bad = copy.deepcopy(graph["braid_ledger"]["capsules"][graph["braid_head"]])
        bad["carrier"] += 1
        graph["braid_ledger"]["capsules"][graph["braid_head"]] = bad
        result = verify_weave(graph["weave_head"], graph["weave_ledger"], graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_braid_invalid")

    def test_parent_carrier_mismatch_is_invalid(self):
        graph = build_complete_graph()
        polluted = copy.deepcopy(graph["weave_parent_set"])
        polluted["parents"][0]["carrier"] += 1
        polluted = make_parent_set(polluted["parents"])
        weave_ledger, weave_head = rebuild_weave(graph, polluted)
        result = verify_weave(weave_head, weave_ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_carrier_mismatch")

    def test_parent_root_set_mismatch_is_invalid(self):
        graph = build_complete_graph()
        polluted = copy.deepcopy(graph["weave_parent_set"])
        polluted["parents"][0]["root_set_digest"] = canonical_digest(make_root_set(["wrong-root"]))
        polluted = make_parent_set(polluted["parents"])
        weave_ledger, weave_head = rebuild_weave(graph, polluted)
        result = verify_weave(weave_head, weave_ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_root_set_mismatch")

    def test_rehashed_kind_substitution_is_invalid(self):
        graph = build_complete_graph()
        polluted = copy.deepcopy(graph["weave_parent_set"])
        braid_parent = next(p for p in polluted["parents"] if p["kind"] == "braid")
        braid_parent["kind"] = "spine"
        polluted = make_parent_set(polluted["parents"])
        weave_ledger, weave_head = rebuild_weave(graph, polluted)
        result = verify_weave(weave_head, weave_ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_kind_mismatch")

    def test_rehashed_parent_without_kind_is_invalid(self):
        graph = build_complete_graph()
        parent_set = copy.deepcopy(graph["weave_parent_set"])
        del parent_set["parents"][0]["kind"]
        parent_digest = canonical_digest(parent_set)
        merge = {
            "schema": "dogram.lineage-weave-merge-receipt/v0",
            "specimen": "LINEAGE-WEAVE-001",
            "operator": "sum",
            "parent_set_digest": parent_digest,
            "inputs": [109, 36],
            "output": 145,
        }
        root_set = graph["weave_root_set"]
        capsule = {
            "schema": "dogram.lineage-weave-capsule/v0",
            "specimen": "LINEAGE-WEAVE-001",
            "carrier": 145,
            "carrier_origin": "typed_parent_set_merge",
            "parent_set_digest": parent_digest,
            "merge_receipt_digest": canonical_digest(merge),
            "root_set_digest": canonical_digest(root_set),
        }
        ledger = make_weave_ledger()
        ledger["parent_sets"][parent_digest] = parent_set
        store_root_set(ledger, root_set)
        store_merge_receipt(ledger, merge)
        head = store_weave_capsule(ledger, capsule)
        result = verify_weave(head, ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "parent_descriptor_shape_mismatch")

    def test_rehashed_wrong_sum_is_invalid(self):
        graph = build_complete_graph()
        ledger = copy.deepcopy(graph["weave_ledger"])
        capsule = copy.deepcopy(ledger["capsules"][graph["weave_head"]])
        merge = copy.deepcopy(ledger["merge_receipts"][capsule["merge_receipt_digest"]])
        merge["output"] = 146
        merge_digest = canonical_digest(merge)
        ledger["merge_receipts"][merge_digest] = merge
        capsule["carrier"] = 146
        capsule["merge_receipt_digest"] = merge_digest
        head = canonical_digest(capsule)
        ledger["capsules"][head] = capsule
        result = verify_weave(head, ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "merge_output_mismatch")

    def test_rehashed_capsule_cannot_smuggle_ancestry(self):
        graph = build_complete_graph()
        ledger = copy.deepcopy(graph["weave_ledger"])
        capsule = copy.deepcopy(ledger["capsules"][graph["weave_head"]])
        capsule["ancestry"] = {"recursive": True}
        head = canonical_digest(capsule)
        ledger["capsules"][head] = capsule
        result = verify_weave(head, ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "capsule_shape_mismatch")

    def test_rehashed_wrong_root_union_is_invalid(self):
        graph = build_complete_graph()
        parent_set = graph["weave_parent_set"]
        wrong_root_set = make_root_set(["wrong-root"])
        merge = make_sum_merge(parent_set)
        capsule = make_weave_capsule(parent_set, wrong_root_set, merge)
        ledger = make_weave_ledger()
        store_parent_set(ledger, parent_set)
        store_root_set(ledger, wrong_root_set)
        store_merge_receipt(ledger, merge)
        head = store_weave_capsule(ledger, capsule)
        result = verify_weave(head, ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "root_union_mismatch")

    def test_bool_carrier_alias_cannot_impersonate_integer_one(self):
        graph = build_zero_one_weave()
        ledger = copy.deepcopy(graph["weave_ledger"])
        capsule = copy.deepcopy(ledger["capsules"][graph["weave_head"]])
        self.assertEqual(capsule["carrier"], 1)
        capsule["carrier"] = True
        head = canonical_digest(capsule)
        ledger["capsules"][head] = capsule
        result = verify_weave(head, ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "invalid_weave_carrier")

    def test_bool_merge_inputs_cannot_impersonate_zero_and_one(self):
        graph = build_zero_one_weave()
        ledger = copy.deepcopy(graph["weave_ledger"])
        capsule = copy.deepcopy(ledger["capsules"][graph["weave_head"]])
        merge = copy.deepcopy(ledger["merge_receipts"][capsule["merge_receipt_digest"]])
        self.assertEqual(merge["inputs"], [0, 1])
        merge["inputs"] = [False, True]
        merge_digest = canonical_digest(merge)
        ledger["merge_receipts"][merge_digest] = merge
        capsule["merge_receipt_digest"] = merge_digest
        head = canonical_digest(capsule)
        ledger["capsules"][head] = capsule
        result = verify_weave(head, ledger, graph["braid_ledger"], graph["spine_ledger"])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["reason"], "merge_inputs_mismatch")


if __name__ == "__main__":
    unittest.main()
