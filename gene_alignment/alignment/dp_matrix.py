__author__ = 'Nhuy'

from alignment.score_computation import *

"""
Generate the 3 DP matrices (M, Ix, Iy)

Parameters:
- str1, str2: (str) the two strings to compare
- match_score, mismatch_score, gap, space: (int) scores for match, mismatch, gap, space

Returns: a dictionary containing the 3 matrices (M, Ix, Iy)
"""
def make_matrices(str1, str2, match_score, mismatch_score, gap, space):

    # pre-compute the dimensions for the 3 matrices
    nrow = len(str1)
    ncol = len(str2)

    # initialize the matrices with an infinitely small (negative) number
    matrices = {'m': [[-100000]*ncol for i in range(nrow)], 'ix': [[-100000]*ncol for i in range(nrow)], 'iy': [[-100000]*ncol for i in range(nrow)]}

    # loop over the rows and columns and computes the score for each position
    for i in range(nrow):
        for j in range(ncol):
            # initialize the matrices (edges)
            if i == 0:
                matrices['iy'][i][j] = gap + space * j
            if j == 0:
                matrices['ix'][i][j] = 0
            if i == j == 0:
                matrices['m'][i][j] = 0

            # for all other locations compute the score of each cell using global alignment DP for the affine gap penalty
            if i != 0 and j != 0:
                # compute s, the match/mismatch score
                s = compute_s(str1, str2, i, j, match_score, mismatch_score)

                # compute value for m
                matrices['m'][i][j] = max( compute_m(matrices, i, j, s, gap, space).values() )

                # compute value for ix
                matrices['ix'][i][j] = max( compute_ix(matrices, i, j, s, gap, space).values() )

                # compute value for iy
                matrices['iy'][i][j] = max( compute_iy(matrices, i, j, s, gap, space).values() )

    # return the 3 matrices in a dictionary
    return matrices