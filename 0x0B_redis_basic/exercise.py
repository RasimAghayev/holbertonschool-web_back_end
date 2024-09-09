#!/usr/bin/env python3
""" Redis Cache Class with Data Retrieval """
import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis and optionally apply a transformation.

        Args:
            key (str): The key of the data to retrieve.
            fn (Callable, optional): A function to apply to the data. Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The data stored in Redis, optionally transformed.
        """
        data = self._redis.get(key)  # Get the data from Redis
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[str]: The retrieved string, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[int]: The retrieved integer, or None if the key does not exist.
        """
        return self.get(key, fn=int)
