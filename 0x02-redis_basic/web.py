#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker
"""
from functools import wraps
from typing import Callable
import requests
import redis

redis_client = redis.Redis()


def cache(expiration: int) -> Callable:
    """_summary_

    Args:
        expiration (int): _description_

    Returns:
        Callable: _description_
    """
    def decorator(func: Callable) -> Callable:
        """_summary_

        Args:
            func (Callable): _description_

        Returns:
            Callable: _description_
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            """_summary_

            Returns:
                str: _description_
            """
            key = f"{func.__name__}:{args}:{kwargs}"
            redis_client.incr(f"count:{key}")
            result = redis_client.get(f"result:{key}")
            if result:
                return result.decode("utf-8")
            result = func(*args, **kwargs)
            redis_client.setex(f"result:{key}", expiration, result)
            return result
        return wrapper
    return decorator


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
        @wraps(func)
        def wrapper(*args, **kwargs):
            """sumary_line

            Keyword arguments:
            argument -- description
            Return: return_description
            """

            # Generate a key based on the function name and arguments
            key = f'{func.__name__}:{args}:{kwargs}'
            # Check if the result is already cached
            result = redis_client.get(key)
            if result is not None:
                # If it is, return the cached result
                return result.decode('utf-8')
            else:
                # If it isn't, execute the function and cache the result with
                # expiration time
                result = func(*args, **kwargs)
                redis_client.setex(key, time, result)
                return result
        return wrapper
    return decorator


@cache
@expiration(10)
def get_page(url: str) -> str:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        str: _description_
    """
    return requests.get(url).text
