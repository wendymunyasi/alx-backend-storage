#!/usr/bin/env python3
from functools import wraps
import time
from typing import Callable
import requests
import redis

redis_client = redis.Redis()


def cache(expirration: int) -> Callable:
    """A decorator that caches the result of a function with a Redis backend.

    Args:
        expiration (int): The expiration time of the cache in seconds.

    Returns:
        Callable: A decorated function that caches its result.
    """
    @wraps(expirration)
    def wrapper(func: callable) -> Callable:
        """The actual caching decorator.

        Args:
            func (callable): The function to cache.

        Returns:
            Callable:  A wrapper function that caches the result of func.
        """
        def inner(url: str) -> str:
            """The wrapper function that caches the result of func.

            Args:
                url (str): The URL to retrieve.

            Returns:
                str: The cached HTML content of the URL, if available;
                otherwise, the result of func.
            """
            cache_key = "cache:{}".format(url)
            # Check if the result is cached and not expired
            if redis_client.exists(cache_key) and time.time() \
                    - float(redis_client.hget(cache_key,
                                              'timestamp')) < expirration:
                # Cache hit: return the cached content
                print("Cache hit for URL: {}".format(url))
                return redis_client.hget(cache_key, 'content').decode('utf-8')
            else:
                # Cache miss: retrieve the result from the function & cache it
                print("Cache miss for URL: {}".format(url))
                # call the original function to get the result
                content = func(url)
                # cache the result
                redis_client.hmset(
                    cache_key, {'timestamp': time.time(), 'content': content})
                # set the expiration time
                redis_client.expire(cache_key, expirration)
                return content
        return inner
    return wrapper


@cache(expiration=10)
def get_page(url: str) -> str:
    """Retrieves the HTML content of a URL.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
