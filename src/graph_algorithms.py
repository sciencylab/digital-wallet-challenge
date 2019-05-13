def copy_adj_list (adj):
    """
    Use this method to make a "deep" copy of an adjacent list. Don't use .cop
    """
    res  = {}
    for key in adj.keys ():
        res [key] = adj [key].copy ()
    return res

class Graph:
    """
    list of functions/procedures:
    
    1. __init__ (self, adj_dict)
    2. __str__ (self)
    3. __repr__ (self)
    4. next_degree_friends (self, friends)
    5. next_degree_friends_sc (self, friends, elem)
    6. distance (self, pair, n = -1)
    7. distance_lte (self, pair, n)
    8. add_edges (self, edges)
    9. add_edge (self, edge)
    10. is_self_consistent (self)
    11. build_adj (self)
    12. copy (self)
    13. if_lte_deg1 (self, pair)
    14. if_lte_deg2 (self, pair)
    15. if_lte_deg4 (self, pair)
    16. friends_of_friends (self, start)
    17. is_equal_to (self, graph)
    18. degree_lte (self, pair, degree)
    19. initialize_from_edges (self, edges)
    """
    
    
    def __init__ (self, edges = {}):
        d = {}  # the adjacency list
    
        for pair in edges:
            x, y = pair

            # confirm x & y are in d. if not, initialize singleton set
            if x not in d: d [x] = {x}
            if y not in d: d [y] = {y}

            # Add x & y as neighbors, but first making sure the info is new and not redundant
            d [x].add (y)
            d [y].add (x)
        

        # inclusive 1st order adjacency list
        self.adj = d
        self.num_nodes = len (d)
        
        return None
            
    def __str__ (self):
        return str (self.adj)
    
    def __repr__ (self):
        return self.__str__ ()
    
    
    def next_degree_friends (self, friends):
        """
        Given a set of ids, 'friends,' this function outputs a new list of ids of
        degree 1 separated from any element in 'friends' as according to the adjacency
        list 'self.adj.'
        
        Outputs a set, the friends of friends.
        """
        if not isinstance (friends, set):
            friends = set (friends)
#        assert isinstance (friends, set), "function next_degree_friends requires that parameter 'friends' be a set."

        friends_of_friends = set ()  # initialize as empty set

        # add to the set 'friends_of_friends' the neighbors of all elements of set 'friends.'
        for x in friends:
            friends_of_friends.update (self.adj [x]) # A.update (B) is the same as A union B

        return friends_of_friends


    def next_degree_friends_sc (self, friends, elem):
        """
        Given a set of ids, 'friends,' this function outputs a new list of ids of
        degree 1 separated from any element in 'friends' as according to the adjacency
        list 'self.adj.'
        
        Outputs a set, the friends of friends.
        Note: This is the shortcut (sc) version. It will return a singleton set, {elem}, if
        'elem' is found.
        """
        if not isinstance (friends, set):
            friends = set (friends)
