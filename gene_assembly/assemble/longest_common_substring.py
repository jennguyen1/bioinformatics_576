__author__ = 'Nhuy'

from assemble.Edges import *


"""
Auxiliary function to find longest common substring (lcs) b/n prefix of 1 string & suffix of another
Parameters: 2 strings
Returns: the lcs

Treats 1 string as the from string, takes suffixes from "from" string of increasing length and
finds matches in the "to" string. Saves the longest suffix that matches to the 0 position of the
to string.
"""
def aux_lcs(x, y):

    # initialize the position to begin the suffix of the from string, the looping parameter, and the lcs
    pos = len(x) - 1
    cont = True
    lcs = ""

    # loop to find the lcs
    while cont and pos >= 0:
        # obtain the suffix of the from string and search for a match in the to string
        match = y.find(x[pos:])

        # if there is no match, exit the loop with the current lcs
        if match == -1:
            cont = False
        # if there is a match and it starts at the beginning of the to string, save that suffix as lcs and continue search
        elif match == 0:
            lcs = x[pos:]
            pos -= 1
        # if there is not a match, decrement position to obtain a longer suffix; continue search
        else:
            pos -= 1

    # return the longest common substring
    return lcs

"""
Function to determine the longest common substring (lcs) b/n prefix of 1 string & suffix of the other
Parameters: 2 strings
Returns: an edge object if it exists
Complexity: O(n) in the worst case where n = max(len(str1), len(str2))
"""
def longest_common_substring(str1, str2):

    # find the longest common substring treating str1 as the from string, str2 as the to string and vice versa
    common_string_1 = aux_lcs(str1, str2)
    common_string_2 = aux_lcs(str2, str1)

    # save an edge object if the common string b/n the prefix/suffix of 2 strings contains letters
    if common_string_1 != "" or common_string_2 != "":
        # save the edge that corresponds to the largest common substring between the two strings
        if len(common_string_1) > len(common_string_2):
            edge = node_edge_node(str1, str2, common_string_1)
        else:
            edge = node_edge_node(str2, str1, common_string_2)
    else:
        edge = None

    # return the edge object
    return edge