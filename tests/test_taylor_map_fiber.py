import json
from pathlib import Path

import pytest

from dogram.taylor_map_fiber import (
    fiber_collision_receipt,
    fiber_value,
    formal_series_realization_receipt,
)


FIXTURE = Path(__file__).parent / "fixtures" / "taylor_map_fiber_001.json"


def test_flat_perturbations_share_declared_complete_taylor_data():
    data = json.loads(FIXTURE.read_text())
    receipt = fiber_collision_receipt(
        data["base_taylor_coefficients"],
        data["flat_scales"],
        flat_kernel_fact_declared=True,
    )
    assert receipt["same_complete_taylor_series"] is True
    assert receipt["distinct_germs_witnessed"] is True
    assert receipt["fiber_cardinality_lower_bound"] == 3


def test_fiber_members_differ_off_origin():
    coeffs = [1, -2, 3]
    x = 0.5
    values = [fiber_value(coeffs, scale, x) for scale in (0, 1, 2)]
    assert len(set(values)) == 3


def test_flat_kernel_claim_requires_declared_theorem():
    with pytest.raises(ValueError, match="flat-kernel theorem"):
        fiber_collision_receipt([1, -2, 3], [0, 1], flat_kernel_fact_declared=False)


def test_borel_surjectivity_is_a_declared_proof_obligation_not_finite_enumeration():
    arbitrary_prefix = [7, 0, -5, 11, 2]
    receipt = formal_series_realization_receipt(
        arbitrary_prefix,
        borel_theorem_declared=True,
    )
    assert receipt["smooth_realization_exists"] is True
    assert receipt["proof_basis"] == "declared Borel theorem"
    assert receipt["canonical_representative_selected"] is False


def test_borel_claim_is_refused_when_theorem_is_withheld():
    with pytest.raises(ValueError, match="Borel theorem"):
        formal_series_realization_receipt([1, 2, 3], borel_theorem_declared=False)
