#!/usr/bin/env python3
""" Redis Cache Class """
import redis
import uuid
from typing import Union


class Cache:
    """Cache class to interact with Redis"""

    def __init__(self):
        """Initialize the Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The randomly generated key.
        """
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data with the key
        return key
