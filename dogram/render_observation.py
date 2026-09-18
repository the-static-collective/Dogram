"""Finite decoded-pixel observations; experimental, not a public operator.

No decoder, renderer, filesystem or process capability enters this module.
Sampling and quantization can hide differences. No perceptual claim is made.
"""

from fractions import Fraction
from hashlib import sha256

from .engine import evaluate_specimen

CELL_ORDER = ("00", "01", "10", "11")
SAMPLER = {
    "id": "gray32x18-6fps-q16/v0",
    "width": 32,
    "height": 18,
    "fps": 6,
    "pixel_format": "gray",
    "quantization_step": 16,
    "filter": "fps=6,scale=32:18:flags=area,format=gray",
}


def scalar(value):
    exact = Fraction(value)
    if exact.denominator == 1:
        return {"kind": "integer", "value": exact.numerator}
    return {"kind": "rational", "numerator": exact.numerator, "denominator": exact.denominator}


def observe_frames(data: bytes, *, width=32, height=18):
    """Measure all supplied fixed-size grayscale frames, keeping exact fractions."""
    if type(width) is not int or width <= 0 or width % 2 or type(height) is not int or height <= 0:
        raise ValueError("positive dimensions and an even width are required")
    size = width * height
    if not isinstance(data, bytes) or len(data) % size or len(data) < 2 * size:
        raise ValueError("at least two complete grayscale frames are required")
    frames = [data[i:i + size] for i in range(0, len(data), size)]
    quantized = [bytes(pixel // 16 for pixel in frame) for frame in frames]
    total_change = sum(abs(a - b) for left, right in zip(frames, frames[1:]) for a, b in zip(left, right))
    states = set()
    for frame in frames:
        left = sum(frame[row * width + col] for row in range(height) for col in range(width // 2))
        right = sum(frame[row * width + col] for row in range(height) for col in range(width // 2, width))
        states.add((left // (size // 2 * 16), right // (size // 2 * 16)))
    period = next((lag for lag in range(1, len(frames) // 2 + 1)
                   if all(quantized[i] == quantized[i - lag] for i in range(lag, len(frames)))), None)
    unique = len(set(quantized))
    return {
        "frame_count": len(frames),
        "width": width,
        "height": height,
        "quantization_step": 16,
        "temporal_change": scalar(Fraction(total_change, (len(frames) - 1) * size * 255)),
        "unique_quantized_frames": unique,
        "duplicate_fraction": scalar(Fraction(len(frames) - unique, len(frames))),
        "quantized_frame_sha256": [sha256(frame).hexdigest() for frame in quantized],
        "visited_split_luma_states": [list(state) for state in sorted(states)],
        "split_luma_state_capacity": 256,
        "split_luma_coverage": scalar(Fraction(len(states), 256)),
        "smallest_sampled_period": period,
    }


def compare_observations(cells, experiment_id, axis_a, axis_b):
    if set(cells) != set(CELL_ORDER):
        raise ValueError("exactly four named cells 00,01,10,11 are required")
    geometry = {(c["frame_count"], c["width"], c["height"], c["quantization_step"]) for c in cells.values()}
    if len(geometry) != 1:
        raise ValueError("all cells must have the same sample count and geometry")
    comparisons = {}
    for metric in ("temporal_change", "duplicate_fraction", "split_luma_coverage"):
        specimen = {
            "schema": "dogram.specimen/v0",
            "specimen_id": f"{experiment_id}:{metric}",
            "operator": "rectangle",
            "operator_version": 1,
            "inputs": {"axis_a": axis_a, "axis_b": axis_b,
                       "cells": {key: cells[key][metric] for key in CELL_ORDER}},
            "assumptions": ["Finite sampled-pixel comparison only; no artistic or causal verdict."],
            "metadata": {"adapter": "toaster-paired-render/v0", "metric": metric},
        }
        comparisons[metric] = {"specimen": specimen, "receipt": evaluate_specimen(specimen)}
    return comparisons
