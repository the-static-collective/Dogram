import json
from pathlib import Path

from dogram.successor_class_quotient import quotient_receipt


def specimen():
    states = ["ready", "blocked", "green", "hold"]
    quotient = {"ready": "pending", "blocked": "pending", "green": "green", "hold": "hold"}
    transitions = [("ready", "advance", "green"), ("blocked", "advance", "hold")]
    return quotient_receipt(states, quotient, transitions)


def test_enabledness_factors_but_successor_class_does_not():
    pending = specimen()["classes"]["pending"]
    assert pending["enabled_factors"] is True
    assert pending["enabled"]["ready"] == ("advance",)
    assert pending["enabled"]["blocked"] == ("advance",)
    assert pending["successor_classes"]["advance"]["ready"] == ("green",)
    assert pending["successor_classes"]["advance"]["blocked"] == ("hold",)
    assert pending["successor_factors"]["advance"] is False
    assert pending["exact_one_step_factors"] is False


def test_frozen_fixture():
    frozen = json.loads((Path(__file__).parent / "fixtures" / "successor_class_quotient_001.json").read_text())
    pending = specimen()["classes"]["pending"]
    assert frozen["enabled_factors"] == pending["enabled_factors"]
    assert frozen["successor_factors_advance"] == pending["successor_factors"]["advance"]
    assert frozen["exact_one_step_factors"] == pending["exact_one_step_factors"]
