__author__ = 'Nerrtica'

import json
from svmutil import *
# Read data in LIBSVM format

# read json format file, calculate optimum feature set combination and it's accuracy in 10-fold cross validation
class performance_measure:
    def __init__ (self, jsonFileName, featureList):
        self.jsonFileName = jsonFileName
        self.featureList = featureList

    def readFile (self):
        f = open(self.jsonFileName, 'r')
        self.parsed_json = json.loads(f.read())
        f.close()

    def makeFile (self, fileName, featureList):
        f = open(fileName, 'w')
        for i in range(len(self.parsed_json)):
            f.write("%d " % i)
            # label file not exists

            for feature in featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def makeAllCombi (self):
        for i in range(1, 2 ** len(self.featureList)):
            selectedFeatureList = []
            j = i
            index = 0
            while j > 0:
                if j % 2 == 1:
                    selectedFeatureList.append(self.featureList[index])
                index += 1
                j //= 2
            self.makeFile("{0}{1}{2}".format(self.jsonFileName[:-5], i, ".txt"), selectedFeatureList)

    def play (self):
        self.readFile()
        self.makeAllCombi()
        SCCresult = []
        for i in range(1, 2 ** len(self.featureList)):
            print("order", i)
            prob = svm_read_problem("{0}{1}{2}".format(self.jsonFileName[:-5], i, ".txt"))
            result = svm_train(prob[0], prob[1], "-s 3 -t 0 -v 10 -q")
            SCCresult.append(result[1])
        print("order", SCCresult.index(max(SCCresult)), "is optimum combination")

fileName = "data/data.json"
featureList = ["frequancy_unigram", "frequancy_bigram", "frequancy_trigram"]
pm = performance_measure(fileName, featureList)
pm.play()
