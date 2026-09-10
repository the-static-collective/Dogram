from fractions import Fraction
import unittest

from dogram.split_exact_section_fiber import (
    difference_of_sections,
    is_kernel_vector,
    project,
    section,
)


class SplitExactSectionFiberTests(unittest.TestCase):
    def test_each_declared_section_is_a_right_inverse(self):
        for c in (Fraction(0), Fraction(1), Fraction(2), Fraction(-3, 5)):
            for q in (Fraction(0), Fraction(3, 2), Fraction(-7, 3)):
                self.assertEqual(project(section(c, q)), q)

    def test_same_quotient_value_has_distinct_lifts(self):
        q = Fraction(3, 2)
        lifts = {section(c, q) for c in (Fraction(0), Fraction(1), Fraction(2))}
        self.assertEqual(len(lifts), 3)
        self.assertEqual({project(v) for v in lifts}, {q})

    def test_difference_of_sections_lands_in_kernel(self):
        q = Fraction(5, 4)
        delta = difference_of_sections(Fraction(2), Fraction(-1), q)
        self.assertEqual(delta, (Fraction(0), Fraction(15, 4)))
        self.assertTrue(is_kernel_vector(delta))

    def test_section_parameter_is_recoverable_from_linear_lift_of_one(self):
        for c in (Fraction(-2), Fraction(0), Fraction(7, 3)):
            lift_of_one = section(c, Fraction(1))
            self.assertEqual(lift_of_one[0], Fraction(1))
            self.assertEqual(lift_of_one[1], c)


if __name__ == "__main__":
    unittest.main()
