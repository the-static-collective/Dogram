import unittest
from fractions import Fraction

from dogram.values import ValueDecodeError, compare_values, decode_value, encode_value


class ValueTests(unittest.TestCase):
    def test_decode_rational_is_exact(self):
        value = decode_value({"kind": "rational", "numerator": 1, "denominator": 3})
        self.assertEqual(value.value, Fraction(1, 3))

    def test_encode_rational_is_canonical(self):
        value = decode_value({"kind": "rational", "numerator": 2, "denominator": 6})
        self.assertEqual(encode_value(value), {"kind": "rational", "numerator": 1, "denominator": 3})

    def test_opaque_comparison_never_emits_numeric_delta(self):
        left = decode_value({"kind": "opaque", "value": "a"})
        right = decode_value({"kind": "opaque", "value": "b"})
        self.assertEqual(compare_values(left, right), {"relation": "DIFFERENT"})

    def test_exact_numeric_comparison_emits_exact_delta(self):
        left = decode_value({"kind": "rational", "numerator": 1, "denominator": 3})
        right = decode_value({"kind": "integer", "value": 1})
        self.assertEqual(compare_values(left, right), {"relation": "DIFFERENT", "delta": {"kind": "rational", "numerator": 2, "denominator": 3}})

    def test_zero_denominator_refuses_decode(self):
        with self.assertRaises(ValueDecodeError):
            decode_value({"kind": "rational", "numerator": 1, "denominator": 0})


if __name__ == "__main__":
    unittest.main()
