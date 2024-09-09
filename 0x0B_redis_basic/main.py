#!/usr/bin/env python3
""" Test Cache class """
from exercise import Cache

cache = Cache()

# Define test cases
TEST_CASES = {
    b"foo": None,  # No conversion
    123: int,  # Convert back to int
    "bar": lambda d: d.decode("utf-8")  # Decode as UTF-8 string
}

for value, fn in TEST_CASES.items():
  key = cache.store(value)  # Store the value
  assert cache.get(key,
                   fn=fn) == value  # Test retrieval with optional conversion
