from research.strict3_interchange_factorization_001 import verify_strict_interchange_specimen


def test_strict_interchange_and_eckmann_hilton_shape():
    r = verify_strict_interchange_specimen()
    assert r["carrier_size"] == 4
    assert r["quadruples_checked"] == 256
    assert r["unit_0"] and r["unit_1"]
    assert r["interchange"]
    assert r["operations_coincide"]
    assert r["commutative"]


def test_same_boundary_and_composite_do_not_recover_factorization_order():
    r = verify_strict_interchange_specimen()
    assert r["same_boundary"]
    assert r["paths_distinct"]
    assert r["path_left"] == ("Gamma", "Delta")
    assert r["path_right"] == ("Delta", "Gamma")
    assert r["composite_left"] == (1, 1)
    assert r["composite_right"] == (1, 1)
    assert r["same_composite"]
