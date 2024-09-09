#!/usr/bin/env python3
""" Redis Cache Class with Call Counting and Call History """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    redis = method.__self__._redis  # Access the Redis instance from the method
    key = method.__qualname__  # Qualified name of the method

    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    # Get input and output lists from Redis
    inputs = redis.lrange(input_key, 0, -1)
    outputs = redis.lrange(output_key, 0, -1)

    # Display call history
    print(f"{key} was called {len(inputs)} times:")
    for input_value, output_value in zip(inputs, outputs):
        input_str = input_value.decode("utf-8")
        output_str = output_value.decode("utf-8")
        print(f"{key}(*{input_str}) -> {output_str}")


class Cache:
    """Cache class to interact with Redis"""

    def __init__(self):
        """Initialize the Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random key."""
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data with the key
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis and optionally apply a transformation."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis."""
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis."""
        return self.get(key, fn=int)
