__author__ = 'Nerrtica'

class Data:
    def __init__ (self, parsed_json, featureList):
        self.label = []
        self.feature = [[]]
        for i in range(len(parsed_json)):
            self.label.insert(i, float(parsed_json[i]['label']))
            self.feature.append([])
            for featurelist in featureList:
                temp = parsed_json[i][featurelist].split(" ")
                if temp == ['']:
                    break
                for eachFeature in temp:
                    temp2 = eachFeature.split(":")
                    self.feature[i].insert(int(temp2[0]), float(temp2[1]))

    def setInterval (self, index):
        pass

    def calculInterval (self, index):
        pass

    def makeChiTable (self, ):
        pass