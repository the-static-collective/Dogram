from fractions import Fraction

from dogram.scalarization_visibility_001 import (
    epsilon_constraint_winners,
    frozen_receipt,
    pareto_minimal,
    weighted_winners,
)

POINTS = {"A": (Fraction(0), Fraction(4)), "B": (Fraction(2), Fraction(3)), "C": (Fraction(4), Fraction(0))}


def test_all_three_are_pareto_minimal():
    assert all(pareto_minimal(POINTS, name) for name in POINTS)


def test_B_cannot_win_any_normalized_nonnegative_weighted_sum():
    # B <= A requires 3-w <= 4-4w => w <= 1/3.
    # B <= C requires 3-w <= 4w => w >= 3/5.
    assert Fraction(1, 3) < Fraction(3, 5)
    # Exhaustive rational grid is a hostile computational control, not the proof.
    for numerator in range(1001):
        assert "B" not in weighted_winners(POINTS, Fraction(numerator, 1000))


def test_epsilon_constraint_recovers_B_exactly():
    winners, feasible = epsilon_constraint_winners(POINTS, Fraction(3))
    assert tuple(sorted(feasible)) == ("B", "C")
    assert winners == ("B",)


def test_epsilon_is_declared_and_changes_visibility():
    winners_low, _ = epsilon_constraint_winners(POINTS, Fraction(2))
    winners_exact, _ = epsilon_constraint_winners(POINTS, Fraction(3))
    winners_high, _ = epsilon_constraint_winners(POINTS, Fraction(4))
    assert winners_low == ("C",)
    assert winners_exact == ("B",)
    assert winners_high == ("A",)


def test_receipt_keeps_method_relative_result_and_no_authority():
    receipt = frozen_receipt()
    assert receipt["B_weighted_sum_selectable"] is False
    assert receipt["B_epsilon_selectable"] is True
    assert receipt["authority"] == "none"
