#!/usr/bin/env python3

import asyncio
import random
import time
import uuid

async def randsleep(caller) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f'{caller} sleeping for {i} seconds.')
    await asyncio.sleep(i)

async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in range(n + 1):
        await randsleep(f'Producer {name}')
        i = str(uuid.uuid4())
        t = time.perf_counter()
        await q.put((i, t))
        print(f'Producer {name} added <{i}> to queue.')

async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f'Consumer {name}')
        i, t = await q.get()
        now = time.perf_counter()
        print(f'Consumer {name} got element <{i}>'
              f' in {now-t:0.5f} seconds.')
        q.task_done()

async def main():
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(3)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(2)]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()

if __name__ == '__main__':
    random.seed(444)
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f'Program completed in {elapsed:0.5f} seconds.')