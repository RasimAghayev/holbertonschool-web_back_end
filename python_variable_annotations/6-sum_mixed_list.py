#!/usr/bin/env python3
"""
    Truncate float to integer
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
        Args:
            n: float number

        Return:
            Float number truncated to floor
    """

    result: float = 0

    for x in mxd_lst:
        result += x

    return result
