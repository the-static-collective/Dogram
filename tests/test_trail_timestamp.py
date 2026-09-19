from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import unittest

from dogram.trail_timestamp import (
    TrailTimestampError,
    _horizontal,
    create_trail,
    create_trail_receipt,
)


FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures" / "trail_timestamp" / "trail-022100-git-001.json"
)


class TrailTimestampTests(unittest.TestCase):
    def setUp(self) -> None:
        self.specimen = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_five_frozen_git_events_replay_with_stable_receipts(self) -> None:
        first = create_trail(self.specimen)
        second = create_trail(self.specimen)
        self.assertEqual(first, second)
        self.assertEqual(first["receipt_count"], 5)
        self.assertEqual(first["trail_sha256"], first["receipts"][-1]["trail_link"]["entry_sha256"])
        self.assertIsNone(first["receipts"][0]["trail_link"]["previous_entry_sha256"])
        self.assertEqual(first["receipts"][1]["trail_link"]["previous_entry_sha256"], first["receipts"][0]["trail_link"]["entry_sha256"])
        self.assertEqual(first["receipts"][1]["trail_link"]["microseconds_since_previous_event"], 43_000_000)
        self.assertEqual(
            [r["event"]["utc"] for r in first["receipts"]],
            [e["utc"] for e in self.specimen["events"]],
        )
        for receipt in first["receipts"]:
            self.assertEqual(len(receipt["receipt_sha256"]), 64)
            self.assertFalse(receipt["observer"]["is_actual_user_location"])
            self.assertFalse(receipt["target"]["is_identified_celestial_object"])

    def test_pr8_gmst_matches_independent_wolfram_and_is_not_local_ra_hit(self) -> None:
        pr8 = create_trail(self.specimen)["receipts"][-1]
        projection = pr8["projection"]
        # Independent Wolfram Julian-century calculation, from freeze pressure:
        self.assertAlmostEqual(projection["gmst_hours"], 5.001134115, places=6)
        self.assertAlmostEqual(projection["lst_hours"], 11.667800782, places=6)
        self.assertAlmostEqual(projection["hour_angle_hours_signed"], 9.317800782, places=6)
        self.assertAlmostEqual(projection["altitude_deg_ideal"], -31.06182977, places=4)
        self.assertAlmostEqual(
            projection["azimuth_deg_north_through_east"], 315.64433263, places=4
        )
        self.assertFalse(projection["above_ideal_horizon"])

    def test_declination_is_required_for_altitude_and_azimuth(self) -> None:
        subset = deepcopy(self.specimen)
        subset["target"]["declination_deg"] = None
        subset["target"]["declination_basis"] = None
        projection = create_trail(subset)["receipts"][0]["projection"]
        self.assertIsNotNone(projection["hour_angle_hours_signed"])
        self.assertIsNone(projection["altitude_deg_ideal"])
        self.assertIsNone(projection["azimuth_deg_north_through_east"])
        self.assertIsNone(projection["above_ideal_horizon"])

    def test_zenith_is_an_explicitly_constructed_identity_not_a_discovery(self) -> None:
        altitude, azimuth = _horizontal(22.0, 22.0, 0.0)
        self.assertAlmostEqual(altitude, 90.0)
        self.assertIsNone(azimuth)

    def test_same_utc_different_longitude_changes_local_projection(self) -> None:
        first = create_trail(self.specimen)["receipts"][0]
        modified = deepcopy(self.specimen)
        modified["observer"]["longitude_deg"] = 0
        second = create_trail(modified)["receipts"][0]
        self.assertEqual(first["event"], second["event"])
        self.assertEqual(first["projection"]["gmst_hours"], second["projection"]["gmst_hours"])
        self.assertNotEqual(first["projection"]["lst_hours"], second["projection"]["lst_hours"])
        self.assertNotEqual(first["receipt_sha256"], second["receipt_sha256"])

    def test_provenance_changes_receipt_not_physical_projection(self) -> None:
        first = create_trail(self.specimen)["receipts"][0]
        modified = deepcopy(self.specimen)
        modified["events"][0]["source_kind"] = "USER_REPORTED_TIME"
        second = create_trail(modified)["receipts"][0]
        self.assertEqual(first["projection"], second["projection"])
        self.assertNotEqual(first["receipt_sha256"], second["receipt_sha256"])

    def test_trail_refuses_backwards_time(self) -> None:
        backwards = deepcopy(self.specimen)
        backwards["events"][0], backwards["events"][1] = backwards["events"][1], backwards["events"][0]
        with self.assertRaises(TrailTimestampError) as caught:
            create_trail(backwards)
        self.assertEqual(caught.exception.reason_code, "NON_CHRONOLOGICAL_TRAIL")

    def test_rejects_invalid_coordinates_and_time(self) -> None:
        scenarios = [
            ("observer", "latitude_deg", 91, "INVALID_COORDINATE"),
            ("observer", "longitude_deg", 181, "INVALID_COORDINATE"),
            ("observer", "latitude_deg", True, "INVALID_COORDINATE"),
            ("observer", "longitude_deg", float("nan"), "INVALID_COORDINATE"),
            ("target", "ra_hms", "24:00:00", "INVALID_RA"),
            ("target", "declination_deg", 91, "INVALID_COORDINATE"),
            ("events", 0, {"utc": "2026-09-19T05:07:34"}, "UTC_REQUIRED"),
            ("events", 0, {"utc": "2026-09-19T05:07:34+00:00"}, "UTC_REQUIRED"),
            ("events", 0, {"utc": "2026-09-19T05:07:34Z", "event_id": ""}, "INVALID_PROVENANCE"),
        ]
        for section, key, value, reason in scenarios:
            candidate = deepcopy(self.specimen)
            if section == "events":
                candidate["events"][key].update(value)
            else:
                candidate[section][key] = value
            with self.subTest(reason=reason, section=section, key=key):
                with self.assertRaises(TrailTimestampError) as caught:
                    create_trail(candidate)
                self.assertEqual(caught.exception.reason_code, reason)

    def test_duplicate_ids_and_unbound_declination_refused(self) -> None:
        duplicate = deepcopy(self.specimen)
        duplicate["events"][1]["event_id"] = duplicate["events"][0]["event_id"]
        with self.assertRaises(TrailTimestampError) as caught:
            create_trail(duplicate)
        self.assertEqual(caught.exception.reason_code, "DUPLICATE_EVENT_ID")

        unbound = deepcopy(self.specimen)
        unbound["target"]["declination_basis"] = None
        with self.assertRaises(TrailTimestampError) as caught:
            create_trail(unbound)
        self.assertEqual(caught.exception.reason_code, "INVALID_PROVENANCE")


if __name__ == "__main__":
    unittest.main()
