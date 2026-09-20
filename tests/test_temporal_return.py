import pytest

from dogram.temporal_return import TemporalReturnError, compare_temporal_return


def anchor():
    return {"sourceRef": "urn:fixture:webp:John:1", "scriptureRef": {"translationId": "engwebp", "book": "John", "chapter": 1, "verse": 1}}


def packet(instant, solar, tithi, nakshatra=5, *, ayanamsa=24):
    return {"kind": "experimental_astronomical_coordinate_packet", "instant_utc": instant,
            "provider": {"name": "synthetic", "version": "fixture-1", "source": "fixture",
                         "coordinate_frame": "geocentric_apparent_ecliptic_of_date"},
            "ayanamsa": {"name": "fixture", "degrees": ayanamsa},
            "chinese_solar": {"index_from_vernal_equinox_zero_based": solar},
            "hindu_angular": {"tithi": tithi, "nakshatra": nakshatra, "yoga": 10,
                              "karana": {"half_tithi_index": 0}}}


def specimen():
    a = "2026-09-20T14:00:00Z"
    b = "2026-10-20T14:00:00Z"
    return {"schema": "dogram.temporal-return/specimen-v0", "specimen_id": "fixture-001",
            "encounters": [
                {"encounterId": "enc-a", "anchor": anchor(), "instant_utc": a,
                 "temporalWitness": packet(a, 11, 10)},
                {"encounterId": "enc-b", "anchor": anchor(), "instant_utc": b,
                 "temporalWitness": packet(b, 13, 10)},
            ]}


def test_different_encounters_same_anchor_selected_changed_axis():
    r = compare_temporal_return(specimen())
    assert r["status"] == "OK" and r["encounter_refs"] == ["enc-a", "enc-b"]
    assert r["coordinate_comparison"]["chinese_solar_sector"]["status"] == "changed_coordinate"
    assert r["coordinate_comparison"]["hindu_tithi"]["status"] == "same_coordinate"
    assert r["elapsed_microseconds"] > 0
    assert r["witness_digests"][0] != r["witness_digests"][1]
    assert r["input_digest"].startswith("sha256:")


def test_absent_witness_does_not_become_agreement():
    sample = specimen()
    sample["encounters"][1]["temporalWitness"] = None
    r = compare_temporal_return(sample)
    assert all(c["status"] == "unavailable" for c in r["coordinate_comparison"].values())
    assert r["witness_digests"][1] is None


def test_separately_declared_sidereal_conventions_do_not_mix():
    sample = specimen()
    sample["encounters"][1]["temporalWitness"]["ayanamsa"]["degrees"] = 25
    r = compare_temporal_return(sample)
    assert r["coordinate_comparison"]["hindu_nakshatra"]["status"] == "incomparable_sidereal_convention"
    assert r["coordinate_comparison"]["hindu_tithi"]["status"] == "same_coordinate"


def test_rejects_occurrence_timestamp_mismatch():
    sample = specimen()
    sample["encounters"][1]["temporalWitness"]["instant_utc"] = "2026-10-19T14:00:00Z"
    with pytest.raises(TemporalReturnError, match="witness instant") as exc:
        compare_temporal_return(sample)
    assert exc.value.code == "TIMESTAMP_MISMATCH"


def test_rejects_same_id_and_changed_anchor():
    sample = specimen()
    sample["encounters"][1]["encounterId"] = "enc-a"
    with pytest.raises(TemporalReturnError) as exc:
        compare_temporal_return(sample)
    assert exc.value.code == "DUPLICATE_OCCURRENCE"
    sample = specimen()
    sample["encounters"][1]["anchor"]["scriptureRef"]["verse"] = 2
    with pytest.raises(TemporalReturnError) as exc:
        compare_temporal_return(sample)
    assert exc.value.code == "ANCHOR_MISMATCH"


def test_rejects_invalid_coordinate():
    sample = specimen()
    sample["encounters"][1]["temporalWitness"]["hindu_angular"]["tithi"] = 31
    with pytest.raises(TemporalReturnError) as exc:
        compare_temporal_return(sample)
    assert exc.value.code == "INVALID_COORDINATE"


def test_rejects_wrong_frame_and_backward_time():
    sample = specimen()
    sample["encounters"][1]["temporalWitness"]["provider"]["coordinate_frame"] = "topocentric"
    r = compare_temporal_return(sample)
    assert r["coordinate_comparison"]["chinese_solar_sector"]["status"] == "incomparable_frame"
    sample = specimen()
    sample["encounters"].reverse()
    with pytest.raises(TemporalReturnError) as exc:
        compare_temporal_return(sample)
    assert exc.value.code == "REVERSED_TIME"


def test_distinct_source_witnesses_same_scripture_address():
    sample = specimen()
    sample["encounters"][1]["anchor"]["sourceRef"] = "urn:fixture:second-selection"
    result = compare_temporal_return(sample)
    assert result["same_source_ref"] is False
    assert result["source_anchors"][0]["sourceRef"] != result["source_anchors"][1]["sourceRef"]
    assert result["shared_scripture_ref"]["verse"] == 1
