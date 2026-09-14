import unittest

from dogram.petri_incidence_concurrency import (
    frozen_specimen,
    incidence_matrix,
    reachable_labeled_edges,
    fire_sequence,
    step_enabled,
)


class PetriIncidenceConcurrencyTests(unittest.TestCase):
    def test_same_incidence_and_same_sequential_reachability(self):
        specimen = frozen_specimen()
        parallel = specimen["parallel"]
        mutex = specimen["mutex"]

        self.assertEqual(incidence_matrix(parallel), incidence_matrix(mutex))
        self.assertEqual(
            reachable_labeled_edges(parallel),
            reachable_labeled_edges(mutex),
        )

    def test_both_interleavings_reach_the_same_final_marking_in_both_nets(self):
        specimen = frozen_specimen()
        expected_final = specimen["final_marking"]

        for net in (specimen["parallel"], specimen["mutex"]):
            self.assertEqual(fire_sequence(net, ("a", "b")), expected_final)
            self.assertEqual(fire_sequence(net, ("b", "a")), expected_final)

    def test_joint_step_separates_parallel_from_shared_resource_net(self):
        specimen = frozen_specimen()
        initial = specimen["initial_marking"]

        self.assertTrue(step_enabled(specimen["parallel"], initial, ("a", "b")))
        self.assertFalse(step_enabled(specimen["mutex"], initial, ("a", "b")))

    def test_shared_self_loop_is_invisible_to_incidence_but_visible_to_preconditions(self):
        specimen = frozen_specimen()
        parallel = specimen["parallel"]
        mutex = specimen["mutex"]

        self.assertEqual(parallel["pre"]["guard"], {"a": 0, "b": 0})
        self.assertEqual(parallel["post"]["guard"], {"a": 0, "b": 0})
        self.assertEqual(mutex["pre"]["guard"], {"a": 1, "b": 1})
        self.assertEqual(mutex["post"]["guard"], {"a": 1, "b": 1})
        self.assertEqual(
            incidence_matrix(parallel)["guard"],
            incidence_matrix(mutex)["guard"],
        )


if __name__ == "__main__":
    unittest.main()
