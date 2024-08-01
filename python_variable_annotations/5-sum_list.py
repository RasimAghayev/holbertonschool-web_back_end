#!/usr/bin/env python3
"""
    Truncate float to integer
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
        Args:
            n: float number

        Return:
            Float number truncated to floor
    """

    result: float = 0

    for x in input_list:
        result += x

    return result
