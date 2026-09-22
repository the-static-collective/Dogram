from fractions import Fraction
from research.transport_metric_ranking_001 import specimen


def test_both_declared_geometries_are_metrics():
    assert specimen()["metrics_valid"] is True


def test_same_couplings_reverse_ranking_under_changed_metric():
    r = specimen()
    assert r["left_costs"] == (Fraction(2), Fraction(3))
    assert r["right_costs"] == (Fraction(2), Fraction(1))
    assert r["ranking_reverses"] is True


def test_coupling_receipts_are_held_fixed():
    r = specimen()
    assert r["pi"] == (0, 1, 3, 2)
    assert r["rho"] == (0, 2, 1, 3)
    assert r["pi"] != r["rho"]
