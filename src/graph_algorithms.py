class Graph:
    """
    list of functions/procedures:
    
    1. __init__ (self, adj_dict)
    2. __str__ (self)
    3. __repr__ (self)
    4. next_degree_friends (self, friends)
    5. distance (self, a, b, n = -1)
    6. degree_list (self, start, upto = -1)
    7. add_edges (self, edges)
    8. add_edge (self, edge)
    """
    
    
    def __init__ (self, adj_dict = {}):
        self.graph = adj_dict
        self.length = len (adj_dict.keys ())
            
            
    def __str__ (self):
        return str (self.graph)
    
    def __repr__ (self):
        return self.__str__ ()
    
    
    def next_degree_friends (self, friends):
        """
        Given a set of ids, 'friends,' this function outputs a new list of ids of
        degree 1 separated from any element in 'friends' as according to the adjacency
        list 'self.graph.'
        """
        if not isinstance (friends, set):
            friends = set (friends)
#        assert isinstance (friends, set), "function next_degree_friends requires that parameter 'friends' be a set."

        friends_of_friends = set ()  # initialize as empty set

        # add to the set 'friends_of_friends' the neighbors of all elements of set 'friends.'
        for x in friends:
            friends_of_friends.update (self.graph [x]) # A.update (B) is the same as A union B

        return friends_of_friends


    def distance (self, a, b, n = -1):
        """
        From adjacency list 'self.graph', this figures out whether 'a' and 'b' are neighbors 
        of degree fewer than 'n.'

        If neighbors of degree <= n, outputs 'k,' where 'k' is the degree of separation.

        Otherwise, outputs -1.


        Tests
        Here, 'transactions' refers to the graph built using batch_processing.txt.

        1. transactions = distance (49466, 27060006)  should return -1 since
            27060006 is not in adj_list.

        2. transactions = distance (49466, 2706) should return 4.
        """
        # check if a == b
        if a == b:
            return 0
        
        if n < 0:
            n = self.length
        
        # check to see if both nodes are in graph
        if a not in self.graph.keys () or b not in self.graph.keys ():
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
            friends = self.next_degree_friends (friends) - visited

            # If b is in this list of friends, then deg_separation (a, b) = k + 1
            if b in friends:
                return k + 1

            # add to the set 'visited' the new elements in 'friends'
            visited.update (friends)

        return -1
    
    def distance_lt_n (self, a, b, n):
        """
        Note: distance_lt_n "(if) distance is less than n."
        
        From adjacency list 'self.graph', this figures out whether 'a' and 'b' are neighbors 
        of degree fewer than 'n.'

        If neighbors of degree <= n, outputs True; otherwise, False.
        """
        # check if a == b
        if a == b:
            return 0
        
        assert n >= 0, "Need a n >= 0"
        
        # check to see if both nodes are in graph
        if a not in self.graph.keys () or b not in self.graph.keys ():
            return False

        # while 'a' is a single node, the algorithm requires a set, so 'a' is converted.
        friends = set ([a])

        # initializing the set of visited nodes. 'a' is included as it is degree 0 separated
        #     from 'a' itself.
        visited = friends 

        # begin loop
        for k in range (n):

            # If there are no more elements in 'friends,' then that means all nodes have been
            #     visited already. So, return False
            if len (friends) == 0:
                return False

            # caculate next degree neighbors & remove those that have already been seen
            friends = self.next_degree_friends (friends) - visited

            # If b is in this list of friends, then deg_separation (a, b) = k + 1
            if b in friends:
                return True

            # add to the set 'visited' the new elements in 'friends'
            visited.update (friends)

        return False


    def degree_list (self, start, upto = -1):
        """
        Calculates the degree of separation for all nodes (up to degree 'upto') connected
        to node 'start' as according to the adjacency list 'self.graph.'

        Outputs a list 'deg,' where the n-th element is a set containing all nodes of degree of
        separation 'n' away from node 'start'. If node 'elem' is degree 2 away from node
        'start,' then 'elem' will be contained in the set 'deg [2]' and no other.

        The optional parameter 'upto' is to indicate how many degrees of separation to search up to.
        If a negative integer is provided, it will attempt to travers the entire graph as provided
        by the adjacency list 'self.graph.'
        
        If 'start' is not in 'self.graph,' then return empty list
        """
        
        # check to see if both nodes are in graph
        if start not in self.graph.keys ():
            return []

        # Requires that start be a node in adj_dict, else throw exception
        assert start in self.graph.keys (), "node start is a node in self.graph."

        # If upto is negative, replace w/ the total number of nodes in 'adj_dict.'
        if upto < 0:
            upto = self.length

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

            # caculate next degree neighbors & remove those that have already been seen
            friends = self.next_degree_friends (friends) - visited

            # If there are no more elements in 'friends,' then that means all nodes have been
            #     visited already. So, break from loop
            if len (friends) == 0:
                break

            # add to the set 'visited' the new elements in 'friends'
            visited.update (friends)

            # append to list 'deg' the set of nodes 'friends' of degree of separation n.
            deg.append (friends)

        return deg
    
    def add_edges (self, edges):
        """
        Given a list of edges, iteratively apples add_edge to each.
        """
        assert isinstance (edges, list), "The input to self.add_edges needs to be a list."
        for edge in edges:
            self.add_edge (edge)
            
       
    def add_edge (self, edge):
        """
        Adds an edge = (x, y) pair to the adjacency list self.graph.
        """
        
        assert len (edge) == 2, "Each edge needs to be of length 2."

        x, y = edge

        # add y to x
        if x in self.graph:
            self.graph [x].add (y)
        else:
            #print ('New node ', x, 'graph length: ', self.length)
            self.length += 1
            self.graph [x] = {y}

        if y in self.graph:
            self.graph [y].add (x)
        else:
            #print ('New node ', y, 'graph length: ', self.length)
            self.length += 1
            self.graph [y] = {x}

    