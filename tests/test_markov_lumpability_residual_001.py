from fractions import Fraction

from research.markov_lumpability_residual_001 import analyze_residual


def specimen():
    states = ("a", "b", "c")
    block = {"a": "A", "b": "A", "c": "B"}
    transition = {
        "a": {"a": Fraction(1, 2), "b": 0, "c": Fraction(1, 2)},
        "b": {"a": Fraction(1, 4), "b": 0, "c": Fraction(3, 4)},
        "c": {"a": 0, "b": 0, "c": 1},
    }
    return states, block, transition


def test_exact_residual_receipts_mass_collision():
    r = analyze_residual(*specimen())
    assert r["strong_lumpable"] is False
    assert r["maximum_total_variation"] == Fraction(1, 4)
    w = r["maximum_witness"]
    assert w["pair"] == ("a", "b")
    assert w["max_block_discrepancy"] == Fraction(1, 4)
    assert set(w["signed_block_delta"].values()) == {Fraction(1, 4), Fraction(-1, 4)}


def test_tolerance_is_declared_and_does_not_change_exact_status():
    r = analyze_residual(*specimen(), tolerance=Fraction(1, 4))
    assert r["within_declared_tolerance"] is True
    assert r["strong_lumpable"] is False
    tighter = analyze_residual(*specimen(), tolerance=Fraction(1, 5))
    assert tighter["within_declared_tolerance"] is False


def test_exact_control_has_zero_residual():
    states, block, transition = specimen()
    transition["b"] = {"a": Fraction(1, 8), "b": Fraction(3, 8), "c": Fraction(1, 2)}
    r = analyze_residual(states, block, transition)
    assert r["strong_lumpable"] is True
    assert r["maximum_total_variation"] == 0


def test_bad_tolerance_refused():
    states, block, transition = specimen()
    try:
        analyze_residual(states, block, transition, tolerance=Fraction(5, 4))
    except ValueError:
        pass
    else:
        raise AssertionError("expected invalid tolerance refusal")
