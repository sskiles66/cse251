"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Stephen Skiles

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

I believe that my work on this assignment is a 4/4 because it meets the requirements of the assignment. 
The factory and dealer classes are working as intended (running concurrently) and the chart is being populated with the appropiate data.

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, sem, sem2, log):
        super().__init__()
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        self.queue = queue
        self.sem = sem
        self.sem2 = sem2
        self.log = log


    def run(self):
        i = 1
        while i < CARS_TO_PRODUCE:
            # TODO Add you code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
        """
           
            # if (self.queue.size() < MAX_QUEUE_SIZE ):
            #     self.sem2.acquire()
            #     car = Car()
            #     self.queue.put(car)
            #     i += 1
            #     self.sem.release()
            # else:
            #     continue

            self.sem2.acquire()
            car = Car()
            self.queue.put(car)
            i += 1
            self.sem.release()
            
                
           
            #print(i)
        # signal the dealer that there there are not more cars
        #The else statement is for inserting none into the queue if the queue isn't full
        print("no more cars")
        if (self.queue.size() < MAX_QUEUE_SIZE):
            self.queue.put(None)
        else:
            print("Had to wait")
            time.sleep(1)
            self.queue.put(None)
        


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue, sem, sem2, stats):
        super().__init__()
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        self.queue = queue
        self.sem = sem
        self.stats = stats
        self.sem2 = sem2

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            # if (self.queue.size() > 0):
            #     self.sem.acquire()
            #     self.stats[self.queue.size() - 1] += 1
            #     car = self.queue.get()
            #     self.sem2.release()
            #     if car is None:
            #         break
            if (self.queue.size() > 0):
                self.sem.acquire()
                self.stats[self.queue.size() - 1] += 1
                car = self.queue.get()
                self.sem2.release()
                if car is None:
                    break
                    

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

           



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    sem = threading.Semaphore(MAX_QUEUE_SIZE)
    sem2 = threading.Semaphore(MAX_QUEUE_SIZE)
    # TODO Create queue251 
    queue = Queue251()
    # TODO Create lock(s) ?

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    #print(queue_stats)

    # TODO create your one factory

    factory = Factory(queue, sem, sem2, log)

    # TODO create your one dealership

    dealer = Dealer(queue, sem, sem2, queue_stats)

    log.start_timer()

    # TODO Start factory and dealership

    factory.start()

    dealer.start()

    # TODO Wait for factory and dealership to complete

    factory.join()

    dealer.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
