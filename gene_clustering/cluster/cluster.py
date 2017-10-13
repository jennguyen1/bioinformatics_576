__author__ = 'Nhuy'

from cluster_build import *

def cluster(file_name, link, k):

    # open file info
    file = open(file_name, 'r')

    # save gene info
    genes = []

    # save data
    for l in file.readlines():
        # split up the columns
        cols = l.split('\t')
        cols[ len(cols) - 1 ] = cols[ len(cols) - 1 ].replace("\n", "")
        genes.append(cols)

    # close file
    file.close()

    # build cluster
    c = cluster_build(genes, link, k)

    # print cluster info
    c.print_cluster_info()

