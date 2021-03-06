#!/usr/bin/env python3

import asyncio
import concurrent.futures
import time
import random

def calculate_pi(terms):
    total = 0
    sign = 1

    for i in range(terms):
        term = 1.0 / (i * 2 + 1)
        total += sign * term
        sign = sign * (-1)

    return total * 4

def cpu_bound(n):
    start = time.perf_counter()
    i = random.randint(6, 7)
    calculate_pi(10 ** i)
    end = time.perf_counter()
    print(f'Task {n} takes in {end-start:0.5f} seconds.')
    return n

async def run_blocking_tasks(executor):
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, cpu_bound, i)
        for i in range(6)
    ]

    res = await asyncio.gather(*blocking_tasks)
    print(f'Result: {res}')

if __name__ == '__main__':
    start = time.perf_counter()
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=3)
    asyncio.run(run_blocking_tasks(executor))
    end = time.perf_counter()
    print(f'Total takes in {end-start:0.5f} seconds.')