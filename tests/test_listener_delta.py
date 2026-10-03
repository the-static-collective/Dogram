import copy
import unittest

from dogram.canonical import sha256_json
from dogram.listener_delta import ListenerDeltaError, compare_listener_responses


PARENT_WINDOW = "autodisco-audio-window-v0:" + "1" * 64
CHILD_WINDOW = "autodisco-audio-window-v0:" + "2" * 64
PARENT_PAIR = "autodisco-audio-look-twice-pair-v0:" + "3" * 64
CHILD_PAIR = "autodisco-audio-look-twice-pair-v0:" + "4" * 64
PROPOSAL = "sha256:" + "5" * 64
GENERATION = "sha256:" + "6" * 64


LISTENERS = {
    "static-sam": {
        "id": "static-sam",
        "role": "Static Sam",
        "brief": "Dry and attentive to structure, motion, texture, and continuity. Never pretend prior familiarity.",
    },
    "juniper": {
        "id": "juniper",
        "role": "Juniper",
        "brief": "Emotionally exact and unhurried. Keep heard fact separate from felt interpretation.",
    },
}


def raw_hash(value):
    return sha256_json(value).split(":", 1)[1]


def seal(*, pair_id, window_id, audio_digit, listener_id, response, model="fixture-model"):
    response_hash = raw_hash(response)
    body = {
        "schema": "autodisco.audio-look-twice-first-response/v0",
        "pair_id": pair_id,
        "packet_id": "autodisco-audio-look-twice-first-v0:" + (
            "7" if listener_id == "static-sam" else "8"
        ) * 64,
        "listener": LISTENERS[listener_id],
        "window_id": window_id,
        "audio_sha256": audio_digit * 64,
        "model_used": model,
        "response_sha256": response_hash,
        "response": response,
        "laws": [
            "FIRST LISTEN PRECEDES DIALOGUE",
            "SEALED FIRST LISTEN != DIALOGUE",
            "HEARD != INTERPRETED",
        ],
    }
    return {
        **body,
        "first_response_id": (
            "autodisco-audio-look-twice-response-v0:" + raw_hash(body)
        ),
    }


def parent_response(listener_id):
    if listener_id == "static-sam":
        return {
            "observations": [
                {"mode": "OBSERVED", "text": "A repeated pulse sits under the window."},
                {"mode": "INTERPRETATION", "text": "The cutoff feels unresolved."},
            ],
            "lingering_intrigue": True,
            "closing_line": "I want to hear what happens after the cut.",
        }
    return {
        "observations": [
            {"mode": "OBSERVED", "text": "The texture thins near the ending."},
            {"mode": "METAPHOR", "text": "It feels like a door left open."},
        ],
        "lingering_intrigue": True,
        "closing_line": "The ending keeps pulling forward.",
    }


def child_response(listener_id):
    if listener_id == "static-sam":
        return {
            "observations": [
                {"mode": "OBSERVED", "text": "A repeated pulse sits under the window."},
                {"mode": "OBSERVED", "text": "The cutoff feels unresolved."},
                {"mode": "DERIVED", "text": "The ending arrives sooner."},
            ],
            "lingering_intrigue": False,
            "closing_line": "The cut now feels more final.",
        }
    return {
        "observations": [
            {"mode": "OBSERVED", "text": "The texture thickens near the ending."},
            {"mode": "METAPHOR", "text": "It feels like a door left open."},
            {"mode": "INTERPRETATION", "text": "The ending feels more final."},
        ],
        "lingering_intrigue": True,
        "closing_line": "The ending lands instead of pulling forward.",
    }


def request():
    return {
        "schema": "dogram.listener-delta-request/v0",
        "transform": {
            "relation": "ADMITTED_PROPOSAL_AS_NEW_AUDIO_SPECIMEN",
            "human_action": "explicit-admit",
            "parent_window_id": PARENT_WINDOW,
            "child_window_id": CHILD_WINDOW,
            "proposal_receipt_hash": PROPOSAL,
            "generation_delta_receipt_hash": GENERATION,
        },
        "parent_responses": [
            seal(
                pair_id=PARENT_PAIR,
                window_id=PARENT_WINDOW,
                audio_digit="a",
                listener_id=listener_id,
                response=parent_response(listener_id),
            )
            for listener_id in ("static-sam", "juniper")
        ],
        "child_responses": [
            seal(
                pair_id=CHILD_PAIR,
                window_id=CHILD_WINDOW,
                audio_digit="b",
                listener_id=listener_id,
                response=child_response(listener_id),
            )
            for listener_id in ("static-sam", "juniper")
        ],
    }


