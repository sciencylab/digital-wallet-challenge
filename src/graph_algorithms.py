def next_degree_friends (friends, adj_dict):
    """
    Given a set of ids, 'friends,' this function outputs a new list of ids of
    degree 1 separated from any element in 'friends' as according to the adjacency
    list 'adj_dict.'
    """
    assert isinstance (friends, set), "function next_degree_friends requires that parameter 'friends' be a set."
    
    friends_of_friends = set ()  # initialize as empty set
    
    # add to the set 'friends_of_friends' the neighbors of all elements of set 'friends.'
    for x in friends:
        friends_of_friends.update (adj_dict [x]) # A.update (B) is the same as A union B
    
    return friends_of_friends


def is_nth_neighbors (a, b, n, adj_dict):
    """
    From adjacency list 'adj_dict', this figures out whether 'a' and 'b' are neighbors 
    of degree fewer than 'n.'
    
    If neighbors of degree <= n, outputs 'k,' where 'k' is the degree of separation.
    
    Otherwise, outputs -1.
    
    
    Tests
    Here, adj_list refers to the adjacency list built using batch_processing.txt.
    
    1. is_nth_neighbors (49466, 27060006, 4, adj_list)  should return -1 since
        27060006 is not in adj_list.
      
    2. is_nth_neighbors (49466, 2706, 4, adj_list) should return 4.
    """
    
    # check to see if both nodes are in graph
    if a not in adj_dict.keys () or b not in adj_dict.keys ():
        return -1
    
    # while 'a' is a single node, the algorithm requires a set, so 'a' is converted.
    friends = set ([a])
    
    # initializing the set of visited nodes. 'a' is included as it is degree 0 separated
    #     from 'a' itself.
    visited = friends 

    # begin loop
    for k in range (n):
        
        # If there are no more elements in 'friends,' then that means all nodes have been
        #     visited already. So, break from loop
        if len (friends) == 0:
            break
            
        # caculate next degree neighbors & remove those that have already been seen
        friends = next_degree_friends (friends, adj_dict) - visited
        
        # If b is in this list of friends, then deg_separation (a, b) = k + 1
        if b in friends:
            return k + 1
        
        # add to the set 'visited' the new elements in 'friends'
        visited.update (friends)
        
    return -1


def degree_list (start, adj_dict, upto = 4):
    """
    Calculates the degree of separation for all nodes (up to degree 'upto') connected
    to node 'start' as according to the adjacency list 'adj_dict'.
    
    Outputs a list 'deg,' where the n-th element is a set containing all nodes of degree of
    separation 'n' away from node 'start'. If node 'elem' is degree 2 away from node
    'start,' then 'elem' will be contained in the set 'deg [2]' and no other.
    
    The optional parameter 'upto' is to indicate how many degrees of separation to search up to.
    If a negative integer is provided, it will attempt to travers the entire graph as provided
    by the adjacency list 'adj_dict.'
    """
    
    # Requires that start be a node in adj_dict, else throw exception
    assert start in adj_dict.keys (), "node start is a node in adj_dict."
    
    # If upto is negative, replace w/ the total number of nodes in 'adj_dict.'
    if upto < 0:
        upto = len (adj_dict)
        
    # If 'start' is a single integer, e.g. 42352, and not a set of integers, then convert it
    #    to a set, i.e. {42352}.
    if not isinstance (start, set):
        friends = set ([start])
    
    # visited nodes
    visited = friends.copy ()
    
    # degree friends with node 'start'
    deg = list ()
    deg.append (friends)
    
    
    for n in range (upto): 
        # calculate deg [n]
        
        # If there are no more elements in 'friends,' then that means all nodes have been
        #     visited already. So, break from loop
        if len (friends) == 0: 
            break

        # caculate next degree neighbors & remove those that have already been seen
        friends = next_degree_friends (friends, adj_dict) - visited
        
        # add to the set 'visited' the new elements in 'friends'
        visited.update (friends)
        
        # append to list 'deg' the set of nodes 'friends' of degree of separation n.
        deg.append (friends)
            
    return deg