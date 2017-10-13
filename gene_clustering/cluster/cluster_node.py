__author__ = 'Nhuy'

import math

"""
Compute euclidian distance b/n two entities
"""
def euclidian_distance(x, y):
    diff = [(x[i] - y[i])**2 for i in range(len(x))]
    distance = math.sqrt(sum(diff))
    return distance

"""
Cluster node class for clustering tree
"""
class cluster_node:

    """
    Initialize class
    If the node is a leaf:
        Parameters: gene id & descr (str); data (array)
    If the node is a not a leaf:
        Parameters: none

    Initialize the height, children/data, id
    """
    def __init__(self, id = "", descr = "", data = []):
        # if node is a leaf, save id and description in an array
        self.id = [id, descr]
        # initialize height, children, data, expression averages from all leaves
        self.height = 0
        self.children = []
        self.data = []
        self.average = 0
        # if the node is a leaf, save data and compute its average expression ratio
        if len(data) > 0:
            self.data.append(data)
            self.average = float(sum(data)) / len(data)

    """
    String representation for node
    """
    def __repr__(self):
        return ":".join(self.id)

    """
    Set & get children nodes & obtain data (leaves)
    """
    def add_children(self, child):
        # add child
        self.children.append(child)

        # add child's data (all the leaf nodes)
        for d in child.get_data():
            self.data.append(d)

    def get_children(self):
        return self.children

    """
    Height functions: set and get
    """
    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    """
    Get data: obtain all leaf node data
    """
    def get_id(self):
        return " ".join(self.id)

    def get_data(self):
        return self.data

    def get_average(self):
        return self.average

    """
    Compute all pairwise distances between two clusters
    """
    def __sub__(self, other_node):

        # obtain data
        d1 = self.get_data()
        d2 = other_node.get_data()

        # initialize distances
        distances = []

        # loop through leaves in self
        for i in range(len(d1)):
            # loop through leaves in other
            for j in range(len(d2)):
                # compute the distance between the two
                d = abs( euclidian_distance(d1[i], d2[j]) )
                distances.append( d )

        # return all pairwise distances between two clusters
        return distances
