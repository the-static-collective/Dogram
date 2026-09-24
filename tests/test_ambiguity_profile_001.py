from dogram.ambiguity_profile_001 import CODE_A, CODE_B, receipt


def test_same_coarse_invariants_different_ambiguity_profiles():
    a = receipt(CODE_A)
    b = receipt(CODE_B)
    coarse = ("length", "cardinality", "minimum_distance", "covering_radius", "maximum_list_size")
    assert tuple(a[k] for k in coarse) == (4, 4, 2, 2, 3)
    assert tuple(b[k] for k in coarse) == (4, 4, 2, 2, 3)
    assert a["list_size_profile"] == {0: 4, 1: 8, 3: 4}
    assert b["list_size_profile"] == {0: 4, 1: 6, 2: 4, 3: 2}
    assert a["list_size_profile"] != b["list_size_profile"]
    assert a["authority"] == b["authority"] == "none"


def test_receipt_retains_local_lists_not_only_histogram():
    a = receipt(CODE_A)
    b = receipt(CODE_B)
    assert a["lists"]["0010"] == ("0000", "0011", "0110")
    assert b["lists"]["0010"] == ("0000", "0011", "1010")
