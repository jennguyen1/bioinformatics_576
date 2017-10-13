__author__ = 'Nhuy'


from CS576.gene_annotation.gene_markov.predict_exons import *
from CS576.gene_annotation.gene_markov.viterbi_algorithm import *
from CS576.gene_annotation.gene_markov.markov_chain import *
from CS576.gene_annotation.gene_markov.markov_states import *

train = open('CS576/gene_annotation/small.train', 'r').read().splitlines()
mm = make_markov_chain(train)