__author__ = 'Nerrtica'

import json
from svmutil import *
# Read data in LIBSVM format

SVMparameter = "-s 3 -t 0 -q"

# read json format file, calculate optimum feature set combination and it's accuracy in 10-fold cross validation
class performance_measure:
    def __init__ (self, parsed_json, featureList, SVMparameter):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.SVMparameter = SVMparameter

    def readFile (self, jsonFileName):
        f = open(jsonFileName, 'r')
        self.parsed_json = json.loads(f.read())
        f.close()

    def readFeatureList (self, featureListFileName):
        f = open(featureListFileName, 'r')
        self.featureList = json.loads(f.read())
        f.close()

    def makeFile (self, fileName, featureList):
        f = open(fileName, 'w')
        for i in range(len(self.parsed_json)):
            if "-s 3" in self.SVMparameter or "-s 4" in self.SVMparameter:
                f.write("%s " % self.parsed_json[i]['label'])
            else:
                # not regression
                pass
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
            self.makeFile("{0}{1}{2}".format("data/data", i, ".txt"), selectedFeatureList)

    def svmCalculate (self):
        SCCresult = []
        for i in range(1, 2 ** len(self.featureList)):
            print("order", i)
            prob = svm_read_problem("{0}{1}{2}".format("data/data", i, ".txt"))
            result = svm_train(prob[0], prob[1], self.SVMparameter)
            SCCresult.append(result[1])
        return SCCresult

    def saveResult (self, SCCresult):
        f = open("data/result.json", 'w')
        selectedFeatureList = []
        i = SCCresult.index(max(SCCresult)) + 1
        index = 0
        while i > 0:
            if i % 2 == 1:
                selectedFeatureList.append(self.featureList[index])
            index += 1
            i //= 2
        json.dump(selectedFeatureList, f)
        f.close()

    def play (self):
        self.makeAllCombi()
        SCCresult = self.svmCalculate()
        self.saveResult(SCCresult)
        print("order", SCCresult.index(max(SCCresult)) + 1, "is optimum combination")

# performance_measure class use example
"""fileName = "data/data.json"
featureListFileName = "data/featureList.json"
def readFeatureList (featureListFileName):
    f = open(featureListFileName, 'r')
    parsed_featureList = json.loads(f.read())
    f.close()
    return parsed_featureList
featureList = readFeatureList(featureListFileName)
SVMparameter = "-s 3 -t 0 -q"
pm = performance_measure(fileName, featureList)
pm.play()"""


class make_model:
    def __init__ (self, parsed_json, featureList, modelFileName, SVMparameter):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = modelFileName
        self.SVMparameter = SVMparameter

    def __init__ (self, parsed_json, featureList):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = "model.txt"
        self.SVMparameter = "-s 3 -t 0 -q"

    def readFile (self):
        f = open(self.jsonFileName, 'r')
        self.parsed_json = json.loads(f.read())
        f.close()

    def readFeatureList (self, featureListFileName):
        f = open(featureListFileName, 'r')
        self.featureList = json.loads(f.read())
        f.close()

    def makeFile (self):
        f = open("data/data.txt", 'w')
        for i in range(len(self.parsed_json)):
            if "-s 3" in self.SVMparameter or "-s 4" in self.SVMparameter:
                f.write("%s " % self.parsed_json[i]['label'])
            else:
                # not regression
                pass
            for feature in self.featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def svmTrain (self):
        prob = svm_read_problem("data/data.txt")
        model = svm_train(prob[0], prob[1], self.SVMparameter)
        svm_save_model(self.modelFileName, model)

    def play (self):
        self.makeFile()
        self.svmTrain()

# make_model class use example
"""modelFileName = "data/model.txt"
featureList = readFeatureList("data/result.json")
mm = make_model(fileName, featureList, modelFileName, SVMparameter)
mm.play()"""


class predict_label:
    def __init__ (self, parsed_json, featureList, modelFileName):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = modelFileName

    def __init__ (self, parsed_json, featureList):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = "model.txt"

    def readFile (self):
        f = open(self.jsonFileName, 'r')
        self.parsed_json = json.loads(f.read())
        f.close()

    def readFeatureList (self, featureListFileName):
        f = open(featureListFileName, 'r')
        self.featureList = json.loads(f.read())
        f.close()

    def makeFile (self):
        f = open("data/data.txt", 'w')
        for i in range(len(self.parsed_json)):
            f.write("%s " % self.parsed_json[i]['label'])
            for feature in self.featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def svmPredict (self):
        prob = svm_read_problem("data/data.txt")
        model = svm_load_model (self.modelFileName)
        result = svm_predict(prob[0], prob[1], model, "-q")
        return result[0]

    def play (self):
        self.makeFile()
        result = self.svmPredict()
        return result

# predict_label class use example
"""predictFileName = "data/data.json"
featureList = readFeatureList("data/result.json")
pl = predict_label(predictFileName, featureList, modelFileName)
result = pl.play()"""