#        assert isinstance (friends, set), "function next_degree_friends requires that parameter 'friends' be a set."

        friends_of_friends = set ()  # initialize as empty set

        # add to the set 'friends_of_friends' the neighbors of all elements of set 'friends.'
        for x in friends:
            if elem in self.adj [x]:
                return {elem}
            else:
                friends_of_friends.update (self.adj [x]) # A.update (B) is the same as A union B

        return friends_of_friends


    def distance (self, pair, n = -1):
        """
        Note: This method uses breadth first search (BFS) and can be slow. Should modify to the
              bi-directional version for speed.
        
        From adjacency list 'self.adj', this figures out whether the pair '(a, b)' are neighbors 
        of degree fewer than 'n.'

        If neighbors of degree <= n, outputs 'k,' where 'k' is the degree of separation.

        Otherwise, outputs -1.


        Tests
        Here, 'transactions' refers to the graph built using batch_processing.txt.

        1. transactions = distance (49466, 27060006)  should return -1 since
            27060006 is not in adj_list.

        2. transactions = distance (49466, 2706) should return 4.
        """
        a, b = pair
        
        # check if a == b
        if a == b:
            return 0
        
        if n < 0:
            n = self.num_nodes
        
        # check to see if both nodes are in graph
        if a not in self.adj.keys ():
            return -1
        elif b not in self.adj.keys ():
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
    
    def distance_lte (self, pair, n):
        """
        Note: This method uses breadth first search (BFS) and can be slow. Should modify to the
              bi-directional version for speed.
              
        Note: distance_lte "(if) distance is less than n."
        
        From adjacency list 'self.adj', this figures out whether the pair '(a, b)' are neighbors 
        of degree fewer than 'n.'

        If neighbors of degree <= n, outputs True; otherwise, False.
        """
        a, b = pair
        
        # check if a == b
        if a == b:
            return True
        
        assert n >= 0, "Need a n >= 0"
        
        # check to see if both nodes are in graph
        if a not in self.adj.keys ():
            return False
        elif b not in self.adj.keys ():
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
            # Note: Uses shortcut version of next_degree_friends
            friends = self.next_degree_friends_sc (friends, elem = b) - visited

            # If b is in this list of friends, then deg_separation (a, b) = k + 1
            if b in friends:
                return True

            # add to the set 'visited' the new elements in 'friends'
            visited.update (friends)

        return False


     
    def add_edges (self, edges):
        """
        Given a list of edges, iteratively apples add_edge to each.
        """
        assert isinstance (edges, list), "The input to self.add_edges needs to be a list."
        for edge in edges:
            self.add_edge (edge)
            
       
    def add_edge (self, edge):
        """
        Adds an edge = (x, y) pair to the adjacency list self.adj.
        """
        
        assert len (edge) == 2, "Each edge needs to be of length 2."

        x, y = edge
        
        # Add node if not in graph
        if x not in self.adj:
            self.num_nodes += 1
            self.adj [x] = set ()
        if y not in self.adj:
            self.num_nodes += 1
            self.adj [y] = set ()
        
        # add edge
        self.adj [x].update (set (edge))
        self.adj [y].update (set (edge))
        
        return None
        
        
    def is_self_consistent (self):
        """
        Checks graph for self-consistency by making sure that it is symmetric: For 
        adjacency list 'adj' and any nodes x, y of G, y is in adj [x] iff x is in adj [y].
        """
        try:
            for key in self.adj.keys ():
                for elem in self.adj [key]:
                    if key not in self.adj [elem]:
                        print ('key {} not in adj [{}]'.format (key, elem))
                        return False
            return True
        except:
            print ("Self-consistency error: ", key, elem)
    
    def build_adj (self):
        """
        Turns the exclusive 1st order adjacency lists into the inclusive version.
        """
        # Make adj inclusive (just add the node itself to its adjacency list)
        for key in self.adj.keys ():
            self.adj [key].add (key)

        return None
        
    def copy (self):
        """
        Returns a copy of the Graph object.
        
        Note: Let g be some instance of Graph, then the difference between
                   1. x = g
                   2. y = g.copy ()
              is that x is just another name for g, whereas y is a new object. If x were
              to be modified, g would also be modified since they're the same object.
        """
        res = Graph ()
        res.num_nodes = self.num_nodes
        res.adj = copy_adj_list (self.adj)
        return res


    def if_lte_deg1 (self, pair):
        """
        Returns True if the pair is separated by 0 or 1 degree and False otherwise.
        """
        a, b = pair

        # check if a & b are both in the graph
        if a not in self.adj.keys ():
            return False
        elif b not in self.adj.keys ():
            return False
        
        # 0th and 1st degree check
        return a in self.adj [b]
     
    
    def if_lte_deg2 (self, pair):
        """
        Returns True if the pair is separated by 0, 1, or 2 degree and False otherwise.
        """
        a, b = pair

        # check if a & b are both in the graph
        if a not in self.adj.keys ():
            return False
        elif b not in self.adj.keys ():
            return False
        
        # 0th and 1st degree check
        elif a in self.adj [b]:
            return True
        
        # 2nd degree check
        return len (self.adj [a] & self.adj [b]) != 0 # see if their intersection is empty
    
    
    def if_lte_deg4 (self, pair):
        """
        Returns True if the pair is separated by 0, 1, 2, 3, or 4 degree and False otherwise.
        """
        a, b = pair
        
        # check if a & b are both in the graph
        if a not in self.adj.keys ():
            return False
        elif b not in self.adj.keys ():
            return False
        
        # 0th and 1st degree check
        elif a in self.adj [b]:
            return True
        
        # 2nd degree check
        elif len (self.adj [a] & self.adj [b]) != 0: # see if their intersection is empty
            return True
        
        # 3rd and 4th degree checks
        ffa = self.next_degree_friends (self.adj [a])  # friends of friends of a
        ffb = self.next_degree_friends (self.adj [b])  # friends of friends of b
        return len (ffa & ffb) != 0 # see if their intersection is empty
        
        
    def friends_of_friends (self, start):
        """
        Given a node, 'start,' outputs the set of nodes separated from 'start' by no more than a distance of 2.
        That is, the output set includes nodes of 0, 1, and 2 degrees of separation from 'start.'
        """
        assert start in self.adj.keys ()
        
        return self.next_degree_friends (self.adj [start])
    
    def is_equal_to (self, graph):
        return self.adj == graph.adj
    
    def degree_lte (self, pair, degree):
        """
        Tests if a given pair is separated by <= n degrees. Note: n can only be 0, 1, 2, or 4.
        Returns True/False.
        """
        assert degree in {0, 1, 2, 4}, "degree needs to be either 0, 1, 2, or 4."
        
        x, y = pair
        
        if degree == 0:
            return x == y
        elif degree == 1:
            return self.if_lte_deg1 (pair)
        elif degree == 2:
            return self.if_lte_deg2 (pair)
        else: # degree == 4
            return self.if_lte_deg4 (pair)
        
        # should not reach this return statement
        return None
    