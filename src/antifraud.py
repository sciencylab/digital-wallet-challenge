
def read_adj_dict_from_file (name, verbose = False):
    """
    Read in csv file 'name' of payment transfers and output adjacency list of
    id's of people involved.
    """
    id1, id2 = read_into_lists (name, verbose)
    return adjacency_dict (id1, id2)

def read_into_lists (name, verbose = False):
    """
    Read in csv file 'name' of payment transfers and outputs the columns id1, id2
    as lists
    """
    id1 = []
    id2 = []

    with open (name, 'r') as file:

        file.readline () # don't need the header

        for line in file:
            try:  # for when the row actually conforms to the header
                
                # split up into list
                ids = line.split (',') 
                
                # column 2 & 3 are ids, ignore the rest of data
                ids = list (map (lambda x: int (x), ids [1:3]))

                # read the data into lists
                id1.append (ids [0])
                id2.append (ids [1])
                
            except: # for when something's screwy
                # see what's wrong
                # lol. It's the same 5 or so lines over and over again
                # changed default value to false since these lines are meant
                # to be ignored.
                if verbose: 
                    print (line)
                
    return id1, id2

def adjacency_dict (list1, list2):
    """
    Input: list1, list2. The n-th element of list1 is assumed to have either
        given payment to or received payment from the n-th element of list2.
        From this info, an adjacency list 'd' is created.
    Example: If list1[10] = 'a' and list2 [10] = 'b,' then money is assumed
        to have exchanged between 'a' and 'b.' And so, d [b] will contain 'a'
        and d [a] will contain 'b.'
    
    
    
    Test Case:
    
    adjacency_dict (['a', 'a', 'b', 'c', 'd'],
                    ['b', 'c', 'c', 'd', 'e']) == {'a': ['b', 'c'],
                                                   'b': ['a', 'c'],
                                                   'c': ['a', 'b', 'd'],
                                                   'd': ['c', 'e'],
                                                   'e': ['d']}
    """
    assert len (list1) == len (list2), "The 2 lists' lengths are not equal."

    d = {}  # the adjacency list
    
    for idx in range (len (list1)):
        # get the idx-th item of list1 and list2
        x, y = list1 [idx], list2 [idx]
        
        # confirm x & y are in d. if not, initialize to empty list
        if x not in d: d [x] = [] 
        if y not in d: d [y] = [] 
        
        # Add x & y as neighbors, but first making sure the info is new and not redundant
        if y not in d [x]: d[x].append (y)
        if x not in d [y]: d[y].append (x)
    return d