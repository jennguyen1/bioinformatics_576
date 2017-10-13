__author__ = 'Nhuy'

"""
Import Auxiliary Classes & Methods
"""
from assemble.Queue import *
from assemble.Graph import *

"""
Greedy Assemble Method:
Parameters: string, file_name containing the reads
"""
def greedy_assembly(file_name):

    """
    Opens the file containing the reads
    """
    reads = open(file_name, 'r').read().splitlines()

    """
    Add reads to a queue
    """
    q = Priority_Queue()
    # loop through reads and adds all unique pairwise comparisons of reads to the queue
    for i in range( len(reads) ):
        j = i + 1
        while(j < len(reads)):
            # enqueue method will add only if the longest common substring (lcs) is 1 character or longer;
            # method will determine which of the strings are the "from" and "to strings
            q.enqueue(reads[i], reads[j])
            j += 1


    # make the graph
    """
    Generate graph and add reads
    """
    # initialize graph and add reads as nodes
    g = Graph()
    for r in reads:
        g.add_node(r)

    """
    Using Hamiltonian path to generate string:
    """

    """
    while graph is disconnected
    """
    while not g.is_weak_connected():
        """
        pop off the next edge e = (u,v) off the queue; this edge has the greatest weight (length of lcs)
        """
        edge = q.dequeue()

        # obtain u, v the two reads
        from_id = edge.get_from_node()
        to_id = edge.get_to_node()

        # obtain the node in graph corresponding to u, v
        from_node = g.get_node(from_id)
        to_node = g.get_node(to_id)

        # obtain the weight between the u, v edge
        weight = edge.get_weight()

        """
        Part 1:
        adds edge to graph if outdegree(u) == 0, indegre(v) == 0 and
        e does not create a cycle (there is not a path from "to" node to "from" node

        Part 2:
        implements the tiebreaker for edges with the same weights, using lexicographical ordering:
        # if the from node is already connected and the to node is not yet connected, the edge in question
        # might be a better fit, lexicographically

        # if the to_node is already connected, then it was connected with greater priority to another node,
        # don't replace it
        """

        if from_node.out_degree() == 0 and to_node.in_degree() == 0 and not g.is_path(to_id, from_id):
            g.add_link(from_id, to_id, weight)

        elif from_node.out_degree() == 1 and to_node.in_degree() == 0:
            # obtain the current to node from the "from" node, its id, and weight of that linkage
            current_node = from_node.get_outgoing()
            current_to_id = current_node.get_id()
            current_to_weight = current_node.get_in_weight()

            # if the two nodes in question have the same weights and the to_id comes before current_to_id lexicographically
            # then replace the current_to_node with the to_node
            if weight == current_to_weight and current_to_id > to_id:
                g.remove_link(from_id, current_to_id)
                g.add_link(from_id, to_id, current_to_weight)

    """
    Tie the string together by traversing the graph
    """
    # get a node
    a_key = g.get_all_nodes().keys()
    start_node = g.get_node(a_key[0])

    # initialize the sequence
    seq = start_node.get_id()

    # proceed forward from start_node until there are no more nodes, adding each node's value to the return seq
    current = start_node
    while not current.get_outgoing() is None:
        current = current.get_outgoing()
        weight = current.get_in_weight()
        id = current.get_id()
        # the weight is # of overlap chars, which is removed from the prefix of the "to" string
        # so that it can be combined to the seq
        seq += id[weight : ]

    # proceed backwards from start_node until there are no more nodes, adding each node's value to the return seq
    current = start_node
    while not current.get_incoming() is None:
        current = current.get_incoming()
        weight = current.get_out_weight()
        id = current.get_id()
        # the weight is # of overlap chars, which is removed from suffix of the "from" string
        # so that it can be combined to the seq
        seq = id[ : len(id) - weight] + seq

    """
    Return the assembled sequence
    """
    return seq
