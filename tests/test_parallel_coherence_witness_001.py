from research.parallel_coherence_witness_001 import receipt, specimen


def test_parallel_2_cells_are_distinct():
    alpha, beta, _, _ = specimen()
    assert alpha != beta
    assert (alpha.source, alpha.target) == (beta.source, beta.target)


def test_parallel_3_cells_are_distinct_despite_same_boundary():
    _, _, gamma, delta = specimen()
    assert gamma != delta
    assert gamma.source == delta.source
    assert gamma.target == delta.target


def test_receipt_keeps_coherence_identity_separate():
    r = receipt()
    assert r["parallel_2_cells"] is True
    assert r["parallel_3_cells"] is True
    assert r["same_2_cell_equivalence"] is True
    assert r["same_coherence_witness"] is False
