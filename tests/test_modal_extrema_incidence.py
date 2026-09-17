from dogram.modal_extrema_incidence import compare, receipt


def test_same_modal_extrema_do_not_determine_representative_family():
    left = (("a", "b"), ("a", "c"))
    right = (("a",), ("a", "b", "c"))
    out = compare(left, right)
    assert out["same_may_union"] is True
    assert out["same_must_intersection"] is True
    assert out["same_exact_family"] is False
    assert out["same_member_size_multiset"] is False
    assert out["left"]["may_union"] == ("a", "b", "c")
    assert out["left"]["must_intersection"] == ("a",)


def test_receipt_refuses_empty_representative_family():
    try:
        receipt(())
    except ValueError as exc:
        assert "at least one representative" in str(exc)
    else:
        raise AssertionError("empty family must be refused")
