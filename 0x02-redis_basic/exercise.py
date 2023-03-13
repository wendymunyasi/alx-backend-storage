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
from typing import Union, Optional, Callable


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

    def get(self, key: str, fn:
            Optional[Callable[[bytes], Union[str, bytes, int, float]]] = None)\
            -> Union[str, bytes, int, float, None]:
        """Method to get data from Redis and optionally apply a conversion
        function to the retrieved data.

        Args:
            key (str): The key used to store the data in Redis.
            fn (Optional): An optional callable that is used to convert the
            retrieved data to the desired format. Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted to the desired format.
        """
        # get the data from Redis
        data = self._redis.get(key)
        # if the key is not in Redis, return None
        if data is None:
            return None
        # if a conversion function is provided, apply it to the data
        if fn is not None:
            data = fn(data)
        # return the data
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Method to get a string from Redis.

        Args:
            key: The key used to store the string in Redis.

        Returns:
            Optional[str]: The retrieved string or None if the key does not
            exist.
        """
        # use get with a conversion function to retrieve a string
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Method to get an integer from Redis.

        Args:
            key: The key used to store the integer in Redis.

        Returns:
            Optional[int]: The retrieved integer or None if the key does not
            exist.
        """
        # use get with a conversion function to retrieve an integer
        return self.get(key, lambda x: int(x))
