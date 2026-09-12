import json
from pathlib import Path
import unittest

from dogram.path_tree_test_language import (
    adjacency_matrix,
    branching_star_hom_count,
    homomorphism_count,
    path_recurrence_certificate,
    total_walk_counts,
)


FIXTURE = Path(__file__).parent / "fixtures" / "path_tree_test_language_001.json"


class PathTreeTestLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.left = adjacency_matrix(
            cls.fixture["left"]["vertex_count"], cls.fixture["left"]["edges"]
        )
        cls.right = adjacency_matrix(
            cls.fixture["right"]["vertex_count"], cls.fixture["right"]["edges"]
        )
        cls.source = adjacency_matrix(
            cls.fixture["branching_source"]["vertex_count"],
            cls.fixture["branching_source"]["edges"],
        )
        cls.expected = cls.fixture["expected"]

    def test_all_path_counts_share_the_same_recurrence_certificate(self):
        expected = self.expected["path_walk_counts_0_through_8"]
        self.assertEqual(total_walk_counts(self.left, 8), expected)
        self.assertEqual(total_walk_counts(self.right, 8), expected)

        left_certificate = path_recurrence_certificate(self.left, 2)
        right_certificate = path_recurrence_certificate(self.right, 2)
        self.assertTrue(left_certificate["valid"])
        self.assertTrue(right_certificate["valid"])
        self.assertEqual(left_certificate["vertex_count"], 7)
        self.assertEqual(right_certificate["vertex_count"], 7)
        self.assertEqual(left_certificate["first_walk_count"], 12)
        self.assertEqual(right_certificate["first_walk_count"], 12)
        self.assertEqual(left_certificate["eigenvalue"], 2)
        self.assertEqual(right_certificate["eigenvalue"], 2)

    def test_first_branching_tree_separates_the_same_carriers(self):
        left_star = branching_star_hom_count(self.left, 3)
        right_star = branching_star_hom_count(self.right, 3)
        self.assertEqual(left_star, self.expected["left_K1_3_hom_count"])
        self.assertEqual(right_star, self.expected["right_K1_3_hom_count"])
        self.assertEqual(right_star - left_star, self.expected["branching_delta"])

        self.assertEqual(homomorphism_count(self.source, self.left), left_star)
        self.assertEqual(homomorphism_count(self.source, self.right), right_star)

    def test_degree_receipt_explains_the_branching_delta(self):
        self.assertEqual(
            [sum(row) for row in self.left], self.expected["left_degrees"]
        )
        self.assertEqual(
            [sum(row) for row in self.right], self.expected["right_degrees"]
        )
        self.assertEqual(sum(value ** 3 for value in self.expected["left_degrees"]), 48)
        self.assertEqual(sum(value ** 3 for value in self.expected["right_degrees"]), 54)


if __name__ == "__main__":
    unittest.main()
