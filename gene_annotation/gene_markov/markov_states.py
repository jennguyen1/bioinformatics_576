__author__ = 'Nhuy'

import math

"""
A transition state
name: exon or intron
emit_probs: emission probabilities, dictionary of int for A, T, C, G
trans_probs: transition probabilities, dictionary of int for E (exon) and I (intron)
"""
class state:

    """ intialize all fields """
    def __init__(self, name):
        self.name = name
        self.emit_probs = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
        self.trans_probs = {'E': 0, 'I': 0}

    """ class representation is the state name """
    def __repr__(self):
        return self.name

    """
    Computes the emitting probability for the given state using laplace estimates
    Parameters:
        (str): string of all exon or intron train cases
        (char): the character (A/T/C/G) to compute probability of
    Returns: sets the emission probability, returns nothing
    """
    def compute_emit_probs(self, str, char):
        # compute denominator: length of string + 4 for laplace estimates
        denom = len(str) + 4

        # compute numerator: count the number of specified string + 1 for laplace estimates
        num = str.count(char) + 1

        # compute & set the maximum likelihood estimate for emission probability
        self.set_emit_probs(char, math.log(num / float(denom)))

    """
    Set emission probabilities
    Parameters:
        (char): A, T, C or G
        (value): the emission probability
    Returns: NA
    Throws an error if char is an invalid base
    """
    def set_emit_probs(self, char, value):
        if char in self.emit_probs.keys():
            self.emit_probs[char] = value
        else:
            raise Exception("Not a valid emitting character")

    """
    Gets emission probabilities
    Parameters: (char) A, T, C or G
    Returns: emission probability for char
    Throws an error if char is an invalid base
    """
    def get_emit_probs(self, char):
        if char in self.emit_probs.keys():
            return self.emit_probs[char]
        else:
            raise Exception("Not a valid emitting character")

    """
    Computes the transmission probabilities
    Parameters: (arr): array of dictionaries, corresponding to each train sequence string
    Returns: sets the transmission probability, returns nothing
    """
    def compute_trans_probs(self, arr):

        # self identify its own state (i for intron, e for exon
        current_state = self.name[0]

        # transitions to intron or exon - names to obtain data from arr
        trans_to_i = current_state + 'i'
        trans_to_e = current_state + 'e'

        # compute numerator: count the number of char transitions + 1 for laplace estimates
        numerator_to_i = sum([a[trans_to_i] for a in arr]) + 1
        numerator_to_e = sum([a[trans_to_e] for a in arr]) + 1

        # compute denominator: count total number of transitions + 2 for laplace estimates (already accounted for in numerator calc)
        denominator = numerator_to_i + numerator_to_e

        # if the state is an exon, account for the transition to "end"
        if self.name == 'exon':
            denominator += len(arr)

        # compute & set max likelihood estimate for transmission probability
        self.set_trans_probs('I', math.log(numerator_to_i / float(denominator)))
        self.set_trans_probs('E', math.log(numerator_to_e / float(denominator)))

    """
    Set transmission probabilities
    Parameters:
        (char): E or I
        (value): the transmission probability
    Returns: NA
    Throws an error if char is an invalid state
    """
    def set_trans_probs(self, char, value):
        if char in self.trans_probs.keys():
            self.trans_probs[char] = value
        else:
            raise Exception("Not a valid transmission chararacter")

    """
    Gets transmission probabilities
    Parameters: (char) E or I
    Returns: transmission probability for char
    Throws an error if char is an invalid state
    """
    def get_trans_probs(self, char):
        if char in self.trans_probs.keys():
            return self.trans_probs[char]
        else:
            raise Exception("Not a valid transmission character")