class ListenerDeltaTests(unittest.TestCase):
    def test_measures_each_same_listener_without_grading_person_or_music(self):
        receipt = compare_listener_responses(request())

        self.assertEqual(receipt["schema"], "dogram.listener-delta-receipt/v0")
        self.assertEqual(receipt["specimen"], "LISTENER-DELTA-001")
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(
            receipt["cohort"]["classification"],
            "MEASURED_RESPONSE_CHANGE",
        )
        self.assertEqual(receipt["cohort"]["changed_listener_count"], 2)
        self.assertEqual(set(receipt["listeners"]), {"static-sam", "juniper"})
        self.assertIn("closing_line", receipt["cohort"]["shared_changed_axes"])
        self.assertIn(
            "audio_change_causality_not_established",
            receipt["residuals"],
        )
        self.assertIn("RESPONSE DELTA != CAUSAL EFFECT", receipt["laws"])
        self.assertIn("DELTA != VALUE", receipt["laws"])
        self.assertTrue(receipt["receipt_hash"].startswith("sha256:"))

    def test_exact_observation_persistence_and_mode_migration_are_separate(self):
        receipt = compare_listener_responses(request())
        sam = receipt["listeners"]["static-sam"]["delta"]

        persisted = {
            (item["mode"], item["normalized_text"])
            for item in sam["exact_observations"]["persisted"]
        }
        self.assertIn(
            ("OBSERVED", "a repeated pulse sits under the window."),
            persisted,
        )
        self.assertEqual(
            sam["mode_migrations"],
            [{
                "normalized_text": "the cutoff feels unresolved.",
                "parent_modes": ["INTERPRETATION"],
                "child_modes": ["OBSERVED"],
            }],
        )
        self.assertEqual(sam["intrigue_relation"], "TRUE_TO_FALSE")

    def test_same_sealed_response_content_yields_no_measured_response_change(self):
        req = request()
        req["child_responses"] = [
            seal(
                pair_id=CHILD_PAIR,
                window_id=CHILD_WINDOW,
                audio_digit="b",
                listener_id=listener_id,
                response=parent_response(listener_id),
            )
            for listener_id in ("static-sam", "juniper")
        ]

        receipt = compare_listener_responses(req)

        self.assertEqual(
            receipt["cohort"]["classification"],
            "NO_MEASURED_RESPONSE_CHANGE",
        )
        self.assertEqual(receipt["cohort"]["changed_listener_count"], 0)
        for item in receipt["listeners"].values():
            self.assertEqual(
                item["delta"]["classification"],
                "NO_MEASURED_RESPONSE_CHANGE",
            )

    def test_model_change_is_measured_as_context_change_not_hidden(self):
        req = request()
        child = req["child_responses"][0]
        req["child_responses"][0] = seal(
            pair_id=CHILD_PAIR,
            window_id=CHILD_WINDOW,
            audio_digit="b",
            listener_id="static-sam",
            response=child["response"],
            model="fixture-model-v2",
        )

        receipt = compare_listener_responses(req)
        sam = receipt["listeners"]["static-sam"]["delta"]

        self.assertEqual(sam["model_relation"], "DIFFERENT")
        self.assertIn("model_used", sam["changed_axes"])
        self.assertIn(
            "stochastic_generation_effect_not_separated",
            receipt["residuals"],
        )

    def test_listener_descriptor_change_is_refused(self):
        req = request()
        altered = copy.deepcopy(req["child_responses"][0])
        altered["listener"]["role"] = "Someone Else"
        body = {k: altered[k] for k in altered if k != "first_response_id"}
        altered["first_response_id"] = (
            "autodisco-audio-look-twice-response-v0:" + raw_hash(body)
        )
        req["child_responses"][0] = altered

        with self.assertRaisesRegex(
            ListenerDeltaError,
            "listener descriptor changed",
        ):
            compare_listener_responses(req)

    def test_tampered_response_digest_is_refused(self):
        req = request()
        req["child_responses"][0]["response_sha256"] = "f" * 64

        with self.assertRaisesRegex(
            ListenerDeltaError,
            "response_sha256 mismatch",
        ):
            compare_listener_responses(req)

    def test_parent_and_child_must_bind_declared_window_ids(self):
        req = request()
        req["child_responses"][0]["window_id"] = PARENT_WINDOW
        body = {
            k: req["child_responses"][0][k]
            for k in req["child_responses"][0]
            if k != "first_response_id"
        }
        req["child_responses"][0]["first_response_id"] = (
            "autodisco-audio-look-twice-response-v0:" + raw_hash(body)
        )

        with self.assertRaisesRegex(
            ListenerDeltaError,
            "window identity mismatch",
        ):
            compare_listener_responses(req)

    def test_receipt_is_deterministic(self):
        req = request()
        first = compare_listener_responses(req)
        second = compare_listener_responses(req)

        self.assertEqual(first, second)
        self.assertEqual(first["receipt_hash"], second["receipt_hash"])


if __name__ == "__main__":
    unittest.main()
