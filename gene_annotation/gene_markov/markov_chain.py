__author__ = 'Nhuy'

from gene_markov.markov_states import *

"""
Compute the number of different transitions
Parameters: (str) a string, individual train cases
Returns: a dictionary, with counts of each type of transition
"""
def compute_trans_n(str):
    # initialize counts of transitions at 0
    ee = 0
    ei = 0
    ii = 0
    ie = 0

    # loop through the string and counts the types of transitions
    for i in range(len(str) - 1):
        # original position is an exon
        if str[i] == "E":
            # next position is an exon
            if str[i + 1] == "E":
                ee += 1
            # next position is an intron
            else:
                ei += 1
        # original position is an intron
        else:
            # next position is an intron
            if str[i + 1] == "I":
                ii += 1
            # next position is an exon
            else:
                ie += 1

    # return the counts for str
    return{'ee': ee, 'ei': ei, 'ii': ii, 'ie': ie}


"""
Map an individual base to either transition states
Parameters: (c) a single character base
Returns: the state
"""
def map_to_state(c):
    # map to "E" for exon
    if c.isupper():
        return "E"
    # map to "I" for intron
    else:
        return "I"


"""
Compute maximum likelihood estimates
- create markov model
"""
def make_markov_chain(seq):

    """
    Conditional emission probabilities
    """
    # join all sequences into 1 string
    all_seq = ''.join(seq)

    # extract all uppercase characters
    all_upper = filter(str.isupper, all_seq)

    # extract all lower cases
    all_lower = filter(str.islower, all_seq).upper()

    # create the exon state with the max likelihood estimates for emission
    exon = state("exon")
    [exon.compute_emit_probs(all_upper, C) for C in ["A", "T", "C", "G"]]

    # create the intron state with the max likelihood estimates for emission
    intron = state("intron")
    [intron.compute_emit_probs(all_lower, C) for C in ["A", "T", "C", "G"]]

    """
    Conditional Transmission Probabilities
    """

    # for transition probabilities, the individual characters are uninformative,
    # convert them all to 'E' (exon) or 'I' (intron) for easier handling
    mapped_seq = [''.join(map(map_to_state, S)) for S in seq]

    # counts the number of transitions for each transition type (exon -> exon, exon -> intron, intron -> intron, intron-> exon)
    trans_n = [compute_trans_n(S) for S in mapped_seq]

    # loops through all possible transition types, computes and sets transmission probabilities
    exon.compute_trans_probs(trans_n)
    intron.compute_trans_probs(trans_n)

    # save the markov chain
    markov_chain = {'exon': exon, 'intron': intron}

    # return markov chain
    return markov_chain

