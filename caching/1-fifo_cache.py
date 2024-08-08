#!/usr/bin/python3
"""
    BaseCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache define a FIFO algorithm to use cache

      To use:
      >>> my_cache = BasicCache()
      >>> my_cache.print_cache()
      Current cache:

      >>> my_cache.put("A", "Hello")
      >>> my_cache.print_cache()
      A: Hello

      >>> print(my_cache.get("A"))
      Hello

      Ex:
      >>> print(self.cache_data)
      {A: "Hello", B: "World", C: "Holberton", D: "School"}
      >>> my_cache.put("C", "Street")
      >>> print(self.cache_data)
      {A: "Hello", B: "World", C: "Street", D: "School"}

      >>> my_cache.put("F", "COD")
      DISCARD: A
      >>> print(self.cache_data)
      {F: "COD", B: "World", C: "Holberton", D: "School"}
    """

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()

    def put(self, key, item):
        """
            modify cache data

            Args:
                key: of the dict
                item: value of the key
        """

        if key is None or item is None:
            return
        if (
            len(self.cache_data.items()) == BaseCaching.MAX_ITEMS
            and (key not in self.cache_data.keys())
        ):
            firstItem = list(self.cache_data)[0]
            print("DISCARD:", firstItem)
            self.cache_data.pop(firstItem)
        self.cache_data[key] = item

    def get(self, key):
        """
            modify cache data

            Args:
                key: of the dict

            Return:
                value of the key
        """

        valuecache = self.cache_data.get(key)
        return valuecache
