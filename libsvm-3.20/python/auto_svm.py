__author__ = 'Nerrtica'

import json

def readFile (fileName):
    f = open(fileName, 'r')
    parsed_json = json.loads(f.read())
    f.close()
    return parsed_json

def makeFile (fileName, parsed_json, featureList):
    f = open(fileName, 'w')
    for i in range(len(parsed_json)):
        f.write("%d " % i)
        # label file not exists
        for feature in featureList:
            f.write("%s " % parsed_json[i][feature])
        f.write("\n")
    f.close()

def makeAllCombi (fileName, parsed_json, featureList):
    for i in range(1, 2 ** len(featureList)):
        selectedFeatureList = []
        j = i
        index = 0
        while j > 0:
            if j % 2 == 1:
                selectedFeatureList.append(featureList[index])
            index += 1
            j //= 2
        makeFile("{0}{1}{2}".format(fileName[:-5], i, ".txt"), parsed_json, selectedFeatureList)

fileName = "data/data.json"
featureList = ["frequancy_unigram", "frequancy_bigram", "frequancy_trigram"]
parsed_json = readFile(fileName)
makeAllCombi(fileName, parsed_json, featureList)


from svmutil import *
# Read data in LIBSVM format

for i in range(1, 2 ** len(featureList)):
    prob = svm_read_problem("{0}{1}{2}".format(fileName[:-5], i, ".txt"))
    m = svm_train(prob[0], prob[1], "-s 3 -t 0")
    svm_predict(prob[0], prob[1], m)

