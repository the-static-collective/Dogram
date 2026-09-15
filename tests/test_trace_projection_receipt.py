from dogram.trace_projection_receipt import specimen


def test_projection_family_separates_trace_pair():
    r = specimen()
    assert r["trace_classes_disjoint"] is True
    assert r["differing_dependent_projections"] == ("ab",)
    assert r["left_projection_receipt"]["ab"] == "aba"
    assert r["right_projection_receipt"]["ab"] == "baa"


def test_omitting_one_required_projection_collapses_receipt():
    r = specimen()
    assert r["omitted_projection"] == "ab"
    assert r["reduced_receipts_equal"] is True


def test_exact_trace_classes_are_frozen():
    r = specimen()
    assert r["left_trace_class"] == ("abac", "abca")
    assert r["right_trace_class"] == ("baac", "baca", "bcaa")
