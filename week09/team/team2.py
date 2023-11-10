"""
Course: CSE 251
Lesson Week: 09
File: team2.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- This is the same problem as last team activity.  However, you will implement a waiter.  
  When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be a issue picking up the two forks since the waiter is in control of 
  the forks and when philosophers eat.  When a philosopher is finished eating, it will 
  informs the waiter that he/she is finished.  If the waiter indicates to a philosopher
  that they can not eat, the philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- When a philosopher is not eating, it will think for 3 to 5 seconds.
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat
"""

# import time
# import threading

# PHILOSOPHERS = 5
# MAX_MEALS = PHILOSOPHERS * 5

# def main():
#     # TODO - create the waiter (A class would be best here)
#     # TODO - create the forks
#     # TODO - create PHILOSOPHERS philosophers
#     # TODO - Start them eating and thinking
#     # TODO - Display how many times each philosopher ate

#     pass

# if __name__ == '__main__':
#     main()


import time
import threading
import random
import queue

PHILOSOPHERS = 5
MAX_MEALS_EATEN = PHILOSOPHERS * 5

class Waiter(threading.Thread):

    # constructor
    def __init__(self):
        # calling parent class constructor
        super().__init__()

        # Create or assign any variables that you need
        
        
    
    # This is the method that is run when start() is called
    def run(self):
        
        pass

class Phil(threading.Thread):

    # constructor
    def __init__(self, fork1, fork2, cond, stats, counter, q, i):
        # calling parent class constructor
        super().__init__()

        # Create or assign any variables that you need
        self.fork1 = fork1
        self.fork2 = fork2
        self.cond = cond
        self.stats = stats
        self.counter = counter
        self.q = q
        self.i = i
        
    
    # This is the method that is run when start() is called
    def run(self):
        
        while (self.counter < MAX_MEALS_EATEN):
          if self.q.qsize() > 0:
              self.q.put("1")
              break
          self.fork1.acquire()
          self.fork2.acquire()
          print("Phil eating")
          time.sleep(random.randrange(1,4))
          print(f"rand: {random.randrange(1,4)}")
          self.stats[self.i] += 1
          self.counter += 1
          print(self.counter)
          # print(self.q.qsize())
          self.fork1.release()
          self.fork2.release()
          print("Phil thinking")
          time.sleep(random.randrange(1,4))
          
          if self.counter == MAX_MEALS_EATEN:
              print("MAMXBHDHB")
              self.q.put("2")
              print(self.q.qsize())
              break
              # self.cond.notifyAll()
          

          

        

def main():
    condition = threading.Condition()

    # stats = list[[0] * PHILOSOPHERS]
    stats = [0] * PHILOSOPHERS
    print(stats)

    counter = 0

    q = queue.Queue()
    
    forks = [threading.Lock() for _ in range(PHILOSOPHERS)]

    # Create philosopher threads dynamically
    philosophers = []
    for i in range(PHILOSOPHERS):
        phil = Phil(forks[i], forks[(i + 1) % PHILOSOPHERS], condition, stats, counter, q, i)
        philosophers.append(phil)
        phil.start()

    # Wait for all philosopher threads to finish
    for phil in philosophers:
        phil.join()
        # TODO - Display how many times each philosopher ate
        
    print(stats)

if __name__ == '__main__':
    main()