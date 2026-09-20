from fractions import Fraction as F
from research.markov_lumpability_001 import analyze


STATES = ("a", "b", "c")
BLOCK = {"a": "A", "b": "A", "c": "B"}


def test_same_quotient_support_can_fail_strong_lumpability():
    p = {
        "a": {"a": F(1,2), "b": 0, "c": F(1,2)},
        "b": {"a": F(1,4), "b": 0, "c": F(3,4)},
        "c": {"a": 0, "b": 0, "c": 1},
    }
    r = analyze(STATES, BLOCK, p)
    assert r["quotient_support"]["a"] == r["quotient_support"]["b"] == ("A", "B")
    assert r["support_counterexample"] is None
    assert r["strong_lumpable"] is False
    assert r["mass_counterexample"] == ("a", "b", "A", F(1,2), F(1,4))
    assert r["induced_transition"] is None


def test_matching_block_mass_descends_even_when_raw_rows_differ():
    p = {
        "a": {"a": F(1,2), "b": 0, "c": F(1,2)},
        "b": {"a": 0, "b": F(1,2), "c": F(1,2)},
        "c": {"a": 0, "b": 0, "c": 1},
    }
    r = analyze(STATES, BLOCK, p)
    assert r["strong_lumpable"] is True
    assert r["induced_transition"]["A"] == {"A": F(1,2), "B": F(1,2)}


def test_exact_fraction_validation_refuses_bad_rows():
    bad = {
        "a": {"a": F(1,2), "b": 0, "c": F(1,2)},
        "b": {"a": F(1,4), "b": 0, "c": F(1,2)},
        "c": {"a": 0, "b": 0, "c": 1},
    }
    try:
        analyze(STATES, BLOCK, bad)
    except ValueError as exc:
        assert "sum exactly to 1" in str(exc)
    else:
        raise AssertionError("invalid stochastic row accepted")
