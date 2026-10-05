from __future__ import annotations

import copy
import unittest

from dogram.ice_cube import _pixel_for, work_address
from dogram.sparse_ice_probe import (
    CLAIM_SCOPE,
    deterministic_probe_indices,
    verify_sparse_region_claims,
)


def content_address(value):
    import hashlib
    import json
    data = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def fixture():
    work = {
        "kind": "ghot.ice-cube-work",
        "version": "0",
        "family": "lucas-halley-mandelbrot-mapping-torus/v0",
        "lucas_index": 2,
        "period": 3,
        "c": {"re": "0", "im": "0"},
        "halley": {"tolerance": "1e-9"},
        "render": {
            "width": 4,
            "height": 4,
            "xmin": "-1.2",
            "xmax": "1.2",
            "ymin": "-1.2",
            "ymax": "1.2",
            "max_halley_iter": 8,
        },
    }
    address = work_address(work)
    regions = []
    claims = []
    for y in range(4):
        for x in range(4):
            index = y * 4 + x
            descriptor = {
                "work_address": address,
                "index": index,
                "x": x,
                "y": y,
            }
            region_id = content_address(descriptor)
            regions.append({**descriptor, "region_id": region_id})
            claims.append({
                "region_id": region_id,
                "index": index,
                "x": x,
                "y": y,
                "value": _pixel_for(work, x, y),
            })
    plan_body = {
        "kind": "ghot.lightwalker.pixel-region-plan",
        "version": "0",
        "authority": "derived-root-work-region-plan",
        "continuation_lineage_id": "lineage:test",
        "work_address": address,
        "region_semantics": "one-canonical-render-pixel",
        "width": 4,
        "height": 4,
        "region_count": 16,
        "regions": regions,
        "operational_accounting_policy": {
            "scope": "sparse-ice-field-001",
            "unit": "compute-minute",
            "quantity_per_region": 1,
        },
        "execution_authority": "none",
        "settlement_authority": "none",
        "laws": [],
    }
    plan = {
        **plan_body,
        "pixel_region_plan_id": content_address(plan_body),
    }
    return work, plan, claims


class SparseIceProbeTests(unittest.TestCase):
    def test_clean_claims_stop_after_root_probes(self):
        work, plan, claims = fixture()
        receipt = verify_sparse_region_claims(
            work,
            plan,
            claims,
            root_probe_count=4,
        )
        self.assertEqual(receipt["status"], "OK")
        self.assertFalse(receipt["branch_triggered"])
        self.assertEqual(receipt["probed_region_count"], 4)
        self.assertEqual(receipt["claim_scope"], CLAIM_SCOPE)

    def test_root_mismatch_expands_to_full_and_refuses(self):
        work, plan, claims = fixture()
        damaged = copy.deepcopy(claims)
        index = deterministic_probe_indices(work, plan, 4)[0]
        damaged[index]["value"] ^= 0x01
        receipt = verify_sparse_region_claims(
            work,
            plan,
            damaged,
            root_probe_count=4,
        )
        self.assertEqual(receipt["status"], "REFUSED")
        self.assertTrue(receipt["branch_triggered"])
        self.assertEqual(receipt["probed_region_count"], 16)
        self.assertTrue(receipt["mismatches"])

    def test_prior_changes_cost_interpretation_not_evidence(self):
        work, plan, claims = fixture()
        heavy_clean = verify_sparse_region_claims(
            work,
            plan,
            claims,
            root_probe_count=4,
            prior={"clean": "3/4", "dirty": "1/4"},
        )
        uniform = verify_sparse_region_claims(
            work,
            plan,
            claims,
            root_probe_count=4,
            prior={"clean": "1/2", "dirty": "1/2"},
        )
        self.assertEqual(heavy_clean["status"], uniform["status"])
        self.assertEqual(
            heavy_clean["probed_region_indices"],
            uniform["probed_region_indices"],
        )
        self.assertNotEqual(
            heavy_clean["cost_analysis"]["adaptive_expected_cost_if_prior_declared"],
            uniform["cost_analysis"]["adaptive_expected_cost_if_prior_declared"],
        )


if __name__ == "__main__":
    unittest.main()
