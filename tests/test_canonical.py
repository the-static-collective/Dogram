import unittest

from dogram.canonical import canonical_json_bytes, sha256_json


class CanonicalTests(unittest.TestCase):
    def test_object_key_order_does_not_change_bytes(self):
        a = {"b": 2, "a": 1}
        b = {"a": 1, "b": 2}
        self.assertEqual(canonical_json_bytes(a), canonical_json_bytes(b))
        self.assertEqual(sha256_json(a), sha256_json(b))

    def test_canonical_json_has_no_incidental_whitespace(self):
        self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')


if __name__ == "__main__":
    unittest.main()
