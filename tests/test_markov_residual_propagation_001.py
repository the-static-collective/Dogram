from fractions import Fraction
from research.markov_residual_propagation_001 import tv, dobrushin, row_residual, propagate, frozen_specimen


def test_frozen_noncontractive_accumulation():
    r=frozen_specimen(Fraction(1,10),10)
    assert r["epsilon"] == Fraction(1,10)
    assert r["kappa"] == 1
    assert r["steps"][0]["tv"] == Fraction(1,10)
    assert r["steps"][-1]["tv"] == 1-Fraction(9,10)**10
    assert r["steps"][-1]["bound"] == 1
    assert r["steps"][-1]["tv"] > Fraction(3,5)


def test_contractive_envelope_is_geometric_not_linear():
    # P forgets its input completely: kappa=0.
    P=((Fraction(1,2),Fraction(1,2)),)*2
    Q=((Fraction(3,5),Fraction(2,5)),)*2
    r=propagate((Fraction(1),Fraction(0)),P,Q,10)
    assert r["epsilon"] == Fraction(1,10)
    assert r["kappa"] == 0
    assert all(x["bound"] == Fraction(1,10) for x in r["steps"])
    assert all(x["tv"] == Fraction(1,10) for x in r["steps"])


def test_intermediate_contraction_bound():
    P=((Fraction(3,4),Fraction(1,4)),(Fraction(1,4),Fraction(3,4)))
    Q=((Fraction(4,5),Fraction(1,5)),(Fraction(3,10),Fraction(7,10)))
    r=propagate((Fraction(1),Fraction(0)),P,Q,8)
    assert r["kappa"] == Fraction(1,2)
    assert r["epsilon"] == Fraction(1,20)
    assert all(x["tv"] <= x["bound"] for x in r["steps"])
    assert r["steps"][-1]["bound"] < Fraction(1,10)


def test_tv_and_row_residual_exact():
    P=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)))
    Q=((Fraction(9,10),Fraction(1,10)),(Fraction(0),Fraction(1)))
    assert row_residual(P,Q) == Fraction(1,10)
    assert dobrushin(P) == 1
    assert tv(P[0],Q[0]) == Fraction(1,10)
