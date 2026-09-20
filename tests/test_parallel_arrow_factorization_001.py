from research.parallel_arrow_factorization_001 import A, B, E, compose, hostile_pair, verify


def test_klein_four_exact_arithmetic():
    assert compose(A, A) == E
    assert compose(B, B) == E
    assert A != B
    assert A != E and B != E


def test_same_object_sequence_and_composite_do_not_fix_arrow_path():
    left, right = hostile_pair()
    assert left.objects == right.objects == ("X", "X", "X")
    assert left.composite == right.composite == E
    assert left.arrows != right.arrows
    assert left.arrows == (A, A)
    assert right.arrows == (B, B)


def test_receipt_refuses_endpoint_collapse():
    result = verify()
    assert result["same_objects"] is True
    assert result["same_composite"] is True
    assert result["different_arrows"] is True
    assert result["all_arrows_nonidentity"] is True
