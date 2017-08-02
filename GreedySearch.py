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

# calculate similar pair in a group of list
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
    weight = []
    print len(groupList)
    for i in range(len(groupList[0]) - 1):
        weight.append(1)
    # weight = 1, calculate accuracy
    similarPairs = calSimilarPairs(groupList, weight)
    # print similarPairs
    similarPairs_Dr = ['12','02','12','02','12','02','01','01','12','02','02','01','01','02','01','12','01','12','01','01','02','12','12','12','12','12','01','12','12','12','01','12','02','02','12','12','02','12','01','12','12']
    # print similarPairs_Dr
    accuracy = calAccuracy(similarPairs, similarPairs_Dr)
    best = 0
    while True:
        accuracy_change = []
        n = 0
        count = 0
        improve = 0
        acc = []
        weightIncrease = []
        while True:
            n += 1
            for i in range(len(weight)):
                weight[i] += 1
                similarPairs_new = calSimilarPairs(groupList, weight)
                accuracy_new = calAccuracy(similarPairs_new, similarPairs_Dr)
                accuracy_change.append(accuracy_new - accuracy)
                weight[i] -= 1
            # print accuracy_change
            # print accuracy_change.index(max(accuracy_change))
            # print accuracy + accuracy_change[accuracy_change.index(max(accuracy_change))]
            maxImprove = accuracy_change[accuracy_change.index(max(accuracy_change))]
            acc.append(accuracy + maxImprove)
            if maxImprove != improve:
                improve = maxImprove
                count = 0
                weightIncrease.append(weight)
            else:
                count += 1
    # randomly
            maxIndex = []
            for j in range(len(weight)):
                if accuracy_change[j] == maxImprove:
                    maxIndex.append(j)
            r = randint(0, (len(maxIndex)-1))
            weight[maxIndex[r]] += 1


            # weight[accuracy_change.index(max(accuracy_change))] += 1
            # print weight
            
            accuracy_change = []
            n += 1
            
            if count >= 200:
                if (accuracy + maxImprove) > best:
                    best = accuracy + maxImprove
                    print best
                    print weight
                    with open("output.csv",'wb') as resultFile:
                        # wr = csv.writer(resultFile, dialect='excel')
                        resultFile.write(str(acc)[1:-1] + '\n')
                        resultFile.write(str(weightIncrease)[1:-1] + '\n')
                        resultFile.write(str(weight)[1:-1])
                    # with open("output2.csv",'wb') as resultFile2:
                    #     # wr = csv.writer(resultFile2, dialect='excel')
                    #     resultFile2.write(weight)
                break
        
        # print similarPairs_Dr
        # print similarPairs
        # print similarPairs_new
        # print n
    