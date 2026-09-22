from fractions import Fraction
import pytest

from dogram.unsupported_pareto_001 import (
    dominates, frozen_specimen, pareto_minima, scalar_cost, support_interval,
)


def test_all_three_points_are_pareto_minimal():
    s = frozen_specimen()
    assert s["pareto_minima"] == ("A", "B", "C")
    for left in s["points"]:
        for right in s["points"]:
            if left != right:
                assert not dominates(s["points"][left], s["points"][right])


def test_middle_point_is_unsupported_by_every_nonnegative_linear_weight():
    s = frozen_specimen()
    assert s["support_intervals"]["B"] is None
    assert s["support_intervals"]["A"] == (Fraction(1, 2), Fraction(1))
    assert s["support_intervals"]["C"] == (Fraction(0), Fraction(1, 2))


def test_exact_hostile_inequalities_have_disjoint_requirements():
    points = frozen_specimen()["points"]
    # B <= A iff w <= 1/3; B <= C iff w >= 3/5. No w satisfies both.
    assert scalar_cost(points["B"], Fraction(1, 3)) == scalar_cost(points["A"], Fraction(1, 3))
    assert scalar_cost(points["B"], Fraction(3, 5)) == scalar_cost(points["C"], Fraction(3, 5))
    assert Fraction(1, 3) < Fraction(3, 5)


def test_supported_control_can_be_selected():
    points = frozen_specimen()["points"]
    assert scalar_cost(points["A"], Fraction(3, 4)) < scalar_cost(points["B"], Fraction(3, 4))
    assert scalar_cost(points["C"], Fraction(1, 4)) < scalar_cost(points["B"], Fraction(1, 4))


def test_invalid_weight_refused():
    with pytest.raises(ValueError):
        scalar_cost((0, 4), Fraction(5, 4))
