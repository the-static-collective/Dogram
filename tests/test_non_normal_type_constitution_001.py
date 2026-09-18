from research.non_normal_type_constitution_001 import (
    CYCLE_012,
    IDENTITY,
    TRANSPOSE_01,
    conjugate_subgroup,
    left_coset,
    receipt,
    right_coset,
)


def test_declared_order_two_subgroup_is_not_normal_in_s3():
    h = {IDENTITY, TRANSPOSE_01}
    transported = conjugate_subgroup(CYCLE_012, h)
    assert transported != h
    assert transported == {IDENTITY, (0, 2, 1)}


def test_left_and_right_cosets_expose_non_normality():
    h = {IDENTITY, TRANSPOSE_01}
    assert left_coset(CYCLE_012, h) != right_coset(h, CYCLE_012)


def test_frozen_receipt_keeps_structural_transport_separate_from_declaration():
    r = receipt()
    assert r["group_order"] == 6
    assert r["subgroup_order"] == 2
    assert r["index"] == 3
    assert r["subgroup_is_normal"] is False
    assert r["conjugate_equals_declared"] is False
    assert r["left_equals_right"] is False
    assert "CHANGE OF FRAME != CHANGE OF DECLARATION" in r["refusals"]
