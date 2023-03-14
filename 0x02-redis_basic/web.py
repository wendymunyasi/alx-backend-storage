#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker
"""
from functools import wraps
from typing import Callable
import requests
import redis

redis_client = redis.Redis()

# Define a new function to handle expiration time for cached results
def expiration(time: int) -> Callable[[Callable], Callable]:
    """_summary_

    Args:
        time (int): _description_

    Returns:
        Callable[[Callable], Callable]: _description_
    """
    def decorator(func: Callable) -> Callable:
        """_summary_

        Args:
            func (Callable): _description_

        Returns:
            Callable: _description_
        """
        # Define a new wrapper function to apply the caching logic
        @wraps(func)
        def wrapper(*args, **kwargs):
            """_summary_

            Returns:
                _type_: _description_
            """
            # Generate a key based on the function name and arguments
            key = f'{func.__name__}:{args}:{kwargs}'
            # Check if the result is already cached
            result = redis_client.get(key)
            if result is not None:
                # If it is, return the cached result
                return result.decode('utf-8')
            else:
                # If it isn't, execute the function and cache the result
                result = func(*args, **kwargs)
                redis_client.setex(key, time, result)
                return result
        return wrapper
    return decorator

# Apply the cache decorator to the get_page function with a 10 second expiration time
@expiration(10)
def get_page(url: str) -> str:
    """Retrieves the HTML content of a URL.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The HTML content of the URL.
    """
    return requests.get(url).text
