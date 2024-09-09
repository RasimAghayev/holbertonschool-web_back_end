#!/usr/bin/env python3
""" Test Cache call history and replay """
from exercise import Cache, replay

cache = Cache()

# Store values
cache.store("foo")
cache.store("bar")
cache.store(42)

# Replay the history of store method
replay(cache.store)
