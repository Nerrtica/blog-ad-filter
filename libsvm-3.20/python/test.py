from auto_svm import *


def readFile (jsonFileName):
    f = open(jsonFileName, 'r')
    parsed_json = json.loads(f.read())
    f.close()
    return parsed_json

parsed_json = readFile("data/data.json")
featureList = readFile("data/featureList.json")

"""
SVMparameter = ["-s 3 -t 0 -q", "-s 3 -t 2 -q", "-s 0 -t 0 -q", "-s 0 -t 2 -q", "-s 2 -t 0 -q"]
for param in SVMparameter:
    pm = performance_measure(parsed_json, featureList, param)
    pm.play()
"""


mm = make_model(parsed_json, featureList)
mm.play()

parsed_json = readFile("data/testdata.json")

pl = predict_label(parsed_json, featureList)
result = pl.play()

print(result)
