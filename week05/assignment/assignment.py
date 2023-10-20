"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Stephen Skiles

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier
- Do not use try...except statements
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

I believe that my work on this assignment is a 4/4 because my program meets all of the requirements. The Factory and Dealeship class are
running in parallel and are returning the factory and dealer stats to a log.

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
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

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        #print(f'{self.make} {self.model}, {self.year}')
        pass


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, barrier, fac_sem, del_sem, lock, dealer_count, factory_stats, i):
        super().__init__()
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.queue = queue
        self.barrier = barrier
        self.fac_sem = fac_sem
        self.del_sem = del_sem
        self.lock = lock
        self.count = dealer_count
        self.stats = factory_stats
        self.i = i 

    def run(self):
        # TODO produce the cars, the send them to the dealerships
        print(self.cars_to_produce)
        for i in range(self.cars_to_produce):
            self.del_sem.acquire()
 
            car = Car()
            
            self.queue.put(car)

            self.stats[self.i] += 1

            print(f"facotry{self.stats[self.i]}")
            
            #print(i)
            self.fac_sem.release()

        
        # TODO wait until all of the factories are finished producing cars
        self.barrier.wait()

        #self.lock.acquire()

        for _ in range(self.count):
            self.fac_sem.release()

        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this

        self.queue.put("stop")

        #self.lock.release()

        return



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue:Queue251, fac_sem, del_sem, lock, dealer_stats, i):
        super().__init__()
        self.queue = queue
        self.fac_sem = fac_sem
        self.del_sem = del_sem
        self.lock = lock
        self.stats = dealer_stats
        self.i = i

    def run(self):
        while True:
            # TODO handle a car
            self.fac_sem.acquire()
            car = self.queue.get()
            self.stats[self.i] += 1
            print(f"dealer{self.stats[self.i]}")
            if car == "stop":
                self.stats[self.i] -= 1
                self.queue.put("stop")
                #print("supppoosde to breakksfkapks")
                return
            
            self.del_sem.release()
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))
            
            



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create semaphore(s) if needed

    dealer_sem = threading.Semaphore(MAX_QUEUE_SIZE)
    factory_sem = threading.Semaphore(0)

    # TODO Create queue

    car_queue = Queue251()

    # TODO Create lock(s) if needed

    lock = threading.Lock()

    # TODO Create barrier
    barrier = threading.Barrier(factory_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([factory_count] * dealer_count)

    factory_stats = list([dealer_count] * factory_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY

    factories = []

    for i in range(factory_count):
        factory = Factory(car_queue, barrier, factory_sem, dealer_sem, lock, dealer_count, factory_stats, i)
        factories.append(factory)

    # TODO create your dealerships

    dealers = []

    for i in range(dealer_count):
        dealer = Dealer(car_queue, factory_sem, dealer_sem, lock, dealer_stats, i)
        dealers.append(dealer)

    log.start_timer()

    # TODO Start all dealerships

    for dealer in dealers:
        dealer.start()
    

    # TODO Start all factories

    for factory in factories:
        factory.start()

    # TODO Wait for factories and dealerships to complete

    for dealer in dealers:
        dealer.join()

    for factory in factories:
        factory.join()

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


