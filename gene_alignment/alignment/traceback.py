__author__ = 'Nhuy'

from alignment.score_computation import *

"""
Finds the best alignment following generation of DP matrices

Parameters: matrices (dictionary of 3 DP matrices)

Returns: name of the matrix (str), row and column (int) that corresponds to the best score
"""
def best_align(matrices):

    # find the last row - in which we will look for the best alignment
    row = len(matrices['m']) - 1

    # obtain the last rows of each matrix and store values in a dict
    last_rows = { k: v[row] for k,v in matrices.items() }

    # obtain the maximum value of each row and store the values in a dict
    max_per_matrix = { k: max(v) for k,v in last_rows.items() }

    # compute the best score from the max of each row of each matrix
    best_score = max( max_per_matrix.values() )

    # find the original matrix containing the best score - finds the key that best score corresponds to in max_per_matrix
    best_matrix = [ k for k,v in max_per_matrix.items() if v == best_score ].pop()

    # obtains the column of the best score by finding best score in the last rows
    col = last_rows[best_matrix].index(best_score)

    # returns the name of the best matrix, the row and column of the best alignment score
    return best_matrix, row, col

"""
Traceback 1 step based on score of current position

Parameters:
- matrices: dictionary of 3 DP matrices
- current_score: (int) current score, to match to traceback
- current_matrix, current_row, current_col: (str, 2 int) current position
- s, gap, space: (int) scores

Returns: next matrix (str), row and column (int) corresponding to best score
"""
def back_step(matrices, current_score, current_matrix, current_row, current_col, s, gap, space):

    # traceback depends on what the current start matrix is
    # depending on the current matrix, find the next position in traceback
    if current_matrix == "m":
        compute_scores = compute_m

        next_row = current_row - 1
        next_col = current_col - 1

    elif current_matrix == "ix":
        compute_scores = compute_ix

        next_row = current_row - 1
        next_col = current_col

    else:
        compute_scores = compute_iy

        next_row = current_row
        next_col = current_col - 1

    # compute all possible scores that could have led to current score
    possible_scores = compute_scores(matrices, current_row, current_col, s, gap, space)

    # obtain the name of the next matrix in traceback based on matching scores
    # the keys of possible_scores are ['iy', 'ix', 'm], so by popping, we always obtain them in the order specified (m, ix, iy) priority
    next_matrix = [k for k,v in possible_scores.items() if v == current_score].pop()

    # return the next matrix, next row and next column in traceback
    return next_matrix, next_row, next_col

"""
Traceback through all 3 matrices

Parameters:
- matrices: dictionary of 3 DP matrices
- str1, str2: (str) strings to compare
- current_matrix, current_row, current_column: (str, 2 int) current position
- match, mismatch, gap, space: (int) scores

Returns: (str) strings with alignment and gaps
"""
def traceback(matrices, str1, str2, current_matrix, current_row, current_col, match, mismatch, gap, space):

    # intialize the strings, saves the portions of the string that come after the best alignment
    # reverses the string so we can easily add to it (will un-reverse later
    str_x = str1[current_row + 1 : ][::-1]
    str_y = str2[current_col + 1 : ][::-1]

    # add the character that corresponds to the best alignment
    str_x += str1[current_row]
    str_y += str2[current_col]

    # to start the current matrix, row, column correspond to the best score in the last row
    # continues through the loop until we reach the upper left corner of the DP matrix
    while not current_row == current_col == 0:
        # obtains the score corresponding to the current matrix, row & column
        current_score = matrices[current_matrix][current_row][current_col]

        # compute the match/mismatch function
        s = compute_s(str1, str2, current_row, current_col, match, mismatch)

        # find the next matrix, row, column in traceback
        current_matrix, current_row, current_col = back_step(matrices, current_score, current_matrix, current_row, current_col, s, gap, space)

        # if the matrix is M, then the best alignment is x (in str1) aligned to y (in str2)
        if current_matrix == "m":
            str_x += str1[current_row]
            str_y += str2[current_col]

        # if the matrix is Iy, then the best alignment is a gap (in str1) aligned to y (in str2)
        elif current_matrix == "iy":
            str_x += " "
            str_y += str2[current_col]

        # if the matrix is Ix, then the best alignment is x (in str1) aligned to a gap (in str2)
        elif current_matrix == "ix":
            str_x += str1[current_row]
            str_y += " "

    # reverse the order of the string, remove the first character (which is a space)
    str_x = str_x[::-1][1:]
    str_y = str_y[::-1][1:]

    # reformat string by adding the '-' where appropriate
    # s1 argument is the string in which its suffix is aligned to the other string
    if str_x[0] != " ":
        str_x, str_y = str_reformat(str_x, str_y)

    if str_y[0] != " ":
        str_y, str_x = str_reformat(str_y, str_x)

    # return two strings, aligned
    return str_x, str_y

"""
Replace the spaces with actual gaps ('-')

Parameters: 2 strings
- s1: string where its suffix is aligned
- s2: string where its prefix is aligned

Returns: 2 strings with spaces replaced with gaps where appropriate
"""
def str_reformat(s1, s2):
    # removes leading & trailing spaces from first string
    s1.strip()

    # turn other string into a list - to replace spaces with '-'
    s2 = list(s2)

    # loop over the entire string
    replace = False
    for i in range(len(s2)):

        # replace the space (between two sequences) to a gap
        if s2[i] == " " and replace:
            s2[i] = "-"

        # set replace to true, once it reaches the first nonspace character, set replace to True so that all spaces
        # after is replace with a gap. (The initial space characters are to align the second string to the first)
        if s2[i] != " ":
            replace = True

    # turn s1 into a list
    s1 = list(s1)

    # loop over entire string
    for j in range(len(s1)):

        # replace all spaces with gap spaces; leading and trailing spaces are removed prior to this
        if s1[j] == " ":
            s1[j] = "-"

    # return both strings
    return "".join(s1), "".join(s2)