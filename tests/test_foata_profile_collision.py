import unittest

from dogram.foata_profile_collision import (
    foata_layers,
    frozen_specimen,
    layer_size_profile,
    parikh_vector,
    trace_class,
)


class FoataProfileCollisionTests(unittest.TestCase):
    def test_same_alphabet_independence_and_parikh_surface(self):
        s = frozen_specimen()
        self.assertEqual(parikh_vector(s["left_word"]), parikh_vector(s["right_word"]))
        self.assertEqual(parikh_vector(s["left_word"]), (("a", 1), ("b", 1), ("c", 1), ("d", 1)))

    def test_words_are_trace_inequivalent(self):
        s = frozen_specimen()
        left = trace_class(s["left_word"], s["independence"])
        right = trace_class(s["right_word"], s["independence"])
        self.assertEqual(left, frozenset({"abcd", "bacd"}))
        self.assertEqual(right, frozenset({"abdc", "badc"}))
        self.assertTrue(left.isdisjoint(right))

    def test_full_foata_layers_separate_the_traces(self):
        s = frozen_specimen()
        self.assertEqual(foata_layers(s["left_word"], s["independence"]), (("a", "b"), ("c",), ("d",)))
        self.assertEqual(foata_layers(s["right_word"], s["independence"]), (("a", "b"), ("d",), ("c",)))

    def test_layer_size_profile_collides(self):
        s = frozen_specimen()
        self.assertEqual(layer_size_profile(s["left_word"], s["independence"]), (2, 1, 1))
        self.assertEqual(layer_size_profile(s["right_word"], s["independence"]), (2, 1, 1))


if __name__ == "__main__":
    unittest.main()
