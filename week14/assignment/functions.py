"""
Course: CSE 251, week 14
File: functions.py
Author: Stephen Skiles

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

I sped up part 1 by using recursion to traverse through the tree (DFS) and then I started up a new thread 
with the ThreadPoolExecutor class that I imported in to manage the threads that were being created recursively.
I also had a different set of threads running concurrenly when retreiving all of the information on every person
in each family (threaded_fs function). The run time for this part is around 5 seconds.


Describe how to speed up part 2

I sped up part 2 by using an array that contains arrays which represents each generation and this array
of arrays acts as a queue for families to be processed. Each family in each generation gets processed concurrently
and this gets done by starting a new thread for each family in each generation. I made a function named 
bfs_thread that processes each family and then adds the husband's and wife's parent_id to the next generation
of the array of arrays. To process each person in the family, I reused the same function that was used 
in part 1 (threaded_fs) so that each person gets processed concurrently. 
Unfortunately, this code runs in about 19 seconds because there is a race condition
when concurrently processing the families.Therefore, a lock was necessary to prevent this race condition but this 
resulted in the code running slower than desired.



Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

I believe my work on this assignment is a 3/4 since I was able to 
meet most requirements for this assignment. I used threads for both parts, I used recursion for part 1, I took 
an iterative approach for part 2 and I was able to retrieve family and person data and add this data to the tree.
While I was able to run part 1 under 10 seconds (runs in about 5 seconds), I was not able to do the same for 
part 2 (runs in about 19 seconds).

"""
from common import *
import threading, queue


from concurrent.futures import ThreadPoolExecutor



threads = []

def threaded_fs(family_response, result_dict, id_request, type_of_id_response, tree:Tree):

    request = Request_thread(f'{TOP_API_URL}/person/{id_request}')
    request.start()
    request.join()
    result_dict[type_of_id_response] = request.get_response()
    family_member = Person(result_dict[type_of_id_response])

    if tree.does_person_exist(id_request) == False:

        tree.add_person(family_member)
        
# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree: Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    result_dict = {}
  
    family_request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    family_request.start()
    family_request.join()
    family_response = family_request.get_response()

    if family_response:

        family = Family(family_response)
        tree.add_family(family)

        if family_response["husband_id"] != None:

            husband_thread = threading.Thread(target=threaded_fs, args=(family_response, result_dict, family_response["husband_id"], "husband_response", tree))
            husband_thread.start()

        if family_response["wife_id"] != None:        
            wife_thread = threading.Thread(target=threaded_fs, args=(family_response, result_dict, family_response["wife_id"], "wife_response", tree))
            wife_thread.start()

        children = family_response["children"]

        child_threads = []

        for child in children:

            child_thread = threading.Thread(target=threaded_fs, args=(family_response, result_dict, child, "child_response", tree))
            child_thread.start()
            child_threads.append(child_thread)

        
        if family_response["husband_id"] != None: 
            husband_thread.join()
        if family_response["wife_id"] != None: 
            wife_thread.join()

        for thread in child_threads:
            thread.join()

        with ThreadPoolExecutor() as executor:

            if family_response["husband_id"] != None:

                husband_response = result_dict["husband_response"]

                if husband_response["parent_id"] != None:

                    executor.submit(depth_fs_pedigree, husband_response["parent_id"], tree)

                else:
                    return
                
            if family_response["wife_id"] != None: 
            
                wife_response = result_dict["wife_response"]

                if wife_response["parent_id"] != None:

                    executor.submit(depth_fs_pedigree, wife_response["parent_id"], tree)

                else:
                    return


def bfs_thread(tree: Tree, result_dict, q, level, family, lock):

    curr_family = family
    
    family_request = Request_thread(f'{TOP_API_URL}/family/{curr_family}')

    lock.acquire()
    family_request.start()
    family_request.join()
    lock.release()

    family_response = family_request.get_response()

    if family_response:

        family2 = Family(family_response)
        tree.add_family(family2)

        children = family_response["children"]
        child_threads = []

        for child in children:

            child_thread = threading.Thread(target=threaded_fs, args=(family_response, result_dict, child, "child_response", tree))
            child_thread.start()
            child_threads.append(child_thread)

        if family_response["husband_id"] != None: 

            husband_thread = threading.Thread(target=threaded_fs, args=(family_response, result_dict, family_response["husband_id"], "husband_response", tree))
            husband_thread.start()

        if family_response["wife_id"] != None: 
                
            wife_thread = threading.Thread(target=threaded_fs, args=(family_response, result_dict, family_response["wife_id"], "wife_response", tree))
            wife_thread.start()

        for thread in child_threads:

            thread.join()

        if family_response["husband_id"] != None: 

            husband_thread.join()

        if family_response["wife_id"] != None: 

            wife_thread.join()

    
        if family_response["husband_id"] != None: 
                    
            husband_response = result_dict["husband_response"]

            if husband_response["parent_id"] != None:
                
                 if level != 5:

                    # print(f"{curr_family} ADDEDDDEDED {husband_response['parent_id']}")

                    q[level + 1].append(husband_response["parent_id"])

        if family_response["wife_id"] != None: 
    
            wife_response = result_dict["wife_response"]

            if wife_response["parent_id"] != None:

                if level != 5:
                        
                    # print(f"{curr_family} ADDEDDDEDED {wife_response['parent_id']}")
                    q[level + 1].append(wife_response["parent_id"])

        
# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree:Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    # level by level traversal

    result_dict = {}

    lock = threading.Lock()

    # Initialize a queue (which is an array of arrays in this case) with the root
    q = [[family_id], [], [], [], [], []]

    level = 0

    while level != 6:

        threads = []

        for family in q[level]:

            # print(f"FAMILY     jcnnodinjiod {family}")
            t1 = threading.Thread(target=bfs_thread, args=(tree, result_dict, q, level, family, lock))
            threads.append(t1)
        
        for thread in threads:

            thread.start()
           
        for thread in threads:

            thread.join()

        level += 1

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass