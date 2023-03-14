#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker
"""
from functools import wraps
from typing import Callable
import requests
import redis

redis_client = redis.Redis()

def cache(func: Callable) -> Callable:
    """_summary_

    Args:
        func (Callable): _description_

    Returns:
        Callable: _description_
    """
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
            redis_client.set(key, result)
            return result
    return wrapper

def expiration(time: int) -> Callable[[Callable], Callable]:
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
                # If it isn't, execute the function and cache the result with expiration time
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
    response = requests.get(url)
    return response.text
