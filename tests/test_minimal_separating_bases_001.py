from dogram.minimal_separating_bases_001 import analyze_minimal_bases, separates


STATES = ("00", "01", "10", "11")
PROBES = {
    "x": {"00": 0, "01": 0, "10": 1, "11": 1},
    "y": {"00": 0, "01": 1, "10": 0, "11": 1},
    "xor": {"00": 0, "01": 1, "10": 1, "11": 0},
}


def test_each_two_probe_basis_separates_all_four_states():
    for family in (("x", "y"), ("x", "xor"), ("y", "xor")):
        assert separates(STATES, PROBES, family)


def test_no_single_binary_probe_separates_four_states():
    for name in PROBES:
        assert not separates(STATES, PROBES, (name,))


def test_three_distinct_minimum_bases_same_cardinality():
    receipt = analyze_minimal_bases(STATES, PROBES)
    assert receipt["minimum_cardinality"] == 2
    assert set(receipt["minimum_families"]) == {
        ("x", "xor"), ("x", "y"), ("xor", "y")
    }
    assert set(receipt["inclusion_minimal_families"]) == set(receipt["minimum_families"])


def test_every_probe_is_indispensable_inside_each_minimal_basis():
    receipt = analyze_minimal_bases(STATES, PROBES)
    for family in receipt["minimum_families"]:
        assert set(receipt["indispensable_within_minimal_family"][family]) == set(family)


def test_full_family_has_redundancy_despite_local_indispensability_in_bases():
    assert separates(STATES, PROBES, ("x", "y", "xor"))
    for removed in PROBES:
        remainder = tuple(name for name in PROBES if name != removed)
        assert separates(STATES, PROBES, remainder)
