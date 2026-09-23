from research.probe_separation_001 import analyze, specimen


def test_coarse_probe_collides_distinct_states():
    r = specimen()
    assert r["states"]["x"] != r["states"]["y"]
    assert r["coarse"]["signatures"]["x"] == r["coarse"]["signatures"]["y"]
    assert ("x", "y") in r["coarse"]["indistinguishable_pairs"]
    assert r["coarse"]["separates_states"] is False


def test_added_probe_separates_all_states():
    r = specimen()
    assert r["refined"]["indistinguishable_pairs"] == ()
    assert r["refined"]["separates_states"] is True
    assert r["refined"]["pair_count_checked"] == 3


def test_constant_probe_is_maximally_nonseparating():
    states = {"a": {"constant": 0}, "b": {"constant": 0}, "c": {"constant": 0}}
    r = analyze(states, ("constant",))
    assert r["pair_count_checked"] == 3
    assert len(r["indistinguishable_pairs"]) == 3
    assert r["separates_states"] is False
