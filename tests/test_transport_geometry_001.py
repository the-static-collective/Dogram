from fractions import Fraction as F
import importlib.util
from pathlib import Path

p = Path(__file__).parents[1] / "research" / "transport_geometry_001.py"
spec = importlib.util.spec_from_file_location("transport_geometry_001", p)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


def test_same_marginals_and_disagreement_different_cost():
    r = m.specimen()
    u = (F(1,3),) * 3
    assert r["marginals_pi01"] == (u,u)
    assert r["marginals_pi12"] == (u,u)
    assert r["disagreement_pi01"] == r["disagreement_pi12"] == F(2,3)
    assert r["cost_pi01"] == F(2,3)
    assert r["cost_pi12"] == F(4,3)
    assert r["cost_pi01"] != r["cost_pi12"]


def test_discrete_metric_collapses_cost_to_disagreement():
    r = m.specimen(); z=F(0); o=F(1)
    discrete=((z,o,o),(o,z,o),(o,o,z))
    assert m.transport_cost(r["pi01"], discrete) == F(2,3)
    assert m.transport_cost(r["pi12"], discrete) == F(2,3)


def test_metric_is_declared_not_inferred():
    r=m.specimen()
    assert r["metric"][0][2] == r["metric"][0][1] + r["metric"][1][2]
