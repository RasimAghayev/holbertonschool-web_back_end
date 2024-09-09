#!/usr/bin/env python3
""" Redis Cache Class with Call Counting and Call History """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to increment the call count in Redis."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with history tracking.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to store function call history in Redis."""
        # Qualified name of the method
        key = method.__qualname__
        # Store inputs
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        # Convert input arguments to string and push to Redis
        self._redis.rpush(input_key, str(args))

        # Execute the original method and capture the output
        result = method(self, *args, **kwargs)

        # Store the result (output) in Redis
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


class Cache:
    """Cache class to interact with Redis"""

    def __init__(self):
        """Initialize the Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
        data = self._redis.get(key)
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
