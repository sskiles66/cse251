"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

- After you can copy a text file word by word exactly,
  Change the program (any way you want) to be faster 
  (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import time
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(conn, file, count):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(file, 'r') as f:

        text = f.read()
        words = text.split(" ")
        for word in words:
            conn.send(word)
            count += 1
        conn.close()


def receiver(conn, file):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(file, 'w') as f:
        word = conn.recv()
        f.write(word)


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 

    parent_conn, child_conn = mp.Pipe()
    
    # TODO create variable to count items sent over the pipe

    count = 0

    # TODO create processes 

    process1 = mp.Process(target=sender, args=(parent_conn , filename1, count))

    process2 = mp.Process(target=sender, args=(child_conn , filename2 ))



    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 

    process1.start()
    process2.start()
    
    # TODO wait for processes to finish

    process1.join()
    process2.join()

    stop_time = log.get_time()


#replace 1 and 2 wirh counter variables
    log.stop_timer(f'Total time to transfer content = {count}: ')
    log.write(f'items / second = {count / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    #dir_path = os.path.dirname(os.path.abspath(__file__))

    #file_path = os.path.join(dir_path, 'gettysburg.txt')

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')
