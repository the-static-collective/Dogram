from dogram.list_decoding_ambiguity_001 import analyze


def test_even_parity_radius_one_list_geometry():
    code = [(0,0,0), (0,1,1), (1,0,1), (1,1,0)]
    receipt = analyze(code, radius=1)
    assert receipt["minimum_distance"] == 2
    assert receipt["covering_radius"] == 1
    assert receipt["maximum_list_size"] == 3
    assert receipt["list_size_distribution"] == {1: 4, 3: 4}
    rows = {r["received"]: r for r in receipt["rows"]}
    assert rows[(0,0,1)]["candidates"] == ((0,0,0), (0,1,1), (1,0,1))
    assert rows[(0,0,1)]["status"] == "ambiguous"
    assert rows[(0,0,0)]["candidates"] == ((0,0,0),)
    assert rows[(0,0,0)]["status"] == "unique"
    assert receipt["authority"] == "none"


def test_list_receipt_does_not_select_candidate():
    receipt = analyze([(0,0,0), (0,1,1), (1,0,1), (1,1,0)], 1)
    ambiguous = [r for r in receipt["rows"] if r["status"] == "ambiguous"]
    assert len(ambiguous) == 4
    assert all("selected" not in r and len(r["candidates"]) == 3 for r in ambiguous)
