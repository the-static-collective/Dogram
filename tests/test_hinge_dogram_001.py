import copy

import pytest

from research.hinge_dogram_001 import exact_relation_delta, verify_alex_hinge_receipt


BEFORE = [
    {"selector": "sign:hinge", "relation": "reading:mechanical-joint"},
    {"selector": "sign:wire", "relation": "reading:carrier"},
]

AFTER = [
    {"selector": "sign:hinge", "relation": "reading:constitutive-relation"},
    {"selector": "sign:wire", "relation": "reading:carrier"},
    {"selector": "sign:crossing", "relation": "reading:relation-site"},
]

ALEX_RECEIPT = {
    "added_rules": [
        {"selector": "sign:crossing", "relation": "reading:relation-site"},
    ],
    "removed_rules": [],
    "retargeted_rules": [
        {
            "selector": "sign:hinge",
            "before": "reading:mechanical-joint",
            "after": "reading:constitutive-relation",
        }
    ],
    "unchanged_rules": [
        {"selector": "sign:wire", "relation": "reading:carrier"},
    ],
    "grammar_changed": True,
    "authority": "none",
    "meaning_verdict": "none",
}


def test_exact_relation_delta_is_order_independent():
    r1 = exact_relation_delta(BEFORE, AFTER)
    r2 = exact_relation_delta(list(reversed(BEFORE)), list(reversed(AFTER)))
    assert r1 == r2
    assert r1["added"] == (("sign:crossing", "reading:relation-site"),)
    assert r1["retargeted"] == (
        ("sign:hinge", "reading:mechanical-joint", "reading:constitutive-relation"),
    )
    assert r1["unchanged"] == (("sign:wire", "reading:carrier"),)


def test_alex_hinge_receipt_recomputes_exactly():
    r = verify_alex_hinge_receipt(BEFORE, AFTER, ALEX_RECEIPT)
    assert r["verdict"] == "EXACT_MATCH"
    assert r["authority_preserved"] is True
    assert r["meaning_verdict_preserved"] is True
    assert "semantic_truth" in r["does_not_establish"]


def test_tampered_retarget_is_detected():
    receipt = copy.deepcopy(ALEX_RECEIPT)
    receipt["retargeted_rules"][0]["after"] = "reading:other"
    r = verify_alex_hinge_receipt(BEFORE, AFTER, receipt)
    assert r["verdict"] == "MISMATCH"


def test_authority_change_does_not_change_math_but_is_exposed():
    receipt = copy.deepcopy(ALEX_RECEIPT)
    receipt["authority"] = "granted"
    r = verify_alex_hinge_receipt(BEFORE, AFTER, receipt)
    assert r["verdict"] == "EXACT_MATCH"
    assert r["authority_preserved"] is False


def test_duplicate_selector_is_refused_by_math_boundary():
    bad = BEFORE + [{"selector": "sign:hinge", "relation": "reading:duplicate"}]
    with pytest.raises(ValueError):
        exact_relation_delta(bad, AFTER)


def test_same_rules_new_order_has_zero_delta():
    r = exact_relation_delta(BEFORE, list(reversed(BEFORE)))
    assert r["grammar_changed"] is False
    assert r["added"] == ()
    assert r["removed"] == ()
    assert r["retargeted"] == ()
