from feature_selection import *
from auto_svm import *


def readFile (jsonFileName):
    f = open(jsonFileName, 'r')
    parsed_json = json.loads(f.read())
    f.close()
    return parsed_json

"""
def calculCorrelation (person):
    ty = []
    pv = []
    for i in range(len(person)):
        temp = person[i].split(",")
        ty.append(int(temp[0]))
        pv.append(int(temp[1]))
    result = evaluations(ty, pv)
    print(result[1])
    print(result[2])
    return result
"""

parsed_json = readFile("data/data.json")
featureList = readFile("data/featureList.json")

data = Data(parsed_json, featureList)


"""
person = readFile("data/person.json")

calculCorrelation(person)
"""


# SVMparameter = ["-s 3 -t 0 -v 10 -q", "-s 3 -t 2 -v 10 -q", "-s 0 -t 0 -v 10 -q", "-s 0 -t 2 -v 10 -q", "-s 2 -t 0 -v 10 -q"]
SVMparameter = ["-s 0 -t 0 -v 10 -q", "-s 0 -t 2 -v 10 -q"]
for param in SVMparameter:
    resultFileName = "data/result" + param + ".txt"
    pm = performance_measure(parsed_json, [], featureList, param, resultFileName)
    pm.play()


"""
mm = make_model(parsed_json, featureList)
mm.play()

parsed_json = readFile("data/testdata.json")ㅎㅎ

pl = predict_label(parsed_json, featureList)
result = pl.play()

print(result)
"""
