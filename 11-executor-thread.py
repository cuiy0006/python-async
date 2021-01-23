#!/usr/bin/env python3

import asyncio
import concurrent.futures
import time
import random

def io_bound(n):
    start = time.perf_counter()
    i = random.randint(1, 10)
    time.sleep(i)
    end = time.perf_counter()
    print(f'Task {n} takes in {end-start:0.5f} seconds.')
    return n

async def run_blocking_tasks(executor):
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, io_bound, i)
        for i in range(6)
    ]

    res = await asyncio.gather(*blocking_tasks)
    print(f'Result: {res}')

if __name__ == '__main__':
    start = time.perf_counter()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    asyncio.run(run_blocking_tasks(executor))
    end = time.perf_counter()
    print(f'Total takes in {end-start:0.5f} seconds.')