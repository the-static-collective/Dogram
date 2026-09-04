import unittest

from dogram.cohomologous_associator_gauge import (
    associator,
    coboundary,
    shifted_associator,
    cocycle_residuals,
    normalized_2cochains_matching,
    table_delta,
)


class CohomologousAssociatorGaugeTests(unittest.TestCase):
    def test_shifted_associator_is_pointwise_different_but_differs_by_declared_coboundary(self):
        delta = table_delta()
        self.assertEqual(
            delta,
            {
                (1, 1, 2): 2,
                (1, 2, 2): 1,
                (2, 1, 1): 1,
                (2, 2, 1): 2,
            },
        )
        for triple, value in delta.items():
            self.assertEqual(value, coboundary(*triple))
            self.assertEqual(
                shifted_associator(*triple),
                (associator(*triple) + value) % 3,
            )

    def test_both_associator_tables_are_normalized_3cocycles(self):
        for cochain in (associator, shifted_associator):
            self.assertEqual(set(cocycle_residuals(cochain).values()), {0})
            for g in range(3):
                for h in range(3):
                    for k in range(3):
                        if 0 in (g, h, k):
                            self.assertEqual(cochain(g, h, k), 0)

    def test_base_associator_is_not_a_normalized_2cochain_coboundary(self):
        matches = normalized_2cochains_matching(associator)
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
