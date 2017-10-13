__author__ = 'Nhuy'

"""
Compute the score of an alignment

Parameters:
- str1, str2: (str) the two strings to compare
- str1_i, str2_i: (int) index referring to the character in the string to compare
- match, mismatch: (int) scores

Returns: (int) score of the alignment
"""
def compute_s(str1, str2, str1_i, str2_i, match, mismatch):
    # assign s to the correct score depending on the character comparison
    if str1[str1_i] == str2[str2_i]:
        s = match
    else:
        s = mismatch

    # return score
    return s

"""
Computes the 3 possible scores for the M matrix (best score given that x is aligned to y)

Parameters:
- matrices: (dict) dictionary of matrices that contain the M, Ix, Iy matrices
- row, col: (int) row and column with which we want to compute the score of
- s, gap, space: (int) scores

Returns: dictionary w/ 3 possible score values
"""
def compute_m(matrices, row, col, s, gap, space):

    # compute values, named by the matrix the score is derived
    m = matrices['m'][row - 1][col - 1] + s
    ix = matrices['ix'][row - 1][col - 1] + s
    iy = matrices['iy'][row - 1][col - 1] + s

    # return possible scores
    return {'m': m, 'ix': ix, 'iy': iy}

"""
Computes the 3 possible scores for the Ix matrix (best score given that x is aligned to a gap)

Parameters:
- matrices: (dict) dictionary of matrices that contain the M, Ix, Iy matrices
- row, col: (int) row and column with which we want to compute the score of
- s, gap, space: (int) scores

Returns: dictionary w/ 3 possible score values
"""
def compute_ix(matrices, row, col, s, gap, space):

    # compute values, named by the matrix the score is derived
    m = matrices['m'][row - 1][col] + gap + space
    ix = matrices['ix'][row - 1][col] + space

    # based on the instructions, all Ix(i, 0) values are initialized to 0
    if col == 0:
        ix = 0

    # return possible scores
    return {'m': m, 'ix': ix}

"""
Computes the 3 possible scores for the Iy matrix (best score given that y is aligned to a gap)

Parameters:
- matrices: (dict) dictionary of matrices that contain the M, Ix, Iy matrices
- row, col: (int) row and column with which we want to compute the score of
- s, gap, space: (int) scores

Returns: dictionary w/ 3 possible score values
"""
def compute_iy(matrices, row, col, s, gap, space):

    # compute values, named by matrix the score is derived
    m = matrices['m'][row][col - 1] + gap + space
    iy = matrices['iy'][row][col - 1] + space

    # return the possible scores
    return {'m': m, 'iy': iy}
