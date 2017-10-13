__author__ = 'Nhuy'

from cluster_node import *

"""
Class to build a hierarchical cluster tree
"""
class cluster_build:

    def __init__(self, genes, link, k):
        # set the link and k clusters
        self.link = link
        self.k = k

        # build cluster
        self.clusters = self.hclust(genes)

        # collect leaves in the k clusters
        self.clusters = self.collect_leaves(self.clusters)

    def __repr__(self):
        return "Hierarchical cluster with " + str(self.k) + " clusters"

    """
    Function to merge two clusters, computes distance matrix and make a new cluster based off the min
    Parameters:
        clusters (array) of cluster nodes
        link (str) type of linkage
        cluster_id (int) identifier for new cluster
    """
    def clust(self, clusters, cluster_id):
        # initialize the distance matrix
        dist_matrix = [[10000]*len(clusters) for i in range(len(clusters))]

        # save the smallest value
        min_val = 10000
        imin = -1
        jmin = -1

        # fill out the distance matrix (lower half)
        for i in range(len(clusters)):
            j = i - 1
            while j >= 0:
                # compute pairwise distances b/n clusters
                pairwise_distances = clusters[i] - clusters[j]

                # fill out distance matrix depending on the link
                if self.link == "S":
                    d = min(pairwise_distances)
                elif self.link == "C":
                    d = max(pairwise_distances)
                elif self.link == "A":
                    d = float( sum(pairwise_distances) ) / len(pairwise_distances)

                dist_matrix[i][j] = d

                # save info regarding
                if d < min_val:
                    min_val = d
                    imin = i
                    jmin = j

                # decrement j
                j -= 1

        # make new cluster based off new information
        new_cluster = cluster_node(id = cluster_id)
        new_cluster.add_children(clusters[imin])
        new_cluster.add_children(clusters[jmin])
        new_cluster.set_height(min_val)

        # add new cluster union, remove unioned clusters
        clusters.append(new_cluster)
        clusters.remove(clusters[imin])
        clusters.remove(clusters[jmin])

    """
    Function to run hierarchical clustering
    Parameters:
        genes (array of arrays) each index should specify gene id, descr, expr ratios
        link (str) "S" for single, "C" for complete, "A" for average linkage
        k (int) number of clusters want to output
    Returns: array of cluster nodes, of length k
    """
    def hclust(self, genes):

        # initialize the leaf clusters based off the genes
        # 1st value is gene id, 2nd value is gene description, 3rd value is vector of expr values
        clusters = [cluster_node(g[0], g[1], map(float, g[2:])) for g in genes]

        # identifier for cluster merges
        i = len(clusters) + 1

        # run clustering algorithm until there is only k nodes left (specified by user
        while len(clusters) > self.k:
            # merge two nodes
            id = "cluster_" + str(i)
            self.clust(clusters, id)

            # increment
            i += 1

        # return clusters
        return clusters


    """
    Upper-Level Collect
    Parameters: clusters (array of cluster_nodes), should be k entries
    Returns: all_collect (array of leaf cluster_nodes), should be k entries
    """
    def collect_leaves(self, clusters):
        # initialize data for k clusters
        all_collect = []

        # loop through all clusters and collect the leaves from each cluster
        for c in clusters:
            # collection array for the leaves in cluster c
            collect = []

            # if node is a leaf node, add it to all collect
            if len(c.get_children()) == 0:
                all_collect.append([c])

            # if node is not a leaf node, recursively find all leaves in the cluster
            else:
                self.aux_collect_leaves(c.get_children()[0], collect)
                self.aux_collect_leaves(c.get_children()[1], collect)
                all_collect.append(collect)

        # return array of length k (num clusters specified), where each element are the leaves in that cluster
        return all_collect

    """
    Auxiliary recursive matrix to collect leaves
    Parameters:
        node (cluster_node) to extract from
        collect (array of cluster nodes) to collect different the various leaves
    Returns: returns nothing (collect is updated along the way)
    """
    def aux_collect_leaves(self, node, collect):
        # if the node has no children, it is a leaf node; add it to the collection array
        if len( node.get_children() ) == 0:
            collect.append(node)

        # if node has children, collect leaves from its two children
        else:
            self.aux_collect_leaves(node.get_children()[0], collect)
            self.aux_collect_leaves(node.get_children()[1], collect)

    """
    Prints the leaves in each cluster
    Parameters: clusters (array of cluster_nodes) corresponding to the leaves in each cluster; should be k entries
    Returns: returns nothing, prints out cluster info
    """
    def print_cluster_info(self):

        # initialize cluster printing order
        print_descr = []
        print_avr = []

        # loop through the k clusters
        for c in self.clusters:

            # initialize string to print
            s = ""

            # obtain the averages
            averages = [l.get_average() for l in c]

            # obtain the printing/looping order (sorted by average
            print_order = [a for a in averages]
            print_order.sort()

            # compute the cluster average (for later)
            cluster_average = float(sum(averages)) / len(averages)

            # loop through the leaves in each cluster
            for k in print_order:
                # finds the index of specified average, obtains the leaf from cluster, removes leaf from cluster
                index = averages.index(k)
                leaf = c[index]

                # save leaf and average
                s += leaf.get_id() + " " + "%.3f" % leaf.get_average()
                s += "\n"

            # save cluster averages & descriptions
            print_descr.append(s)
            print_avr.append( cluster_average )

        # obtain overall averages
        cluster_order = [a for a in print_avr]
        cluster_order.sort()

        # loop through clusters and prints data
        for i in cluster_order:
            # obtains index in order
            index = print_avr.index(i)

            # print description and average
            descr = print_descr[index]
            print descr[ : (len(descr) - 1)]
            print "%.3f" % print_avr[index]

            # print a dividing line
            print ""

