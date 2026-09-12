import json
from fractions import Fraction
from pathlib import Path
import unittest

from dogram.signed_affine_intertwiner import (
    adjacency_matrix,
    degree_transport,
    has_negative_entry,
    isolate_nonnegative_obstruction,
    is_affine_intertwiner,
    total_walk_counts,
)


FIXTURE = Path(__file__).parent / "fixtures" / "signed_affine_intertwiner_001.json"


def parse_fraction_matrix(rows):
    return [[Fraction(value) for value in row] for row in rows]


class SignedAffineIntertwinerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.left = adjacency_matrix(
            cls.fixture["left"]["vertex_count"], cls.fixture["left"]["edges"]
        )
        cls.right = adjacency_matrix(
            cls.fixture["right"]["vertex_count"], cls.fixture["right"]["edges"]
        )
        cls.witness = parse_fraction_matrix(cls.fixture["signed_witness"])

    def test_signed_affine_intertwiner_is_exact(self):
        self.assertTrue(is_affine_intertwiner(self.left, self.witness, self.right))
        self.assertTrue(has_negative_entry(self.witness))

        left_degree, transported_degree = degree_transport(
            self.left, self.witness, self.right
        )
        self.assertEqual(left_degree, transported_degree)
        self.assertEqual(
            [int(value) for value in left_degree],
            self.fixture["expected"]["left_degrees"],
        )

    def test_nonnegative_fractional_witness_is_impossible(self):
        obstruction = isolate_nonnegative_obstruction(self.left, self.right)
        self.assertEqual(obstruction["isolated_left_vertices"], [6])
        self.assertEqual(obstruction["right_min_degree"], 1)
        self.assertTrue(obstruction["nonnegative_row_stochastic_impossible"])

    def test_path_walk_receipt_collides_through_frozen_depth(self):
        left_counts = total_walk_counts(self.left, 8)
        right_counts = total_walk_counts(self.right, 8)
        expected = [Fraction(value) for value in self.fixture["expected"]["walk_counts_0_through_8"]]
        self.assertEqual(left_counts, expected)
        self.assertEqual(right_counts, expected)


if __name__ == "__main__":
    unittest.main()
