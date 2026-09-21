import json
import subprocess
import sys

from dogram.game_mechanics_stdio import (
    REQUEST_SCHEMA,
    RESPONSE_SCHEMA,
    handle_request,
)


def test_budget_rounding_operation_reuses_existing_dogram_receipt():
    response = handle_request(
        {
            "schema": REQUEST_SCHEMA,
            "operation": "budget_rounding",
            "weights": {"a": 5, "b": 4, "c": 1},
            "budget": 7,
            "method": "largest_fractional_remainder",
        }
    )

    assert response["schema"] == RESPONSE_SCHEMA
    assert response["ok"] is True
    assert response["authority"] == "none"
    assert response["result"]["allocation"] == {"a": 3, "b": 3, "c": 1}
    assert response["result"]["residuals"] == {
        "a": "-1/2",
        "b": "1/5",
        "c": "3/10",
    }


def test_successor_delta_receipts_foreclosed_new_and_retained_without_deciding():
    response = handle_request(
        {
            "schema": REQUEST_SCHEMA,
            "operation": "successor_delta",
            "beforeActions": ["feed-home", "share-meal", "rest"],
            "afterActions": ["share-meal", "rest", "ask-help"],
        }
    )

    assert response["ok"] is True
    assert response["result"] == {
        "experiment": "SUCCESSOR-DELTA-001",
        "before_actions": ["feed-home", "rest", "share-meal"],
        "after_actions": ["ask-help", "rest", "share-meal"],
        "foreclosed": ["feed-home"],
        "newly_available": ["ask-help"],
        "retained": ["rest", "share-meal"],
        "authority": "none",
        "non_claims": [
            "available successor != occurred successor",
            "foreclosed successor != morally preferred alternative",
            "same successor set != same underlying state",
        ],
    }


def test_invalid_request_is_structured_and_non_authoritative():
    response = handle_request(
        {
            "schema": REQUEST_SCHEMA,
            "operation": "budget_rounding",
            "weights": {"a": True},
            "budget": 1,
        }
    )
    assert response["ok"] is False
    assert response["error"]["code"] == "INVALID_INPUT"
    assert response["authority"] == "none"


def test_module_stdio_exchanges_one_json_document():
    request = {
        "schema": REQUEST_SCHEMA,
        "operation": "successor_delta",
        "beforeActions": ["a", "b"],
        "afterActions": ["b", "c"],
    }
    completed = subprocess.run(
        [sys.executable, "-m", "dogram.game_mechanics_stdio"],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=True,
    )
    response = json.loads(completed.stdout)
    assert response["schema"] == RESPONSE_SCHEMA
    assert response["ok"] is True
    assert response["result"]["foreclosed"] == ["a"]
    assert response["result"]["newly_available"] == ["c"]
