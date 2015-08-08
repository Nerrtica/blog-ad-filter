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
            f.write("%s " % self.parsed_json[i]['label'])
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

    def svmCalculate (self):
        SCCresult = []
        for i in range(1, 2 ** len(self.featureList)):
            print("order", i)
            prob = svm_read_problem("{0}{1}{2}".format(self.jsonFileName[:-5], i, ".txt"))
            result = svm_train(prob[0], prob[1], "-s 3 -t 0 -v 10 -q")
            SCCresult.append(result[1])
        return SCCresult

    def saveResult (self, SCCresult):
        f = open("data/result.json", 'w')
        selectedFeatureList = []
        i = SCCresult.index(max(SCCresult))
        index = 0
        while i > 0:
            if i % 2 == 1:
                selectedFeatureList.append(self.featureList[index])
            index += 1
            i //= 2
        json.dump(selectedFeatureList, f)
        f.close()

    def play (self):
        self.readFile()
        self.makeAllCombi()
        SCCresult = self.svmCalculate()
        self.saveResult(SCCresult)
        print("order", SCCresult.index(max(SCCresult)), "is optimum combination")

# performance_measure class use example
fileName = "data/data.json"
featureListFileName = "data/featureList.json"
def readFeatureList (featureListFileName):
    f = open(featureListFileName, 'r')
    parsed_featureList = json.loads(f.read())
    f.close()
    return parsed_featureList
featureList = readFeatureList(featureListFileName)
pm = performance_measure(fileName, featureList)
pm.play()


class make_model:
    def __init__ (self, jsonFileName, featureList, modelFileName):
        self.jsonFileName = jsonFileName
        self.featureList = featureList
        self.modelFileName = modelFileName

    def readFile (self):
        f = open(self.jsonFileName, 'r')
        self.parsed_json = json.loads(f.read())
        f.close()

    def makeFile (self):
        f = open("{0}{1}".format(self.jsonFileName[:-5], ".txt"), 'w')
        for i in range(len(self.parsed_json)):
            f.write("%s " % self.parsed_json[i]['label'])
            for feature in self.featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def svmTrain (self):
        prob = svm_read_problem("{0}{1}".format(self.jsonFileName[:-5], ".txt"))
        model = svm_train(prob[0], prob[1], "-s 3 -t 0 -q")
        svm_save_model(self.modelFileName, model)

    def play (self):
        self.readFile()
        self.makeFile()
        self.svmTrain()

# make_model class use example
modelFileName = "data/model.txt"
featureList = readFeatureList("data/result.json")
mm = make_model(fileName, featureList, modelFileName)
mm.play()


class predict_label:
    def __init__ (self, jsonFileName, featureList, modelFileName):
        self.jsonFileName = jsonFileName
        self.featureList = featureList
        self.modelFileName = modelFileName

    def readFile (self):
        f = open(self.jsonFileName, 'r')
        self.parsed_json = json.loads(f.read())
        f.close()

    def makeFile (self):
        f = open("{0}{1}".format(self.jsonFileName[:-5], ".txt"), 'w')
        for i in range(len(self.parsed_json)):
            f.write("%s " % self.parsed_json[i]['label'])
            for feature in self.featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def svmPredict (self):
        prob = svm_read_problem("{0}{1}".format(self.jsonFileName[:-5], ".txt"))
        model = svm_load_model (self.modelFileName)
        result = svm_predict(prob[0], prob[1], model, "-q")
        return result[0]

    def play (self):

        self.readFile()
        self.makeFile()
        result = self.svmPredict()
        return result

# predict_label class use example
predictFileName = "data/data.json"
featureList = readFeatureList("data/result.json")
pl = predict_label(predictFileName, featureList, modelFileName)
result = pl.play()