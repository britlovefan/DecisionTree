import math
from node import Node
import sys
import copy

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    data_set = copy.deepcopy(data_set)
    num_splits = copy.deepcopy(numerical_splits_count)
    node = Node()
    Default = 0
    best_value = []

    if not data_set:
        return "Empty_data"
    elif depth == 0:
        node.label = mode(data_set)
        return node
    elif check_homogenous(data_set) != None:        
        node.label = check_homogenous(data_set)       
        return node  
    elif len(data_set[0]) == 1:
        node.label = mode(data_set)
        return node                      
    elif len(attribute_metadata) == 0:  
        node.label = mode(data_set)
        return node
    else:
        node.label = None
        #print num_splits
        
        (best_attrnumber,split_value) = pick_best_attribute(data_set, attribute_metadata,num_splits)
        node.decision_attribute = best_attrnumber
        node.splitting_value = split_value
        node.name = attribute_metadata[best_attrnumber].values()[1]
        #print node.decision_attribute
        if attribute_metadata[best_attrnumber].values()[0]:
            node.is_nominal = True
            node.splitting_value = None
            examples = split_on_nominal(data_set, best_attrnumber)
        else:
            node.is_nominal = False
            node.splitting_value = split_value
            examples = split_on_numerical(data_set, best_attrnumber,split_value)
            num_splits[best_attrnumber] = num_splits[best_attrnumber] - 1 
        if num_splits[best_attrnumber] == 0:
            del attribute_metadata[best_attrnumber] 
        if node.is_nominal == True: 
            for v in examples.keys():
                if num_splits[best_attrnumber] <= 0:  
                    for i in range(len(examples[v])):
                        del examples[v][i][best_attrnumber]
                node.children[v] = ID3(examples[v], attribute_metadata, num_splits, depth-1)
            return node
        else:
            for i in range(len(examples)): 
                if num_splits[best_attrnumber] <= 0:                            
                    for j in range(len(examples[i])):
                        del examples[i][j][best_attrnumber]
                node.children[i] = ID3(examples[i], attribute_metadata, num_splits, depth-1)
            return node   

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
    N = len(data_set)
    count = 0
    for n in data_set:
        label = n[0]
        #print label
        if label == data_set[0][0]:
            count = count + 1
    if count == N:        
        return data_set[0][0]
    else:
        return None

def check_homogenous_nom(data_set, attr):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    sample = [[row[attr]] for row in data_set]
    attr = list(set(map(tuple,sample)))
    if len(attr) == 1:
        return True
    else:
        return False

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
    best_attr = 0
    best = 0
    gr_list = []
    if len(attribute_metadata) == 2:
        best = 1
    else:
        for i in range(1,len(attribute_metadata)):
            if attribute_metadata[i].values()[0]: 
                temp = gain_ratio_nominal(data_set, i);
                gr_list.append(temp)
            else:
                temp = gain_ratio_numeric(data_set, i, 10)[0];
                gr_list.append(temp)
        for i in range(len(gr_list)):
            if gr_list[i] > best_attr:
                best_attr = gr_list[i]
                best = i+1
    if attribute_metadata[best].values()[0]: 
        return best,False 
    else:    
        split_value = gain_ratio_numeric(data_set, best, 1)[1]   
        return best,split_value


# # # # ======== Test Cases =============================
# numerical_splits_count = [20,20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False},{'name': "weather",'is_nominal': True}]
# data_set = [[1, 0.27, 0], [0, 0.42, 0], [0, 0.86, 2], [0, 0.68, 2], [0, 0.04, 3], [1, 0.01, 1], [1, 0.33, 4], [1, 0.42, 2], [0, 0.51, 2], [1, 0.4, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)

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
    N = len(data_set)
    labels = {}
    max_value = 0
    for n in data_set:
        label = n[0]
        if label not in labels.keys():
            labels[label] = 0
        labels[label] += 1 
    if len(labels.keys()) == 1:
        #print labels
        return labels.keys()[0]
    else:        
        if labels.values()[0] > labels.values()[1]:
            max_value = 0
        else:
            max_value = 1
        return max_value

    
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
    return entropy

