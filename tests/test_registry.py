import unittest

from dogram.registry import RegistryLookupError, build_bootstrap_registry


class RegistryTests(unittest.TestCase):
    def test_unknown_intrinsic_is_not_resolved(self):
        registry = build_bootstrap_registry()
        with self.assertRaises(RegistryLookupError):
            registry.resolve("host.eval@1")

    def test_registry_contains_exact_bootstrap_floor(self):
        registry = build_bootstrap_registry()
        self.assertEqual(
            set(registry.ids()),
            {
                "core.get@1",
                "core.same@1",
                "core.add@1",
                "core.sub@1",
                "core.length@1",
                "core.gt@1",
                "core.select_first@1",
                "trace.compare_ordered@1",
                "graph.apply_mutation@1",
                "graph.reachable_pairs@1",
                "graph.query_paths@1",
                "set.difference@1",
            },
        )

    def test_registry_resolves_callable_without_exposing_it_as_data(self):
        registry = build_bootstrap_registry()
        intrinsic = registry.resolve("core.same@1")
        self.assertTrue(callable(intrinsic))
        self.assertNotIn("callable", registry.describe("core.same@1"))


if __name__ == "__main__":
    unittest.main()
