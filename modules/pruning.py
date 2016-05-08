from node import Node
from ID3 import *
from operator import xor
import copy
# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    '''
    if root.label != None or not validation_set:
        return root

    else:
        baseacc = validation_accuracy(root,validation_set)
        #treebest = root
        # To prune the tree, remove the subtree and assign 
        # it a leaf node whose value is the most common 
        # classification of examples associated with that node.
        newtree = Node()
        newtree.label = mode(validation_set)
        if validation_accuracy(newtree,validation_set) > baseacc:
            return newtree 
        if root.is_nominal: # if the tree split according to nominal
            new = split_on_nominal(validation_set, root.decision_attribute)
            i = 0
            for key in root.children:
                validation_set = new[i]
                root.children[key] = reduced_error_pruning(root.children[key],training_set,validation_set)
                i = i + 1
        else: # if the tree split according to numeric 
            new = split_on_numerical(validation_set, root.decision_attribute, root.splitting_value)
            validation0 = new[0]
            validation1 = new[1]
            root.children[0] = reduced_error_pruning(root.children[0],training_set,validation0)
            root.children[1] = reduced_error_pruning(root.children[1],training_set,validation1)
        return root
        
def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
	Function that takes in a validation set, tree, and a header and calculates the percent accuracy on that set.
	'''
    count = 0
    for x in validation_set:
        #print tree.classify(x)
        if tree.classify(x) == x[0]:
            count = count + 1
    #print count
    return 1.0*count / len(validation_set) 
