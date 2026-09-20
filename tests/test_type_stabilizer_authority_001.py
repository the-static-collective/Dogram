from research.type_stabilizer_authority_001 import admissible_automorphisms, receipt


def test_c4_symmetry_splits_at_declared_type_boundary():
    r = receipt()
    assert r["untyped_automorphism_count"] == 8
    assert r["type_preserving_count"] == 4
    assert r["type_swapping_count"] == 4
    assert r["admissible_without_swap_declaration"] == 4
    assert r["admissible_with_swap_declaration"] == 8
    assert r["all_automorphisms_have_uniform_type_action"] is True


def test_swap_permission_is_explicit_not_inferred_from_symmetry():
    assert len(admissible_automorphisms(("preserve",))) == 4
    assert len(admissible_automorphisms(("preserve", "swap"))) == 8


def test_unknown_type_action_is_refused():
    try:
        admissible_automorphisms(("preserve", "infer"))
    except ValueError:
        pass
    else:
        raise AssertionError("undeclared type action must be refused")
