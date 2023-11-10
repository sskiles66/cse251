"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.

"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp
from multiprocessing import Value




# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0



# TODO Add your threaded class definition here


class RequestThread(threading.Thread):
    

    def __init__(self, url, count):
        # calling parent class constructor
        #WIll have to use call count as global and increment when the run method is run.
        super().__init__()

        self.url = url

        self.response = {}

        self.count = count

        

       

    # TODO Add any functions you need here
    
    def run(self):
        
        global call_count
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            call_count += 1
            self.count.value += 1
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


def format(response, target, count):
    #character_urls = t1.response["characters"]

    response_urls = response

    threads = []

    items = []
    
    for url in response_urls:
        th = RequestThread(url, count)

        threads.append(th)

        th.start()

      
    for thread in threads:
        
        thread.join()
        items.append(thread.response["name"])

      
    single_items = ""

    items = sorted(items)

    for item in items:
        single_items += item + ", "


    return target + ":" + " " + str(len(items)), single_items


def test():
    pass
    


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    count = Value('i', 0)

    # TODO Retrieve Top API urls

    #urls = requests.get(TOP_API_URL)

    t = RequestThread(TOP_API_URL, count)

    t.start()

    t.join()

    response_data = t.response

    added_num = response_data["films"] + "6"

    # TODO Retireve Details on film 6

    t1 = RequestThread(added_num, count)

    t1.start()

    t1.join()


    # TODO Display results

    log.write("Title: " + t1.response["title"])
    log.write("Director: " + t1.response["director"])
    log.write("Producer: " + t1.response["producer"])
    log.write("Release Date: " + t1.response["release_date"])
    log.write()


    character_urls = t1.response["characters"]

    planet_urls = t1.response["planets"]

    starship_urls = t1.response["starships"]

    vehicles_urls = t1.response["vehicles"]

    species_urls = t1.response["species"]


    pool = mp.Pool(4)
    list = [(character_urls, "Characters"),(planet_urls, "Planets"), (planet_urls, "Planets"), (starship_urls, "Starships"), (vehicles_urls, "Vehicles"), (species_urls, "Species")]

    results = [pool.apply_async(format, args=(url, target, count)) for url, target in list]

    output = [p.get() for p in results]

    


    for thing in output:
        log.write(thing)
        log.write()

    #print(output)


   #  x, y = format(character_urls, "Characters")
    

   #  x2, y2 = format(planet_urls, "Planets")


   #  x3, y3 = format(starship_urls, "Starships")

    
   #  x4, y4 = format(vehicles_urls, "Vehicles")

   

   #  x5, y5 = format(species_urls, "Species")

   #  log.write(x)
   #  log.write(y)

   #  log.write()

   

   #  log.write(x2)
   #  log.write(y2)

   #  log.write()

   

   #  log.write(x3)
   #  log.write(y3)

   #  log.write()
    
   

   #  log.write(x4)
   #  log.write(y4)

   #  log.write()

    

   #  log.write(x5)
   #  log.write(y5)

   #  log.write()

        

    log.stop_timer('Total Time To complete')
    log.write(f'There were {count.value} calls to the server')
    

if __name__ == "__main__":
    main()
