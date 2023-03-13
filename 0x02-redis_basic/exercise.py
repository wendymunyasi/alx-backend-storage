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
from functools import wraps
from typing import Any, Union, Optional, Callable


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs for a
    particular function in Redis.

    Args:
        method (Callable): A callable that represents the original
        function to be decorated.

    Returns:
        Callable: A new callable that wraps the original function
        and adds input and output history to Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ Wrapper function that adds input and output history to Redis.

        Returns:
            The output of the original function.
        """
        input_list_key = f"{method.__qualname__}:inputs"
        output_list_key = f"{method.__qualname__}:outputs"
        # Add the input arguments to the input list
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_list_key, str(args))
        # Execute the original function and store the output
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_list_key, output)
        # Return the output
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called.

    Args:
        method: The method to decorate.

    Returns:
        Callable: A decorated version of the method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function that adds input and output history to Redis.

        Returns:
            The output of the original function.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def replay(fn: callable) -> None:
    """Displays the history of calls of a particular function.

    Args:
        fn (callable): The function whose history of calls is to be
        displayed.

    Returns:
        None
    """
    # Check if the function is not None and has a __self__ attribute
    if fn is None or not hasattr(fn, '__self__'):
        return
    # Get the Redis instance associated with the function
    redis_store = getattr(fn.__self__, '_redis', None)
    # Check if the Redis instance is of the right type
    if not isinstance(redis_store, redis.Redis):
        return
    # Get the name of the function
    func_name = fn.__qualname__
    # Create keys for the input and output lists of the function
    input_list_key = "{}:inputs".format(func_name)
    output_list_key = "{}:outputs".format(func_name)
    # Get the number of times the function has been called
    func_call_count = 0
    if redis_store.exists(func_name) != 0:
        func_call_count = int(redis_store.get(func_name))
    # Print the history of calls
    print("{} was called {} times:".format(func_name, func_call_count))
    # Get the input and output lists from Redis
    inputs = redis_store.lrange(input_list_key, 0, -1)
    outputs = redis_store.lrange(output_list_key, 0, -1)
    # Print the input and output of each function call
    for inp, out in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            func_name,
            inp.decode("utf-8"),
            out,
        ))
    # Return None
    return None


class Cache:
    """Cache class.
    """

    def __init__(self):
        """Cache class constructor that initializes a Redis client instance
        and flushes the database with flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
