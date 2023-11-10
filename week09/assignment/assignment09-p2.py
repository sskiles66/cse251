"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>

Why would it work?

<Answer here>

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color




def solve_find_end(maze: Maze):
    """finds the end position using threads.  Nothing is returned"""
    # When one of the threads finds the end position, stop all of them
    global stop
    stop = False

    cond = threading.Condition()

    def backtrack(x, y, color):
        """Recursively backtracks through the maze, creating new threads for each new direction"""
        # Base case: If we've reached the end position, return True.
        # color = get_color()

        with cond:
            if maze.at_end(x, y) == True:
                print("found end at:", x, y)

                # Set the stop flag to True to stop all threads
                global stop
                stop = True

                # Only notify threads that haven't found the end yet
                cond.notify_all()

                return True

        # Check if the stop flag is set before proceeding with the recursive call.
        if stop:
            return True

        # Get all possible moves from the current position.
        possible_moves = maze.get_possible_moves(x, y)

        # Create a list to store the threads
        threads = []
        

        for next_x, next_y in possible_moves:
            # Mark the current position as visited.
            if len(possible_moves) > 1:

                color = get_color()
            
            if maze.can_move_here(next_x, next_y):
                maze.move(next_x, next_y, color)
                
            
            thread = threading.Thread(
                    target=backtrack, args=(next_x, next_y, color)
                )
            thread.start()
            threads.append(thread)
            global thread_count
            thread_count += 1
            print(f"length of threads {thread_count}")
            

            
        # Check the stop flag before waiting for all threads to finish.
        if stop:
            return True

        
        # Wait for all threads to finish before continuing.
        for thread in threads:
            thread.join()

        

        # If a thread found the end, set the stop flag and return True.
        with cond:
            if stop:
                return True
            
        # with cond:


        return False

    # Reset the stop flag before each maze solution
    stop = False

    path = []
    start_x, start_y = maze.get_start_pos()
    path.append((start_x, start_y))

    maze.move(start_x, start_y, (0, 0, 255))

    # Start the recursive backtracking from the initial position.
    color = get_color()
    backtrack(start_x, start_y, color)

    





def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()