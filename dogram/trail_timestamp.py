"""TRAIL-TIMESTAMP-001: UTC event -> declared Earth/sky projection.

This is a geometric, mean-sidereal research specimen, not an ephemeris,
an actual observation, a secure timestamp authority, or a prediction.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from math import asin, atan2, cos, degrees, isfinite, radians, sin
import re
from typing import Any


MODEL_VERSION = "TRAIL-TIMESTAMP-001/v1"
TIME_MODEL = "UTC_as_UT1_GMST_approx_mean_equinox_of_date"
RA_PATTERN = re.compile(r"^(\\d{2}):(\\d{2}):(\\d{2})$")
UTC_PATTERN = re.compile(
    r"^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$"
)


class TrailTimestampError(ValueError):
    def __init__(self, reason_code: str, residual: str) -> None:
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


def _number(value: Any, label: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TrailTimestampError("INVALID_COORDINATE", f"{label} must be a finite number")
    number = float(value)
    if not isfinite(number) or not minimum <= number <= maximum:
        raise TrailTimestampError(
            "INVALID_COORDINATE",
            f"{label} must be finite and within [{minimum}, {maximum}]",
        )
    return number


def _utc(value: str) -> datetime:
    if not isinstance(value, str) or not UTC_PATTERN.fullmatch(value):
        raise TrailTimestampError(
            "UTC_REQUIRED", "timestamp must be ISO 8601 with seconds and an explicit Z"
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise TrailTimestampError("INVALID_TIMESTAMP", str(error)) from error
    return parsed.astimezone(timezone.utc)


def _right_ascension(value: str) -> float:
    if not isinstance(value, str):
        raise TrailTimestampError("INVALID_RA", "right ascension must be HH:MM:SS")
    match = RA_PATTERN.fullmatch(value)
    if match is None:
        raise TrailTimestampError("INVALID_RA", "right ascension must be HH:MM:SS")
    hours, minutes, seconds = map(int, match.groups())
    if hours >= 24 or minutes >= 60 or seconds >= 60:
        raise TrailTimestampError("INVALID_RA", "right ascension is outside 24h")
    return hours + minutes / 60.0 + seconds / 3600.0


def _julian_date_utc(utc: datetime) -> float:
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    interval = utc - epoch
    microseconds = (
        interval.days * 86_400_000_000
        + interval.seconds * 1_000_000
        + interval.microseconds
    )
    return 2440587.5 + microseconds / 86_400_000_000


def _gmst_hours(utc: datetime) -> float:
    """Approximate Greenwich mean sidereal time, treating UTC as UT1.

    Classical Julian-century formula (mean equinox of date); not GAST.
    The lack of observed DUT1 and precession/nutation/frame conversion
    makes sub-second or exact celestial alignment claims inappropriate.
    """
    days = _julian_date_utc(utc) - 2451545.0
    centuries = days / 36525.0
    degrees = (
        280.46061837
        + 360.98564736629 * days
        + 0.000387933 * centuries * centuries
        - centuries * centuries * centuries / 38710000.0
    )
    return (degrees % 360.0) / 15.0


def _horizontal(
    latitude_deg: float,
    declination_deg: float,
    hour_angle_hours: float,
) -> tuple[float, float | None]:
    """Ideal geometric altitude and north-through-east azimuth.

    Azimuth is undefined at zenith/nadir; atmospheric refraction,
    parallax, topography and geodetic/geocentric corrections omitted.
    """
    phi = radians(latitude_deg)
    delta = radians(declination_deg)
    angle = radians(hour_angle_hours * 15.0)
    east = -cos(delta) * sin(angle)
    north = cos(phi) * sin(delta) - sin(phi) * cos(delta) * cos(angle)
    up = sin(phi) * sin(delta) + cos(phi) * cos(delta) * cos(angle)
    altitude = degrees(asin(max(-1.0, min(1.0, up))))
    if east * east + north * north < 1e-24:
        return altitude, None
    azimuth = degrees(atan2(east, north)) % 360.0
    return altitude, azimuth


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TrailTimestampError("INVALID_PROVENANCE", f"{label} must be nonblank")
    return value


def create_trail_receipt(event: dict[str, Any], observer: dict[str, Any],
                         target: dict[str, Any], decoder: str) -> dict[str, Any]:
    if not isinstance(event, dict) or not isinstance(observer, dict) or not isinstance(target, dict):
        raise TrailTimestampError("INVALID_SPECIMEN", "event, observer and target must be objects")
    event_id = _required_text(event.get("event_id"), "event_id")
    source_url = _required_text(event.get("source_url"), "source_url")
    source_kind = _required_text(event.get("source_kind"), "source_kind")
    decoder = _required_text(decoder, "decoder")
    utc = _utc(event.get("utc"))
    latitude = _number(observer.get("latitude_deg"), "latitude_deg", -90, 90)
    longitude = _number(observer.get("longitude_deg"), "longitude_deg", -180, 180)
    ra_text = target.get("ra_hms")
    ra = _right_ascension(ra_text)
    declination_input = target.get("declination_deg")
    basis = target.get("declination_basis")
    if declination_input is None:
        if basis is not None:
            raise TrailTimestampError("UNBOUND_DECLINATION", "declination_basis requires declination_deg")
        declination = None
    else:
        declination = _number(declination_input, "declination_deg", -90, 90)
        basis = _required_text(basis, "declination_basis")
    gmst = _gmst_hours(utc)
    lst = (gmst + longitude / 15.0) % 24.0
    hour_angle = ((lst - ra + 12.0) % 24.0) - 12.0
    if declination is None:
        altitude, azimuth = None, None
    else:
        altitude, azimuth = _horizontal(latitude, declination, hour_angle)
    stamp = utc.isoformat(timespec="microseconds" if utc.microsecond else "seconds").replace("+00:00", "Z")
    receipt = {
        "model_version": MODEL_VERSION,
        "event": {
            "event_id": event_id,
            "source_kind": source_kind,
            "source_url": source_url,
            "utc": stamp,
        },
        "decoder": decoder,
        "observer": {
            "latitude_deg": latitude,
            "longitude_deg_east_positive": longitude,
            "is_actual_user_location": False,
        },
        "target": {
            "ra_hms": ra_text,
            "ra_hours": ra,
            "declination_deg": declination,
            "declination_basis": basis,
            "frame": "declared_mean_equator_and_equinox_of_date_model",
            "is_identified_celestial_object": False,
        },
        "projection": {
            "julian_date_utc": round(_julian_date_utc(utc), 8),
            "gmst_hours": round(gmst, 9),
            "lst_hours": round(lst, 9),
            "hour_angle_hours_signed": round(hour_angle, 9),
            "altitude_deg_ideal": None if altitude is None else round(altitude, 8),
            "azimuth_deg_north_through_east": None if azimuth is None else round(azimuth, 8),
            "above_ideal_horizon": None if altitude is None else altitude > 0,
        },
        "limitations": {
            "time_model": TIME_MODEL,
            "missing_ut1_minus_utc": True,
            "mean_not_apparent_sidereal": True,
            "no_catalog_frame_transform_or_proper_motion": True,
            "no_refraction_parallax_topography": True,
            "no_authentication_of_event_source": True,
            "no_inference_of_intent_or_causation": True,
        },
    }
    content = json.dumps(receipt, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    receipt["receipt_sha256"] = sha256(content.encode("utf-8")).hexdigest()
    return receipt


def create_trail(specimen: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(specimen, dict):
        raise TrailTimestampError("INVALID_SPECIMEN", "input must be an object")
    events = specimen.get("events")
    if not isinstance(events, list) or not events:
        raise TrailTimestampError("INVALID_SPECIMEN", "events must be a nonempty array")
    ids: set[str] = set()
    receipts = []
    for event in events:
        receipt = create_trail_receipt(event, specimen.get("observer"),
                                       specimen.get("target"), specimen.get("decoder"))
        event_id = receipt["event"]["event_id"]
        if event_id in ids:
            raise TrailTimestampError("DUPLICATE_EVENT_ID", event_id)
        ids.add(event_id)
        receipts.append(receipt)
    return {
        "trail_version": MODEL_VERSION,
        "receipt_count": len(receipts),
        "receipts": receipts,
    }


__all__ = ["MODEL_VERSION", "TIME_MODEL", "TrailTimestampError",
           "create_trail", "create_trail_receipt"]
