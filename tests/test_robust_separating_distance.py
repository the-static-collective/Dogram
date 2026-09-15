from dogram.robust_separating_distance import SPECIMEN, all_erasures_separate, minimum_distance, pair_receipt


def test_all_pairs_have_distance_two():
    assert minimum_distance(SPECIMEN) == 2
    assert {row["distance"] for row in pair_receipt(SPECIMEN)} == {2}


def test_any_one_view_can_be_erased_without_collision():
    assert all_erasures_separate(SPECIMEN, 1)


def test_two_view_erasures_are_not_guaranteed_safe():
    assert not all_erasures_separate(SPECIMEN, 2)
