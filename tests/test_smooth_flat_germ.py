import json
import math
from pathlib import Path

from dogram.smooth_flat_germ import derivative_polynomials, flat_value, zero_taylor_jet


FIXTURE = Path(__file__).parent / "fixtures" / "smooth_flat_germ_001.json"


def test_frozen_zero_taylor_probe():
    data = json.loads(FIXTURE.read_text())
    orders = data["declared_probe_orders"]
    assert zero_taylor_jet(max(orders)) == data["expected_taylor_coefficients"]


def test_flat_germ_is_not_zero_off_origin():
    data = json.loads(FIXTURE.read_text())
    samples = [1.0, 0.5, -0.5]
    assert data["expected_off_origin_nonzero"] is True
    assert all(flat_value(x) > 0.0 for x in samples)
    assert flat_value(0.0) == 0.0


def test_exact_derivative_recurrence_begins_correctly():
    polys = derivative_polynomials(4)
    assert polys[0] == (1,)
    assert polys[1] == (0, 0, 0, 2)
    assert polys[2] == (0, 0, 0, 0, 6, 0, -4, 0, 4)
    assert len(polys) == 5


def test_declared_finite_probe_cannot_distinguish_zero_germ_from_flat_germ():
    for order in range(9):
        assert zero_taylor_jet(order) == [0] * (order + 1)
    assert flat_value(0.5) != 0.0
