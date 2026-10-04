from __future__ import annotations

import hashlib
import json
from typing import Any

from .mapping_torus import analyze_mapping_torus
from .receipt import ok_receipt, refusal_receipt


SCHEMA = "static.ice-cube-specimen/v0"
FAMILY = "lucas-halley-mandelbrot-mapping-torus/v0"
OPERATOR = "ICE_CUBE_VERIFY"
OPERATOR_VERSION = 0


def lucas(index: int) -> int:
    if not isinstance(index, int) or isinstance(index, bool) or index < 0:
        raise ValueError("lucas_index must be a non-negative integer")
    a, b = 2, 1
    if index == 0:
        return a
    for _ in range(1, index):
        a, b = b, a + b
    return b


def _mat_mul(a: tuple[tuple[int, int], tuple[int, int]], b: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ),
    )


def fibonacci_matrix_power(power: int) -> tuple[tuple[int, int], tuple[int, int]]:
    if not isinstance(power, int) or isinstance(power, bool) or power < 0:
        raise ValueError("monodromy_power must be a non-negative integer")
    result = ((1, 0), (0, 1))
    base = ((1, 1), (1, 0))
    n = power
    while n:
        if n & 1:
            result = _mat_mul(result, base)
        base = _mat_mul(base, base)
        n >>= 1
    return result


def _complex(value: Any, label: str) -> complex:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    try:
        return complex(float(str(value["re"])), float(str(value["im"])))
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{label} must contain numeric re/im") from exc


def _period_terms(z: complex, c: complex, period: int) -> tuple[complex, complex, complex]:
    value = z
    d1 = 1 + 0j
    d2 = 0 + 0j
    for _ in range(period):
        d2 = 2 * (d1 * d1 + value * d2)
        d1 = 2 * value * d1
        value = value * value + c
    return value - z, d1 - 1, d2


def halley_iterate(z: complex, c: complex, period: int, steps: int) -> complex:
    current = z
    for _ in range(steps):
        g, g1, g2 = _period_terms(current, c, period)
        denominator = 2 * g1 * g1 - g * g2
        if abs(denominator) < 1e-30:
            break
        current = current - (2 * g * g1) / denominator
    return current


def _residual(z: complex, c: complex, period: int) -> float:
    g, _g1, _g2 = _period_terms(z, c, period)
    return abs(g)


