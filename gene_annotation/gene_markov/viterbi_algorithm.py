__author__ = 'Nhuy'

"""
Runs viterbi algorithm for a given test sequence
"""
class viterbi_alg():

    """
    Saves incoming data (markov model and test sequence) and initialize DP matrices
    """
    def __init__(self, markov_model, test_seq):
        # save the incoming data
        self.markov_model = markov_model
        self.test_seq = test_seq

        # initialize the dp matrices
        L = len(test_seq) + 1
        self.dp_matrix_values = {i: [-1000000]*L for i in ["exon", "intron"]}
        self.dp_matrix_class = {i: [""]*L for i in ["exon", "intron"]}


    """
    Compute entry for either intron or exon
    Parameters:
        (state): string, intron or exon
        (current_char): string, the current base
        (prev_intron/prev_exon): double, value of previous entry
        (i): int, the position or base of the test seq
    Returns: fills out entry; returns nothing
    """
    def compute_one_entry(self, state, current_char, prev_intron, prev_exon, i):

        # initial of state (uppercase of first character
        state_initial = state[0].upper()

        # compute the emission probability for state
        emit = self.markov_model[state].get_emit_probs(current_char)

        # compute the probability of transmission from intron vs exon
        trans_from_i = prev_intron + self.markov_model['intron'].get_trans_probs(state_initial)
        trans_from_e = prev_exon + self.markov_model['exon'].get_trans_probs(state_initial)

        # combine probabilities of transition into an array
        incoming = [trans_from_i, trans_from_e]

        # find the most likely transition (max value)
        most_probable_incoming_value = max(incoming)

        # back compute to find the origin class of most likely transition
        if incoming[0] == most_probable_incoming_value:
            most_probable_incoming_class = "intron"
        else:
            most_probable_incoming_class = "exon"

        # save the probability for current position in test_seq
        self.dp_matrix_values[state][i] = emit + most_probable_incoming_value

        # save the most probable previous class
        self.dp_matrix_class[state][i] = most_probable_incoming_class


    """
    Computes the column entries for base i
    Parameters:
        (i): int, the ith column or base of test_seq
    Returns: fills column entries of dp_values and dp_class; returns nothing
    """
    def compute_col_entry(self, i):

        # find the ith character of test_seq
        current_char = self.test_seq[i - 1].upper()

        # find value of the previous entry
        prev_intron = self.dp_matrix_values['intron'][i - 1]
        prev_exon = self.dp_matrix_values['exon'][i - 1]

        # fill out entries for ith position of intron and exon
        self.compute_one_entry("intron", current_char, prev_intron, prev_exon, i)
        self.compute_one_entry("exon", current_char, prev_intron, prev_exon, i)


    """
    Fills the DP matrix
    Parameters: NA
    Returns: fills out the entire DP matrices; returns nothing
    """
    def make_dp_matrices(self):
        # computes the length of the matrix
        L = len(self.test_seq) + 1

        # loops through all columns and fills in DP matrix
        for i in range(L):
            # initialization
            if i == 0:
                self.dp_matrix_values['exon'][i] = 0

            # fill out 1st state
            elif i == 1:
                self.compute_col_entry(i)

                # the first entry cannot be an intron based on Fig2
                self.dp_matrix_values['intron'][i] = -1000000

            # fill out emitting states
            else:
                self.compute_col_entry(i)


    """
    Traceback to determine optimal states
    Parameters: NA
    Returns: saves string array, assignment of 'exon' or 'intron' to each base; returns nothing
    """
    def traceback(self):

        # compute index of last column entry of dp matrix
        last = len(self.test_seq)

        # set the current class to exon as defined by Fig2
        current = "exon"

        # initialize assignments
        self.assignments = []

        # loop through length of string and find the optimal states
        while last > 0:
            # add the current state to assignments
            self.assignments.insert(0, current)

            # obtain the next optimal state
            current = self.dp_matrix_class[current][last]

            # decrement the index
            last -= 1


    """
    Uses the assignments to save the sequence states
    Parameters: NA
    Returns: original string with states annotated
    """
    def print_string(self):

        # convert string to list for easier handling
        new_str = list(self.test_seq)

        # loops through string and assignments and makes the base upper case if it is an exon assignment
        for i in range(len(new_str)):
            if self.assignments[i] == "exon":
                new_str[i] = new_str[i].upper()

        # return the annotated sequence
        return ''.join(new_str)


    """
    Runs Viterbi algorithm, returns annotated string
    """
    def run_alg(self):
        self.make_dp_matrices()
        self.traceback()
        return self.print_string()


    """
    Test functions
    """
    def get_values(self):
        return self.dp_matrix_values

    def get_classes(self):
        return self.dp_matrix_class

