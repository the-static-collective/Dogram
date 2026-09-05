# ORBIT-AUDIO-INVERSE-001

Status: bounded research specimen. No public operator.

## Question

If orbital motion is translated into a family of tones by one declared linear scale, how much of the orbital structure can be recovered from the sound carrier?

For the frozen five-planet mean-motion specimen: enough to recover the declared planet assignment from frequency ratios alone, but not enough to recover absolute periods without the global scale.

## Historical aperture

Laurie Spiegel describes her Voyager realization of Kepler's *Music of the Spheres* as "simply a translation into sound of the angular velocities of the planets" and calls it a transcription rather than a composition. She also notes that orchestration, mixing, pacing, and the choice of planets were artistic decisions.

Source: New Music USA, *Laurie Spiegel: Grassroots Technologist*:
https://newmusicusa.org/nmbx/laurie-spiegel-grassroots-technologist/

This specimen does **not** claim to reproduce Spiegel's exact Bell Labs transform. It isolates one explicit invertible toy decoder so the information boundary can be measured before touching the historical audio.

## Frozen carrier

Use the five planets represented in the fixture:

- Mercury: `87.97` days;
- Venus: `224.70` days;
- Earth: `365.26` days;
- Mars: `686.98` days;
- Jupiter: `4332.71` days.

Source: NASA GSFC StarChild Solar System Data:
https://starchild.gsfc.nasa.gov/docs/StarChild/teachers/orbiting.html

Declare a simple sonification

`f_i = K / T_i`,

where `T_i` is sidereal orbital period in days and `K > 0` is a shared pitch calibration in Hz-days.

The fixture chooses

`K = 238299.05 Hz-days`,

so Jupiter lands at `55 Hz` and all five control tones are positive.

## Exact inverse with declared scale

If `K` is known,

`T_i = K / f_i`.

The frozen tones recover all five frozen periods to floating-point tolerance.

Therefore:

`DECLARED SCALE + TONE != ORBITAL HISTORY`,

but for this declared transform,

`DECLARED SCALE + TONE -> DECLARED MEAN PERIOD`.

## Scale-free inverse

If `K` is unknown, pairwise ratios cancel it:

`f_i / f_j = T_j / T_i`.

Equivalently, for a proposed label assignment each tone-period pair implies a scale sample

`K_i = f_i T_i`.

The finite decoder checks all label permutations and selects the assignment whose `K_i` values agree most closely under one shared scale. The exact frozen carrier recovers the scrambled order

`Earth, Mercury, Jupiter, Mars, Venus`

with maximum relative scale residue below `1e-12`.

This gives the central mathal:

`GLOBAL PITCH SCALE IS GAUGE FOR THE RATIO SIGNATURE.`

and:

`SAME FREQUENCY-RATIO SIGNATURE != SAME ABSOLUTE CALIBRATION.`

## Hostile controls

### Global pitch shift

Multiply every observed frequency by `1.75`.

The recovered planet assignment is unchanged and the residue remains numerical zero, but the estimated global scale also multiplies by `1.75`.

Thus:

`COMMON TRANSPOSITION PRESERVES RELATIVE ORBIT SIGNATURE WHILE CHANGING ABSOLUTE DECODER SCALE.`

### One-tone perturbation

Increase only the first scrambled tone by `1%`.

The same label assignment remains the best finite match, but the common-scale residue becomes nonzero (about `0.008`). The kernel retains that disagreement instead of rounding it into exact equivalence.

Thus:

`BEST MATCH != EXACT MATCH.`

and:

`RESIDUAL MUST SURVIVE DECODING.`

## Dogram pressure

Documented mathematics:
- a shared multiplicative scale cancels from pairwise tone ratios;
- known `K` makes the declared map `f=K/T` exactly invertible for positive values;
- unknown `K` leaves one positive scalar degree of freedom;
- one independently perturbed tone breaks common-scale coherence.

Dogram inference:
- relative structure can survive a carrier after absolute calibration is lost;
- decoder calibration belongs in the receipt rather than being silently reconstructed;
- a carrier can preserve enough relational structure to identify a declared finite model without preserving the model's absolute units;
- reconstruction quality needs an explicit residue rather than a binary match flag.

Speculation / HOLD:
- whether the actual Voyager *Music of the Spheres* carrier preserves a recoverable orbital signature under Spiegel's historical transform is not established here;
- whether a sufficiently alien receiver would choose the same planetary model, tone extraction, units, or matching criterion is not established here;
- no claim is made that musical structure is universally intelligible.

## Explicit refusals

- `TONE != PLANET`;
- `FREQUENCY RATIO != PHYSICAL IDENTITY`;
- `BEST FINITE ASSIGNMENT != HISTORICAL DECODING`;
- `MEAN MOTION != INSTANTANEOUS ANGULAR VELOCITY`;
- `SYNTHETIC INVERTIBILITY != VOYAGER AUDIO INVERTIBILITY`;
- `COMMON SCALE != UNIVERSAL MUSICAL KEY`;
- `STRUCTURAL RECOVERY != SEMANTIC UNDERSTANDING`.

## HOLD

No `orbit_audio_inverse@1`, `sonification@1`, `planet_identity@1`, FFT/audio dependency, CLI/schema dispatch, or public operator promotion.

## Strongest next frontier

Move from the synthetic mean-motion carrier to the historical transformation without pretending they are the same object.

1. Obtain a provenance-clean copy of the Voyager *Music of the Spheres* sound carrier.
2. Receipt the recording format and any transcoding.
3. Extract time-varying frequency ridges without assigning planet labels first.
4. Replace the mean-period toy model with declared Keplerian instantaneous angular-velocity tracks over the historical time window.
5. Ask whether any single time scale, pitch scale, octave folding, and label permutation explains the observed ridges within an explicit residual budget.

The target question is not "can we hear the planets?" It is:

`HOW MUCH OF THE DECLARED WORLD SURVIVES AN UNKNOWN CARRIER TRANSFORM, AND WHICH DECODER ASSUMPTIONS ARE REQUIRED TO GET IT BACK?`
