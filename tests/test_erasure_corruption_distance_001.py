from research.erasure_corruption_distance_001 import analyze, frozen_specimen


def test_even_parity_specimen_has_distance_two():
    r = frozen_specimen()
    assert r["minimum_distance"] == 2
    assert {d for _, _, d in r["pair_distances"]} == {2}


def test_any_one_known_erasure_is_recoverable():
    r = frozen_specimen()
    assert r["single_known_erasure_recoverable"] is True
    assert all(v["unique"] for v in r["punctures"].values())


def test_one_unknown_flip_is_detected_but_not_uniquely_corrected():
    r = frozen_specimen()
    assert r["single_unknown_flip_detectable"] is True
    assert r["single_unknown_flip_uniquely_correctable"] is False


def test_ambiguity_witness_is_retained():
    r = frozen_specimen()
    witnesses = dict(r["ambiguous_one_flip_receipts"])
    assert (0, 0, 1) in witnesses
    assert set(witnesses[(0, 0, 1)]) == {(0, 0, 0), (0, 1, 1), (1, 0, 1)}


def test_distance_three_control_corrects_one_unknown_flip():
    r = analyze(((0, 0, 0), (1, 1, 1)))
    assert r["minimum_distance"] == 3
    assert r["single_unknown_flip_detectable"] is True
    assert r["single_unknown_flip_uniquely_correctable"] is True


def test_distance_one_control_does_not_even_detect_every_flip():
    r = analyze(((0, 0), (0, 1)))
    assert r["minimum_distance"] == 1
    assert r["single_unknown_flip_detectable"] is False
    assert r["single_known_erasure_recoverable"] is False
