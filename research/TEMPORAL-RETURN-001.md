# TEMPORAL-RETURN-001 — two encounters, one Scripture coordinate, independently sourced clocks

**Status:** EXPERIMENTAL / callable Python kernel / not a public Dogram operator. This file describes an independent math-only consumer for the optional Upper Room wire packet and CLOCKWORK-002 observational projection. Nothing is connected to live Upper Room reading, publishing, monitoring or the HOUSE effect runtime.

## The one narrow crossing

```text
Upper Room: participant selects two separate encounter references
    -> opt-in, source-preserving JSON projection
CLOCKWORK-002: optional precomputed read-only UTC astronomical packets
    -> explicitly attached, same exact UTC instant as the encounter
Dogram: compare_temporal_return(specimen)
    -> typed comparison and content-addressed input/witness digests
    -> interpretation remains with the human/Upper Room/ALEX
```

The *same Scripture coordinate* is required; distinct `sourceRef` identities and distinct `encounterId` identities are preserved. A repeated verse is not a repeated encounter. The caller owns proof that either encounter or temporal packet actually happened; this kernel cannot authenticate sources or consent.

### Wire schema `dogram.temporal-return/specimen-v0`

```json
{
  "schema": "dogram.temporal-return/specimen-v0",
  "specimen_id": "fixture-001",
  "encounters": [
    {
      "encounterId": "first",
      "anchor": {
        "sourceRef": "fixture:first-selection",
        "scriptureRef": {"translationId": "engwebp", "book": "John", "chapter": 1, "verse": 1}
      },
      "instant_utc": "2026-09-20T14:00:00Z",
      "temporalWitness": null
    },
    {
      "encounterId": "second",
      "anchor": {
        "sourceRef": "fixture:second-selection",
        "scriptureRef": {"translationId": "engwebp", "book": "John", "chapter": 1, "verse": 1}
      },
      "instant_utc": "2026-10-20T14:00:00Z",
      "temporalWitness": null
    }
  ]
}
```

This JSON is deliberately synthetic and has no personally identifying data or claim to be a historical occurrence. To run a one-off comparison without installing anything new:

```bash
python - <<'PY'
from dogram.temporal_return import compare_temporal_return
import json
with open("examples/temporal_return_001.json", encoding="utf-8") as handle:
    receipt = compare_temporal_return(json.load(handle))
print(json.dumps(receipt, indent=2, ensure_ascii=False))
PY
```

Either temporalWitness can be `null`; a missing packet produces `unavailable` for all compared axes, never agreement or evidence of absence. CLOCKWORK-002 packets, when present, must match their encounter instant exactly and identify `kind`, coordinate frame and, for sidereal axes, a named ayanamsa convention. The ayanamsa **value** may change between epochs within the same named convention. Different frames or named conventions produce `incomparable_*` rather than forced comparisons.

The comparison covers only Chinese solar-term **sector index**; Hindu tithi, nakshatra and yoga indices; and karana half-tithi **position**. These are instantaneous angles, not local religious calendar days, sunrise, observational certainty, a Chinese lunar mansion, a biblical Jubilee, or a physical causal relation. No event is assigned a calendar position from an abstract 60/64 tick count. No user-authored Bible text is imported or redistributed.

The returned receipt includes the full input digest and per-packet digest; it does **not** certify them, introduce a public registry operator, persist anything, mutate a graph, or supply theological interpretations. The `OK` status means only that the declared calculation completed.

## Pressure and follow-up

Frozen tests check source identity preservation; distinct events at the same address; missing packet; mismatched instant; mismatched Scripture ref; incompatible frames; different named sidereal conventions; evolving offset within one convention; and invalid angular indices. Run `pytest -q tests/test_temporal_return.py`.

Next, make one real CLOCKWORK-002 sample from a independently sourced local BSP ephemeris and verify it against external astronomy. Only then expose a manually invoked Upper Room computation lens and allow a source-backed, participant-controlled encounter-to-receipt exchange. Real local Hindu and Hebrew day boundaries require observer-specific sunrise/sunset modeling.
