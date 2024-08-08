#!/usr/bin/python3
"""
    BaseCache module
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict

class LFUCache(BaseCaching):
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

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.freq = defaultdict(int)  # Tracks frequency of use
        self.order = OrderedDict()    # Tracks the order of insertion and access

    def put(self, key, item):
        """
            modify cache data

            Args:
                key: of the dict
                item: value of the key
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update the existing item's frequency
            self.freq[key] += 1
        else:
            # New item, initialize frequency
            self.freq[key] = 1

        # If cache is full, remove the least frequently used item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if key not in self.cache_data:
                # Find the LFU item(s)
                min_freq = min(self.freq.values())
                lfu_keys = [k for k in self.freq if self.freq[k] == min_freq]

                if len(lfu_keys) > 1:
                    # More than one key with the same frequency, use LRU
                    lru_key = None
                    for k in self.order:
                        if k in lfu_keys:
                            lru_key = k
                            break
                    discard_key = lru_key
                else:
                    # Only one key with the minimum frequency
                    discard_key = lfu_keys[0]

                # Remove the least frequently used (or least recently used) item
                del self.cache_data[discard_key]
                del self.freq[discard_key]
                self.order.pop(discard_key)
                print(f"DISCARD: {discard_key}")

        # Insert/update the item in the cache
        self.cache_data[key] = item
        self.order[key] = True  # Update order of usage

        # Maintain the order for LRU by moving the item to the end
        self.order.move_to_end(key)

    def get(self, key):
        """
            modify cache data

            Args:
                key: of the dict

            Return:
                value of the key
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and usage order
        self.freq[key] += 1
        self.order.move_to_end(key)
        
        return self.cache_data[key]
