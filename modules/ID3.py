import math
from node import Node
import sys

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    '''
    # Your code here
    pass

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    attributeZero = data_set[0][0]
    for i in range(1,len(data_set)):
        if(data_set[i][0]!=attributeZero):
            return None
    return attributeZero
    pass
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # loop through the attribute
    # ?What is best split value? 
    pair = {}
    max = 0.0
    zero_count = 0.0
    for i in range(0,len(attribute_metadata)):
        if attribute_metadata[i]['is_nominal']==True:
            val = gain_ratio_nominal(data_set,i)
            if(val==0):
                zero_count+=1
        else:
            if(gain_ratio_numeric(data_set,i,1)==0):
                zero_count+=1
            if(numerical_splits_count[i]!=0):
                val = gain_ratio_numeric(data_set,i,1) #set the default step to 1
        pair[val] = i
    # if gain ratio of all the attributes is zero
    if(zero_count==len(attribute_metadata)): 
        return (False,False)
    max_value = max(pair.keys())
    attribute_value = pair[max_value]
    if(attribute_metadata[i]['is_nominal']==True):
        split = False
    else:
        split = data_set[max_value][attribute_value]
    return (max_value,split)
    pass

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    countOne = 0
    countZero = 0
    for i in range(0,len(data_set)):
        if data_set[i][0]==1 :
            countOne+=1
        if data_set[i][0]==0 :
            countZero+=1
    if countOne>countZero :
        return 1
    else:
        return 0
    pass
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. Number between 0-1. See Textbook for formula
    ========================================================================================================
    '''
    N = len(data_set)
    entropy = 0
    labels = {}
    for n in data_set:
        label = n[0]
        if label not in labels.keys():
            labels[label] = 0
        labels[label] += 1    
    for key in labels:
        prob = (float)(labels[key])/N
        entropy -= prob * math.log(prob,2)
    print entropy
    return entropy
    pass
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0
def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    entropyWhole = entropy(data_set)
    totalNum = len(data_set)
    subset_entropy = 0.0
    intrinsic_val = 0.0
    # Calculate the frequency of each of the values in the target attribute
    val_freq = {}
    for i in range(0,len(data_set)):
        if val_freq.has_key(data_set[i][attribute]):
            val_freq[data_set[i][attribute]] += 1.0
        else:
            val_freq[data_set[i][attribute]] = 1.0
    # Calculate the sum of the entropy for each subset of records weighted
    # by their probability of occuring in the training set.
    for val in val_freq.keys():
        val_prob  = val_freq[val] / totalNum
        data_subset  = [record for record in data_set if record[attribute] == val]
        subset_entropy += val_prob * entropy(data_subset)
        intrinsic_val += - val_prob * math.log(val_prob,2)
    InfoGain = entropyWhole - subset_entropy
    return InfoGain/intrinsic_val
    pass
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    totalNum = len(data_set)
    index = 0
    k = 0
    pair = {}
    while index < totalNum:
        set1 = 0
        set2 = 0
        threshold = data_set[index][attribute]
        # Calculate the two set's size according to the threshold
        for i in range(0,totalNum):
            if(data_set[i][attribute] >= threshold):
                set1 = set1 + 1
            else:
                set2 = set2 + 1
        val_prob1 = set1/totalNum
        val_prob2 = set2/totalNum
        data_subset1 = [record for record in data_set if record[attribute] >= threshold]
        data_subset2 = [record for record in data_set if record[attribute] < threshold]
        entroy_sum = val_prob1 * entropy(data_subset1) + val_prob2 * entropy(data_subset2)
        intrinsic_val = - val_prob1 * math.log(val_prob1,2) - val_prob2 * math.log(val_prob2,2)
        gain_ratio = (entropy(data_set) - entroy_sum) / intrinsic_val
        pair[gain_ratio] = threshold
        # update index and pair value
        k = k + 1
        index = k * step
    max_gain = max(pair.keys)
    return (max_gain,pair[max_gain])
    pass
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 20
# gain_ratio_numeric(data_set,attr,step) == (0.21744375685031775, 0.19)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 30
# gain_ratio_numeric(data_set,attr,step) == (0.4125984252687806, 0.15)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 40
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    pair = {}
    for i in range(0,len(data_set)):
        if pair.has_key(data_set[i][attribute]):
           pair[data_set[i][attribute]].append(data_set[i])
        else:
            pair[data_set[i][attribute]]=[data_set[i]]
    return pair
    pass
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Categorizes data_set into a list that is greater than or equal to the splitting value, and lower.
    ========================================================================================================
    Output: Data less than splitting value and data that is equal to or greater than the splitting value
    ========================================================================================================
    '''
    # Divide the list to two according to the pivet
    list1 = []
    list2 = []
    for i in range(0,len(data_set)):
        if(data_set[i][attribute]>=splitting_value):
            list1.append(data_set[i])
        else:
            list2.append(data_set[i])
    return (list2,list1)
    pass
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])