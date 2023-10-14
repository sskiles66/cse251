"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import queue
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 3

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function

def read_func(queue:mp.Queue):

    with open('data.txt', 'r') as f:

        lines = f.readlines()
        for line in lines:
            queue.put(line.strip())
    print("done")
    queue.put("stop")

# TODO create prime_process function

def process_func(queue:mp.Queue, data):
    while True:
        element = queue.get()
        if (element == "stop"):
            print("Stooped")
            queue.put("stop")
            break
        element = int(element)
        if is_prime(element):
            data.append(element)
        #print("fd")

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures

    q = mp.Queue()

    primes = mp.Manager().list([])

    # TODO create reading thread

    read_thread = threading.Thread(target=read_func,args=(q,))

    

    

    #print(list(q.queue))

    # TODO create prime processes

    processes = [mp.Process(target=process_func, args=(q, primes)) for _ in range(PRIME_PROCESS_COUNT)]

    read_thread.start()

    for i in range(PRIME_PROCESS_COUNT):
        processes[i].start()

    for i in range(PRIME_PROCESS_COUNT):
        processes[i].join()

    print("Join1")
    read_thread.join()
    print("Join2")

    # process = mp.Process(target=process_func, args=(q, primes))
    # process.start()
    # process.join()

    

    # TODO Start them all

    # TODO wait for them to complete

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

