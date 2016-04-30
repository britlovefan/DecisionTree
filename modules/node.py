# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 if numeric and a dictionary if nominal for numeric, 0 if for < and 1 for >=
#
# label - is None if there is a decision attribute, and is 0 or 1 if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the decision attribute being splitted on
#
# is_nominal - is the decision attribute nominal
#
# value - if label is None this should be None.
#         if label is 0, this should be the mode.
#         if label is 1, this should be the homogenous value
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
        for i in range(1,len(instance)):
            if(self.label!=None):
                print self.label
                return self.label
            attribute = instance[i]
            child = self.children
            # 1.if the the children is numeric, "0" for smaller, "1" for bigger
            # 2.navigate to the child whose key matches our instance's attribute value.
            if(type(child)==list):
                if(attribute<self.splitting_value):
                    self = child[0]
                else:
                    self = child[1]
            else:
                self = child[attribute]
        return self.label
        pass
    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        '''
        # Your code here
        pass


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        pass
