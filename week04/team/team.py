"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4       # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q: queue.Queue, log, sem):  # TODO add arguments
    """ Process values from the data_queue """

    

    while True:
        
        # TODO check to see if anything is in the queue

        if (NO_MORE_VALUES == 'No more'):
            continue
        elif q.qsize() > 0:
            sem.acquire()
            print(q.qsize())
            # TODO process the value retrieved from the queue
            value = q.get()
            # TODO make Internet call to get characters name and log it
            new_value = requests.get(value)
            response_data = new_value.json()
            log.write(response_data['name'])
            sem.release()
        else: 
            break

        #could've done if you passed in sentintental values

        # url = q.get()
        # if url == NO_MORE_VALUES:
        #     break
        # log.write(responsedtatat)

    
        
        

        
        


def file_reader(q: queue.Queue, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue

    with open("urls.txt", "r") as f:
        lines = f.readlines()

        for line in lines:
            q.put(line.strip())

    log.write('finished reading file')

    #print(q)

    # TODO signal the retrieve threads one more time that there are "no more values"
    
    global NO_MORE_VALUES
    NO_MORE_VALUES = ""

    #could've also did 

    # for _ in range(RETRIEVE_THREADS):
    #     q.put(NO_MORE_VALUES)



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)
    print(NO_MORE_VALUES)
    sem = threading.Semaphore(RETRIEVE_THREADS)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    threads = []

    reader = threading.Thread(target=file_reader, args=(q,log))


    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader

    print(NO_MORE_VALUES)

    

    for i in range(RETRIEVE_THREADS):
       #sem.acquire()
       retrieve = threading.Thread(target=retrieve_thread, args=(q,log,sem)) 
       retrieve.start()
       threads.append(retrieve)
       #sem.release()

    reader.start()

    # TODO Wait for them to finish - The order doesn't matter

    #reader.join()

    for thread in threads:
        thread.join()

    reader.join()

    print(NO_MORE_VALUES)

    #print(list(q.queue))

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




