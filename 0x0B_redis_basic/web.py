#!/usr/bin/env python3
""" Expiring web cache and tracker """

import redis
import requests
from typing import Callable

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """ Decorator to count how many times a URL is accessed """

    def wrapper(*args, **kwargs):
        url = args[0]
        # Increment the count for the URL
        r.incr(f"count:{url}")
        return method(*args, **kwargs)

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ Fetches the content of a URL and caches it """
    cached_page = r.get(f"cached:{url}")
    if cached_page:
        return cached_page.decode('utf-8')

    # Fetch the page if not cached
    response = requests.get(url)
    html_content = response.text

    # Cache the result for 10 seconds
    r.setex(f"cached:{url}", 10, html_content)

    return html_content


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(f"URL accessed {r.get(f'count:{url}').decode('utf-8')} times")
