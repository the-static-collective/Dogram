from research.type_action_subgroup_001 import receipt, parity


def test_k3_realizes_all_s3_type_actions():
    r = receipt()
    assert r["automorphism_count"] == 6
    assert len({tuple(x) for x in r["induced_type_actions"]}) == 6


def test_declared_a3_admits_exactly_even_actions():
    r = receipt()
    assert r["admissible_count"] == 3
    assert r["refused_structural_symmetry_count"] == 3
    assert r["coset_index"] == 2
    assert all(parity(tuple(p)) == 0 for p in r["admissible_actions"])
    assert all(parity(tuple(p)) == 1 for p in r["refused_actions"])


def test_transposition_exists_structurally_but_is_refused():
    r = receipt()
    assert [1, 0, 2] in r["induced_type_actions"]
    assert [1, 0, 2] in r["refused_actions"]
    assert [1, 0, 2] not in r["admissible_actions"]
