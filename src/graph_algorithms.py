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
    13. if_lte_deg2 (self, pair)
    14. if_lte_deg4 (self, pair)
    15. is_inclusive (self)
    """
    
    
    def __init__ (self, adj_dict = {}):
        self.num_nodes = len (adj_dict.keys ())
        
        # exclusive 1st order adjacency list
        self.adj = adj_dict
        
        # 2nd order adjacency list
        self.adj2 = {}
        
        # build the 2 adjacency lists
        self.build_adj ()
            
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
        if a not in self.adj.keys () or b not in self.adj.keys ():
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
        Note: distance_lte "(if) distance is less than n."
        
        From adjacency list 'self.adj', this figures out whether the pair '(a, b)' are neighbors 
        of degree fewer than 'n.'

        If neighbors of degree <= n, outputs True; otherwise, False.
        """
        a, b = pair
        
        # check if a == b
        if a == b:
            return 0
        
        assert n >= 0, "Need a n >= 0"
        
        # check to see if both nodes are in graph
        if a not in self.adj.keys () or b not in self.adj.keys ():
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
        Adds an edge = (x, y) pair to the adjacency list self.adj and makes correction to self.adj2.
        """
        
        assert len (edge) == 2, "Each edge needs to be of length 2."

        x, y = edge
        
        # corrections to first order adjacency list
        # add y to x
        if x in self.adj:
            self.adj [x].add (y)
            self.adj2 [x].add (y)
        else: # x in neither adj nor adj2
            self.num_nodes += 1
            self.adj [x]  = {x, y}
            self.adj2 [x] = {x, y}
        
        # add x to y
        if y in self.adj:
            self.adj [y].add (x)
            self.adj [x].add (y)
        else: # y in neither adj nor adj2
            self.num_nodes += 1
            self.adj [y]  = {x, y}
            self.adj2 [y] = {x, y}

        # corrections to 2nd order adjacency list
        self.adj2 [x].update (self.adj [y])
        self.adj2 [y].update (self.adj [x])
        for key in self.adj [x]:
            self.adj2 [key].add (y)
        for key in self.adj [y]:
            self.adj2 [key].add (x)
    
    def is_self_consistent (self):
        """
        Checks graph for self-consistency by making sure that it is symmetric: For adjacency list 'adj_list' and
        any nodes x, y of G, y is in adj_list [x] iff x is in adj_list [y].
        """
        for adj_list in [self.adj, self.adj2]:
            for key in adj_list.keys ():
                for elem in adj_list [key]:
                    if key not in adj_list [elem]:
                        return False
        return True
    
    def build_adj (self):
        """
        Builds the inclusive 1st and 2nd order adjacency lists from the exclusive 1st order version.
        """
        # Make adj inclusive (just add the node itself to its adjacency list)
        for key in self.adj.keys ():
            self.adj [key].add (key)

        # Build inclusive 2nd order adjacency list by squaring the inclusive 1st order version
        for key in self.adj.keys ():
            tmp = set ()
            for node in self.adj [key]:
                tmp.update (self.adj [node])
            self.adj2 [key] = tmp
        
        
    def copy (self):
        res = Graph ()
        res.num_nodes = self.num_nodes
        res.adj  = self.adj.copy ()
        res.adj2 = self.adj2.copy ()
        return res

    def if_lte_deg2 (self, pair):
        a, b = pair

        if a == b:
            return True
        elif a not in self.adj.keys () or b not in self.adj.keys (): # >= one of (a, b) is not a node in graph 'adj'
            return False
        else:
            # since adj2 is inclusive, this will return true if dist(a,b) <= 2
            return a in self.adj2 [b]    


    def if_lte_deg4 (self, pair):
        a, b = pair

        if a == b:
            return True
        elif a not in self.adj.keys () or b not in self.adj.keys ():  # >= one of (a, b) is not a node in graph 'adj'
            return False
        elif a in self.adj2 [b]:  # a & b are deg 2 apart or fewer
            return True
        else:                # test if a & b are degs 3 or 4 apart
            for key in self.adj2 [b]:
                if a in self.adj2 [key]:
                    return True
            return False
    
    def is_inclusive (self):
        for key in self.adj.keys ():
            if key not in self.adj2 [key]:
                print ('key {} is not found in adj [key]'.format (key))
                return False
            if not self.adj [key].issubset (self.adj2 [key]):
                print ('adj [{}] is not a subset of adj [key]'.format (key))
                return False
        return True