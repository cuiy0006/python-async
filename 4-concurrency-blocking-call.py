#!/usr/bin/env python3

import time
import queue

def task(name, queue):
    while not queue.empty():
        delay = queue.get()
        print(f'Task {name} running')
        start_time = time.time()
        time.sleep(delay)
        end_time = time.time() - start_time
        print(f'Task {name} elaspsed time: {end_time:.2f}')
        yield

def main():
    '''
    This is the main entry point for the program
    '''
    # Create the queue of work
    work_queue = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    tasks = [task('One', work_queue), task('Two', work_queue)]

    # Run the tasks
    done = False
    start_time = time.time()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True
    end_time = time.time() - start_time
    print(f'Total elapsed time: {end_time:.2f}')

if __name__ == '__main__':
    main()