# import multiprocessing as mp 
import time
import random
import threading

def fill_the_cavity(water_levels:list, filled_to_brim:threading.Semaphore):
    while True:
        # add some water
        print("Water is trickling...")
        filled_to_brim.release() 
        time.sleep(.05)
        
    # notify that it's fill to brim

def empty_the_cavity(water_levels:list, filled_to_brim:threading.Semaphore):
    number_of_times_gushed = 0
    while True:
        for _ in range(10):
            filled_to_brim.acquire()
        # empty the water
        number_of_times_gushed += 1
        print(f"THE WATER GUSHED FORTH {number_of_times_gushed}")
        if number_of_times_gushed > 5:
            break

def main():    
    # Create a value with each thread
    water_levels = [0]
    filled_to_brim = threading.Semaphore(0)
    filler = threading.Thread(target=fill_the_cavity, args=(water_levels, filled_to_brim), daemon=True)
    output = threading.Thread(target=empty_the_cavity, args=(water_levels, filled_to_brim))
    filler.start()
    output.start()
    output.join()
    print(f'done')


if __name__ == '__main__':
    main()