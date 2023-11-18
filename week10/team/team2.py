"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments
"""

import time
import threading
import random
import string
import os
import mmap

# -----------------------------------------------------------------------------


def reverse_file(filename):
    """ Display a file in reverse order using a mmap file. """
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
            for i in reversed(range(map_file.size())):
                print(map_file[i]) 
                print(chr(map_file[i]), end='')



# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    
    with open(filename, mode="r+b") as file_obj:
        
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as map_file:
            
            for i in range(map_file.size()):
                if map_file[i] == ord('a'):
                    map_file[i] = ord('A')
                elif ord('b') <= map_file[i] <= ord('z'):
                    map_file[i] = ord('.')
                print(map_file.size())
                print(i)


# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    with open(filename, mode="r+b") as file_obj:
        
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as map_file:

            split = 200000

            num_threads = map_file.size() / split

            start = 0

            end = split

            threaddds = []
            
            for thread in range(int(num_threads)):
                threead = threading.Thread(target=threads, args=(map_file,start,end))
                start = end
                end += split
                threaddds.append(threead)
                threead.start()

            
            
            for threadd in threaddds:
                threadd.join()

def threads(map_file, start, end):
    i = start
    for i in range(end):
        if map_file[i] == ord('a'):
            map_file[i] = ord('A')
        elif ord('b') <= map_file[i] <= ord('z'):
            map_file[i] = ord('.')
        print(map_file.size())
        print(i)


def create_large_file(filename):
    if not os.path.exists(filename):
        print('Creating large data file', end='')
        words = []

        for _ in range(1000):
            word = ''
            for _ in range(80):
                word += random.choice(string.ascii_lowercase)
            words.append(word)

        with open(filename, 'w') as f:
            for i in range(2000000):
                if i % 25000 == 0:
                    print('.', end='', flush=True)

                f.write(random.choice(words))
                f.write('\n')
            print()


# -----------------------------------------------------------------------------
def main():
    create_large_file('letter_a.txt')
    reverse_file('data.txt')
    # promote_letter_a('letter_a.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    # promote_letter_a_threads('letter_a.txt')

if __name__ == '__main__':
    main()
