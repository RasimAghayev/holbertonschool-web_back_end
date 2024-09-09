#!/usr/bin/env python3
""" Test Cache call history """
from exercise import Cache

cache = Cache()

# Store values
s1 = cache.store("first")
print(s1)  # Should print the generated key
s2 = cache.store("secont")
print(s2)  # Should print the generated key
s3 = cache.store("third")
print(s3)  # Should print the generated key

# Retrieve input and output history
inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

print("inputs: {}".format(inputs))  # Should print a list of inputs
print("outputs: {}".format(outputs))  # Should print a list of outputs
