from fractions import Fraction
import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[1] / "research" / "coupling_witness_001.py"
spec = importlib.util.spec_from_file_location("coupling_witness_001", MODULE)
cw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cw)


def test_same_marginals_same_scalar_disagreement_different_witness():
    identity, a, b = cw.frozen_specimen()
    uniform = (Fraction(1,3),) * 3
    assert a["left_marginal"] == b["left_marginal"] == uniform
    assert a["right_marginal"] == b["right_marginal"] == uniform
    assert a["total_variation"] == b["total_variation"] == 0
    assert a["disagreement"] == b["disagreement"] == Fraction(2,3)
    assert a["matrix"] != b["matrix"]
    assert a["support"] != b["support"]


def test_coupling_inequality_and_maximal_control():
    identity, a, b = cw.frozen_specimen()
    assert identity["coupling_inequality_holds"]
    assert identity["maximal"]
    assert identity["disagreement"] == identity["total_variation"] == 0
    assert a["coupling_inequality_holds"] and b["coupling_inequality_holds"]
    assert not a["maximal"] and not b["maximal"]


def test_rejects_malformed_mass():
    try:
        cw.coupling_receipt(((Fraction(1,2), 0), (0, 0)))
    except ValueError:
        pass
    else:
        raise AssertionError("must reject mass not summing to one")
