"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, conn, marble_count, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.conn = conn
        self.marble_count = marble_count
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        # print(MARBLE_COUNT)
        for _ in range(self.marble_count):
            marble = random.choice(self.colors)
            print(f"Marble: {marble}")
            self.conn.send(marble)
            time.sleep(self.delay)
        self.conn.send("create done")



class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, rec_conn, send_conn, marbles_per_bag, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.rec_conn = rec_conn
        self.send_conn = send_conn
        self.marbles_per_bag = marbles_per_bag
        self.delay = delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag = Bag()
        while True:
            marble = self.rec_conn.recv()
            print(f"sent marble: {marble}")
            if (marble == "create done"):
                self.send_conn.send("bag done")
                return
            bag.add(marble)
            if bag.get_size() == self.marbles_per_bag:
                self.send_conn.send(bag)
                bag = Bag()
            time.sleep(self.delay)
        
            
            


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, rec_conn, send_conn, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.rec_conn = rec_conn
        self.send_conn = send_conn
        self.delay = delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''

        while True:
            marble_bag = self.rec_conn.recv()
            print(f"Marble Bag: {marble_bag}")
            if marble_bag == "bag done":
                self.send_conn.send("assembler done")
                return
            large_marble = random.choice(self.marble_names)
            gift = Gift(large_marble, marble_bag)
            self.send_conn.send(gift)
            time.sleep(self.delay)




class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, rec_conn, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.rec_conn = rec_conn
        self.delay = delay

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''

        with open(BOXES_FILENAME, 'w') as f:
            while True:
                box = self.rec_conn.recv()
                print(box)
                if box == "assembler done":
                    return
                f.write(f"Created - {str(datetime.now().time())}: {str(box)} \n")
                time.sleep(self.delay)




def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')


    marble_count = settings[MARBLE_COUNT]
    marble_delay = settings[CREATOR_DELAY]
    marble_per_bag = settings[NUMBER_OF_MARBLES_IN_A_BAG]
    bagger_delay = settings[BAGGER_DELAY]
    assembler_delay = settings[ASSEMBLER_DELAY]
    wrapper_delay = settings[WRAPPER_DELAY]

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper

    #print(settings[MARBLE_COUNT])

    cre_send_con, bag_rec_con = mp.Pipe()
    bag_send_con, as_rec_con = mp.Pipe()
    as_send_con, wra_rec_con = mp.Pipe()

    # TODO create variable to be used to count the number of gifts

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)

    marb_pro = Marble_Creator(cre_send_con, marble_count, marble_delay)

    bagg_pro = Bagger(bag_rec_con, bag_send_con, marble_per_bag, bagger_delay)

    assem_pro = Assembler(as_rec_con, as_send_con, assembler_delay)

    wrapp_pro = Wrapper(wra_rec_con, wrapper_delay)



    log.write('Starting the processes')
    # TODO add code here

    marb_pro.start()
    bagg_pro.start()
    assem_pro.start()
    wrapp_pro.start()
    

    log.write('Waiting for processes to finish')
    # TODO add code here

    marb_pro.join()
    bagg_pro.join()
    assem_pro.join()
    wrapp_pro.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.




if __name__ == '__main__':
    main()

