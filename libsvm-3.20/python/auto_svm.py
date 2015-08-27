__author__ = 'Nerrtica'

import json
import time
import os
from svmutil import *
# Read data in LIBSVM format

# read json format input, calculate optimum feature set combination and its accuracy in 10-fold cross validation
class performance_measure:
    def __init__ (self, parsed_json, selectedFeatureList, featureList, SVMparameter, resultFileName):
        self.parsed_json = parsed_json
        self.selectedFeatureList = selectedFeatureList
        self.featureList = featureList
        self.SVMparameter = SVMparameter
        self.resultFileName = resultFileName

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
                f.write("%d " % round(float(self.parsed_json[i]['label'])))
            for feature in featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def findBestAdd (self, selectedFeatureList, featureList):
        performance = {}
        for feature in featureList:
            tempList = list(selectedFeatureList)
            tempList.extend(self.selectedFeatureList)
            tempList.append(feature)
            self.makeFile("temp/data.txt", tempList)
            prob = svm_read_problem("temp/data.txt")
            result = svm_train(prob[0], prob[1], self.SVMparameter)
            if "-s 3" in self.SVMparameter or "-s 4" in self.SVMparameter:
                performance[feature] = result[1]
                print("feature " + feature + " added, SCC is " + str(result[1]))
            else:
                performance[feature] = result
                print("feature " + feature + " added, ACC is " + str(result))
        return ( max(performance, key = performance.get) , max(performance.values()) )

    def findBestDel (self, featureList):
        performance = {}
        for feature in featureList:
            tempList = list(featureList)
            tempList.extend(self.selectedFeatureList)
            tempList.remove(feature)
            self.makeFile("temp/data.txt", tempList)
            prob = svm_read_problem("temp/data.txt")
            result = svm_train(prob[0], prob[1], self.SVMparameter)
            if "-s 3" in self.SVMparameter or "-s 4" in self.SVMparameter:
                performance[feature] = result[1]
                print("feature " + feature + " deleted, SCC is " + str(result[1]))
            else:
                performance[feature] = result
                print("feature " + feature + " deleted, ACC is " + str(result))
        return ( max(performance, key = performance.get), max(performance.values()) )

    def saveResult (self, result):
        f = open(self.resultFileName, 'w')
        for str in result:
            f.write(str)
        f.close()

    def play (self):
        selectedFeatureList = []
        featureList = list(self.featureList)
        result = []
        while 1 :
            bestAdd = self.findBestAdd(selectedFeatureList, featureList)
            selectedFeatureList.append(bestAdd[0])
            featureList.remove(bestAdd[0])
            result.append("selected feature list : {0}, correlation : {1}".format(selectedFeatureList, bestAdd[1]))
            print("selected feature list : {0}, correlation : {1}".format(selectedFeatureList, bestAdd[1]))
            if (len(featureList) == 0):
                break
            bestAdd = self.findBestAdd(selectedFeatureList, featureList)
            selectedFeatureList.append(bestAdd[0])
            featureList.remove(bestAdd[0])
            result.append("selected feature list : {0}, correlation : {1}".format(selectedFeatureList, bestAdd[1]))
            print("selected feature list : {0}, correlation : {1}".format(selectedFeatureList, bestAdd[1]))
            bestDel = self.findBestDel(selectedFeatureList)
            selectedFeatureList.remove(bestDel[0])
            featureList.append(bestDel[0])
            result.append("selected feature list : {0}, correlation : {1}".format(selectedFeatureList, bestDel[1]))
            print("selected feature list : {0}, correlation : {1}".format(selectedFeatureList, bestDel[1]))
        self.saveResult(result)

# performance_measure class use example
"""
pm = performance_measure(parsed_json, featureList, SVMparameter, resultFileName)
pm.play()
"""

class make_model:
    def __init__ (self, parsed_json, featureList, path):

        self.parsed_json = parsed_json
        self.featureList = featureList
        self.modelFileName = path + "/model.txt"
        self.SVMparameter = "-s 3 -t 0 -q"

    def makeFile (self):
        f = open("temp/data.txt", 'w')
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
        prob = svm_read_problem("temp/data.txt")
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

        MODELRECORD = "./model/model_record.txt"
        f_MODELRECORD = open(MODELRECORD, "r")
        recent_MODELRECORD = f_MODELRECORD.read().splitlines()[-1]
        f_MODELRECORD.close()
        self.modelFileName = "model/" + recent_MODELRECORD + "/model.txt"

    def makeFile (self):
        f = open("temp/data.txt", 'w')
        for i in range(len(self.parsed_json)):
            f.write("%s " % self.parsed_json[i]['label'])
            for feature in self.featureList:
                f.write("%s " % self.parsed_json[i][feature])
            f.write("\n")
        f.close()

    def svmPredict (self):
        prob = svm_read_problem("temp/data.txt")
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