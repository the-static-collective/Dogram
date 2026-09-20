from dogram.biregular_incidence_collision import receipt


def test_same_modal_extrema_and_both_degree_multisets_can_hide_wiring():
    cycle = receipt((("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")))
    split = receipt((("a", "b"), ("a", "b"), ("c", "d"), ("c", "d")))

    for key in (
        "may_union",
        "must_intersection",
        "row_degree_multiset",
        "column_degree_multiset",
        "edge_count",
    ):
        assert cycle[key] == split[key]

    assert cycle["may_union"] == ("a", "b", "c", "d")
    assert cycle["must_intersection"] == ()
    assert cycle["row_degree_multiset"] == (2, 2, 2, 2)
    assert cycle["column_degree_multiset"] == (2, 2, 2, 2)
    assert cycle["edge_count"] == 8

    # Residual: C8 is connected; the second realization is two K2,2 components.
    assert cycle["component_sizes"] == (8,)
    assert split["component_sizes"] == (4, 4)
    assert cycle["incidence"] != split["incidence"]


def test_representative_and_successor_relabeling_cannot_remove_component_delta():
    cycle = receipt((("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")))
    split = receipt((("a", "b"), ("a", "b"), ("c", "d"), ("c", "d")))
    assert cycle["component_sizes"] != split["component_sizes"]
