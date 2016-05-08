import os.path
from operator import xor
from parse import *
# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    # first calculate the predict list 
    predict_set, _ = parse(predict, True)
    predict_set = changemissing(predict_set)
    predictedClasslist = []
    for x in predict_set:
        predictedClass = tree.classify(x)
        predictedClasslist.append(predictedClass)
    # next output the file to csv 
    with open(predict,'r') as csvinput:
        with open('./output/PS2.csv', 'wb') as csvoutput:
            writer = csv.writer(csvoutput)
            reader = csv.reader(csvinput)
            i = 0
            size = len(predictedClasslist)
            for row in reader:
                if(i!=0 and i<=size):
                    row[len(row)-1] = predictedClasslist[i-1]
                writer.writerow(row)
                i+=1
    csvoutput.close()
    csvinput.close()


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

