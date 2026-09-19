from research.factorization_path_001 import ID, receipt


def test_same_composite_different_factorization_history():
    r = receipt()
    assert r["group_order"] == 6
    assert r["source_equals_target"] is True
    assert r["composites_equal"] is True
    assert tuple(r["composite"]) == ID
    assert r["paths_distinct"] is True
    assert r["intermediate_constitutions_distinct"] is True


def test_refusal_boundary_is_frozen():
    r = receipt()
    assert "same composite != same provenance" in r["nonclaims"]
    assert "transport arrow != occurrence" in r["nonclaims"]
    assert "groupoid composition != causal composition" in r["nonclaims"]
