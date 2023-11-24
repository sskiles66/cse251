"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp
from multiprocessing import Array, Value

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(lock1, lock2, id, guests, start_time, count):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    # lock1.acquire()
    # print("cleaner working")
    # time.sleep(2)
    # lock1.release()

    while time.time() - start_time < TIME:
        cleaner_waiting()

        # lock1.acquire()
        if guests.value == 0:
            lock1.acquire()
            # lock2.acquire()
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(id)
            print(STOPPING_CLEANING_MESSAGE)
            count.value += 1
            lock1.release()
            # lock2.release()
        # lock1.release()

        # time.sleep(1)


   
def guest(lock1, lock2, semaphore, id, guests, start_time, count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    # lock1.acquire()
    # semaphore
    # print("guest working")
    # time.sleep(2)
    # lock1.release()

    while time.time() - start_time < TIME:
        guest_waiting()

        lock1.acquire()
        if guests.value == 0:
            print(STARTING_PARTY_MESSAGE)
        guests.value += 1
        lock1.release()

        guest_partying(id, guests.value)

        lock1.acquire()
        guests.value -= 1
        if guests.value == 0:
            print(STOPPING_PARTY_MESSAGE)
            count.value += 1
        lock1.release()

        # time.sleep(1)





def main():
    # Start time of the running of the program. 
    start_time = time.time()

    lock1 = mp.Lock()
    lock2 = mp.Lock()

    semaphore = mp.Semaphore(HOTEL_GUESTS)

    # TODO - add any variables, data structures, processes you need

    guests = Value('i', 0)
    cleaned_count = Value('i', 0)
    party_count = Value('i', 0)

    processes = []

    for i in range(HOTEL_GUESTS):
        guest_pro = mp.Process(target=guest, args=(lock1, lock2, semaphore, f"Guest {i}", guests, start_time, party_count))
        processes.append(guest_pro)
        guest_pro.start()

    for i in range(CLEANING_STAFF):
        cleaning_pro = mp.Process(target=cleaner, args=(lock1, lock2, f"Cleaner {i}", guests, start_time, cleaned_count))
        processes.append(cleaning_pro)
        cleaning_pro.start()

    for process in processes:
        process.join()
    

    # TODO - add any arguments to cleaner() and guest() that you need

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')
    # print("end")


if __name__ == '__main__':
    main()

