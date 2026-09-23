from research.robust_separation_margin_001 import analyze, frozen_specimen


def test_full_x_y_xor_has_margin_two():
    full, _ = frozen_specimen()
    assert full["separating"] is True
    assert full["margin"] == 2
    assert full["single_probe_loss_tolerant"] is True
    assert set(full["signatures"].values()) == {
        (0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)
    }


def test_every_single_probe_deletion_still_separates_but_margin_drops():
    _, deletions = frozen_specimen()
    assert set(deletions) == {"x", "y", "xor"}
    assert all(r["separating"] for r in deletions.values())
    assert all(r["margin"] == 1 for r in deletions.values())
    assert not any(r["single_probe_loss_tolerant"] for r in deletions.values())


def test_one_minimal_basis_separates_without_single_loss_tolerance():
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    result = analyze(states, {"x": lambda s: s[0], "y": lambda s: s[1]})
    assert result["separating"] is True
    assert result["margin"] == 1
    assert result["single_probe_loss_tolerant"] is False


def test_single_probe_is_not_separating_four_states():
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    result = analyze(states, {"x": lambda s: s[0]})
    assert result["margin"] == 0
    assert result["separating"] is False


def test_distance_receipt_retains_pair_witnesses():
    full, _ = frozen_specimen()
    assert len(full["pair_distances"]) == 6
    assert {d for _, _, d in full["pair_distances"]} == {2}
