import unittest

from dogram.mazurkiewicz_trace_quotient import (
    frozen_specimen,
    parikh_vector,
    trace_class,
    trace_partition,
)


class MazurkiewiczTraceQuotientTests(unittest.TestCase):
    def test_same_linear_language_and_same_parikh_surface(self):
        specimen = frozen_specimen()
        words = specimen["words"]

        self.assertEqual(words, ("ab", "ba"))
        self.assertEqual(parikh_vector("ab"), parikh_vector("ba"))

    def test_parallel_independence_collapses_the_two_interleavings(self):
        specimen = frozen_specimen()
        independence = specimen["parallel_independence"]

        self.assertEqual(trace_class("ab", independence), frozenset({"ab", "ba"}))
        self.assertEqual(
            trace_partition(specimen["words"], independence),
            (frozenset({"ab", "ba"}),),
        )

    def test_ordered_control_keeps_the_same_words_as_distinct_traces(self):
        specimen = frozen_specimen()
        independence = specimen["ordered_independence"]

        self.assertEqual(trace_class("ab", independence), frozenset({"ab"}))
        self.assertEqual(
            trace_partition(specimen["words"], independence),
            (frozenset({"ab"}), frozenset({"ba"})),
        )

    def test_independence_relation_is_the_only_declared_delta(self):
        specimen = frozen_specimen()

        self.assertEqual(specimen["alphabet"], ("a", "b"))
        self.assertEqual(specimen["words"], ("ab", "ba"))
        self.assertEqual(specimen["ordered_independence"], frozenset())
        self.assertEqual(
            specimen["parallel_independence"],
            frozenset({("a", "b"), ("b", "a")}),
        )


if __name__ == "__main__":
    unittest.main()
