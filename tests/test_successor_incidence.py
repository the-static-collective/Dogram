from dogram.successor_incidence import receipt_successor_incidence


def test_modal_extrema_do_not_determine_representative_successor_incidence():
    left = receipt_successor_incidence(
        {
            "r0": {"a", "b"},
            "r1": {"a", "c"},
        }
    )
    right = receipt_successor_incidence(
        {
            "r0": {"a"},
            "r1": {"a", "b", "c"},
        }
    )

    assert left["may"] == right["may"] == ["a", "b", "c"]
    assert left["must"] == right["must"] == ["a"]
    assert left["incidence"] != right["incidence"]
    assert left["member_sizes"] == [2, 2]
    assert right["member_sizes"] == [1, 3]


def test_incidence_receipt_is_deterministic_under_input_order():
    first = receipt_successor_incidence({"z": {"b", "a"}, "x": {"c", "a"}})
    second = receipt_successor_incidence({"x": {"a", "c"}, "z": {"a", "b"}})

    assert first == second


def test_empty_family_is_refused():
    try:
        receipt_successor_incidence({})
    except ValueError as exc:
        assert str(exc) == "representative family must be non-empty"
    else:
        raise AssertionError("expected ValueError")
