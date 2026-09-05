import json
from pathlib import Path

from dogram.laplacian_cospectral_structure import graph_receipt


FIXTURE = Path(__file__).parent / "fixtures" / "laplacian_cospectral_structure_001.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_frozen_pair_has_same_complete_laplacian_characteristic_polynomial():
    fixture = load_fixture()
    a = graph_receipt(fixture["graph_a"]["vertex_count"], fixture["graph_a"]["edges"])
    b = graph_receipt(fixture["graph_b"]["vertex_count"], fixture["graph_b"]["edges"])

    expected = tuple(fixture["shared"]["laplacian_characteristic_coefficients"])
    assert a["laplacian_characteristic_coefficients"] == expected
    assert b["laplacian_characteristic_coefficients"] == expected
    assert a["connected"] is True
    assert b["connected"] is True
    assert a["edge_count"] == b["edge_count"] == fixture["shared"]["edge_count"]


def test_same_spectrum_does_not_preserve_degree_sequence_or_triangle_count():
    fixture = load_fixture()
    a = graph_receipt(fixture["graph_a"]["vertex_count"], fixture["graph_a"]["edges"])
    b = graph_receipt(fixture["graph_b"]["vertex_count"], fixture["graph_b"]["edges"])

    assert list(a["degree_sequence"]) == fixture["graph_a"]["degree_sequence"]
    assert list(b["degree_sequence"]) == fixture["graph_b"]["degree_sequence"]
    assert a["degree_sequence"] != b["degree_sequence"]
    assert a["triangle_count"] == fixture["graph_a"]["triangle_count"]
    assert b["triangle_count"] == fixture["graph_b"]["triangle_count"]
    assert a["triangle_count"] != b["triangle_count"]


def test_spectrum_derived_spanning_tree_count_is_preserved():
    fixture = load_fixture()
    a = graph_receipt(fixture["graph_a"]["vertex_count"], fixture["graph_a"]["edges"])
    b = graph_receipt(fixture["graph_b"]["vertex_count"], fixture["graph_b"]["edges"])

    expected = fixture["shared"]["spanning_tree_count_from_spectrum"]
    assert a["spanning_tree_count_from_spectrum"] == expected
    assert b["spanning_tree_count_from_spectrum"] == expected
