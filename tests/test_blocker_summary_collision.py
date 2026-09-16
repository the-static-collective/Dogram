from dogram.blocker_summary_collision import specimen


def test_coarse_summaries_collide_but_geometry_does_not():
    r = specimen()
    assert r["same_edge_size_multiset"]
    assert r["same_transversal_number"]
    assert r["same_blocker_size_multiset"]
    assert r["different_degree_sequence"]
    assert r["different_blocker_degree_sequence"]
    assert r["both_round_trip"]


def test_frozen_exact_values():
    r = specimen()
    assert r["left"]["edge_size_multiset"] == (2, 2, 2)
    assert r["right"]["edge_size_multiset"] == (2, 2, 2)
    assert r["left"]["transversal_number"] == 2
    assert r["right"]["transversal_number"] == 2
    assert r["left"]["blocker_size_multiset"] == (2, 2, 2)
    assert r["right"]["blocker_size_multiset"] == (2, 2, 2)
    assert r["left"]["degree_sequence"] == (2, 2, 2, 0)
    assert r["right"]["degree_sequence"] == (2, 2, 1, 1)
    assert r["left"]["blocker_degree_sequence"] == (2, 2, 2, 0)
    assert r["right"]["blocker_degree_sequence"] == (2, 2, 1, 1)


def test_exact_blockers_are_retained():
    r = specimen()
    assert r["left"]["blocker"] == ((0, 1), (0, 2), (1, 2))
    assert r["right"]["blocker"] == ((0, 1), (0, 2), (1, 3))
