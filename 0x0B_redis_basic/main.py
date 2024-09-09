#!/usr/bin/env python3
""" Test Cache class """
import redis
from exercise import Cache

cache = Cache()

# Test storing data
data = b"hello"
key = cache.store(data)
print(key)

# Verify the data is correctly stored in Redis
local_redis = redis.Redis()
print(local_redis.get(key))  # Should output: b'hello'
