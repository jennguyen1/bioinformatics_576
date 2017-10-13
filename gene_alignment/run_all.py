__author__ = 'Nhuy'

import sys
from alignment.overlap_align import *

results = overlap_align(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]) )
print results[0]
print results[1]
print results[2]