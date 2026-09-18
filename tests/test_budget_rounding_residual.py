from dogram.budget_rounding_residual import receipt_integer_budget


def test_same_exact_budget_can_have_different_integer_realizations():
    weights = {"a": 5, "b": 4, "c": 1}

    largest = receipt_integer_budget(
        weights,
        7,
        method="largest_fractional_remainder",
    )
    declared = receipt_integer_budget(
        weights,
        7,
        method="declared_order_remainder",
    )

    assert largest["exact"] == declared["exact"] == {
        "a": "7/2",
        "b": "14/5",
        "c": "7/10",
    }
    assert largest["allocation"] == {"a": 3, "b": 3, "c": 1}
    assert declared["allocation"] == {"a": 4, "b": 3, "c": 0}
    assert largest["allocation"] != declared["allocation"]
    assert largest["residual_sum"] == declared["residual_sum"] == "0"
    assert largest["allocated_total"] == declared["allocated_total"] == 7


def test_exact_proportion_needs_no_rounding_residual():
    receipt = receipt_integer_budget(
        {"three": 3, "two": 2, "one": 1},
        12,
        method="largest_fractional_remainder",
    )

    assert receipt["allocation"] == {"one": 2, "three": 6, "two": 4}
    assert receipt["residuals"] == {"one": "0", "three": "0", "two": "0"}


def test_invalid_budget_or_weights_are_refused():
    for weights, budget, expected in (
        ({}, 7, "weights must be non-empty"),
        ({"a": 0}, 7, "weights must be positive integers"),
        ({"a": 1}, -1, "budget must be a non-negative integer"),
    ):
        try:
            receipt_integer_budget(weights, budget)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError("expected ValueError")
