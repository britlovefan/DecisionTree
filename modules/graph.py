from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
import random
import numpy as np

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct, depth,iterations):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    
    if int(len(train_set)*pct) == 0:
        return 0
    else:
        examples_list = []
        for i in range(iterations):
            examples = random.sample(train_set, int(len(train_set)*pct))
            examples_list.append(examples)
    acc = 0
    for x in examples_list:
        tree = ID3(x, attribute_metadata, numerical_splits_count, depth)
        acc += validation_accuracy(tree, validate_set)
    
    return acc/iterations

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts, depth):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''

    array_origin = []
    acc_origin = 0
    acc_pruned = 0
    acc_origin += get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pcts, depth,iterations)     
    array_origin.append(acc_origin)
    return array_origin

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    x = np.linspace(lower, upper, int((upper - lower) / increment) + 1).tolist()
    #print x,len(x)
    origin = []
    #print iterations
    for pct in x:
        array_origin = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pct, depth)
        origin.append(array_origin)
    #print origin
    #plt.plot(x, pruned, 'k-x', label='pruned')
    plt.plot(x, origin, 'r-o', label='origin')
    plt.title('Learning Curve')    
    plt.xlabel('percentage')
    plt.ylabel('Accuracy')
    plt.legend(loc=4)
    plt.savefig('output/curve.png')
    plt.show()
