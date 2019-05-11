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
    9. is_self_consistent (self)
    10. build_higher_order_adj_lists (self)
    11. copy (self)
    """
    
    
    def __init__ (self, adj_dict = {}):
        self.num_nodes = len (adj_dict.keys ())
        
        # exclusive 1st order adjacency list
        self.adj = adj_dict
        
        # inclusive higher order adjacency lists
        self.adj_1 = {}
        self.adj_2 = {}
        self.adj_4 = {}
            
    def __str__ (self):
        return str (self.adj)
    
    def __repr__ (self):
        return self.__str__ ()
    
    
    def next_degree_friends (self, friends):
        """
        Given a set of ids, 'friends,' this function outputs a new list of ids of
        degree 1 separated from any element in 'friends' as according to the adjacency
        list 'self.adj_1.'
        """
        if not isinstance (friends, set):
            friends = set (friends)
#        assert isinstance (friends, set), "function next_degree_friends requires that parameter 'friends' be a set."

        friends_of_friends = set ()  # initialize as empty set

        # add to the set 'friends_of_friends' the neighbors of all elements of set 'friends.'
        for x in friends:
            friends_of_friends.update (self.adj_1 [x]) # A.update (B) is the same as A union B

        return friends_of_friends


    def distance (self, a, b, n = -1):
        """
        From adjacency list 'self.adj_1', this figures out whether 'a' and 'b' are neighbors 
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
            n = self.num_nodes
        
        # check to see if both nodes are in graph
        if a not in self.adj_1.keys () or b not in self.adj_1.keys ():
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
        
        From adjacency list 'self.adj_1', this figures out whether 'a' and 'b' are neighbors 
        of degree fewer than 'n.'

        If neighbors of degree <= n, outputs True; otherwise, False.
        """
        # check if a == b
        if a == b:
            return 0
        
        assert n >= 0, "Need a n >= 0"
        
        # check to see if both nodes are in graph
        if a not in self.adj_1.keys () or b not in self.adj_1.keys ():
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
        to node 'start' as according to the adjacency list 'self.adj_1.'

        Outputs a list 'deg,' where the n-th element is a set containing all nodes of degree of
        separation 'n' away from node 'start'. If node 'elem' is degree 2 away from node
        'start,' then 'elem' will be contained in the set 'deg [2]' and no other.

        The optional parameter 'upto' is to indicate how many degrees of separation to search up to.
        If a negative integer is provided, it will attempt to travers the entire graph as provided
        by the adjacency list 'self.adj_1.'
        
        If 'start' is not in 'self.adj_1,' then return empty list
        """
        
        # check to see if both nodes are in graph
        if start not in self.adj_1.keys ():
            return []

        # Requires that start be a node in adj_dict, else throw exception
        assert start in self.adj_1.keys (), "node start is a node in self.adj_1."

        # If upto is negative, replace w/ the total number of nodes in 'adj_dict.'
        if upto < 0:
            upto = self.num_nodes

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
        Adds an edge = (x, y) pair to the adjacency list self.adj_1.
        """
        
        assert len (edge) == 2, "Each edge needs to be of length 2."

        x, y = edge

        # add y to x
        if x in self.adj:
            self.adj [x].add (y)
        else:
            #print ('New node ', x, 'graph length: ', self.num_nodes)
            self.num_nodes += 1
            self.adj [x] = {y}

        if y in self.adj:
            self.adj [y].add (x)
        else:
            #print ('New node ', y, 'graph length: ', self.num_nodes)
            self.num_nodes += 1
            self.adj [y] = {x}

    
    def is_self_consistent (self):
        """
        Checks graph for self-consistency by making sure that it is symmetric: For adjacency list 'adj_list' and
        any nodes x, y of G, y is in adj_list [x] iff x is in adj_list [y].
        """
        for adj_list in [self.adj, self.adj_1, self.adj_2, self.adj_4]:
            for key in adj_list.keys ():
                for elem in adj_list [key]:
                    if key not in adj_list [elem]:
                        return False
        return True
    
    def build_adj (self):
        """
        Builds the inclusive adjacency list from the exclusive version.
        """
        # just add the node itself to its adjacency list
        for key in self.adj.keys ():
            self.adj_1 [key] = {key} | self.adj [key]
    
    def build_higher_order_adj_lists (self):
        self.adj_2 = next_order_adj_list (self.adj_1)
        self.adj_4 = next_order_adj_list (self.adj_2)
        
    def copy (self):
        res = Graph ()
        res.num_nodes = self.num_nodes
        res.adj_1 = self.adj_1.copy ()
        res.adj_2 = self.adj_2.copy ()
        res.adj_4 = self.adj_4.copy ()
        return res
        
def next_order_adj_list (adj_list):
    next_adj_list = {}
    for key in adj_list.keys ():
        tmp = set ()
        for node in adj_list [key]:
            # inclusive higher order adjacency list (e.g. if H is a 2nd-order
            # adjacency list, then for node x of graph G, H [x] is the set of
            # nodes separated from node x by degrees 1 and 2.
            tmp.update (adj_list [node])
            
            # exclusive higher order adjacency version
            # tmp.update (adj_list [node] - adj_list [key])
        next_adj_list [key] = tmp
    return next_adj_list