def canonical_work_bytes(work: dict[str, Any]) -> bytes:
    return json.dumps(
        work,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def work_address(work: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_work_bytes(work)).hexdigest()


def challenge_coordinates(work: dict[str, Any], count: int = 16) -> list[tuple[int, int]]:
    render = work["render"]
    width = int(render["width"])
    height = int(render["height"])
    if width <= 0 or height <= 0:
        raise ValueError("render dimensions must be positive")
    seed = hashlib.sha256(canonical_work_bytes(work)).digest()
    coords: list[tuple[int, int]] = []
    counter = 0
    while len(coords) < min(count, width * height):
        block = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
        x = int.from_bytes(block[:8], "big") % width
        y = int.from_bytes(block[8:16], "big") % height
        item = (x, y)
        if item not in coords:
            coords.append(item)
        counter += 1
    return coords


def _pixel_for(work: dict[str, Any], x: int, y: int) -> int:
    render = work["render"]
    width = int(render["width"])
    height = int(render["height"])
    xmin = float(str(render["xmin"]))
    xmax = float(str(render["xmax"]))
    ymin = float(str(render["ymin"]))
    ymax = float(str(render["ymax"]))
    max_iter = int(render["max_halley_iter"])
    tolerance = float(str(work["halley"]["tolerance"]))
    period = int(work["period"])
    c = _complex(work["c"], "work.c")

    re = xmin if width == 1 else xmin + (xmax - xmin) * x / (width - 1)
    im = ymin if height == 1 else ymax - (ymax - ymin) * y / (height - 1)
    z = complex(re, im)

    used = max_iter
    for step in range(max_iter + 1):
        if _residual(z, c, period) <= tolerance:
            used = step
            break
        if step == max_iter:
            break
        g, g1, g2 = _period_terms(z, c, period)
        denominator = 2 * g1 * g1 - g * g2
        if abs(denominator) < 1e-30:
            used = max_iter
            break
        z = z - (2 * g * g1) / denominator

    if max_iter <= 0:
        return 255
    return max(0, min(255, 255 - round(255 * used / max_iter)))


def _parse_pgm(render_bytes: bytes, width: int, height: int) -> bytes:
    prefix = f"P5\n{width} {height}\n255\n".encode("ascii")
    if not render_bytes.startswith(prefix):
        raise ValueError("render is not canonical P5 PGM for declared dimensions")
    pixels = render_bytes[len(prefix):]
    if len(pixels) != width * height:
        raise ValueError("render pixel count does not match declared dimensions")
    return pixels


def verify_ice_cube(specimen: dict[str, Any], render_bytes: bytes | None = None) -> dict[str, Any]:
    consumed = [
        "schema",
        "family",
        "work",
        "work_address",
        "lucas_value",
        "monodromy",
        "mapping_torus",
        "halley_witnesses",
        "render",
    ]
    try:
        if specimen.get("schema") != SCHEMA:
            raise ValueError("wrong specimen schema")
        if specimen.get("family") != FAMILY:
            raise ValueError("wrong specimen family")

        work = specimen.get("work")
        if not isinstance(work, dict):
            raise ValueError("work must be an object")
        expected_work_address = work_address(work)
        if specimen.get("work_address") != expected_work_address:
            raise ValueError("work address mismatch")

        index = int(work["lucas_index"])
        expected_lucas = lucas(index)
        if int(work["period"]) != expected_lucas:
            raise ValueError("period must equal L_n")
        if int(specimen["lucas_value"]) != expected_lucas:
            raise ValueError("claimed Lucas value mismatch")

        monodromy = specimen["monodromy"]
        power = int(monodromy["power"])
        if power != 2 * index:
            raise ValueError("monodromy power must be 2*n")
        expected_matrix = fibonacci_matrix_power(power)
        claimed_matrix = tuple(tuple(int(v) for v in row) for row in monodromy["matrix"])
        if claimed_matrix != expected_matrix:
            raise ValueError("monodromy matrix mismatch")
        trace = expected_matrix[0][0] + expected_matrix[1][1]
        determinant = expected_matrix[0][0] * expected_matrix[1][1] - expected_matrix[0][1] * expected_matrix[1][0]
        if trace != lucas(power):
            raise ValueError("matrix trace != Lucas(power)")
        if int(monodromy["trace"]) != trace or int(monodromy["determinant"]) != determinant:
            raise ValueError("monodromy invariant mismatch")
        if determinant != 1:
            raise ValueError("even Fibonacci monodromy must lie in SL(2,Z)")

        torus = specimen["mapping_torus"]
        fiber_count = int(torus["fiber_count"])
        shift = int(torus["shift"])
        if shift != trace % fiber_count:
            raise ValueError("finite torus shift must be trace mod fiber_count")
        analysis = analyze_mapping_torus(fiber_count, shift)
        for key, value in analysis.to_data().items():
            if int(torus[key]) != value:
                raise ValueError(f"mapping torus claim mismatch: {key}")

        c = _complex(work["c"], "work.c")
        period = int(work["period"])
        tolerance = float(str(work["halley"]["tolerance"]))
        max_residual = 0.0
        witnesses = specimen.get("halley_witnesses")
        if not isinstance(witnesses, list) or not witnesses:
            raise ValueError("at least one Halley witness is required")
        for witness in witnesses:
            z0 = _complex(witness["z0"], "witness.z0")
            claimed = _complex(witness["final"], "witness.final")
            steps = int(witness["steps"])
            replayed = halley_iterate(z0, c, period, steps)
            replay_delta = abs(replayed - claimed)
            residual = _residual(claimed, c, period)
            max_residual = max(max_residual, residual)
            if replay_delta > tolerance:
                raise ValueError("Halley replay mismatch")
            if residual > tolerance:
                raise ValueError("Halley witness does not satisfy periodic residual")

        render = specimen["render"]
        width = int(work["render"]["width"])
        height = int(work["render"]["height"])
        if render_bytes is None:
            raise ValueError("render bytes required for projection verification")
        digest = "sha256:" + hashlib.sha256(render_bytes).hexdigest()
        if render.get("address") != digest:
            raise ValueError("render address mismatch")
        pixels = _parse_pgm(render_bytes, width, height)

        expected_coords = challenge_coordinates(work, int(render["challenge_count"]))
        claims = render.get("pixel_challenges")
        if not isinstance(claims, list) or len(claims) != len(expected_coords):
            raise ValueError("pixel challenge count mismatch")
        for (x, y), claim in zip(expected_coords, claims):
            if int(claim["x"]) != x or int(claim["y"]) != y:
                raise ValueError("pixel challenge coordinate mismatch")
            actual = pixels[y * width + x]
            expected = _pixel_for(work, x, y)
            if int(claim["value"]) != actual or actual != expected:
                raise ValueError("pixel challenge failed")

        result = {
            "work_address": expected_work_address,
            "lucas_index": index,
            "lucas_value": expected_lucas,
            "period": period,
            "monodromy_power": power,
            "monodromy_trace": trace,
            "monodromy_determinant": determinant,
            "mapping_torus": analysis.to_data(),
            "halley_witnesses_verified": len(witnesses),
            "max_halley_residual": format(max_residual, ".17g"),
            "render_address": digest,
            "pixel_challenges_verified": len(expected_coords),
            "claim_scope": "bounded-math-and-projection-witness/v0",
        }
        return ok_receipt(specimen, OPERATOR, OPERATOR_VERSION, consumed, result)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return refusal_receipt(
            specimen,
            OPERATOR,
            OPERATOR_VERSION,
            "REFUSED",
            "ICE_CUBE_VERIFICATION_FAILED",
            [str(exc)],
            consumed,
        )


__all__ = [
    "FAMILY",
    "SCHEMA",
    "challenge_coordinates",
    "fibonacci_matrix_power",
    "halley_iterate",
    "lucas",
    "verify_ice_cube",
    "work_address",
]
