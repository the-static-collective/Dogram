"""TEMPORAL-RETURN-001: deterministic comparison of two independently witnessed encounters.

The shared JSON wire shape belongs to neither Upper Room nor CLOCKWORK.
Calendar positions are caller-supplied projections, never evidence of human events.
No imported biblical texts, clocks, ephemerides, external services or effects.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import isfinite
from typing import Any

from .canonical import sha256_json

SCHEMA = "dogram.temporal-return/specimen-v0"
OPERATOR = "temporal-return@1"
AXES = (
    ("chinese_solar_sector", ("chinese_solar", "index_from_vernal_equinox_zero_based"), 0, 23),
    ("hindu_tithi", ("hindu_angular", "tithi"), 1, 30),
    ("hindu_nakshatra", ("hindu_angular", "nakshatra"), 1, 27),
    ("hindu_yoga", ("hindu_angular", "yoga"), 1, 27),
    ("hindu_karana_position", ("hindu_angular", "karana", "half_tithi_index"), 0, 59),
)
SIDEREAL_AXES = frozenset(("hindu_nakshatra", "hindu_yoga"))


class TemporalReturnError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code


def _required(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 256:
        raise TemporalReturnError("INVALID_INPUT", f"{label}: nonblank string <=256 required")
    return value


def _utc(value: Any) -> datetime:
    text = _required(value, "instant_utc")
    if not text.endswith("Z"):
        raise TemporalReturnError("INVALID_TIME", "UTC timestamp must end in Z")
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TemporalReturnError("INVALID_TIME", "invalid ISO-8601 UTC instant") from exc
    if dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise TemporalReturnError("INVALID_TIME", "non-UTC offset")
    return dt


def _anchor(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"sourceRef", "scriptureRef"}:
        raise TemporalReturnError("INVALID_ANCHOR", "anchor needs exact sourceRef + scriptureRef")
    source = _required(value["sourceRef"], "anchor.sourceRef")
    ref = value["scriptureRef"]
    if not isinstance(ref, dict) or set(ref) not in ({"translationId", "book", "chapter"}, {"translationId", "book", "chapter", "verse"}):
        raise TemporalReturnError("INVALID_ANCHOR", "invalid ScriptureRef field set")
    _required(ref["translationId"], "translationId")
    _required(ref["book"], "book")
    for label in ("chapter", "verse"):
        if label in ref and (type(ref[label]) is not int or ref[label] < 1):
            raise TemporalReturnError("INVALID_ANCHOR", f"{label} must be positive integer")
    return {"sourceRef": source, "scriptureRef": dict(ref)}


def _extract(packet: dict[str, Any], path: tuple[str, ...], lo: int, hi: int) -> int | None:
    cursor: Any = packet
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            return None
        cursor = cursor[key]
    if type(cursor) is not int or not lo <= cursor <= hi:
        raise TemporalReturnError("INVALID_COORDINATE", f"{'.'.join(path)} outside declared integer range")
    return cursor


def _frame(packet: dict[str, Any]) -> str:
    provider = packet.get("provider")
    if not isinstance(provider, dict):
        raise TemporalReturnError("INVALID_PROVIDER", "missing provider metadata")
    return _required(provider.get("coordinate_frame"), "provider.coordinate_frame")


def _sidereal(packet: dict[str, Any]) -> tuple[str, float]:
    item = packet.get("ayanamsa")
    if not isinstance(item, dict):
        raise TemporalReturnError("INVALID_AYANAMSA", "missing sidereal convention")
    name = _required(item.get("name"), "ayanamsa.name")
    deg = item.get("degrees")
    if isinstance(deg, bool) or not isinstance(deg, (int, float)) or not isfinite(deg) or not -360 <= deg <= 360:
        raise TemporalReturnError("INVALID_AYANAMSA", "finite ayanamsa degrees required")
    return (name, float(deg))


def compare_temporal_return(specimen: dict[str, Any]) -> dict[str, Any]:
    """Compare caller-owned occurrence references, then typed coordinate projections."""
    if not isinstance(specimen, dict) or specimen.get("schema") != SCHEMA:
        raise TemporalReturnError("INVALID_SCHEMA", f"expected {SCHEMA}")
    if set(specimen) != {"schema", "specimen_id", "encounters"}:
        raise TemporalReturnError("INVALID_INPUT", "unknown or missing specimen fields")
    _required(specimen["specimen_id"], "specimen_id")
    entries = specimen["encounters"]
    if not isinstance(entries, list) or len(entries) != 2:
        raise TemporalReturnError("INVALID_INPUT", "exactly two encounters are required")
    ids: list[str] = []
    anchors: list[dict[str, Any]] = []
    times: list[datetime] = []
    packets: list[dict[str, Any] | None] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"encounterId", "anchor", "instant_utc", "temporalWitness"}:
            raise TemporalReturnError("INVALID_INPUT", "invalid encounter field set")
        ids.append(_required(entry["encounterId"], "encounterId"))
        anchors.append(_anchor(entry["anchor"]))
        instant = _utc(entry["instant_utc"])
        times.append(instant)
        packet = entry["temporalWitness"]
        if packet is not None:
            if not isinstance(packet, dict) or packet.get("kind") != "experimental_astronomical_coordinate_packet":
                raise TemporalReturnError("INVALID_WITNESS", "unrecognized temporal packet")
            if _utc(packet.get("instant_utc")) != instant:
                raise TemporalReturnError("TIMESTAMP_MISMATCH", "witness instant differs from encounter instant")
            _frame(packet)
        packets.append(packet)
    if ids[0] == ids[1]:
        raise TemporalReturnError("DUPLICATE_OCCURRENCE", "two encounters require distinct IDs")
    if times[1] < times[0]:
        raise TemporalReturnError("REVERSED_TIME", "second encounter must not precede first")
    if anchors[0] != anchors[1]:
        raise TemporalReturnError("ANCHOR_MISMATCH", "this specimen requires the exact same Scripture anchor")
    comparison: dict[str, Any] = {}
    for label, path, lo, hi in AXES:
        first, second = (_extract(p, path, lo, hi) if p is not None else None for p in packets)
        if first is None or second is None:
            status = "unavailable"
        elif _frame(packets[0]) != _frame(packets[1]):
            status = "incomparable_frame"
        elif label in SIDEREAL_AXES and _sidereal(packets[0]) != _sidereal(packets[1]):
            status = "incomparable_sidereal_convention"
        else:
            status = "same_coordinate" if first == second else "changed_coordinate"
        comparison[label] = {"first": first, "second": second, "status": status}
    return {
        "schema": "dogram.temporal-return/receipt-v0", "operator": OPERATOR,
        "specimen_id": specimen["specimen_id"], "input_digest": sha256_json(specimen),
        "status": "OK", "encounter_refs": ids, "anchor": anchors[0],
        "elapsed_microseconds": (times[1] - times[0]) // timedelta(microseconds=1),
        "witness_digests": [sha256_json(p) if p is not None else None for p in packets],
        "coordinate_comparison": comparison,
        "non_claims": ["calendar projection does not authenticate an occurrence",
                       "numeric agreement is not causal or theological evidence",
                       "OK means computation completed, not authority or interpretation"],
    }
