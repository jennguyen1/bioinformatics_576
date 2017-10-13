__author__ = 'Nhuy'

from alignment.dp_matrix import *
from alignment.traceback import *

"""
Outputs the optimal overlap alignment b/n prefix and suffix of two strings

Parameters:
- file: (str) for file containing the two strings
- match_score, mismatch_score, gap_score, space_score: (int) scores for algorithm

Returns:
"""
def overlap_align(file, match_score, mismatch_score, gap_score, space_score):

    # save the sequences
    sequences = open(file, 'r').read().splitlines()

    # adds a space before each sequence so the DP matrix is made accurately
    str1 = " " + sequences[0]
    str2 = " " + sequences[1]

    # generate the 3 DP matrices and stores it as a matrix
    matrices = make_matrices(str1, str2, match_score, mismatch_score, gap_score, space_score)

    # finds location of best alignment
    start_matrix, start_row, start_col =  best_align(matrices)

    # obtain the best score
    best_score = matrices[start_matrix][start_row][start_col]

    # given the best alignment score, traceback to obtain two strings
    x,y = traceback(matrices, str1, str2, start_matrix, start_row, start_col, match_score, mismatch_score, gap_score, space_score)

    # return the two aligned strings and the best score
    return x, y, best_score
