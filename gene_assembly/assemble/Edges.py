__author__ = 'Nhuy'

"""
Structure to encapsulate the edges
# Contains the from_node and to_node as strings and
# the edge (ie longest common substring) as a string
"""
class node_edge_node:

    """
    Constructor:
    Parameters: 3 strings, the "from" string, the "to" string and the edge signifying the overlap
    """
    def __init__(self, from_str, to_str, edge):
        self.from_str = from_str
        self.to_str = to_str
        self.edge = edge

    """
    Class representation: used in testing
    Returns: string describing the from node, to node, and edge
    """
    def __repr__(self):
        return self.from_str + " " +  self.to_str + " " + self.edge

    """
    Retrieve weight of the edge: used in determining priority
    Returns: the length of the edge string, ie the length of overlap between "from" and "to"
    """
    def get_weight(self):
        return len(self.edge)

    """
    Retrieval Methods
    Returns: "from" string, "to" string, or edge string depending on method
    """
    def get_from_node(self):
        return self.from_str

    def get_to_node(self):
        return self.to_str

    def get_edge(self):
        return self.edge

    """
    Comparison methods for edges: compares the weights of the edges (length of longest overlap)
    """
    def __eq__(self, other_node):
        return self.get_weight() == other_node.get_weight()

    def __lt__(self, other_node):
        return self.get_weight() < other_node.get_weight()

    def __gt__(self, other_node):
        return self.get_weight() > other_node.get_weight()
