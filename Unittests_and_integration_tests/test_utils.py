#!/usr/bin/env python3
"""Unit test
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """ Access nested map """

    @parameterized.expand([
        ({
            "a": 1
        }, ("a", ), 1),
        ({
            "a": {
                "b": 2
            }
        }, ("a", ), {
            "b": 2
        }),
        ({
            "a": {
                "b": 2
            }
        }, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Access nested method

            args:
                nested_map: {"a": 1},
                path: ("a",)
                result_expec: 1

            return
                Ok if its correct
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
