#!/usr/bin/env python3
from functools import wraps
from typing import Callable
import requests
import redis

redis_client = redis.Redis()


def cache(expirration: Callable) -> Callable:
    """A decorator that caches the result of a function with a Redis backend.

    Args:
        expiration (int): The expiration time of the cache in seconds.

    Returns:
        Callable: A decorated function that caches its result.
    """
    @wraps(expirration)
    def wrapper(func: callable) -> str:
        """The actual caching decorator.

        Args:
            func (callable): The function to cache.

        Returns:
            str:  A wrapper function that caches the result of func.
        """
        # increment the count of how many times this func has been requested
        redis_client.incr('count:{}'.format(func))
        # get the cached result for this func
        result = redis_client.get('result:{}'.format(func))
        # if there is a cached result, return it
        if result:
            return result.decode('utf-8')
        # if there is no cached result, fetch the data and cache it
        result = expirration(func)
        redis_client.set('count:{}'.format(func), 0)
        # set the result to expire after 10 seconds
        redis_client.setex('result:{}'.format(func), 10, result)
        return result
    # return the wrapped function
    return wrapper


@cache()
def get_page(url: str) -> str:
    """Retrieves the HTML content of a URL.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
