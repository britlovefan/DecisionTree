import os.path
from operator import xor
from parse import *

# DOCUMENTATION
# ========================================
# parse - takes a filename and returns attribute information and all the data in array of arrays
#         This function also rotates the data so that the 0 index is the winner attribute, and returns
#        corresponding attribute metadata
#
# Note: nominal data are integers while numeric data consists of floats

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
# For test see grader