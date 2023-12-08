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

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

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

                    # husband_parent_request = Request_thread(f'{TOP_API_URL}/family/{husband_response["parent_id"]}')
                    # husband_parent_request.start()
                    # husband_parent_request.join()
                    # husband_parent_response = husband_parent_request.get_response()

                    # t1 = threading.Thread(target=depth_fs_pedigree, args=(husband_response["parent_id"], tree))

                    # threads.append(t1)

                    # t1.start()

                    # t1.join()

                    executor.submit(depth_fs_pedigree, husband_response["parent_id"], tree)


                    # depth_fs_pedigree(husband_parent_response["id"], tree)

                else:
                    return
                
            if family_response["wife_id"] != None: 
            
                wife_response = result_dict["wife_response"]

                if wife_response["parent_id"] != None:

                    # wife_parent_request = Request_thread(f'{TOP_API_URL}/family/{wife_response["parent_id"]}')
                    # wife_parent_request.start()
                    # wife_parent_request.join()
                    # wife_parent_response = wife_parent_request.get_response()

                    # depth_fs_pedigree(wife_parent_response["id"], tree)

                    # t1 = threading.Thread(target=depth_fs_pedigree, args=(wife_response["parent_id"], tree))

                    # threads.append(t1)

                    # t1.start()

                    # t1.join()

                    executor.submit(depth_fs_pedigree, wife_response["parent_id"], tree)

                else:
                    return
        

        # for thread in threads:
        #     thread.join()

      


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree:Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    # level by level traversal

    result_dict = {}

    # Initialize a queue with the root
    q = queue.Queue()
    q.put(family_id)
    
    while not q.empty():

        curr_family = q.get()
        family_request = Request_thread(f'{TOP_API_URL}/family/{curr_family}')
        family_request.start()
        family_request.join()
        family_response = family_request.get_response()

        if family_response:

            family = Family(family_response)
            tree.add_family(family)

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

            husband_response = result_dict["husband_response"]

            if husband_response["parent_id"] != None:

                # husband_parent_request = Request_thread(f'{TOP_API_URL}/family/{husband_response["parent_id"]}')
                # husband_parent_request.start()
                # husband_parent_request.join()
                # husband_parent_response = husband_parent_request.get_response()
                q.put(husband_response["parent_id"])
 
            wife_response = result_dict["wife_response"]

            if wife_response["parent_id"] != None:

                # wife_parent_request = Request_thread(f'{TOP_API_URL}/family/{wife_response["parent_id"]}')
                # wife_parent_request.start()
                # wife_parent_request.join()
                # wife_parent_response = wife_parent_request.get_response()
                q.put(wife_response["parent_id"])


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass