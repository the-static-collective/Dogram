import json
import unittest
from pathlib import Path

from dogram.delta import evaluate_delta
from dogram.rectangle import evaluate_rectangle


class VariationCubeTests(unittest.TestCase):
    def load(self):
        return json.loads(
            (Path(__file__).parent / "fixtures" / "variation" / "variation-cube-001.json").read_text()
        )

    @staticmethod
    def value(vertices, a, b, c):
        return vertices[f"{a}{b}{c}"]

    @staticmethod
    def delta(left, right, boundary):
        result, _ = evaluate_delta(
            {
                "boundary_order": [boundary],
                "left": {boundary: {"kind": "integer", "value": left}},
                "right": {boundary: {"kind": "integer", "value": right}},
            }
        )
        return result["comparisons"][0]["delta"]["value"]

    @staticmethod
    def rectangle(f00, f01, f10, f11, axis_a, axis_b):
        result, _ = evaluate_rectangle(
            {
                "axis_a": axis_a,
                "axis_b": axis_b,
                "cells": {
                    "00": {"kind": "integer", "value": f00},
                    "01": {"kind": "integer", "value": f01},
                    "10": {"kind": "integer", "value": f10},
                    "11": {"kind": "integer", "value": f11},
                },
            }
        )
        return result["mixed_delta"]["value"]

    def test_twelve_openings_lower_to_twelve_delta_evaluations(self):
        fixture = self.load()
        vertices = fixture["vertices"]
        observed = {"A": {}, "B": {}, "C": {}}

        for b in (0, 1):
            for c in (0, 1):
                key = f"{b}{c}"
                observed["A"][key] = self.delta(
                    self.value(vertices, 0, b, c),
                    self.value(vertices, 1, b, c),
                    "A",
                )

        for a in (0, 1):
            for c in (0, 1):
                key = f"{a}{c}"
                observed["B"][key] = self.delta(
                    self.value(vertices, a, 0, c),
                    self.value(vertices, a, 1, c),
                    "B",
                )

        for a in (0, 1):
            for b in (0, 1):
                key = f"{a}{b}"
                observed["C"][key] = self.delta(
                    self.value(vertices, a, b, 0),
                    self.value(vertices, a, b, 1),
                    "C",
                )

        self.assertEqual(observed, fixture["expected_first_differences"])
        self.assertEqual(sum(len(axis) for axis in observed.values()), 12)

    def test_face_rectangles_expose_pair_interactions(self):
        fixture = self.load()
        v = fixture["vertices"]

        observed = {
            "AB|C=0": self.rectangle(v["000"], v["010"], v["100"], v["110"], "A", "B"),
            "AB|C=1": self.rectangle(v["001"], v["011"], v["101"], v["111"], "A", "B"),
            "AC|B=0": self.rectangle(v["000"], v["001"], v["100"], v["101"], "A", "C"),
            "AC|B=1": self.rectangle(v["010"], v["011"], v["110"], v["111"], "A", "C"),
            "BC|A=0": self.rectangle(v["000"], v["001"], v["010"], v["011"], "B", "C"),
            "BC|A=1": self.rectangle(v["100"], v["101"], v["110"], v["111"], "B", "C"),
        }

        self.assertEqual(observed, fixture["expected_pair_interactions"])
        self.assertEqual(len(observed), 6)

    def test_three_independent_face_paths_recover_same_whole_residual(self):
        fixture = self.load()
        pair = fixture["expected_pair_interactions"]

        residuals = {
            "AB_then_C": self.delta(pair["AB|C=0"], pair["AB|C=1"], "C"),
            "AC_then_B": self.delta(pair["AC|B=0"], pair["AC|B=1"], "B"),
            "BC_then_A": self.delta(pair["BC|A=0"], pair["BC|A=1"], "A"),
        }

        self.assertEqual(
            residuals,
            {
                "AB_then_C": fixture["expected_whole_residual"],
                "AC_then_B": fixture["expected_whole_residual"],
                "BC_then_A": fixture["expected_whole_residual"],
            },
        )
