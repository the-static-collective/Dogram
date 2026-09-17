from dogram.may_union_quotient import (
    exact_successor_factorization,
    may_union,
    must_intersection,
    specimen_receipt,
)


def test_same_enabled_label_and_aggregate_may_surface_do_not_imply_exact_factorization():
    receipt = specimen_receipt()
    assert receipt["enabled_labels_per_representative"] == {
        "left": ("advance",),
        "right": ("advance",),
    }
    assert receipt["may_union"] == ("green", "hold")
    assert receipt["representative_successor_classes"] == {
        "left": ("green",),
        "right": ("hold",),
    }
    assert receipt["exact_successor_factorization"] is False


def test_may_and_must_surfaces_are_distinct_declared_constructions():
    receipt = specimen_receipt()
    assert receipt["may_union"] == ("green", "hold")
    assert receipt["must_intersection"] == ()


def test_hostile_control_exact_factorization_when_representatives_match():
    quotient = {"left": "pending", "right": "pending", "green": "green"}
    transitions = (("left", "advance", "green"), ("right", "advance", "green"))
    exact, per_rep = exact_successor_factorization(transitions, quotient, "pending", "advance")
    assert exact is True
    assert per_rep == {"left": ("green",), "right": ("green",)}
    assert may_union(transitions, quotient, "pending", "advance") == ("green",)
    assert must_intersection(transitions, quotient, "pending", "advance") == ("green",)
