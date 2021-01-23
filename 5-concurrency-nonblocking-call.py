#!/usr/bin/env python3

import asyncio
import time

async def task(name, work_queue):
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f'Task {name} running')
        start_time = time.time()
        await asyncio.sleep(delay)
        end_time = time.time() - start_time
        print(f'Task {name} elaspsed time: {end_time:.2f}')

async def main():
    '''
    This is the main entry point for the program
    '''
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)
        

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