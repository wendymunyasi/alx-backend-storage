#!/usr/bin/env python3
"""Module for task 0

Create a Cache class. In the __init__ method, store an instance of the
Redis client as a private variable named _redis (using redis.Redis()) and
flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the input
data in Redis using the random key and return the key.
"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class.
    """
    def __init__(self):
        """Cache class constructor that initializes a Redis client instance
        and flushes the database with flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method to store data in Redis and return a key for the stored
        data.

        Args:
            data (Union[str, bytes, int, float]): The data to store. Can
            be a str, bytes, int, or float.

        Returns:
            str: A randomly generated key that can be used to retrieve
            the stored data.
        """
        # generate a random key using uuid
        key = str(uuid.uuid4())
        # store the data in Redis using the key
        self._redis.set(key, data)
        # return the key
        return key
