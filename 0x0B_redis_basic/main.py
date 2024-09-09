#!/usr/bin/env python3
""" Test Cache call counting """
from exercise import Cache

cache = Cache()

# Test storing data and incrementing call count
cache.store(b"first")
print(cache.get(cache.store.__qualname__))  # Should print '1'

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))  # Should print '3'
