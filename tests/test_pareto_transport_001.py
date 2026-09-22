from fractions import Fraction
import pytest

from dogram.pareto_transport_001 import compare, dominates, frozen_specimen, scalar_cost


def test_frozen_cost_vectors_are_incomparable():
    s = frozen_specimen()
    assert s["pi"] == (Fraction(2), Fraction(2))
    assert s["rho"] == (Fraction(3), Fraction(1))
    assert s["pareto_relation"] == "incomparable"
    assert not dominates(s["pi"], s["rho"])
    assert not dominates(s["rho"], s["pi"])


def test_declared_weights_reverse_scalar_preference():
    s = frozen_specimen()["scalarizations"]
    assert s["favor_metric_1"]["pi"] < s["favor_metric_1"]["rho"]
    assert s["balanced"]["pi"] == s["balanced"]["rho"] == Fraction(2)
    assert s["favor_metric_2"]["rho"] < s["favor_metric_2"]["pi"]


def test_dominance_and_equality_controls():
    assert compare((1, 1), (1, 2)) == "left_dominates"
    assert compare((2, 2), (2, 2)) == "equal_cost_vector"


def test_scalarization_requires_declared_normalized_nonnegative_weights():
    with pytest.raises(ValueError):
        scalar_cost((2, 2), (1, 1))
    with pytest.raises(ValueError):
        scalar_cost((2, 2), (Fraction(3, 2), Fraction(-1, 2)))
