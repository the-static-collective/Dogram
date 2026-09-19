from research.action_groupoid_transport_001 import (
    conjugate_subgroup,
    receipt,
    subgroup_generated_by_transposition,
    transporter,
)


def test_same_endpoints_do_not_determine_transport_arrow():
    H = subgroup_generated_by_transposition()
    arrows = transporter(H, H)
    assert len(arrows) == 2
    assert len(set(arrows)) == 2
    assert all(conjugate_subgroup(g, H) == H for g in arrows)


def test_receipt_keeps_arrow_identity_separate_from_endpoints():
    r = receipt()
    assert r["source"] == r["target"] == "H"
    assert r["transporter_size"] == 2
    assert r["normalizer_size"] == 2
    assert r["endpoint_pair_determines_arrow"] is False
    assert r["seal"] == "SAME SOURCE + SAME TARGET != SAME TRANSPORT ARROW."
