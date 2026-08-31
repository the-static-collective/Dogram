from __future__ import annotations

import pytest

from dogram.mapping_torus import (
    MappingTorusInputError,
    analyze_mapping_torus,
    decompose_winding,
    relative_realignment,
    twisted_mode_fraction,
)


def test_mapping_torus_components_and_orbit_length_are_exact() -> None:
    coprime = analyze_mapping_torus(72, 5)
    assert coprime.to_data() == {
        "fiber_count": 72,
        "shift": 5,
        "normalized_shift": 5,
        "components": 1,
        "orbit_length": 72,
    }

    sixfold = analyze_mapping_torus(72, 6)
    assert sixfold.components == 6
    assert sixfold.orbit_length == 12


def test_negative_and_equivalent_shifts_preserve_input_identity() -> None:
    negative = analyze_mapping_torus(72, -67)
    equivalent = analyze_mapping_torus(72, 5)
    wrapped = analyze_mapping_torus(72, 77)

    assert negative.normalized_shift == equivalent.normalized_shift == wrapped.normalized_shift == 5
    assert negative.components == equivalent.components == wrapped.components == 1
    assert negative.shift == -67
    assert equivalent.shift == 5
    assert wrapped.shift == 77


def test_winding_decomposition_reconstructs_positive_zero_and_negative_counts() -> None:
    for traversal in (145, 0, -1, -73):
        result = decompose_winding(72, traversal)
        assert 0 <= result.residue < 72
        assert 72 * result.winding + result.residue == traversal
        assert result.traversal_count == traversal


def test_relative_realignment_reproduces_researched_72_5_7_case() -> None:
    result = relative_realignment(72, 5, 7)
    assert result.relative_delta == 70
    assert result.realignment_period == 36
    assert result.to_data() == {
        "fiber_count": 72,
        "shift_a": 5,
        "shift_b": 7,
        "relative_delta": 70,
        "realignment_period": 36,
    }


def test_twisted_mode_is_reduced_exact_rational_without_float_drift() -> None:
    result = twisted_mode_fraction(72, 5, longitudinal_index=1, fiber_mode=6)
    assert result.numerator == 17
    assert result.denominator == 12
    assert result.to_data() == {
        "fiber_count": 72,
        "shift": 5,
        "longitudinal_index": 1,
        "fiber_mode": 6,
        "numerator": 17,
        "denominator": 12,
    }


def test_invalid_dimensions_and_non_integer_inputs_refuse_with_typed_codes() -> None:
    for invalid in (0, -1, True, 72.0, "72"):
        with pytest.raises(MappingTorusInputError) as caught:
            analyze_mapping_torus(invalid, 5)  # type: ignore[arg-type]
        assert caught.value.reason_code == "INVALID_FIBER_COUNT"

    for invalid_shift in (True, 5.0, "5"):
        with pytest.raises(MappingTorusInputError) as caught:
            analyze_mapping_torus(72, invalid_shift)  # type: ignore[arg-type]
        assert caught.value.reason_code == "INVALID_INTEGER"


def test_same_coarse_surface_does_not_collapse_calculation_history() -> None:
    first = analyze_mapping_torus(12, 1)
    second = analyze_mapping_torus(12, 5)
    assert (first.components, first.orbit_length) == (second.components, second.orbit_length)
    assert first.to_data() != second.to_data()
