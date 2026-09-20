from research.declared_path_equivalence_001 import congruence_classes, receipt


def test_relation_identifies_without_literal_identity():
    r = receipt()
    assert r["free_paths"] == ["aa", "bb"]
    assert r["free_paths_distinct"] is True
    assert r["same_quotient_class"] is True
    assert r["declared_relation"]["name"] == "alpha"


def test_congruence_propagates_through_bounded_context():
    c = congruence_classes(max_len=4)
    assert c["aa"] == c["bb"]
    assert c["aaa"] == c["abb"]
    assert c["baa"] == c["bbb"]
    assert c["aaaa"] == c["aabb"] == c["bbaa"] == c["bbbb"]


def test_without_declared_generator_paths_remain_distinct():
    c = congruence_classes(lhs="aa", rhs="aa", max_len=4)
    assert c["aa"] != c["bb"]
