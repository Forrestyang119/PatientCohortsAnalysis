import csv
import math
import numpy as np
from random import randint

def readCSV(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        groupList = list(reader)
        listHead = groupList[1]
        groupList = groupList[2:len(groupList)]
    return groupList, listHead

def euclidean(list0, list1, weight):
    '''
    Calculate euclidean distance of two lists (sum of the distances between each attribute)
    @parameter: list attributes
    '''
    distance = 0
    for i in range(len(list0)):
        # distance += math.fabs((float(list0[i]) - float(list1[i]))) * float(weight[i])
        distance += math.pow((float(list0[i]) - float(list1[i])), 2) * float(weight[i])
    return math.sqrt(abs(distance))

def dist(list0, list1, list2, weight):
    '''
    Find out the similar patient pair in a group (each group has three cases)    
    @parameter: 
    '''
    list0 = list0[1:]
    list1 = list1[1:]
    list2 = list2[1:]
    dist = []
    dist.append(euclidean(list0, list1, weight))
    dist.append(euclidean(list1, list2, weight))
    dist.append(euclidean(list0, list2, weight))
    if dist.index(min(dist)) == 0:
        return "01"
    elif dist.index(min(dist)) == 1:
        return "12"
    else:
        return "02"

def calAccuracy(pairs1, pairs2):
    '''
    Calculate the accuracy between two pairs  
    @parameter: 
    '''
    if len(pairs1) != len(pairs2):
        print ("Pairs length not match!")
    total = len(pairs1)
    count = 0
    for i in range(total):
        if pairs1[i] == pairs2[i]:
            count += 1
    return float(count) / total

def calSimilarPairs(groupList, weight):
    '''
    Find out similar patient pairs in a group list
    '''
    similarPairs = []
    for i in range(len(groupList)/3):
        list0 = groupList[i]
        list1 = groupList[i + 1]
        list2 = groupList[i + 2]
        similarPairs.append(dist(list0, list1, list2, weight))
    return similarPairs

if __name__ == "__main__":
    groupList, listHead = readCSV("CopyofRandGroup.csv")
    coloums = len(groupList[0])
    rows = len(groupList)

    # Uniform each coloum attributes
    for i in range(1, coloums):
        maxAttr = max(groupList[:][i])
        groupList[:][i] = [float(attr) / float(maxAttr) for attr in groupList[:][i]]
    
    # Similar pairs of patients in each group labeled by doctor
    similarPairs_Dr = ['12','02','12','02','12','02','01','01','12','02','02','01','01','02','01','12','01','12','01','01','02','12','12','12','12','12','01','12','12','12','01','12','02','02','12','12','02','12','01','12','12']

    best = 0                        # Maximum improvement (global)
    learningRate = 1.0              # Learning rate
    weight = []                     # attribute weights 

    # Initialize weights
    weight = list(np.zeros(len(groupList[0]) - 1))
    n = len(weight)

    similarPairs = calSimilarPairs(groupList, weight)
    accuracy = calAccuracy(similarPairs, similarPairs_Dr)

    print (weight)
    print (accuracy)
    print ("----------------------------")

    while True:
        accuracy = 0
        count = 0
        improve = 0
        record_acc = []
        acc = []
        while True:
            # Try to increase each weight to get the maxImprove weight
            for i in range(n):
                weight[i] += learningRate
                similarPairs_new = calSimilarPairs(groupList, weight)
                accuracy = calAccuracy(similarPairs_new, similarPairs_Dr)
                acc.append(accuracy)
                weight[i] -= learningRate

            # Try to decrease
            for i in range(n):
                if weight[i] - learningRate > 0:
                    weight[i] -= learningRate
                    similarPairs_new = calSimilarPairs(groupList, weight)
                    accuracy = calAccuracy(similarPairs_new, similarPairs_Dr)
                    acc.append(accuracy)
                    weight[i] += learningRate
                else:
                    acc.append(0)

            maxAcc = max(acc)                               # Maximum accuracy
            alpha = acc.count(maxAcc)                       # Count the number of the maximum accuracy

            for i in range(2 * n):
                if acc[i] == maxAcc and i < n:
                    weight[i] += learningRate / alpha       # Weight increment
                elif acc[i] == maxAcc and i >= n:
                    weight[i - n] -= learningRate / alpha   # Weight subtraction
            
            print ("----------")

            # calculate updated accuracy
            similarPairs_new = calSimilarPairs(groupList, weight)
            accuracy = calAccuracy(similarPairs_new, similarPairs_Dr)

            # print updated accuracy
            print (accuracy)
            record_acc.append(maxAcc)
            print (weight)

            # record weights in every step
            with open("weight.csv",'a') as File:
                File.write(str(maxAcc) + ',' + str(weight)[0:-1] + '\n')

            if maxAcc != improve:
                improve = maxAcc
                count = 0
            else:
                count += 1

            acc = []
            
            # record accuracy improvements and break the loops
            if count >= 200:
                if (maxAcc) > best:
                    best = maxAcc
                    print best
                    print weight
                    print "---------------------------------------------------------"
                    with open("weight.csv", "a") as File:
                        File.write('--------------------------------------------------' + '\n')
                    with open("output.csv",'wb') as resultFile:
                        resultFile.write(str(record_acc)[1:-1] + '\n')
                break
        
    
