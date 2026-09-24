from research.outer_distribution_001 import A, B, compare, receipt


def test_same_coarse_radius_one_ambiguity_but_different_outer_distribution():
    r = compare()
    assert r["same_coarse"] is True
    assert r["same_outer_distribution"] is False
    for code in (A, B):
        x = receipt(code)
        assert x["minimum_distance"] == 1
        assert x["covering_radius"] == 2
        assert x["list_size_histogram"] == {0: 4, 1: 6, 2: 4, 3: 2}


def test_exact_pointwise_witness_retained():
    r = compare()
    assert r["witness"] == "0000"
    assert r["A_outer_at_witness"] == (1, 2, 1, 0, 0)
    assert r["B_outer_at_witness"] == (1, 2, 0, 1, 0)


def test_outer_rows_count_all_codewords():
    for code in (A, B):
        x = receipt(code)
        assert len(x["outer_rows"]) == 16
        assert all(sum(row) == 4 for row in x["outer_rows"].values())
