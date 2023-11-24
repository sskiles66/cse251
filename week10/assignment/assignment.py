"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Stephen Skiles


Purpose: assignment for week 10 - reader writer problem


Instructions:


- Review TODO comments


- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)


- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  


- Do not use try...except statements


- Display the numbers received by the reader printing them to the console.


- Create WRITERS writer processes


- Create READERS reader processes


- You can use sleep() statements for any process.


- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.


- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment


- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.


- Not allowed to use Value() or Array() or any other shared data type from
  the multiprocessing package.


- When each reader reads a value from the sharedList, use the following code to display
  the value:
 
                    print(<variable>, end=', ', flush=True)


Add any comments for me:


"""


import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2



"""
A ShareableList is created with a size of BUFFER_SIZE + 4. The first BUFFER_SIZE elements are 
used as a circular buffer for data transfer between the writer and reader processes. The next 
two elements are used as the write and read indices for the circular buffer. 
The third extra element is used as a control signal to indicate when the writer has finished writing data. 
The fourth extra element is used to keep track of the number of values received by the reader.

-6 = Current index so that multiple write process are on the same page when progressing towards the end value
-5 = How many values need to be sent
-4 = write index
-3 = read index
-2 = stop flag
-1 = values received

I believe that my work on this assignment is a 4/4 because I met the requirements of the assignment. 
Using a shareable list that can be used across mutliple reading and writing processes, values (in order) are written and read and 
the amount of items sent is equal to the amount of items received. There can be n number of processes for both reading and writing.

"""


def read(shared_list, lock, i):
    while True:
        lock.acquire()
        if shared_list[-4] != shared_list[-3]:  # If the buffer is not empty, if the write index != read index
            print(f"Received {shared_list[shared_list[-3]]}", end=', ', flush=True)   #Print the element at the index that corresponds to the read index
            shared_list[shared_list[-3]] = 0   # Set the previous element to 0.

            """
            calculates the next read index. The % BUFFER_SIZE part ensures that the index 
            wraps around to the start of the buffer when it reaches the end, hence creating a "circular" buffer.
            """
            shared_list[-3] = (shared_list[-3] + 1) % BUFFER_SIZE  
            shared_list[-1] += 1  # Increment the count of received items
        lock.release()
        if shared_list[-2] == "stop":
            lock.acquire()
            for _ in range(BUFFER_SIZE):
                if shared_list[shared_list[-3]] != 0:
                    
                    print(f"received {shared_list[shared_list[-3]]} after end", end=', ', flush=True)
                    shared_list[shared_list[-3]] = 0
                    shared_list[-1] += 1  # Increment the count of received items
                    
                shared_list[-3] = (shared_list[-3] + 1) % BUFFER_SIZE
            lock.release()
            print(f"Final: {shared_list}")
            
            break




def write(shared_list, items_to_send, lock:mp.Lock, i):

    while shared_list[-6] < shared_list[-5]:
        
        
        lock.acquire()
        next_write_index = (shared_list[-4] + 1) % BUFFER_SIZE  #finds next write index
        """
        If the buffer is not full and the next write index is available.  
        This prevents the write function from overwriting data that has not been read yet, 
        which could cause the number of values sent to not match the number of values received.

        checks if the next write index is not equal to the current read index (shared_list[-3]) 
        and if the value at the next write index is 0. If both conditions are true, this means 
        that the buffer is not full and the next write index is available for writing.
        """
        if next_write_index != shared_list[-3] and shared_list[next_write_index] == 0 and shared_list[-6] < shared_list[-5]:  
            # time.sleep(0.01)
            # print()
            # print("WRITING")   Printing writing for debugging
            # print("Before")
            # print(shared_list)
            # rand_num = random.randint(1,10)
            shared_list[shared_list[-4]] = shared_list[-6]
            shared_list[-4] = next_write_index
            
            # print("After")
            # print(shared_list)   Printing writing for debugging
            # time.sleep(5)

            
            shared_list[-6] += 1
            
            # print(f"write count: {shared_list[-6]} with process {i}")
            # print()        Prinign writing for debugging
        lock.release()
    shared_list[-2] = "stop"




def main():


    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)


    smm = SharedMemoryManager()
    smm.start()


    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))


    share_list = smm.ShareableList([0] * (BUFFER_SIZE + 6))

    
    # TODO - Create any lock(s) or semaphore(s) that you feel you need

    share_list[-5] = items_to_send


    lock = mp.Lock()


    # TODO - create reader and writer processes


    processes = []

    for i in range(WRITERS):
       write_pro =  mp.Process(target=write, args=(share_list, items_to_send, lock, i))
       processes.append(write_pro)

    for i in range(READERS):
       read_pro = mp.Process(target=read, args=(share_list, lock, i))
       processes.append(read_pro)


    for process in processes:
        process.start()

    for process in processes:
        process.join()


    # TODO - Start the processes and wait for them to finish


    print(f'{items_to_send} values sent')


    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')


    print(f'{share_list[-1]} values received')


    smm.shutdown()




if __name__ == '__main__':
    main()


