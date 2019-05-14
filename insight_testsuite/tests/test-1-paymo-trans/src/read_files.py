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

def read_into_list_of_tuples (name, verbose = False):
    """
    Read in csv file 'name' of payment transfers and outputs the columns id1, id2
    as list of tuples.
    """
    stream = []

    with open (name, 'r') as file:

        file.readline () # don't need the header

        for line in file:
            try:  # for when the row actually conforms to the header
                
                # split up into list
                ids = line.split (',') 
                
                # column 2 & 3 are ids, ignore the rest of data
                ids = list (map (lambda x: int (x), ids [1:3]))

                # read the data into list as a pair
                stream.append ((ids [0], ids [1]))
                
            except: # for when something's screwy
                # see what's wrong
                # lol. It's the same 5 or so lines over and over again
                # changed default value to false since these lines are meant
                # to be ignored.
                if verbose: 
                    print (line)
                
    return stream
