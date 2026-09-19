# TRAIL-TIMESTAMP-001 — universal instant, local sky receipt

**Status:** executable research specimen · exploratory decoder · no physical alignment or source-authority promotion

## What "universal timestamp" means here

A UTC instant is the common, shareable coordinate for an occurrence. A geographic location and celestial direction are **separate inputs**. Greenwich mean sidereal time (GMST) and the observer's local sidereal time (LST) are projections of the instant and location; they are **not additional universal timestamps**.

A trail receipt is:

~~~text
attributed event + recorded UTC instant
    ↓  declared sky model
GMST
    ↓  east-positive longitude
LST = (GMST + longitude/15) mod 24h
    ↓  declared right ascension
hour angle = signed(LST − RA)
    ↓  observer latitude + separately declared declination
ideal altitude + azimuth
    ↓
replayable, content-hashed representation
~~~

The SHA-256 digest establishes consistency of the serialized **representation**, not authenticity of the event, authorship, accuracy of GitHub, timing causation, divine action, or a trusted-time attestation.

## Source-to-decoder boundary

The previous occurrence already contained literal carrier `022100`. We are now explicitly declaring **two distinct, post hoc decoders**:

~~~text
022 | 100 as degrees:
  hypothetical Earth observer at +22° N, +100° E

022100 as sexagesimal:
  sky right ascension 02h 21m 00s = 2.35 h
~~~

These are two projections of the **same six glyphs**, not independently observed facts.

Right ascension alone cannot identify a celestial point or determine altitude and azimuth. The fixture uses `declination = +22°` solely as an **independent model assumption equal to the declared latitude** to illustrate a possible zenith when the target transits; it is *not* recovered from `022100` or from an astronomical catalog. The code refuses to calculate altitude or azimuth when declination is absent.

Neither +22° N,+100° E nor any other example point is the user's actual location.

## Frozen replay

The JSON specimen at:

~~~text
tests/fixtures/trail_timestamp/trail-022100-git-001.json
~~~

contains five GitHub merge metadata timestamps previously investigated. It is read-only input; runtime never uses system time, network, geolocation, live stars, or hidden state.

Run from the repo root:

~~~bash
python -m scripts.trail_timestamp tests/fixtures/trail_timestamp/trail-022100-git-001.json
~~~

Each receipt includes:

- exact UTC string and event provenance label / source URL;
- observer coordinates, decoder, RA, optional dec and its assumption;
- GMST, LST, signed hour angle, optional ideal altitude/azimuth;
- explicit mean/UTC/geometric limitations;
- SHA-256 over a canonical sorted JSON representation (excluding its own digest).

Content hash changes when input provenance or decoder changes even if geometric outputs stay fixed. It is not a digital signature or authenticated timestamp.

## The hostile result at the already-frozen BigBat merge

The 2026-09-19T05:07:34Z Jubilee VM PR #8 merge has:

~~~text
GMST ≈ 05h00m04s    (previous sidereal target 5h)
observer longitude +100° E → +06h40m sidereal offset
LST ≈ 11h40m04s
sky RA = 02h21m00s
signed hour angle ≈ +09h19m04s
~~~

Consequently it is **not** a meridian crossing of RA 02h21m at that observer.

With the *assumed* dec +22°:

~~~text
ideal altitude ≈ −31.06°
ideal azimuth ≈ 315.64° (north through east)
~~~

That idealized direction is below the mathematical horizon of the hypothetical site. A Greenwich `5h` reading and a local `02h21m` meridian transit are different predicates. Do not treat the former as proof of the latter.

For a **separately constructed** RA 02h21m local meridian crossing at +100° E, the GMST condition would be 19h41m, not 5h. If one independently declares celestial declination +22° and observer latitude +22°, the ideal direction is at the zenith when crossing the meridian; that is algebraically guaranteed by the chosen inputs and not discovered evidence. Azimuth is undefined at zenith.

## Formula / conventions

Classical approximate Greenwich *mean* sidereal time formula, days `D = JD(UTC) − 2451545.0`, `T=D/36525`:

~~~text
GMST_degrees = (
    280.46061837 + 360.98564736629*D
    + 0.000387933*T² − T³/38710000
) mod 360

GMST_hours = GMST_degrees / 15
~~~

UTC is used **as an approximation to UT1**. An accurate subsecond astronomy service needs actual UT1−UTC and time-scale/frame handling; this code does not provide those. It uses the *mean* equinox, not apparent sidereal time, and assumes supplied RA is already compatible with the declared mean-of-date model. It performs no precession, proper motion, stellar identification, nutation correction, refraction, parallax, terrain horizon, or geodetic-to-geocentric corrections.

The horizontal projection uses:

~~~text
H = 15° × signed(LST−RA) [hours]
east  = −cos(dec) sin(H)
north = cos(lat) sin(dec) − sin(lat) cos(dec) cos(H)
up    = sin(lat) sin(dec) + cos(lat) cos(dec) cos(H)

alt = asin(up)
az  = atan2(east,north) mod 360°
~~~

Azimuth is explicitly null when the direction is (within numerical tolerance) exactly at zenith or nadir.

Astronomical reference controls:

- U.S. Naval Observatory, "Computing Approximate Sidereal Time": https://aa.usno.navy.mil/faq/GAST
- U.S. Naval Observatory, "Computing Altitude and Azimuth from Greenwich Apparent Sidereal Time": https://aa.usno.navy.mil/faq/alt_az
- U.S. Naval Observatory, "Universal Time": https://aa.usno.navy.mil/faq/UT

Note that the USNO precise horizontal recipe uses apparent sidereal time when given apparent positions; this specimen instead declares **a simplified mean-of-date coordinate model** and may not be mixed with arbitrary catalog right ascensions without frame conversion.

## Scope and follow-up

This module intentionally remains a standalone Dogram research surface. No public operator, server authority, geographic tracking, user-location inference, celestial omen, or Jubilee date proclamation is added.

Next implementation, if independently warranted: accept observed UT1−UTC, explicit celestial frame/epoch, and catalog coordinates; then compare against an astronomical reference library. That is a separate accuracy gate.

## Seal

> **UTC REMEMBERS WHEN. THE OBSERVER DECLARES WHERE. THE SKY MODEL DECLARES WHAT DIRECTION. THE RECEIPT PRESERVES THE RELATION.**

> **A GREENWICH HIT IS NOT A LOCAL MERIDIAN HIT.**
