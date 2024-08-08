#!/usr/bin/python3
"""
    BaseCache module
"""


from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache define a LRU algorithm to use cache

      To use:
      >>> my_cache = BasicCache()
      >>> my_cache.print_cache()
      Current cache:

      >>> my_cache.put("A", "Hello")
      >>> my_cache.print_cache()
      A: Hello

      Ex:
      >>> my_cache.print_cache()
      Current cache:
      A: Hello
      B: World
      C: Holberton
      D: School
      >>> print(my_cache.get("B"))
      World
      >>> my_cache.put("E", "Battery")
      DISCARD: A
      >>> my_cache.print_cache()
      Current cache:
      B: World
      C: Holberton
      D: School
      E: Battery
    """
    AGE = 0
    AGE_BITS = {}

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
        if (len(self.cache_data.items()) == BaseCaching.MAX_ITEMS):
            if (key not in self.cache_data.keys()):
                leastItem = {
                    k: v for k, v in sorted(self.AGE_BITS.items(),
                                            key=lambda item: item[1])
                }
                leastItem = list(leastItem)[0]
                print("DISCARD:", leastItem)
                self.cache_data.pop(leastItem)
                self.AGE_BITS.pop(leastItem)

        self.cache_data[key] = item
        self.AGE += 1
        self.AGE_BITS[key] = self.AGE

    def get(self, key):
        """
            modify cache data

            Args:
                key: of the dict

            Return:
                value of the key
        """
        if key not in self.cache_data.keys():
            return None
        else:
            self.AGE += 1
            self.AGE_BITS[key] = self.AGE
            return self.cache_data[key]
