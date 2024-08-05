#!/usr/bin/env python3
'''
Test file for printing the correct output of the wait_random coroutine
'''
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random

print(asyncio.run(wait_random()))
print(asyncio.run(wait_random(5)))
print(asyncio.run(wait_random(15)))
