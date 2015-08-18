__author__ = 'Nerrtica'

import json
from svmutil import *
# Read data in LIBSVM format

# read json format input, calculate optimum feature set combination and its accuracy in 10-fold cross validation
class performance_measure:
    def __init__ (self, parsed_json, featureList, SVMparameter):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.SVMparameter = SVMparameter

    def makeFile (self, fileName, featureList):
        f = open(fileName, 'w')
        for i in range(len(self.parsed_json)):
            if "-s 3" in self.SVMparameter or "-s 4" in self.SVMparameter:
                f.write("%s " % self.parsed_json[i]['label'])
            elif "-s 2" in self.SVMparameter:
                if self.parsed_json[i]['label'] >= 4:
                    f.write("1 ")
                else:
                    f.write("0 ")
            else:
                f.write("%d " % self.parsed_json[i]['label'])
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
        while not SCCresult:
            i = SCCresult.index(max(SCCresult)) + 1
            result = []
            selectedFeatureList = []
            index = 0
            while i > 0:
                if i % 2 == 1:
                    selectedFeatureList.append(self.featureList[index])
                index += 1
                i //= 2
            result.append(set(selectedFeatureList))
            result.append(SCCresult[i])
            json.dump(selectedFeatureList, f)
        f.close()

    def play (self):
        self.makeAllCombi()
        SCCresult = self.svmCalculate()
        self.saveResult(SCCresult)
        print("order", SCCresult.index(max(SCCresult)) + 1, "is optimum combination")

# performance_measure class use example
"""
pm = performance_measure(parsed_json, featureList, SVMparameter)
pm.play()
"""

class make_model:
    def __init__ (self, parsed_json, featureList):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = "model.txt"
        self.SVMparameter = "-s 0 -t 0 -q"

    def makeFile (self):
        f = open("data/data.txt", 'w')
        for i in range(len(self.parsed_json)):
            if "-s 3" in self.SVMparameter or "-s 4" in self.SVMparameter:
                f.write("%s " % self.parsed_json[i]['label'])
            elif "-s 2" in self.SVMparameter:
                if float(self.parsed_json[i]['label']) >= 4:
                    f.write("1 ")
                else:
                    f.write("0 ")
            else:
                f.write("%d " % round(float(self.parsed_json[i]['label'])))
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
"""
mm = make_model(parsed_json, featureList)
mm.play()
"""

class predict_label:
    def __init__ (self, parsed_json, featureList):
        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = "model.txt"

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
"""
pl = predict_label(parsed_json, featureList)
result = pl.play()
"""