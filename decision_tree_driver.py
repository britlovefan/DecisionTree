from modules.ID3 import *
from modules.parse import *
from modules.pruning import *
from modules.graph import *
from modules.predictions import *

# DOCUMENATION
# ===========================================
# decision tree driver - takes a dictionary of options and runs the ID3 algorithm.
#   Supports numerical attributes as well as missing attributes. Documentation on the
#   options can be found in README.md

options = {
    'train' : 'data/test_btrain.csv',
    'validate': 'data/test_bvalidate.csv',
    'predict': 'data/test_btest.csv',
    'limit_splits_on_numerical': 5,
    'limit_depth': 20,
    'print_tree': False,
    'print_dnf' : False,
    'prune' : 'data/test_bvalidate.csv',
    'learning_curve': {
        'upper_bound' : 0.05,
        'increment' : 0.001
    }
}

def changemissing(data):
   #dealing with missing attributes : '?'
    sum_value = 0
    for j in range(1,len(data[0])):
        for i in range(len(data)):
            if data[i][j] == None:
                pass
            else:
                sum_value += data[i][j]
        mean_value = sum_value/len(data)
        for i in range(len(data)):
            if data[i][j] != None:
                pass
            else:
                data[i][j] = mean_value
    return data
                
def decision_tree_driver(train, validate = False, predict = False, prune = False,
    limit_splits_on_numerical = False, limit_depth = False, print_tree = False,
    print_dnf = False, learning_curve = False):
    train_set, attribute_metadata = parse(train, False)
    prune = False
    if limit_splits_on_numerical != False:
        numerical_splits_count = [limit_splits_on_numerical] * len(attribute_metadata)
    else:
        numerical_splits_count = [float("inf")] * len(attribute_metadata)
        
    if limit_depth != False:
        depth = limit_depth
    else:
        depth = float("inf")

    print "###\n#  Training Tree\n###"
    train_set = changemissing(train_set) 
    # call the ID3 classification algorithm with the appropriate options
    tree = ID3(train_set, attribute_metadata, numerical_splits_count, depth)
    print '\n'

    # call reduced error pruning using the pruning set
    if prune != False:
        print '###\n#  Pruning\n###'
        pruning_set, _ = parse(prune, False)
        reduced_error_pruning(tree,train_set,pruning_set)
        print ''
    #print print_tree
    # print tree visually
    if print_tree:
        print '###\n#  Decision Tree\n###'
        cursor = open('./output/tree.txt','w+')
        cursor.write(tree.print_tree())
        cursor.close()
        print 'Decision Tree written to /output/tree'
        print ''
    
    # print tree in disjunctive normalized form
    if print_dnf:
        print '###\n#  Decision Tree as DNF\n###'
        cursor = open('./output/DNF.txt','w+')
        cursor.write(tree.print_dnf_tree())
        cursor.close()
        print 'Decision Tree written to /output/DNF'
        print ''

    # test tree accuracy on validation set
    if validate != False:
        print '###\n#  Validating\n###'
        validate_set, _ = parse(validate, False)
        validate_set = changemissing(validate_set)
        accuracy = validation_accuracy(tree,validate_set)
        print "Accuracy on validation set: " + str(accuracy)
        print ''

    # generate predictions on the test set
    if predict != False:
        print '###\n#  Generating Predictions on Test Set\n###'
        create_predictions(tree,predict)
        print ''

    # generate a learning curve using the validation set
    if learning_curve and validate:
        print '###\n#  Generating Learning Curve\n###'
        iterations = 20 # number of times to test each size
        get_graph(train_set, attribute_metadata, validate_set, 
            numerical_splits_count, depth, 5, 0, learning_curve['upper_bound'],
            learning_curve['increment'])
        print ''

tree = decision_tree_driver( **options )
