#!/usr/bin/env python3
"""
    Truncate float to integer
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
        Args:
            n: float number

        Return:
            Float number truncated to floor
    """

    result: float = 0

    cncat: Tuple(str, Union[int, float])
    cncat = (k, v**2)

    return cncat
