__author__ = 'Nhuy'

# import files
from gene_markov.markov_chain import *
from gene_markov.viterbi_algorithm import *

"""
Predict exons using train & test data
Parameters: (train_file/test_file): string, file names containing train/test sequences
Returns: prints out the predicted annotations on test sequences
"""
def predict_exons(train_file, test_file):

    # open the train & test files
    train = open(train_file, 'r').read().splitlines()
    test = open(test_file, 'r').read().splitlines()

    # using train data, find max likelihoods, markov chain
    markov_model = make_markov_chain(train)

    # runs viterbi algorithm on test files
    for i in range(len(test)):
        model = viterbi_alg(markov_model, test[i])
        print model.run_alg()
