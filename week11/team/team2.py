"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Stack

Instructions:

Part 1:
- Create classes for Queue_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.

"""
import time
import queue
import threading
import multiprocessing as mp

class Queue_t:
    def __init__(self):
        self.queue = queue.Queue()

    def size(self):
        return self.queue.qsize()

    def get(self):
        return self.queue.get()

    def put(self, item):
        self.queue.put(item)

# -------------------------------------------------------------------
class Stack_t:
    def __init__(self):
        self.stack = []
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            self.stack.append(item)

    def pop(self):
        with self.lock:
            return self.stack.pop()

# -------------------------------------------------------------------
class Queue_p:
    def __init__(self):
        self.queue = mp.Queue()

    def size(self):
        return self.queue.qsize()

    def get(self):
        return self.queue.get()

    def put(self, item):
        self.queue.put(item)

# -------------------------------------------------------------------
class Stack_p:
    def __init__(self):
        self.stack = mp.Manager().list()
        self.lock = mp.Lock()

    def push(self, item):
        with self.lock:
            self.stack.append(item)

    def pop(self):
        with self.lock:
            return self.stack.pop()


def worker_queue_t(q, numbers):
    for i in range(10):
        numbers[0] += 1
        q.put(numbers[0])
        time.sleep(0.1)

    while not q.size() == 0:
        print(f"Thread-safe Queue: {q.get()}")
        time.sleep(0.1)

def worker_stack_t(s, numbers):
    for i in range(10):
        numbers[0] += 1
        s.push(numbers[0])
        time.sleep(0.1)

    while True:
        try:
            print(f"Thread-safe Stack: {s.pop()}")
            time.sleep(0.1)
        except IndexError:
            break

def worker_queue_p(q):
    for i in range(10):
        q.put(i)
        time.sleep(0.1)

    while not q.size() == 0:
        print(f"Process-safe Queue: {q.get()}")
        time.sleep(0.1)

def worker_stack_p(s):
    for i in range(10):
        s.push(i)
        time.sleep(0.1)

    while True:
        try:
            print(f"Process-safe Stack: {s.pop()}")
            time.sleep(0.1)
        except IndexError:
            break

def main():
    # Test thread-safe queue and stack
    # queue_t = Queue_t()
    # stack_t = Stack_t()

    # numbers = [0]

    # numbers2 = [0]

    # threads = []
    # for _ in range(5):
    #     t = threading.Thread(target=worker_queue_t, args=(queue_t, numbers))
    #     threads.append(t)
    #     t.start()

    #     t = threading.Thread(target=worker_stack_t, args=(stack_t, numbers2))
    #     threads.append(t)
    #     t.start()

    # for t in threads:
    #     t.join()

    # Test process-safe queue and stack
    queue_p = Queue_p()
    stack_p = Stack_p()

    processes = []
    for _ in range(5):
        p = mp.Process(target=worker_queue_p, args=(queue_p,))
        processes.append(p)
        p.start()

        p = mp.Process(target=worker_stack_p, args=(stack_p,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()