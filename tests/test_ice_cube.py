from __future__ import annotations

import hashlib
import unittest

from dogram.ice_cube import (
    FAMILY,
    SCHEMA,
    challenge_coordinates,
    fibonacci_matrix_power,
    halley_iterate,
    lucas,
    verify_ice_cube,
    work_address,
)


def period_terms(z: complex, c: complex, period: int):
    value = z
    d1 = 1 + 0j
    d2 = 0 + 0j
    for _ in range(period):
        d2 = 2 * (d1 * d1 + value * d2)
        d1 = 2 * value * d1
        value = value * value + c
    return value - z, d1 - 1, d2


def pixel_for(work, x, y):
    render = work["render"]
    width = int(render["width"])
    height = int(render["height"])
    xmin = float(render["xmin"])
    xmax = float(render["xmax"])
    ymin = float(render["ymin"])
    ymax = float(render["ymax"])
    max_iter = int(render["max_halley_iter"])
    tolerance = float(work["halley"]["tolerance"])
    period = int(work["period"])
    c = complex(float(work["c"]["re"]), float(work["c"]["im"]))
    re = xmin + (xmax - xmin) * x / (width - 1)
    im = ymax - (ymax - ymin) * y / (height - 1)
    z = complex(re, im)
    used = max_iter
    for step in range(max_iter + 1):
        g, g1, g2 = period_terms(z, c, period)
        if abs(g) <= tolerance:
            used = step
            break
        if step == max_iter:
            break
        denominator = 2 * g1 * g1 - g * g2
        if abs(denominator) < 1e-30:
            break
        z = z - 2 * g * g1 / denominator
    return max(0, min(255, 255 - round(255 * used / max_iter)))


def specimen_fixture():
    work = {
        "kind": "ghot.ice-cube-work",
        "version": "0",
        "family": FAMILY,
        "lucas_index": 2,
        "period": 3,
        "c": {"re": "0", "im": "0"},
        "halley": {"tolerance": "1e-9"},
        "render": {
            "width": 9,
            "height": 9,
            "xmin": "-1.2",
            "xmax": "1.2",
            "ymin": "-1.2",
            "ymax": "1.2",
            "max_halley_iter": 10,
        },
    }
    pixels = bytearray()
    for y in range(9):
        for x in range(9):
            pixels.append(pixel_for(work, x, y))
    render_bytes = b"P5\n9 9\n255\n" + bytes(pixels)

    matrix = fibonacci_matrix_power(4)
    trace = matrix[0][0] + matrix[1][1]
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    fiber_count = 72
    shift = trace % fiber_count
    from math import gcd
    components = gcd(fiber_count, shift)

    witnesses = []
    c = 0j
    for z0 in (0.1 + 0.05j, -0.1 + 0.05j, 0.2 - 0.1j):
        final = halley_iterate(z0, c, 3, 8)
        witnesses.append({
            "z0": {"re": format(z0.real, ".17g"), "im": format(z0.imag, ".17g")},
            "steps": 8,
            "final": {"re": format(final.real, ".17g"), "im": format(final.imag, ".17g")},
        })

    challenges = [
        {"x": x, "y": y, "value": pixels[y * 9 + x]}
        for x, y in challenge_coordinates(work, 8)
    ]

    specimen = {
        "schema": SCHEMA,
        "specimen_id": "fixture-ice-cube-001",
        "family": FAMILY,
        "work": work,
        "work_address": work_address(work),
        "lucas_value": lucas(2),
        "monodromy": {
            "power": 4,
            "matrix": [list(matrix[0]), list(matrix[1])],
            "trace": trace,
            "determinant": det,
        },
        "mapping_torus": {
            "fiber_count": fiber_count,
            "shift": shift,
            "normalized_shift": shift % fiber_count,
            "components": components,
            "orbit_length": fiber_count // components,
        },
        "halley_witnesses": witnesses,
        "render": {
            "address": "sha256:" + hashlib.sha256(render_bytes).hexdigest(),
            "challenge_count": 8,
            "pixel_challenges": challenges,
        },
    }
    return specimen, render_bytes


class IceCubeTests(unittest.TestCase):
    def test_lucas_and_monodromy_are_exact(self):
        self.assertEqual([lucas(i) for i in range(7)], [2, 1, 3, 4, 7, 11, 18])
        matrix = fibonacci_matrix_power(10)
        self.assertEqual(matrix, ((89, 55), (55, 34)))
        self.assertEqual(matrix[0][0] + matrix[1][1], 123)
        self.assertEqual(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0], 1)

    def test_fixture_verifies_math_and_projection_without_full_rerender(self):
        specimen, render_bytes = specimen_fixture()
        receipt = verify_ice_cube(specimen, render_bytes)
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(receipt["result"]["pixel_challenges_verified"], 8)
        self.assertEqual(receipt["result"]["halley_witnesses_verified"], 3)
        self.assertEqual(receipt["result"]["claim_scope"], "bounded-math-and-projection-witness/v0")

    def test_mutated_lucas_claim_is_refused(self):
        specimen, render_bytes = specimen_fixture()
        specimen["lucas_value"] = 999
        receipt = verify_ice_cube(specimen, render_bytes)
        self.assertEqual(receipt["status"], "REFUSED")

    def test_mutated_render_is_refused(self):
        specimen, render_bytes = specimen_fixture()
        damaged = render_bytes[:-1] + bytes([render_bytes[-1] ^ 0xFF])
        receipt = verify_ice_cube(specimen, damaged)
        self.assertEqual(receipt["status"], "REFUSED")


if __name__ == "__main__":
    unittest.main()
