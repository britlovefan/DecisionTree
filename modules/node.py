# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
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
        self.default = None
    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''

        if self.label != None:
            return self.label
        elif self.is_nominal:
            try:
                child = self.children[instance[self.decision_attribute]]
                return child.classify(instance)
            except KeyError:
                return self.default           
        else:
        
            split = self.splitting_value
            value = instance[self.decision_attribute]
            if value < split:
                
                return self.children[0].classify(instance)
            else:
                return self.children[1].classify(instance)

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        blank = "\t"* indent
        if (self.label != None):
            return blank + "Leaf: " + str(self.label) + "\n"
        else:
            if self.is_nominal == False:
                blank1 = ""
                for key in self.children:
                    blank += blank1 + (str(self.name)+ " : " + str(self.splitting_value) + "\n" + self.children[key].print_tree(indent + 1))
                    blank1 = "\t"* indent
            elif dnf.is_nominal == True:
                blank1 = ""
                for key in self.children:
                    blank += blank1 + (str(self.name) + "\n" + self.children[key].print_tree(indent + 1))
                    blank1 = "\t"* indent                
            return blank
        
        #return print_tree_whole(self, indent = 0)
        #for key in self.children:
        #    self.children[key].print_tree(indent+1)

    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        #list_dnf(self,[])
        return dnf_out(list_dnf(self,[]))
   

def list_dnf(dnf, all =[]):    
    if dnf.label == 1: 
            return ["("] + all + [")"] + ["OR"]
    elif (dnf.is_nominal == True):
        con = []
        for key in dnf.children:
            temp = list_dnf(dnf.children[key], all + [str(dnf.name) + " = " + str(key)])
            con = con + temp
        return con
    elif(dnf.splitting_value != None):
        con = []
        temp = list_dnf(dnf.children[0], all + [str(dnf.name) + " < " + str(dnf.splitting_value)])
        con = con + temp
        temp = list_dnf(dnf.children[1], all + [str(dnf.name) + " >= " + str(dnf.splitting_value)])
        con = con + temp
        return con
    else:
        return []                                                       
def dnf_out(lst):
    out = ''
    for i in range(len(lst)-1):       
        if (lst[i] == "(" or lst[i] == ")"):
            out = out + str(lst[i])
        elif lst[i] == "OR":
            out = out + "\t" + str(lst[i]) + "\n"
        else:
            if lst[i-1] == "(" :
                out = out + str(lst[i])                
            else:
                out = out + " AND " + str(lst[i])  
    return out
