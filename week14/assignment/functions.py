"""
Course: CSE 251, week 14
File: functions.py
Author: <your name>

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
import queue

depth = 6

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree: Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    # Do inorder traversal. Just adding to tree object, not building a new BST.

    global depth
    if depth == 0:
        return

    print(family_id)  ## Print
    
    family_request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    family_request.start()
    family_request.join()
    family_response = family_request.get_response()
    print(family_response)  ## Print

    if family_response:
        family = Family(family_response)
        print(f"Family Info: {family}")  ### Print
        tree.add_family(family)

        children = family_response["children"]

        print(children)  ## Print

        for child in children:
            child_request = Request_thread(f'{TOP_API_URL}/person/{child}')
            child_request.start()
            child_request.join()
            child_response = child_request.get_response()
            child = Person(child_response)
            tree.add_person(child)

            print(f"CHILD INFORMATION: {child}")

        husband_request = Request_thread(f'{TOP_API_URL}/person/{family_response["husband_id"]}')
        husband_request.start()
        husband_request.join()
        husband_response = husband_request.get_response()
        husband = Person(husband_response)
        tree.add_person(husband)
        print(f"Husband INFORMATION: {husband}")

        

        wife_request = Request_thread(f'{TOP_API_URL}/person/{family_response["wife_id"]}')
        wife_request.start()
        wife_request.join()
        wife_response = wife_request.get_response()
        wife = Person(wife_response)
        tree.add_person(wife)
        print(f"Wife INFORMATION: {wife}")

        



            # # Recursive call for each child
            # depth -= 1
            # depth_fs_pedigree(child, tree)
            # depth += 1


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    # level by level traversal

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass