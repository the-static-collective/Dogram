from research.parallel_equivalence_witness_001 import receipt, replay


def test_two_distinct_witnesses_have_same_endpoints():
    r = receipt()
    assert r["same_endpoints"] is True
    assert r["same_induced_path_equivalence"] is True
    assert r["witnesses_distinct"] is True
    assert r["direct_witness"]["states"] == ["aa", "bb"]
    assert r["composite_witness"]["states"] == ["aa", "cc", "bb"]


def test_witness_identity_survives_endpoint_collapse():
    direct = replay(["alpha"])
    composite = replay(["rho", "sigma"])
    assert direct["target"] == composite["target"] == "bb"
    assert direct["rules"] != composite["rules"]
    assert direct["states"] != composite["states"]
