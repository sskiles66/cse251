"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team activity details in I-Learn

"""

from datetime import datetime, timedelta
import threading

# Include cse 251 common Python files
from cse251 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

lock = threading.Lock()

def is_prime(n):
    global numbers_processed
    numbers_processed += 1

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

def callback(start, range_count):

    global prime_count
    for i in range(start, start + range_count):
        
        if is_prime(i):
            prime_count += 1
            #print(i, end=', ', flush=True)
            
    


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    

    start = 10000000000
    range_count = 100000

    new_start = start

    split = int(range_count / 10)

    listt = []

    for i in range(10):
        listt.append(new_start + split)
        new_start = new_start + split


    threads = []

    for i in range(10):
        t = threading.Thread(target=callback, args=(listt[i] - split, split))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
   

    print(flush=True)

    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')


