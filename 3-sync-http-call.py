#!/usr/bin/env python3

import queue
import requests
import time
 
def task(name, work_queue):
    with requests.Session() as session:
        while not work_queue.empty():
            url = work_queue.get()
            print(f'Task {name} getting URL: {url}')
            start_time = time.time()
            session.get(url)
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
    for url in [
        'http://google.com',
        'http://yahoo.com',
        'http://linkedin.com',
        'http://apple.com',
        'http://microsoft.com',
        'http://facebook.com',
        'http://twitter.com',
    ]:
        work_queue.put(url)

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