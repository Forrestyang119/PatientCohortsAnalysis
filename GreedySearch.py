import csv
import math
from random import randint

def readCSV(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        groupList = list(reader)
        listHead = groupList[1]
        groupList = groupList[2:len(groupList)]
    return groupList, listHead

# calculate euclidean distance of two lists
def euclidean(list0, list1, weight):
    distance = 0
    # totalWeight = 0
    # for i in range(len(weight)):
    #     totalWeight += weight[i]
    for i in range(len(list0)):
        # distance += math.fabs((float(list0[i]) - float(list1[i]))) * float(weight[i])
        distance += math.pow((float(list0[i]) - float(list1[i])), 2) * float(weight[i])
    return math.sqrt(distance)

# calculate similar pair in a group of list (each group has three cases)
def dist(list0, list1, list2, weight):
    length = len(list0)
    list0 = list0[1:length]
    list1 = list1[1:length]
    list2 = list2[1:length]
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
    if len(pairs1) != len(pairs2):
        print "Pairs length not match!"
    total = len(pairs1)
    count = 0
    for i in range(total):
        if pairs1[i] == pairs2[i]:
            count += 1
    return float(count) / float(total)

def calSimilarPairs(groupList, weight):
    similarPairs = []
    for i in range(len(groupList)/3):
        list0 = groupList[i]
        list1 = groupList[i + 1]
        list2 = groupList[i + 2]
        similarPairs.append(dist(list0, list1, list2, weight))
    return similarPairs

if __name__ == "__main__":
    groupList, listHead = readCSV("CopyofRandGroup.csv")
    # print groupList
    coloums = len(groupList[0])
    rows = len(groupList)
    #
    # Uniform each coloum
    #
    maxAttr = 0
    for i in range(coloums):
        if i > 0:
            for j in range(rows):
                if float(groupList[j][i]) > float(maxAttr):
                    maxAttr = float(groupList[j][i])
            for j in range(rows):
                groupList[j][i] = float(float(groupList[j][i]) / maxAttr)
            maxAttr = 0
    print groupList
    #
    # weight = 1, calculate accuracy
    #
    weight = []
    for i in range(len(groupList[0]) - 1):
        weight.append(1)
    similarPairs = calSimilarPairs(groupList, weight)
    #
    # Similar pairs of patients in each group labeled by doctor
    #
    similarPairs_Dr = ['12','02','12','02','12','02','01','01','12','02','02','01','01','02','01','12','01','12','01','01','02','12','12','12','12','12','01','12','12','12','01','12','02','02','12','12','02','12','01','12','12']
    accuracy = calAccuracy(similarPairs, similarPairs_Dr)
    best = 0
    while True:
        #
        # Reset weight to [1, 1, ..., 1]
        #
        weight = []
        print len(groupList)
        for i in range(len(groupList[0]) - 1):
            weight.append(1)
        accuracy_change = []
        n = 0
        count = 0
        improve = 0
        acc = []
        weightIncrease = []
        while True:
            n += 1
            #
            # Try to increase each weight to get the maxImprove weight
            #
            for i in range(len(weight)):
                weight[i] += 1
                similarPairs_new = calSimilarPairs(groupList, weight)
                accuracy_new = calAccuracy(similarPairs_new, similarPairs_Dr)
                accuracy_change.append(accuracy_new - accuracy)
                weight[i] -= 1
            maxImprove = accuracy_change[accuracy_change.index(max(accuracy_change))]
            print accuracy + maxImprove
            acc.append(accuracy + maxImprove)
            print weight
            with open("weight.csv",'a') as File:
                File.write(str(accuracy + maxImprove) + '\t' + str(weight)[1:-1] + '\n')

            if maxImprove != improve:
                improve = maxImprove
                count = 0
            else:
                count += 1
            
            #
            # randomly increase weight
            #
            maxIndex = []
            for j in range(len(weight)):
                if accuracy_change[j] == maxImprove:
                    maxIndex.append(j)
            r = randint(0, (len(maxIndex)-1))
            weight[maxIndex[r]] += 1

            # print weight
            
            accuracy_change = []
            n += 1
            
            if count >= 200:
                if (accuracy + maxImprove) > best:
                    best = accuracy + maxImprove
                    print best
                    print weight
                    print "---------------------------------------------------------"
                    with open("weight.csv", "a") as File:
                        File.write('--------------------------------------------------' + '\n')
                    with open("output.csv",'wb') as resultFile:
                        resultFile.write(str(acc)[1:-1] + '\n')
                break
        
    