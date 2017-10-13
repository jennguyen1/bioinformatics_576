__author__ = 'Nhuy'

"""
Structure to encapsulate the graph nodes
# Contains the node key, incoming/outcoming nodes and weights, and whether the node has been visited (for graph traversal)
"""
class Graph_Node:

    """
    Constructor:
    Parameters: string as key of the node (id)

    The rest of the node attributes are set to basic values
    """
    def __init__(self, id):
        self.id = id
        self.in_node = None
        self.out_node = None
        self.in_weight = 0
        self.out_weight = 0
        self.visited = False

    """
    Class representation: used in testing
    Returns: string describing the ids of the incoming node, current node, and outgoing node
    """
    def __repr__(self):
        s = ""
        if not self.in_node is None:
            s += "in: " + self.in_node.get_id()
        s += " " + self.id + " "
        if not self.out_node is None:
            s += "out: " + self.out_node.get_id()
        return s

    """
    Add Node Methods: add the node and set the weight
    Parameters: other node (graph node obj) and link weight (int)
    """
    def add_incoming(self, other_node, weight):
        self.in_node = other_node
        self.in_weight = weight

    def add_outgoing(self, other_node, weight):
        self.out_node = other_node
        self.out_weight = weight

    """
    Remove Node Methods: removes the node and resets the weight
    """
    def remove_incoming(self):
        self.in_node = None
        self.in_weight = 0

    def remove_outgoing(self):
        self.out_node = None
        self.out_weight = 0

    """
    Node Identification: get/set the id
    """
    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    """
    Retrieval Methods: get information regarding the incoming/outgoing nodes
    """
    # Returns: incoming/outgoing nodes
    def get_incoming(self):
        return self.in_node

    def get_outgoing(self):
        return self.out_node

    # Returns: how many incoming/outgoing nodes the current node is linked to
    def in_degree(self):
        return (not self.in_node is None) + 0

    def out_degree(self):
        return (not self.out_node is None) + 0

    # Returns: the weight of the incoming/outgoing linkages
    def get_in_weight(self):
        return self.in_weight

    def get_out_weight(self):
        return self.out_weight

    """
    Visit Status Methods: get/set node visit status (used for graph traversals)
    """
    def is_visited(self):
        return self.visited

    def set_visited(self, visited):
        if not isinstance(visited, bool):
            raise Exception("invalid value")
        else:
            self.visited = visited

"""
Graph structure to hold the string relationships
"""
class Graph:

    """
    Constructor:
    initiates a dictionary to hold the graph nodes
    """
    def __init__(self):
        self.nodes = {}
        self.n_nodes = 0

    # retrieval methods ###########

    # returns node if it exists or raises an exception
    """
    Node retrieval methods
    """

    # Parameters: string, id of node to obtain
    # Returns: graph node object
    def get_node(self, id):
        # exception handling in case the node does not exist
        try:
            return self.nodes[id]
        except KeyError:
            raise Exception("node does not exist")

    # Returns: dictionary object of all graph nodes
    def get_all_nodes(self):
        return self.nodes

    """
    Insertion Methods: node and links
    """
    # Parameters: string, id for the new graph node
    # Adds node to the dictionary where the key is the new node's id
    # There should be no duplicate ids - throws an exception if this is the case
    def add_node(self, id):
        new_node = Graph_Node(id)
        if new_node.get_id() in self.nodes.keys():
            raise Exception("duplicated id")
        else:
            self.nodes[ new_node.get_id() ] = new_node
            self.n_nodes += 1

    """
    Link Methods: for linking nodes
    """
    # Add links
    # Parameters: 2 strings, from id, to id as strings; 1 int as weight
    def add_link(self, from_id, to_id, weight):
        # finds the node
        from_node = self.get_node(from_id)
        to_node = self.get_node(to_id)

        # adds the links
        from_node.add_outgoing( to_node, weight )
        to_node.add_incoming( from_node, weight )

    # Removes link
    # Parameters: 2 strings, id of from node and id of to node
    def remove_link(self, from_id, to_id):
        # finds the node
        from_node = self.get_node(from_id)
        to_node = self.get_node(to_id)

        # remove the link
        from_node.remove_outgoing()
        to_node.remove_incoming()

    """
    Visit status: resets all visit statuses to False
    """
    def set_all_not_visited(self):
        for k in self.nodes.keys():
            self.nodes[k].set_visited(False)

    """
    Other Graph Methods
    """
    # Checks if graph is connected: conducts a 2-way dfs on every key, returns True if all nodes are visited after dfs for each node
    # Returns: boolean, whether the graph is weakly connected
    def is_weak_connected(self):

        # for every key: reset visit status of all nodes, run a 2-way dfs, check whether all nodes have been visited
        for k in self.nodes.keys():
            self.set_all_not_visited()
            dfs(self, k, True)
            not_connected = [n.get_id() for k, n in self.nodes.items() if not n.is_visited()]
            # if a node is connected to all other nodes, breaks loop and return False
            if len(not_connected) != 0:
                return False

        # if made it through the loop, then all nodes are connected - return True
        return True

    # Checks if there is a path between two nodes - used to detect a cycle
    # Parameters: 2 strings, from node id and to node id
    # Returns: whether there is a path from "from" node to "to" node
    def is_path(self, from_id, to_id):
        # throws exception if want to find a path to itself
        if(from_id == to_id):
            raise Exception("from and to cannot be the same")

        # resets visit status of all nodes and run a 1-way dfs from "from" node
        self.set_all_not_visited()
        dfs(self, from_id, False, to_id)

        # returns whether the to node is visited
        return self.get_node(to_id).is_visited()

# graph traversals: returns an array of keys referring to nodes that have not been visited
# depth first search using preceders and sucessors for weak connections
"""
Graph Traversal: depth-first search
Parameters:
    graph object;
    start_id as a string coding the node to start from;
    boolean two_way whether to traverse incoming and outgoing nodes;
    end_id as a string to stop traversal once it hits a certain node (default is None) (used in 1-way dfs only)
Note: the start_id and the end_id cannot be the same
Returns: Nothing, if end_id is supplied, will break the function early

Depth breadth search to traverse a node and set visited nodes as "visited". Option to do 2-way dfs: traverse in both
directions - useful for determine weak connectivity. Option to exit at an end_id - useful for determining path,
computationally efficient if there are a lot of nodes, only available in 1-way searches.
"""
def dfs(graph, start_id, two_way, end_id = None):
    # initialize the stack, will set visit status to True before adding to stack
    s = []

    # find the start node and add it to stack
    start_node = graph.get_node(start_id)
    start_node.set_visited(True)
    s.append(start_node)

    # traverse graph
    while len(s) != 0:
        # retrieves top of stack
        current = s.pop()

        # if two_way option is set to True, will add incoming nodes to stack
        if two_way:
            # adds incoming nodes from current to stack if the node exists
            node = current.get_incoming()
            if not node is None:
                # if node hasn't been visited, set it as visited and add to stack
                if not node.is_visited():
                    node.set_visited(True)
                    s.append( node )

        # adds outgoing nodes from current to stack if node exists
        node = current.get_outgoing()
        if not node is None:
            # if node hasn't been visited, set it as visited and add to stack
            if not node.is_visited():
                node.set_visited(True)
                s.append( node )
                # if option is set to stop at a certain node and arrive at that node, then quit dfs
                if not end_id is None and end_id == node.get_id():
                    return