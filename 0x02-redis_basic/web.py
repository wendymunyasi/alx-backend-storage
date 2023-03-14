#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker
"""
import requests
import time
from functools import wraps

CACHE_EXPIRATION_TIME = 10  # seconds
CACHE = {}


def cache(fn):
    """_summary_

    Args:
        fn (function): _description_

    Returns:
        _type_: _description_
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        """_summary_

        Returns:
            _type_: _description_
        """
        url = args[0]
        if url in CACHE and CACHE[url]["timestamp"] + CACHE_EXPIRATION_TIME > \
                time.time():
            CACHE[url]["count"] += 1
            return CACHE[url]["content"]
        else:
            content = fn(*args, **kwargs)
            CACHE[url] = {"content": content,
                          "timestamp": time.time(), "count": 1}
            return content
    return wrapped


@cache
def get_page(url: str) -> str:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        str: _description_
    """
    global count
    # increment count
    count += 1
    response = requests.get(url)
    return response.content.decode('utf-8')
