"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Stephen Skiles

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
SLOW_SPEED = 100
FAST_SPEED = 1
speed = SLOW_SPEED

# TODO add any functions

def solve_path(maze: Maze):
    """Solve the maze and return the path found between the start and end positions.
    The path is a list of positions, (x, y)."""


    def backtrack(x, y):
        # Base case: If we've reached the end position, return True.
        if maze.at_end(x,y) == True:
            print("found end")
            return True

        # Get all possible moves from the current position.
        possible_moves = maze.get_possible_moves(x, y)

        for next_x, next_y in possible_moves:
            # Mark the current position as visited.
            if (maze.can_move_here(next_x, next_y)):
                maze.move(next_x, next_y, (0, 0, 255))


            # Recurse to explore the next position.
            if backtrack(next_x, next_y):
                path.append((next_x, next_y))
                return True

            # Backtrack by restoring the previous position.
            maze.restore(next_x, next_y)

        return False

    path = []
    start_x, start_y = maze.get_start_pos()
    path.append((start_x, start_y))

    maze.move(start_x, start_y, (0, 0, 255))

    # Start the recursive backtracking from the initial position.
    backtrack(start_x, start_y)

    return path


def get_path(log, filename):
    """ Do not change this function """
    #  'Maze: Press "q" to quit, "1" slow drawing, "2" faster drawing, "p" to play again'
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()