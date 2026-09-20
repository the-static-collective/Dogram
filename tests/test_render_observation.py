import unittest

from dogram.render_observation import observe_frames, compare_observations


class RenderObservationTests(unittest.TestCase):
    def frames(self, *values):
        return b"".join(bytes([v]) * 8 for v in values)

    def observe(self, *values):
        return observe_frames(self.frames(*values), width=4, height=2)

    def test_static_and_alternating_controls(self):
        static = self.observe(0, 0, 0, 0)
        alternating = self.observe(0, 255, 0, 255)
        self.assertEqual(static["temporal_change"], {"kind": "integer", "value": 0})
        self.assertEqual(alternating["temporal_change"], {"kind": "integer", "value": 1})
        self.assertEqual(static["smallest_sampled_period"], 1)
        self.assertEqual(alternating["smallest_sampled_period"], 2)
        self.assertEqual(alternating["visited_split_luma_states"], [[0, 0], [15, 15]])
        self.assertEqual(alternating["split_luma_state_capacity"], 256)

    def test_repeat_requires_two_cycles_and_all_retained_samples(self):
        self.assertIsNone(self.observe(0, 50, 100, 150)["smallest_sampled_period"])
        self.assertIsNone(self.observe(0, 255, 0, 255, 100)["smallest_sampled_period"])

    def test_quantization_loss_is_explicit_and_raw_change_survives(self):
        result = self.observe(1, 2, 1, 2)
        self.assertEqual(result["unique_quantized_frames"], 1)
        self.assertEqual(result["temporal_change"], {"kind": "rational", "numerator": 1, "denominator": 255})

    def test_hostile_empty_partial_and_one_frame_inputs(self):
        for data in (b"", bytes(8), bytes(17)):
            with self.assertRaises(ValueError):
                observe_frames(data, width=4, height=2)
        for width in (0, 3, True):
            with self.assertRaises(ValueError):
                observe_frames(bytes(32), width=width, height=2)

    def test_exact_rectangle_and_noop_axis_control(self):
        zero = self.observe(0, 0, 0, 0)
        change = self.observe(0, 255, 0, 255)
        cells = {"00": zero, "01": zero, "10": zero, "11": change}
        result = compare_observations(cells, "fixture", "motion", "camera")
        self.assertEqual(result["temporal_change"]["receipt"]["result"]["mixed_delta"], {"kind": "integer", "value": 1})
        result = compare_observations({"00": zero, "01": zero, "10": change, "11": change}, "fixture", "motion", "camera")
        self.assertFalse(result["temporal_change"]["receipt"]["result"]["interaction_detected"])

    def test_unbalanced_or_incomplete_cells_refuse(self):
        cells = {key: self.observe(0, 255) for key in ("00", "01", "10", "11")}
        cells["11"] = self.observe(0, 255, 0)
        with self.assertRaises(ValueError):
            compare_observations(cells, "fixture", "a", "b")
        del cells["11"]
        with self.assertRaises(ValueError):
            compare_observations(cells, "fixture", "a", "b")
