import json
from pathlib import Path

from dogram.sheaf_cospectral_gluing import analyze_sheaf_cospectral_gluing


FIXTURE = Path(__file__).parent / "fixtures" / "sheaf_cospectral_gluing_001.json"


def test_same_h0_and_same_laplacian_spectrum_do_not_fix_gluing_class():
    expected = json.loads(FIXTURE.read_text())
    receipt = analyze_sheaf_cospectral_gluing()

    assert list(receipt.charpoly_a) == expected["charpoly"]
    assert receipt.charpoly_a == receipt.charpoly_b
    assert receipt.determinant_a == expected["determinant"]
    assert receipt.determinant_a == receipt.determinant_b
    assert receipt.h0_dimension_a == expected["h0_dimension"]
    assert receipt.h0_dimension_a == receipt.h0_dimension_b

    assert [list(x) for x in receipt.negative_triangle_degree_profiles_a] == expected[
        "negative_triangle_degree_profiles_a"
    ]
    assert [list(x) for x in receipt.negative_triangle_degree_profiles_b] == expected[
        "negative_triangle_degree_profiles_b"
    ]
    assert receipt.negative_triangle_degree_profiles_a != receipt.negative_triangle_degree_profiles_b


def test_negative_cycle_degree_profile_is_switching_isomorphism_invariant_witness():
    receipt = analyze_sheaf_cospectral_gluing()

    # Vertex switching preserves every cycle sign. Any base-graph automorphism
    # preserves vertex degrees. Therefore different degree profiles among
    # negative triangles certify different switching-isomorphism classes.
    assert receipt.negative_triangle_degree_profiles_a == ((2, 5, 5), (2, 5, 5))
    assert receipt.negative_triangle_degree_profiles_b == ((3, 5, 5), (3, 5, 5))