def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, attribute index
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See Textbook for formula
    ========================================================================================================
    '''
    value = {}
    subset_entropy = 0.0
    N = len(data_set)
    for n in data_set:
        if (value.has_key(n[attribute])):
            value[n[attribute]] += 1.0
        else:
            value[n[attribute]]  = 1.0
    IV = 0   
    for i in value.keys(): 
        v_prob = value[i] / N
        data_subset = [n for n in data_set if n[attribute] == i]
        #print data_subset,v_prob
        subset_entropy += v_prob * entropy(data_subset)
        IV += -v_prob * math.log(v_prob, 2) 
    IG = entropy(data_set)- subset_entropy
    if IV == 0:
        IGR = 0
    else:
        IGR = IG/IV
    
    return IGR

# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.21744375685031775, 0.19)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Takes in a data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
 
    ========================================================================================================
    Output: This function returns the gain ratio and splitting value
    ========================================================================================================
    '''
    
    IGratio = []
    splitting_val = []
    values = [x[attribute] for x in data_set]
    for i, val in enumerate(values):
        split = split_on_numerical(data_set, attribute, val)
        if (i%steps == 0):
            a = 0
            b = 0
            for j in range(2):
                temp1 = 0
                temp2 = 0
                if len(split[j]) == 0:
                    pass
                else:
                    for row in split[j]:
                        if row[0] == 0:
                            temp1 += 1
                        else:
                            temp2 += 1
                    if temp1 == 0:
                        IV1 = 0
                    else:
                        IV1 = -(float(temp1)/len(split[j]))*math.log((float(temp1)/len(split[j])),2)
                    if temp2 == 0:
                        IV2 = 0
                    else:
                        IV2 = -(float(temp2)/len(split[j]))*math.log((float(temp2)/len(split[j])),2) 
                    IV = IV1 + IV2
                    a += IV*len(split[j])/len(values)
                    another_IV = -float(len(split[j]))/len(values)*math.log(float(len(split[j]))/len(values),2)
                    b += another_IV
            if b == 0:
                IGR = 0
            else:
                IGR = (entropy([[x[0]] for x in data_set]) - a)/b
            IGratio.append(IGR)
            splitting_val.append(val)    
    final = IGratio.index(max(IGratio))
    return IGratio[final], splitting_val[final]
    

# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 20
# gain_ratio_numeric(data_set,attr,step) == (0.21744375685031775, 0.19)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 30
# gain_ratio_numeric(data_set,attr,step) == (0.4125984252687806, 0.15)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 40
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)
def addWord(theIndex,word,pagenumber): 
  theIndex.setdefault(word, [ ]).append(pagenumber)
def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Takes in a data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    value = {}
    dic = {}
    for n in data_set:
        if (value.has_key(n[attribute])):
            value[n[attribute]] += 1.0
        else:
            value[n[attribute]]  = 1.0
    for n in data_set:
        if (value.has_key(n[attribute])):           
            addWord(dic,n[attribute],n)
        else:
            value[n[attribute]]  = 1.0
    return dic 

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Takes in a data set, the index for a numeric attribute, splitting value from gain_ratio
    ========================================================================================================
    Job:    Categorizes data_set into a list that is greater than or equal to the splitting value and lower.
    Job: Splits data_set into a tuple of two lists.  The first list contains the examples for which the given
    attribute has value less than the splitting value, the second list contains the other examples  
    ========================================================================================================
    Output: Data less than splitting value and data that is equal to or greater than the splitting value
    ========================================================================================================
    '''
    gt = [idx for idx, value in enumerate([row[attribute] >= splitting_value for row in data_set]) if value]
    lt = [idx for idx, value in enumerate([row[attribute] < splitting_value for row in data_set]) if value]
    split = [[],[]]
    for row in lt:
        split[0].append(data_set[row])
    for row in gt:
        split[1].append(data_set[row])
    return (split[0],split[1])
