#!/usr/bin/env python3

import asyncio
import aiohttp
import time

async def task(name, work_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Task {name} getting URL: {url}')
            start_time = time.time()
            async with session.get(url) as response:
                await response.text()
            end_time = time.time() - start_time
            print(f'Task {name} elaspsed time: {end_time:.2f}')

async def main():
    '''
    This is the main entry point for the program
    '''
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for url in [
        'http://google.com',
        'http://yahoo.com',
        'http://linkedin.com',
        'http://apple.com',
        'http://microsoft.com',
        'http://facebook.com',
        'http://twitter.com',
    ]:
        await work_queue.put(url)

    # Run the tasks
    start_time = time.time()
    await asyncio.gather(
        asyncio.create_task(task('One', work_queue)),
        asyncio.create_task(task('Two', work_queue)),
    )
    end_time = time.time() - start_time
    print(f'Total elapsed time: {end_time:.2f}')

if __name__ == '__main__':
    asyncio.run(main())