from dogram.hypergraph_blocker_duality import blocker, normalize, receipt


def test_frozen_blocker_receipt():
    r = receipt()
    assert r["distinction_supports"] == normalize(({0, 1}, {1, 2}, {2, 3}))
    assert r["minimal_retained_view_sets"] == normalize(({0, 2}, {1, 2}, {1, 3}))
    assert r["double_blocker"] == r["distinction_supports"]
    assert r["involution_holds"] is True


def test_each_minimal_retained_set_hits_every_distinction_support():
    r = receipt()
    for retained in r["minimal_retained_view_sets"]:
        assert all(retained & support for support in r["distinction_supports"])
        for view in retained:
            smaller = retained - {view}
            assert not all(smaller & support for support in r["distinction_supports"])


def test_blocker_discards_nonminimal_supersets_before_dualizing():
    vertices = (0, 1, 2, 3)
    edges = ({0, 1}, {0, 1, 2}, {1, 2}, {2, 3})
    assert blocker(vertices, edges) == blocker(vertices, ({0, 1}, {1, 2}, {2, 3}))
